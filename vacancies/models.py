from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Vacancy(models.Model):
    title = models.CharField(verbose_name='Название', max_length=128)
    specialty = models.ForeignKey('Specialty', on_delete=models.CASCADE, verbose_name='Специализация',
                                  related_name='vacancies')
    company = models.ForeignKey('Company', on_delete=models.CASCADE, verbose_name='Компания', related_name='vacancies')
    skills = models.TextField(verbose_name='Навыки', )
    description = models.TextField(verbose_name='Описание', )
    salary_min = models.CharField(verbose_name='Зарплата от', max_length=64)
    salary_max = models.CharField(verbose_name='Зарплата до', max_length=64)
    published_at = models.DateField(verbose_name='Дата размещения')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'вакансию'
        verbose_name_plural = 'вакансии'


class Company(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=128)
    location = models.CharField(verbose_name='Расположение', max_length=64)
    logo = models.ImageField(verbose_name='Логотип', )
    description = models.TextField(verbose_name='Описание', )
    employee_count = models.CharField(verbose_name='Численность', max_length=64)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'компанию'
        verbose_name_plural = 'компании'


class Specialty(models.Model):
    code = models.CharField(max_length=64)
    title = models.CharField(max_length=128)
    picture = models.ImageField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'специализацию'
        verbose_name_plural = 'специализации'


class Application(models.Model):
    written_username = models.CharField(verbose_name='Вас зовут', max_length=64)
    written_phone = models.CharField(verbose_name='Ваш телефон', max_length=64)
    written_cover_letter = models.TextField(verbose_name='Сопроводительное письмо', )
    vacancy = models.ForeignKey('Vacancy', on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')

    def __str__(self):
        return self.written_username

    class Meta:
        verbose_name = 'отклик'
        verbose_name_plural = 'отклики'
