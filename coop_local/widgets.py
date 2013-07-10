
import math
from itertools import chain

from django import forms
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe


from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy
from django.utils.html import escape
from django.conf import settings
from PIL import Image
import os


import datetime
import re

from django.forms.widgets import Widget, Select
from django.utils.dates import MONTHS


class CustomCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    """
    Widget that renders multiple-select checkboxes in columns.
    Constructor takes number of columns and css class to apply
    to the <ul> elements that make up the columns.
    Custom widget that renders multiple-select checkboxes with input + label
    """
    def __init__(self, columns=1, css_class=None, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self.columns = columns
        self.css_class = css_class

    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        choices_enum = list(enumerate(chain(self.choices, choices)))
        
        # This is the part that splits the choices into columns.
        # Slices vertically.  Could be changed to slice horizontally, etc.
        column_sizes = columnize(len(choices_enum), self.columns)
        columns = []
        for column_size in column_sizes:
            columns.append(choices_enum[:column_size])
            choices_enum = choices_enum[column_size:]
        output = []
        for column in columns:
            if self.css_class:
                output.append(u'<ul class="%s"' % self.css_class)
            else:
                output.append(u'<ul>')
            # Normalize to strings
            str_values = set([force_unicode(v) for v in value])
            for i, (option_value, option_label) in column:
                # If an ID attribute was given, add a numeric index as a suffix,
                # so that the checkboxes don't all have the same ID attribute.
                if has_id:
                    final_attrs = dict(final_attrs, id='%s_%s' % (
                            attrs['id'], i))
                    label_for = u' for="%s"' % final_attrs['id']
                else:
                    label_for = ''

                cb = forms.CheckboxInput(
                    final_attrs, check_test=lambda value: value in str_values)
                option_value = force_unicode(option_value)
                rendered_cb = cb.render(name, option_value)
                option_label = conditional_escape(force_unicode(option_label))
                output.append(u'<li>%s<label%s>%s</label></li>' % (
                        rendered_cb, label_for, option_label))
            output.append(u'</ul>')
        return mark_safe(u'\n'.join(output))


def columnize(items, columns):
    """
    Return a list containing numbers of elements per column if `items` items
    are to be divided into `columns` columns.

    >>> columnize(10, 1)
    [10]
    >>> columnize(10, 2)
    [5, 5]
    >>> columnize(10, 3)
    [4, 3, 3]
    >>> columnize(3, 4)
    [1, 1, 1, 0]
    """
    elts_per_column = []
    for col in range(columns):
        col_size = int(math.ceil(float(items) / columns))
        elts_per_column.append(col_size)
        items -= col_size
        columns -= 1
    return elts_per_column



class CustomClearableFileInput(forms.ClearableFileInput):
    initial_text = ugettext_lazy('Currently')
    input_text = ugettext_lazy('Change')
    clear_checkbox_label = ugettext_lazy('Clear')

    #template_with_initial = u'%(initial_text)s: %(initial)s %(clear_template)s<br />%(input_text)s: %(input)s'
    template_with_initial = u'%(initial)s %(clear_template)s<br /><div class="modify">%(input_text)s: %(input)s</div>'

    template_with_clear = u'%(clear)s <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label>'


    def render(self, name, value, attrs=None):
        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        template = u'%(input)s'
        substitutions['input'] = super(forms.ClearableFileInput, self).render(name, value, attrs)

        if value and hasattr(value, "url"):
            template = self.template_with_initial
            substitutions['initial'] = (u'<a href="%s">%s</a>'
                                        % (escape(value.url),
                                           escape(force_unicode(value))))
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
                substitutions['clear'] = forms.CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = self.template_with_clear % substitutions

        return mark_safe(template % substitutions)

  
    


__all__ = ('MonthYearWidget',)

RE_DATE = re.compile(r'(\d{4})-(\d\d?)-(\d\d?)$')

class YearWidget(Widget):
    """
    A Widget that splits date input into one <select> boxes for year only ,
    with 'day' and 'month' defaulting to the firsts (day, month).

    Based on SelectDateWidget, in 

    django/trunk/django/forms/extras/widgets.py

    """
    none_value = (0, '---')
    year_field = '%s_year'

    def __init__(self, attrs=None, years=None, required=True):
        # years is an optional list/tuple of years to use in the "year" select box.
        self.attrs = attrs or {}
        self.required = required
        if years:
            self.years = years
        else:
            this_year = datetime.date.today().year
            self.years = range(this_year, this_year+10)

    def render(self, name, value, attrs=None):
        try:
            year_val, month_val = value.year, value.month
        except AttributeError:
            year_val = month_val = None
            if isinstance(value, basestring):
                match = RE_DATE.match(value)
                if match:
                    year_val, month_val, day_val = [int(v) for v in match.groups()]

        output = []

        if 'id' in self.attrs:
            id_ = self.attrs['id']
        else:
            id_ = 'id_%s' % name

        year_choices = [(i, i) for i in self.years]
        if not (self.required and value):
            year_choices.insert(0, self.none_value)
        local_attrs = self.build_attrs(id=self.year_field % id_)
        s = Select(choices=year_choices)
        select_html = s.render(self.year_field % name, year_val, local_attrs)
        output.append(select_html)

        return mark_safe(u'\n'.join(output))

    def id_for_label(self, id_):
        return '%s_month' % id_
    id_for_label = classmethod(id_for_label)

    def value_from_datadict(self, data, files, name):
        y = data.get(self.year_field % name)
        if y == "0":
            return None
        if y :
            return '%s-%s-%s' % (y, 1, 1)
        return data.get(name, None)
        
