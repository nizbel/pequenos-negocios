"""
Formulários para usuários
"""
import json
from allauth.account.forms import SignupForm, ResetPasswordForm, \
    ResetPasswordKeyForm
from apn.utils import conversor_json, preparar_classes_form


class CustomSignupForm(SignupForm):
    """Formulário para cadastro"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        preparar_classes_form(self)

        self.fields['password1'].help_text = ''
        self.fields_dict = {}
        for field in self.visible_fields():
            self.fields_dict[field.name] = field.value()
            if field.name in self.errors:
                self.fields_dict[field.name +
                                 'Errors'] = list(self.errors[field.name])
            else:
                self.fields_dict[field.name + 'Errors'] = []
        self.fields_dict = json.dumps(self.fields_dict, default=conversor_json)


class CustomResetPasswordForm(ResetPasswordForm):
    """Formulário para resetar senha"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        preparar_classes_form(self)

        self.fields_dict = {}
        for field in self.visible_fields():
            self.fields_dict[field.name] = field.value()
            if field.name in self.errors:
                self.fields_dict[field.name +
                                 'Errors'] = list(self.errors[field.name])
            else:
                self.fields_dict[field.name + 'Errors'] = []
        self.fields_dict = json.dumps(self.fields_dict, default=conversor_json)


class CustomResetPasswordKeyForm(ResetPasswordKeyForm):
    """Formulário para configurar nova senha"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        preparar_classes_form(self)

        self.fields_dict = {}
        for field in self.visible_fields():
            self.fields_dict[field.name] = field.value()
            if field.name in self.errors:
                self.fields_dict[field.name +
                                 'Errors'] = list(self.errors[field.name])
            else:
                self.fields_dict[field.name + 'Errors'] = []
        self.fields_dict = json.dumps(self.fields_dict, default=conversor_json)
