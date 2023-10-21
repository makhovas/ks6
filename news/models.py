from django.db import models

from users.models import User


# Create your models here.
class Client(models.Model):
    email = models.CharField(max_length=150, verbose_name='email', unique=True, null=True, blank=True)
    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    comment = models.CharField(max_length=100, verbose_name='коммент')
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return f'{self.full_name}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Mailing(models.Model):
    start_time = models.DateTimeField(verbose_name='время рассылки')
    frequency_choices = [('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')]
    frequency = models.CharField(max_length=10, choices=frequency_choices, verbose_name='периодичность')
    status_choices = [('created', 'Created'), ('started', 'Started'), ('completed', 'Completed')]
    status = models.CharField(max_length=10, choices=status_choices, verbose_name='статус рассылки')
    recipients = models.ManyToManyField(Client)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

class Message(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, null=True, verbose_name='рассылкa')
    subject = models.CharField(max_length=100, verbose_name='тема письма')
    body = models.TextField(verbose_name='тело письма')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

class Log(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='дата и время последней попытки')
    status = models.CharField(max_length=20, verbose_name='статус попытки')
    response = models.TextField(verbose_name='ответ почтового сервера, если он был')
