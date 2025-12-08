from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .models import Event, Comment
from .forms import EventForm, EventSearchForm, CommentForm, CustomUserCreationForm, UserUpdateForm

def index(request):

    now = timezone.now()
    events = Event.objects.filter(date__gte=now)

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

    return render(request, 'events/index.html', {
        'events': events,
        'search_form': search_form,
        'page_title': 'Предстоящие мероприятия'
    })


def event_detail(request, pk):

    event = get_object_or_404(Event, pk=pk)
    comments = event.comments.filter(active=True).order_by('-created_at')
    comment_form = CommentForm()


    if request.method == 'POST' and 'add_comment' in request.POST:
        if not request.user.is_authenticated:
            messages.error(request, 'Чтобы оставить комментарий, нужно войти в аккаунт.')
            return redirect('login')

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.event = event
            comment.author = request.user
            comment.save()
            messages.success(request, 'Комментарий добавлен!')
            return redirect('event_detail', pk=event.pk)

    return render(request, 'events/event_detail.html', {
        'event': event,
        'is_past': event.date < timezone.now(),
        'comments': comments,
        'comment_form': comment_form,
        'comments_count': comments.count(),
    })


def past_events(request):

    now = timezone.now()
    events = Event.objects.filter(date__lt=now)

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

    return render(request, 'events/past_events.html', {
        'events': events,
        'search_form': search_form,
        'page_title': 'Прошедшие мероприятия'
    })


def add_event(request):

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save()
            messages.success(request, 'Мероприятие успешно добавлено!')
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm()

    return render(request, 'events/add_event.html', {
        'form': form,
        'page_title': 'Добавить мероприятие'
    })
def register(request):

    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('index')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {
        'form': form,
        'title': 'Регистрация'
    })


@login_required
def profile(request):

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    user_comments = Comment.objects.filter(author=request.user).order_by('-created_at')[:10]

    return render(request, 'registration/profile.html', {
        'form': form,
        'user_comments': user_comments,
        'title': 'Мой профиль'
    })