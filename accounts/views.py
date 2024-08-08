from django.contrib import auth, messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, RedirectView, UpdateView, DetailView
from .forms import CustomerRegistrationForm, SalesManagerRegistrationForm, WarehouseManagerRegistrationForm, \
    UserLoginForm, logout
from .forms import CustomerUpdateForm, SalesManagerUpdateForm, WarehouseManagerUpdateForm
from .models import User


class RegisterCustomerView(CreateView):
    model = User
    form_class = CustomerRegistrationForm
    template_name = "accounts/register_customer.html"
    success_url = reverse_lazy("accounts:login")

    extra_context = {"title": "Register as Customer"}

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        password = form.cleaned_data.get("password1")
        user.set_password(password)
        user.user_type = User.CUSTOMER
        user.save()
        return redirect(self.success_url)


class RegisterSalesManagerView(CreateView):
    model = User
    form_class = SalesManagerRegistrationForm
    template_name = "accounts/register_sales_manager.html"
    success_url = reverse_lazy("accounts:login")

    extra_context = {"title": "Register as Sales Manager"}

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        password = form.cleaned_data.get("password1")
        user.set_password(password)
        user.user_type = User.SALES_MANAGER
        user.save()
        return redirect(self.success_url)


class RegisterWarehouseManagerView(CreateView):
    model = User
    form_class = WarehouseManagerRegistrationForm
    template_name = "accounts/register_warehouse_manager.html"
    success_url = reverse_lazy("accounts:login")

    extra_context = {"title": "Register as Warehouse Manager"}

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        password = form.cleaned_data.get("password1")
        user.set_password(password)
        user.user_type = User.WAREHOUSE_MANAGER
        user.save()
        return redirect(self.success_url)


class UpdateCustomerView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomerUpdateForm
    template_name = "accounts/update_customer.html"
    success_url = reverse_lazy("accounts:profile")

    def get_queryset(self):
        return User.objects.filter(user_type=User.CUSTOMER)

    def get_object(self, queryset=None):
        return self.request.user


class UpdateSalesManagerView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = SalesManagerUpdateForm
    template_name = "accounts/update_sales_manager.html"
    success_url = reverse_lazy("accounts:profile")

    def get_queryset(self):
        return User.objects.filter(user_type=User.SALES_MANAGER)

    def get_object(self, queryset=None):
        return self.request.user


class UpdateWarehouseManagerView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = WarehouseManagerUpdateForm
    template_name = "accounts/update_warehouse_manager.html"
    success_url = reverse_lazy("accounts:profile")

    def get_queryset(self):
        return User.objects.filter(user_type=User.WAREHOUSE_MANAGER)

    def get_object(self, queryset=None):
        return self.request.user


class LoginView(FormView):
    form_class = UserLoginForm
    template_name = "accounts/login.html"
    success_url = reverse_lazy("home")

    extra_context = {"title": "Login"}

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        if "next" in self.request.GET and self.request.GET["next"]:
            return self.request.GET["next"]
        return self.success_url

    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class LogoutView(RedirectView):
    url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, "You are now logged out")
        return super().get(request, *args, **kwargs)



