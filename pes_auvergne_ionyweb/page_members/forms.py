# -*- coding: utf-8 -*-

import floppyforms as forms
from ionyweb.forms import ModuloModelForm
from .models import PageApp_Members

class PageApp_MembersForm(ModuloModelForm):

    class Meta:
        model = PageApp_Members