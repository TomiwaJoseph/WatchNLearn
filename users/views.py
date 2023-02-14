from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignupForm, UserUpdateForm, InstructorUpdateForm, CreateClassForm, CreateModuleForm, CreateContentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Instructor, CustomUser, BookmarkList
# from django.utils.encoding import force_bytes, force_text
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode, is_safe_url
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from main.models import LandingPagePictures, InstructorPagePictures
from courses.models import Course, Module
from django.contrib.auth.decorators import permission_required
from random import randint

# Ajax Requests


def delete_bookmark_item(request):
    course_to_delete = int(request.GET.get('_course_id'))
    bookmark_object_qs = BookmarkList.objects.get(user=request.user)
    bookmark_object_qs.folder.remove(Course.objects.get(id=course_to_delete))
    return HttpResponse('Success')


@permission_required("customuser.is_superuser")
def admin_draft_view(request):
    context = {
        "all_drafts": Course.objects.filter(status="draft")
    }
    return render(request, "admin_views/drafts.html", context)


def login_view(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    next_url = request.session['next_url']
    user = authenticate(request,
                        email=email,
                        password=password
                        )
    if user is not None:
        login(request, user)
        if next_url:
            return HttpResponseRedirect(next_url)
        return redirect('index')
    else:
        messages.error(request, "Invalid login")
        return redirect('signup_login')


def sign_in_or_register(request):
    next_url = request.GET.get('next')
    request.session['next_url'] = next_url
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        sign_up_form = SignupForm(request.POST)
        if sign_up_form.is_valid():
            user = sign_up_form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = f'{self.request.scheme}://{self.request.get_host()}'
            link = reverse('activate', kwargs={
                'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })
            activate_url = current_site + link

            mail_subject = 'Activate your WatchnLearn account'
            message = f"Hi {user.first_name}! Please click this link to verify your account\n" + activate_url
            to_email = sign_up_form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send(fail_silently=True)
            return redirect('awaiting_activation')
    else:
        sign_up_form = SignupForm()
    return render(request, 'registration/login_signup.html', {'sign_up_form': sign_up_form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "Welcome! Start learning.")
        return redirect('index')
    else:
        return HttpResponse('Activation link is invalid')


def awaiting_activation(request):
    return render(request, "registration/awaiting_activation.html")


def instructor_profile(request, user_first_name, user_id):
    query = Instructor.objects.filter(
        user__first_name=user_first_name, id=user_id)
    if not query.exists():
        return redirect("courses")
    instructor_courses = Course.objects.filter(
        instructor=query.first().user, status='published')
    context = {
        'instructor_courses': instructor_courses,
        'instructor': query.first(),
    }
    return render(request, 'users/instructor_profile.html', context)


def profile(request, user_first_name, user_id):
    query = Instructor.objects.filter(
        user__first_name=user_first_name, id=user_id)
    if not query.exists():
        return redirect("courses")
    my_courses = Course.objects.filter(
        instructor=request.user, status='published')
    context = {
        'my_courses': my_courses,
        'instructor': query.first(),
    }
    return render(request, 'users/profile.html', context)


@login_required
def profile_edit(request):
    if not request.user.is_instructor:
        return redirect("index")

    user_update_form = UserUpdateForm(instance=request.user)
    instructor_update_form = InstructorUpdateForm(
        instance=Instructor.objects.get(
            user=request.user,
        )
    )

    if request.method == "POST":
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        instructor_update_form = InstructorUpdateForm(
            request.POST, request.FILES,
            instance=Instructor.objects.get(
                user=request.user,
            )
        )
        if user_update_form.is_valid() and instructor_update_form.is_valid():
            user_update_form.save()
            instructor_update_form.save()
            return redirect('profile', request.user.first_name, request.user.user_instructor.first().id)
    context = {
        'user_update_form': user_update_form,
        'instructor_update_form': instructor_update_form,
    }
    return render(request, 'users/edit_profile.html', context)


def instructor(request):
    random_pick = randint(0, InstructorPagePictures.objects.count() - 1)
    random_picture = InstructorPagePictures.objects.all()[random_pick]
    context = {
        "instructor_picture": random_picture,
    }
    return render(request, "users/instructor.html", context)


@login_required
def instrutor_create_class(request):
    if request.method == "POST":
        class_create_form = CreateClassForm(request.POST, request.FILES)
        if class_create_form.is_valid():
            all_keywords = class_create_form.cleaned_data.get("keywords")
            obj = class_create_form.save(commit=False)
            obj.instructor = request.user
            obj.status = "draft"
            obj.save()
            obj.keywords.add(*all_keywords)
            return redirect('await_approval')
    else:
        class_create_form = CreateClassForm()
    return render(request, "users/create_class.html", {"class_create_form": class_create_form})


@login_required
def create_module(request):
    if not request.user.is_instructor:
        return redirect("index")
    if request.method == "POST":
        module_create_form = CreateModuleForm(request.POST)
        if module_create_form.is_valid():
            obj = module_create_form.save(commit=False)
            obj.save()
            if not obj.course in request.user.profile.courses_bought.all():
                request.user.profile.courses_bought.add(obj.course)
            return redirect('create_content')
    else:
        module_create_form = CreateModuleForm()
        module_create_form.fields['course'].queryset = Course.objects.filter(
            instructor=request.user, status="draft")
    return render(request, "instructors/create_module.html", {"module_create_form": module_create_form})


@login_required
def create_content(request):
    if not request.user.is_instructor:
        return redirect("index")
    if request.method == "POST":
        content_create_form = CreateContentForm(request.POST, request.FILES)
        if content_create_form.is_valid():
            content_create_form.save()
            return redirect('create_content')
    else:
        content_create_form = CreateContentForm()
        content_create_form.fields['module'].queryset = Module.objects.filter(
            course__instructor=request.user, course__status="draft")
    return render(request, "instructors/create_content.html", {"content_create_form": content_create_form})


def class_created_pending(request):
    return render(request, "users/class_pending.html")


@login_required
def instructor_drafts(request):
    my_drafts = Course.objects.filter(instructor=request.user, status='draft')
    context = {
        'my_drafts': my_drafts,
    }
    return render(request, "instructors/instructor_drafts.html", context)


@login_required
def my_learning(request):
    all_courses = request.user.profile.courses_bought.all()
    my_courses = [
        course for course in all_courses if course.instructor != request.user]
    context = {
        'my_courses': my_courses,
    }
    return render(request, "users/my_learning.html", context)


@login_required
def my_bookmarks(request):
    try:
        all_bookmarked_courses = request.user.user_bookmarks.folder.all()
    except:
        all_bookmarked_courses = []

    context = {
        'all_bookmarked_courses': all_bookmarked_courses,
    }
    return render(request, "users/my_bookmarks.html", context)
