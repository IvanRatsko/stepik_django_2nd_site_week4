from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView

# Create your views here.
from companies.forms import CreateCompanyForm, CreateVacancyForm
from vacancies.models import Company, Vacancy


class MyCompanyControlView(LoginRequiredMixin, FormView):
    login_url = '/login/'
    model = Company
    fields = ['name', 'location', 'logo', 'description', 'employee_count']
    template_name = 'companies/company-edit.html'
    form_class = CreateCompanyForm
    success_url = '/mycompany/control/'
    is_create = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_create'] = self.request.session.pop('is_create', False)
        context['is_update'] = self.request.session.pop('is_update', False)
        return context

    def get_form(self, form_class=form_class):
        try:
            company = Company.objects.get(owner=self.request.user)
            return form_class(instance=company, **self.get_form_kwargs())
        except Company.DoesNotExist:
            self.is_create = True
            return form_class(**self.get_form_kwargs())

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        form = self.get_form()
        if self.is_create:
            self.request.session['is_create'] = True
        else:
            self.request.session['is_update'] = True
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        instance: Company = form.save(commit=False)
        instance.owner = self.request.user
        instance.save()
        return super(MyCompanyControlView, self).form_valid(form)


class MyCompanyView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'companies/company-create.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if Company.objects.filter(owner=self.request.user).count():
            return redirect('/mycompany/control/')
        return super().dispatch(request, *args, **kwargs)


class MyCompanyVacanciesView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    template_name = 'companies/vacancy-list.html'
    model = Vacancy
    context_object_name = 'vacancies'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vacancies"] = Vacancy.objects.select_related('company').filter(company__owner=self.request.user)
        return context


class MyCompanyVacancyControlView(LoginRequiredMixin, FormView):
    login_url = '/login/'
    model = Vacancy
    fields = ['title', 'specialty', 'skills', 'description', 'salary_min', 'salary_max']
    template_name = 'companies/vacancy-edit.html'
    form_class = CreateVacancyForm
    is_create = False

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not Vacancy.objects.filter(company__owner=self.request.user, id=self.kwargs['vacancy_id']):
            return redirect('/mycompany/vacancies/')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('mycompany:vacancy', kwargs={'vacancy_id': self.kwargs['vacancy_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_create'] = self.request.session.pop('is_create', False)
        context['is_update'] = self.request.session.pop('is_update', False)
        return context

    def get_form(self, form_class=form_class):
        try:
            vacancy = Vacancy.objects.get(id=self.kwargs['vacancy_id'])
            return form_class(instance=vacancy, **self.get_form_kwargs())
        except Vacancy.DoesNotExist:
            self.is_create = True
            return form_class(**self.get_form_kwargs())

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        form = self.get_form()
        if self.is_create:
            self.request.session['is_create'] = True
        else:
            self.request.session['is_update'] = True
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        instance: Vacancy = form.save(commit=False)
        if not self.is_create:
            instance.id = self.kwargs['vacancy_id']
        instance.company = Company.objects.get(owner=self.request.user)
        instance.published_at = timezone.now()
        instance.save()
        return super(MyCompanyVacancyControlView, self).form_valid(form)


class MyCompanyVacancyCreateView(LoginRequiredMixin, FormView):
    login_url = '/login/'
    model = Vacancy
    fields = ['title', 'specialty', 'skills', 'description', 'salary_min', 'salary_max']
    template_name = 'companies/vacancy-edit.html'
    form_class = CreateVacancyForm
    success_url = '/'
    is_create = True
    vacancy_id = 0

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('mycompany:vacancy', kwargs={'vacancy_id': self.vacancy_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_create'] = self.request.session.pop('is_create', False)
        context['is_update'] = self.request.session.pop('is_update', False)
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        form = self.get_form()
        if self.is_create:
            self.request.session['is_create'] = True
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        instance: Vacancy = form.save(commit=False)
        if not self.is_create:
            instance.id = self.kwargs['vacancy_id']
        instance.company = Company.objects.get(owner=self.request.user)
        instance.published_at = timezone.now()
        instance.save()
        self.vacancy_id = instance.id
        return super(MyCompanyVacancyCreateView, self).form_valid(form)
