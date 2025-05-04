from datetime import date, timedelta
from pyexpat.errors import messages
from rest_framework import viewsets, permissions
from .models import Subscription, Category
from .serializers import SubscriptionSerializer, CategorySerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import SubscriptionForm, UserProfileForm
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

@login_required
def subscription_list(request):
    subscriptions = Subscription.objects.filter(user=request.user).order_by('due_date')

    for sub in subscriptions:
        if sub.is_paid and sub.due_date and sub.due_date < date.today():
            sub.is_paid = False
            sub.save()

    return render(request, 'subscriptions/subscription_list.html', {
        'subscriptions': subscriptions,
    })

@login_required
def subscription_add(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.user = request.user
            sub.save()
            return redirect('subscription_list')
    else:
        form = SubscriptionForm()
    return render(request, 'subscriptions/subscription_form.html', {'form': form, 'title': 'Добавить подписку'})

@login_required
def subscription_edit(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk, user=request.user)
    if request.method == 'POST':
        form = SubscriptionForm(request.POST, instance=subscription)
        if form.is_valid():
            form.save()
            return redirect('subscription_list')
    else:
        form = SubscriptionForm(instance=subscription)
    return render(request, 'subscriptions/subscription_form.html', {'form': form, 'title': 'Редактировать подписку'})

@login_required
def subscription_delete(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk, user=request.user)
    if request.method == 'POST':
        subscription.delete()
        return redirect('subscription_list')
    return render(request, 'subscriptions/subscription_confirm_delete.html', {'subscription': subscription})

@login_required
def user_settings(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('subscription_list')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'subscriptions/user_settings.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def mark_as_paid(request, pk):
    sub = get_object_or_404(Subscription, pk=pk, user=request.user)
    sub.is_paid = True
    sub.paid_date = timezone.now().date()
    sub.save()
    return redirect('subscription_list')