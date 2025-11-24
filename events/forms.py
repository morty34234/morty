from django import forms
from .models import Event
from django.utils import timezone


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title', 'description', 'date', 'location',
            'event_type', 'image', 'price'
        ]
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'title': 'Название мероприятия',
            'description': 'Подробное описание',
            'date': 'Дата и время',
            'location': 'Место проведения',
            'event_type': 'Тип мероприятия',
            'image': 'Изображение',
            'price': 'Цена билета',
        }

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date < timezone.now():
            raise forms.ValidationError("Дата мероприятия не может быть в прошлом!")
        return date


class EventSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        label='Поиск',
        widget=forms.TextInput(attrs={'placeholder': 'Поиск мероприятий...'})
    )
    event_type = forms.ChoiceField(
        choices=[('', 'Все типы')] + Event.EVENT_TYPES,
        required=False,
        label='Тип мероприятия'
    )