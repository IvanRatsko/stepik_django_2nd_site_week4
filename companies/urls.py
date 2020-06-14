from django.urls import path

from companies.views import MyCompanyControlView, MyCompanyVacancyCreateView
from companies.views import MyCompanyVacanciesView
from companies.views import MyCompanyVacancyControlView
from companies.views import MyCompanyView

urlpatterns = [
    path('mycompany/', MyCompanyView.as_view()),
    path('mycompany/vacancies/', MyCompanyVacanciesView.as_view()),
    path('mycompany/vacancies/<int:vacancy_id>', MyCompanyVacancyControlView.as_view(), name='vacancy'),
    path('mycompany/vacancies/create_vacancy/', MyCompanyVacancyCreateView.as_view()),
    path('mycompany/control/', MyCompanyControlView.as_view())

]
