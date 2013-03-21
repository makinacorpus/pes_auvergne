# -*- coding: utf-8 -*-

import floppyforms as forms
from ionyweb.forms import ModuloModelForm
from .models import PageApp_CoopAgenda

class PageApp_CoopAgendaForm(ModuloModelForm):

    class Meta:
        model = PageApp_CoopAgenda