import os

import django

from vacancies.models import Specialty, Vacancy, Company

os.environ.setdefault("DJANGO_SETTINGS_MODULE", __file__)

django.setup()

""" Вакансии """

jobs = [

    {"title": "Разработчик на Python", "cat": "backend", "company": "staffingsmarter", "salary_from": "100000",
     "salary_to": "150000", "posted": "2020-03-11", "desc": "Потом добавим"},
    {"title": "Разработчик в проект на Django", "cat": "backend", "company": "swiftattack", "salary_from": "80000",
     "salary_to": "90000", "posted": "2020-03-11", "desc": "Потом добавим"},
    {"title": "Разработчик на Swift в аутсорс компанию", "cat": "backend", "company": "swiftattack",
     "salary_from": "120000", "salary_to": "150000", "posted": "2020-03-11", "desc": "Потом добавим"},
    {"title": "Мидл программист на Python", "cat": "backend", "company": "workiro", "salary_from": "80000",
     "salary_to": "90000", "posted": "2020-03-11", "desc": "Потом добавим"},
    {"title": "Питонист в стартап", "cat": "backend", "company": "primalassault", "salary_from": "120000",
     "salary_to": "150000", "posted": "2020-03-11", "desc": "Потом добавим"}

]

""" Компании """

companies = [

    {"title": "workiro"},
    {"title": "rebelrage"},
    {"title": "staffingsmarter"},
    {"title": "evilthreath"},
    {"title": "hirey"},
    {"title": "swiftattack"},
    {"title": "troller"},
    {"title": "primalassault"}
]

""" Категории """

specialties = [
    {"code": "frontend", "title": "Фронтенд"},
    {"code": "backend", "title": "Бэкенд"},
    {"code": "gamedev", "title": "Геймдев"},
    {"code": "devops", "title": "Девопс"},
    {"code": "design", "title": "Дизайн"},
    {"code": "products", "title": "Продукты"},
    {"code": "management", "title": "Менеджмент"},
    {"code": "testing", "title": "Тестирование"}

]

# Добавление данных в базу

""" Категории """
for specialty in specialties:
    new_specialty = Specialty(code=specialty["code"], title=specialty["title"], picture="https://place-hold.it/100x60")
    # new_specialty.save()

""" Компании """
for company in companies:
    new_company = Company(name=company["title"], logo="https://place-hold.it/100x60")
    # new_company.save()

""" Вакансии """
for job in jobs:
    new_job = Vacancy(title=job["title"], specialty=Specialty.objects.get(code=job["cat"]),
                      salary_min=job["salary_from"], company=Company.objects.get(name=job["company"]),
                      salary_max=job["salary_to"], published_at=job["posted"], description=job["desc"])
    # new_job.save()
