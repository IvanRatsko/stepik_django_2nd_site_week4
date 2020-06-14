from django.urls import path

from vacancies.views import CompanyView, CompaniesView
from vacancies.views import MainView
from vacancies.views import VacanciesCatView
from vacancies.views import VacanciesView
from vacancies.views import VacancySendView
from vacancies.views import VacancyView

urlpatterns = [
    path('', MainView.as_view()),
    path('vacancies/', VacanciesView.as_view()),
    path('vacancies/cat/<str:specialty>', VacanciesCatView.as_view()),
    path('vacancies/<int:vacancy_id>', VacancyView.as_view()),
    path('companies/<int:company_id>', CompanyView.as_view()),
    path('companies/', CompaniesView.as_view()),
    path('vacancies/<int:vacancy_id>/send', VacancySendView.as_view(), name='send'),

]
