# -*- coding: utf-8 -*-
import floppyforms as forms
from ionyweb.forms import ModuloModelForm
from .models import Plugin_CoopAgenda


class Plugin_CoopAgendaForm(ModuloModelForm):

    class Meta:
        model = Plugin_CoopAgenda