from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView, TemplateView, View
from .models import Course, Category, Module, Content
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.text import slugify
from django.conf import settings
from django.http.response import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from .forms import ReviewForm
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import Profile, CustomUser, BookmarkList

stripe.api_key = settings.STRIPE_SECRET_KEY

# ajax request starts


def bookmark_it(request):
    course_id = int(request.GET.get('course_id'))
    course_to_add_to_bookmarks = Course.objects.get(id=course_id)
    try:
        check_bookmarklist_exist = BookmarkList.objects.filter(
            user=request.user).first()
        if check_bookmarklist_exist:
            check_course_exist = course_id in [
                i.id for i in check_bookmarklist_exist.folder.all()]
            if not check_course_exist:
                check_bookmarklist_exist.folder.add(course_to_add_to_bookmarks)
        else:
            create_new_bookmarkslist = BookmarkList.objects.create(
                user=request.user)
            create_new_bookmarkslist
            create_new_bookmarkslist.folder.add(course_to_add_to_bookmarks)
        return JsonResponse({'status': 'success'})
    except TypeError:
        return JsonResponse({'status': 'fail'})


# ajax request ends


class CourseListView(ListView):
    queryset = Course.objects.filter(status="published")
    template_name = 'courses/courses.html'
    context_object_name = 'courses'
    paginate_by = 6


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_in_detail = context['object']
        all_modules = object_in_detail.course_modules.all()
        all_course_students = object_in_detail.students.all()
        all_reviews = object_in_detail.course_review.all()
        if self.request.user.is_superuser or self.request.user in all_course_students or object_in_detail.price == 0:
            context['course_student'] = True
        context['review_form'] = ReviewForm
        context['all_reviews'] = all_reviews
        context['all_modules'] = all_modules
        return context


def get_category_courses(request, category):
    filtered_category = Course.objects.filter(
        category__slug=category, status="published"
    )
    all_filtered_category = request.GET.get('page', 1)
    all_category_courses = Paginator(filtered_category, 6)

    try:
        category_courses = all_category_courses.page(all_filtered_category)
    except PageNotAnInteger:
        category_courses = all_category_courses.page(1)
    except EmptyPage:
        category_courses = all_category_courses.page(
            category_courses.num_pages)

    context = {
        'category_courses': category_courses,
        'category': filtered_category[0].category.category_title,
        'main_category': Category.objects.get(slug=category),
    }
    return render(request, 'courses/course_filter.html', context)


@login_required
def view_content(request, obj, module_slug, content_id):
    course = Module.objects.get(
        course__slug=obj, module_title_slug=module_slug).course
    if request.user.is_superuser or course in request.user.profile.courses_bought.all() or course.price == 0:
        content = Content.objects.get(id=content_id)
    else:
        messages.info(
            request, "You have to buy the course to view the content")
        return redirect('course_detail', slug=course.slug)
    context = {
        'content': content,
    }
    return render(request, "courses/content_view.html", context)


def save_review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        get_course = request.POST.get('course')
        course = Course.objects.get(title=get_course)
        all_course_students = course.students.all()

        if form.is_valid():
            if request.user in all_course_students:
                obj = form.save(commit=False)
                obj.course = course
                obj.student = request.user
                obj.save()

        return redirect('course_detail', slug=course.slug)


def free_course(request):
    query = Course.objects.filter(price=0, status="published")
    context = {
        "free_courses": query,
    }
    return render(request, "courses/free-courses.html", context)


def success(request):
    return render(request, 'courses/success.html')


def cancel(request):
    return render(request, 'courses/cancel.html')


@login_required
def confirm_buy(request, course):
    course_to_buy = Course.objects.get(slug=course)
    if course_to_buy in request.user.profile.courses_bought.all():
        messages.info(request, "You already bought this course.")
        return redirect('course_detail', slug=course_to_buy.slug)
    request.session['course_to_buy'] = course_to_buy.id
    context = {
        "course_to_buy": course_to_buy,
        "STRIPE_PUBLISHABLE_KEY": settings.STRIPE_PUBLISHABLE_KEY
    }
    return render(request, "courses/confirm_buy.html", context)


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        course_to_buy = int(request.session['course_to_buy'])
        course = Course.objects.get(id=course_to_buy)
        domain_url = f'{self.request.scheme}://{self.request.get_host()}'

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': course.get_stripe_price(),
                        'product_data': {
                            'name': course.title,
                            # 'images': [course.thumbnail_image.path],
                            # 'images': ['https://images.unsplash.com/photo-1677131001999-aa1291476c37?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=871&q=80']
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "course_id": course.id,
                "current_user_email": self.request.user.email,
            },
            mode='payment',
            success_url=domain_url + '/course/purchase/success/',
            cancel_url=domain_url + '/course/purchase/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    print(payload)
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    print()
    print(sig_header)
    print()
    event = None

    try:
        print('loggin in...')
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
        print('successful login...')
    except ValueError as e:
        # Invalid payload
        print('valueerror occured...')
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print('signature verification occured...')
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print()
        print('successful pay')
        print()
        session = event['data']['object']

        customer_email = session["customer_details"]["email"]
        course_id = session["metadata"]["course_id"]
        # email = session["metadata"]["current_user_email"]

        course = Course.objects.get(id=course_id)
        # user = Profile.objects.get(user__email=email)

        # course.students.add(user.user)
        # user.courses_bought.add(course)

        send_mail(
            subject="Here is your course",
            message=f'Thanks for purchasing the course "{course.title}".\n Enjoy!',
            recipient_list=[customer_email],
            from_email=settings.EMAIL_HOST_USER
        )

    return HttpResponse(status=200)
