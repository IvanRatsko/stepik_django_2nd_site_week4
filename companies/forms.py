from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column, Field
from django import forms

from vacancies.models import Company, Vacancy


class CreateCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'location', 'logo', 'description', 'employee_count']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('logo', css_class='form-group col-md-6 mb-0'),

            ),
            Row(
                Column('employee_count', css_class='form-group col-md-6 mb-0'),
                Column('location', css_class='form-group col-md-6 mb-0'),
            ),
            'description',
            Submit('submit', 'Сохранить')

        )


class CreateVacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ['title', 'specialty', 'skills', 'description', 'salary_min', 'salary_max']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-6 mb-0'),
                Column('specialty', css_class='form-group col-md-6 mb-0'),

            ),
            Row(
                Column('salary_min', css_class='form-group col-md-6 mb-0'),
                Column('salary_max', css_class='form-group col-md-6 mb-0'),
            ),
            Field('skills', style="height: 75px;", css_class='form-group md-6 mb-0 height'),
            'description',
            Submit('submit', 'Сохранить')

        )
