from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Q
from .models import Event
from .forms import EventForm, EventSearchForm


def index(request):
    """Главная страница с предстоящими мероприятиями"""
    now = timezone.now()
    events = Event.objects.filter(date__gte=now)

    # Поиск и фильтрация
    search_form = EventSearchForm(request.GET)
    if search_form.is_valid():
        search = search_form.cleaned_data.get('search')
        event_type = search_form.cleaned_data.get('event_type')

        if search:
            events = events.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(location__icontains=search)
            )
        if event_type:
            events = events.filter(event_type=event_type)

    context = {
        'events': events,
        'search_form': search_form,
        'page_title': 'Предстоящие мероприятия'
    }
    return render(request, 'events/index.html', context)


def event_detail(request, pk):
    """Страница детального просмотра мероприятия"""
    event = get_object_or_404(Event, pk=pk)
    context = {
        'event': event,
        'is_past': event.is_past_event()
    }
    return render(request, 'events/event_detail.html', context)


def past_events(request):
    """Страница прошедших мероприятий"""
    now = timezone.now()
    events = Event.objects.filter(date__lt=now)

    # Поиск и фильтрация
    search_form = EventSearchForm(request.GET)
    if search_form.is_valid():
        search = search_form.cleaned_data.get('search')
        event_type = search_form.cleaned_data.get('event_type')

        if search:
            events = events.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(location__icontains=search)
            )
        if event_type:
            events = events.filter(event_type=event_type)

    context = {
        'events': events,
        'search_form': search_form,
        'page_title': 'Прошедшие мероприятия'
    }
    return render(request, 'events/past_events.html', context)


def add_event(request):
    """Форма добавления нового мероприятия"""
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save()
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm()

    context = {
        'form': form,
        'page_title': 'Добавить мероприятие'
    }
    return render(request, 'events/add_event.html', context)