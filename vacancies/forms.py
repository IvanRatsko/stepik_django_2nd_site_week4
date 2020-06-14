from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from vacancies.models import Application


class SendApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['written_username', 'written_phone', 'written_cover_letter']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Отозваться на вакансию', css_class='btn btn-primary btn-lg btn-block'))
        self.helper.form_method = 'post'
