from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Order
from django.views import generic
from .forms import SearchForm
from django.http import Http404
from django.urls import reverse_lazy

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer


class OrderCreate(LoginRequiredMixin, CreateView):
    model = Order
    template_name = 'order/order_form.html'
    fields = (
        'mechanism',
        'material',
        'address',
        'contacts'
    )

    # def get_success_url(self):
    #     return self.request.GET['next']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class OrderUpdate(LoginRequiredMixin, UpdateView):
    model = Order
    template_name = 'order/order_form.html'
    fields = (
        'mechanism',
        'material',
        'address',
        'contacts'
    )

    def get_object(self, queryset=None):
        obj = super().get_object()
        if not self.request.user.is_superuser:
            if not obj.author == self.request.user:
                raise Http404
        return obj


class OrderDelete(LoginRequiredMixin, DeleteView):
    model = Order
    template_name = 'order/order_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('order_list')

    def get_object(self, queryset=None):
        obj = super().get_object()
        if not self.request.user.is_superuser:
            if not obj.author == self.request.user:
                raise Http404
        return obj


class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = Order
    template_name = 'order/order_detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object()
        if not self.request.user.is_superuser:
            if not obj.author == self.request.user:
                raise Http404
        return obj


class OrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'order/order_list.html'
    form_class = SearchForm
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm()
        return context

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            if self.request.user.is_superuser:
                return Order.objects.filter(id__icontains=form.cleaned_data['query'])
            else:
                return Order.objects.filter(author=self.request.user).filter(id__icontains=form.cleaned_data['query'])
        if self.request.user.is_superuser:
            return Order.objects.all()
        else:
            return Order.objects.filter(author=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
