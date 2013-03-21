# -*- coding: utf-8 -*-
import floppyforms as forms
from ionyweb.forms import ModuloModelForm
from .models import Plugin_Members


class Plugin_MembersForm(ModuloModelForm):

    class Meta:
        model = Plugin_Members