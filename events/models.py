from django.db import models
from django.contrib.auth.models import User
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
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, verbose_name='Тип мероприятия')
    image = models.ImageField(upload_to='events/', blank=True, null=True, verbose_name='Изображение')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'pk': self.pk})

    def is_past(self):
        return self.date < timezone.now()

    def get_comments_count(self):
        return self.comments.filter(active=True).count()


class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Комментарий от {self.author}'