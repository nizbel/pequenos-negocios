# -*- coding: utf-8 -*-
"""Classes e funções para uso geral"""
import datetime
import json

from django.forms import ModelForm
from django.forms.fields import BooleanField, CharField, DateField, \
    DateTimeField, IntegerField, ChoiceField


def conversor_json(o):
    """Conversões para o JSON do form"""
    if isinstance(o, datetime.date):
        return o.__str__()


class CustomModelForm(ModelForm):
    """ModelForm a ser utilizado"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        preparar_classes_form(self)

        self.serializar_fields()

    def serializar_fields(self):
        self.fields_dict = {}
        for field in self.visible_fields():
            self.fields_dict[field.name] = field.value()
            if field.name in self.errors:
                self.fields_dict[field.name +
                                 'Errors'] = list(self.errors[field.name])
            else:
                self.fields_dict[field.name + 'Errors'] = []
            if isinstance(field.field, ChoiceField):
                self.fields_dict[field.name +
                                 'Choices'] = field.field.choicesFormatado
        for field in self.hidden_fields():
            self.fields_dict[field.name] = field.value()
        self.fields_dict = json.dumps(self.fields_dict, default=conversor_json)


def preparar_classes_form(form):
    """Preparar campos do form"""
    for bound_field in form.visible_fields():
        field = bound_field.field
        if isinstance(field, BooleanField):
            field.widget.attrs.update({
                'class': 'form-boolean'
            })
        elif isinstance(field, CharField):
            if 'class' not in field.widget.attrs or 'form-coordinates' \
                    not in field.widget.attrs['class']:
                field.widget.attrs.update({
                    'class': 'form-text'
                })
        elif isinstance(field, IntegerField):
            field.widget.attrs.update({
                'class': 'form-text'
            })
        elif isinstance(field, DateField):
            field.widget.attrs.update({
                'class': 'form-data'
            })
        elif isinstance(field, DateTimeField):
            field.widget.attrs.update({
                'class': 'form-data-hora'
            })
        elif isinstance(field, ChoiceField):
            field.empty_label = ''
            field.widget.attrs.update({
                'class': 'form-select'
            })
            field.choicesFormatado = [{'id': choice[0], 'nome': choice[1]}
                                      for choice in field.choices]
        # Preencher classes
        field.classes = field.widget.attrs['class']
