from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.core.exceptions import ValidationError
from .models import Instructor
from courses.models import Course, Module, Content

MyUser = get_user_model()


class SignupForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'First name',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Last name',
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Email address',
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat password',
    }))

    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_email = MyUser.objects.filter(email=email)
        if user_email.exists():
            raise ValidationError("User with this email already exists")
        return email


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name')


class InstructorUpdateForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False,
                                       widget=forms.FileInput, error_messages={'invalid': ('Image files only')})

    class Meta:
        model = Instructor
        fields = ('profile_picture', 'about', 'descriptions')


class CreateClassForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ('instructor', 'slug', 'status', 'students')


class CreateModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        exclude = ('module_title_slug',)


class CreateContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ('module', 'title',
                  'content_description', 'content_video',
                  'content_image', 'content_file'
                  )
