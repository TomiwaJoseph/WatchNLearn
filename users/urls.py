from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('sign-in-or-register/', views.sign_in_or_register, name='signup_login'),
    path('profile/<slug:user_first_name>/<int:user_id>/', views.profile, name='profile'),
    path('instructor-profile/<slug:user_first_name>/<int:user_id>/', views.instructor_profile, name='instructor_profile'),
    path('edit-profile/', views.profile_edit, name='edit_profile'),
    path('my-learning/', views.my_learning, name='my_learning'),
    path('become-an-instructor/', views.instructor, name='instructor'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name="registration/password_reset.html"), 
        name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name="registration/password_reset_done.html"), 
        name='password_reset_done'),
    path('password-reset-confim/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="registration/password_reset_confirm.html"), 
        name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="registration/password_reset_complete.html"), 
        name='password_reset_complete'),
    path('awaiting-activation/', views.awaiting_activation, name='awaiting_activation'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    # higher user views
    path('instructor/create-a-class/', views.instrutor_create_class, name='create_class'),
    path('create-a-class/awaiting-approval/', views.class_created_pending, name='await_approval'),
    path('courses/instructor/module/', views.create_module, name='create_module'),
    path('courses/instructor/content/', views.create_content, name='create_content'),
    path('courses/admin/drafts/', views.admin_draft_view, name='drafts'),
    path('courses/instructor/drafts/', views.instructor_drafts, name='instructor_drafts'),
]
