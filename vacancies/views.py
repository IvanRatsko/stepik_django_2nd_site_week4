from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseNotFound, HttpResponseForbidden
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import FormMixin

from vacancies.forms import SendApplicationForm
# Create your views here.
from vacancies.models import Specialty, Company, Vacancy, Application


class MainView(TemplateView):
    template_name = 'vacancies/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specialties'] = Specialty.objects.all()
        context['companies'] = Company.objects.all()
        context['vacancies'] = Vacancy.objects.all()
        return context


class CompanyView(TemplateView):
    template_name = 'vacancies/company.html'

    def get_context_data(self, company_id, **kwargs):
        context = super().get_context_data(**kwargs)
        if not Company.objects.filter(id=company_id).exists():
            raise Http404('Компания с ID {0} отсутствует'.format(company_id))
        context['vacancies'] = Vacancy.objects.select_related('company').filter(company__id=company_id)
        context['company'] = Company.objects.get(id=company_id)
        context['prev_url'] = self.request.META.get('HTTP_REFERER')
        return context


class CompaniesView(ListView):
    model = Company
    queryset = Company.objects.all()
    context_object_name = 'companies'
    template_name = 'vacancies/companies.html'
    title = 'Все компании'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class VacanciesCatView(TemplateView):
    template_name = 'vacancies/vacancies.html'

    def get_context_data(self, specialty, **kwargs):
        context = super().get_context_data(**kwargs)
        if not Specialty.objects.filter(code=specialty).exists():
            raise Http404("Специализация {0} отсутствует".format(specialty))
        context["vacancies"] = Vacancy.objects.filter(specialty__code=specialty)
        context["title"] = Specialty.objects.get(code=specialty).title
        return context


class VacanciesView(ListView):
    model = Vacancy
    queryset = Vacancy.objects.select_related('company').all()
    context_object_name = 'vacancies'
    template_name = 'vacancies/vacancies.html'
    title = 'Все вакансии'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class VacancyView(FormMixin, DetailView):
    template_name = 'vacancies/vacancy.html'
    pk_url_kwarg = 'vacancy_id'
    model = Vacancy
    queryset = Vacancy.objects.select_related('company').all()
    form_class = SendApplicationForm

    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prev_url'] = self.request.META.get('HTTP_REFERER')
        return context

    def get_success_url(self):
        return reverse('vacancies:send', kwargs={'vacancy_id': self.kwargs['vacancy_id']})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        instance: Application = form.save(commit=False)
        instance.vacancy = Vacancy.objects.get(id=self.kwargs[self.pk_url_kwarg])
        instance.user = self.request.user
        instance.save()
        return super(VacancyView, self).form_valid(form)


class VacancySendView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'vacancies/sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prev_url'] = self.request.META.get('HTTP_REFERER')
        return context


def custom_handler404(request, exception):
    return HttpResponseNotFound('<h1 align="center">Ошибка 404 {0}</h1>'.format(exception))


def custom_handler500(request):
    return HttpResponseNotFound('<h1 align="center">Ошибка 500</h1>')
