# -*- coding: utf-8 -*-
import floppyforms as forms
from ionyweb.forms import ModuloModelForm
from .models import Plugin_CoopMembersIcons


class Plugin_CoopMembersIconsForm(ModuloModelForm):

    class Meta:
        model = Plugin_CoopMembersIcons