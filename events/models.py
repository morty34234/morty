from django.db import models
from django.urls import reverse
from django.utils import timezone


class Event(models.Model):
    EVENT_TYPES = [
        ('concert', 'Концерт'),
        ('exhibition', 'Выставка'),
        ('theater', 'Театр'),
        ('festival', 'Фестиваль'),
        ('sport', 'Спорт'),
        ('conference', 'Конференция'),
        ('other', 'Другое'),
    ]

    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    date = models.DateTimeField(verbose_name='Дата и время')
    location = models.CharField(max_length=200, verbose_name='Место проведения')
    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPES,
        verbose_name='Тип мероприятия'
    )
    image = models.ImageField(
        upload_to='events/',
        blank=True,
        null=True,
        verbose_name='Изображение'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Цена'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
        ordering = ['date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'pk': self.pk})

    def is_past_event(self):
        return self.date < timezone.now()

    def is_upcoming_event(self):
        return self.date >= timezone.now()