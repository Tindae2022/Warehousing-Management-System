from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth import logout
from django.shortcuts import redirect


class CustomerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    date_of_birth = forms.DateField(required=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password1", "password2", "date_of_birth"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = User.CUSTOMER
        if commit:
            user.save()
        return user



class SalesManagerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    date_of_birth = forms.DateField(required=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password1", "password2", "date_of_birth"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = User.SALES_MANAGER
        if commit:
            user.save()
        return user


class WarehouseManagerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    date_of_birth = forms.DateField(required=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password1", "password2", "date_of_birth"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = User.WAREHOUSE_MANAGER
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'bio', 'profile_picture', 'instagram_handle', 'twitter_handle']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'bio': 'Bio',
            'profile_picture': 'Profile Picture',
            'instagram_handle': 'Instagram Handle',
            'twitter_handle': 'Twitter Handle',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email != self.instance.email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email


class CustomerUpdateForm(UserUpdateForm):
    class Meta(UserUpdateForm.Meta):
        fields = UserUpdateForm.Meta.fields + ['date_of_birth', 'gender', 'address', 'phone_number']
        labels = UserUpdateForm.Meta.labels
        labels.update({
            'date_of_birth': 'Date of Birth',
            'gender': 'Gender',
            'address': 'Address',
            'phone_number': 'Phone Number',
        })
        widgets = UserUpdateForm.Meta.widgets
        widgets.update({
            'address': forms.Textarea(attrs={'rows': 3}),
        })


class SalesManagerUpdateForm(UserUpdateForm):
    class Meta(UserUpdateForm.Meta):
        fields = UserUpdateForm.Meta.fields + ['date_of_birth', 'gender', 'address', 'phone_number']
        labels = UserUpdateForm.Meta.labels
        labels.update({
            'date_of_birth': 'Date of Birth',
            'gender': 'Gender',
            'address': 'Address',
            'phone_number': 'Phone Number',
        })
        widgets = UserUpdateForm.Meta.widgets
        widgets.update({
            'address': forms.Textarea(attrs={'rows': 3}),
        })


class WarehouseManagerUpdateForm(UserUpdateForm):
    class Meta(UserUpdateForm.Meta):
        fields = UserUpdateForm.Meta.fields + ['date_of_birth', 'gender', 'address', 'phone_number']
        labels = UserUpdateForm.Meta.labels
        labels.update({
            'date_of_birth': 'Date of Birth',
            'gender': 'Gender',
            'address': 'Address',
            'phone_number': 'Phone Number',
        })
        widgets = UserUpdateForm.Meta.widgets
        widgets.update({
            'address': forms.Textarea(attrs={'rows': 3}),
        })


class UserLoginForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'placeholder': 'Enter Email'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'placeholder': "Enter Password"}))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)

            if user is None:
                raise forms.ValidationError('Invalid email or password')
            if not user.is_active:
                raise forms.ValidationError('This account is inactive')

            self.user = user

        return cleaned_data

    def get_user(self):
        return getattr(self, 'user', None)


def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page or any other page
