from django.urls import path
from . import views

urlpatterns = [
    # things ajax request
    path('bookmark-it/', views.bookmark_it, name='bookmark_it'),

    path('courses/', views.CourseListView.as_view(), name='courses'),
    path('courses/free/', views.free_course, name='free_courses'),
    path('course/<slug:slug>', views.CourseDetailView.as_view(), name='course_detail'),
    path('courses/category/<slug:category>/',
         views.get_category_courses, name='course_filter'),
    path('course/<slug:obj>/<slug:module_slug>/<slug:content_id>/',
         views.view_content, name='play_content'),
    path('courses/review/', views.save_review, name='save_review'),
    path('course/buy-now/<slug:course>/',
         views.confirm_buy, name='confirm_buy'),

    # things stripe
    path('create-checkout-session/',
         views.CreateCheckoutSessionView.as_view(), name='create_payment'),
    path('course/purchase/success/', views.success, name='success'),
    path('course/purchase/cancel/', views.cancel, name='cancel'),
    path('webhooks/stripe/', views.stripe_webhook, name='stripe-webhook'),
]
