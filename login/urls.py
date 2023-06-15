from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
from . import forms_forget_passwords


app_name = 'login'

urlpatterns = [
    path('login/', views.classic_login, name='classic-login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('password-change', views.password_change, name='password-change'),
    path('edit-profile', views.edit_profile, name='edit-profile'),
    path('edit-profile-image', views.edit_profile_image, name='edit-profile-image'),
]

urlpatterns += [
    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name='login/templates/forget_password/password_reset.html',
                                              form_class=forms_forget_passwords.PasswordResetF,
                                              from_email='green_apple@gmail.com',
                                              # email_template_name='login/templates/forget_password/password_reset_email.html', OR below:
                                              email_template_name='login/templates/forget_password/subject_email_template.txt',
                                              success_url=reverse_lazy('login:password_reset_done')),
         name='password_reset'),

    path('password_reset_done/',
         auth_views.PasswordResetDoneView.as_view(template_name='login/templates/forget_password/password_reset_done.html'),
         name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='login/templates/forget_password/password_reset_confirm.html',
                                                     form_class=forms_forget_passwords.SetPasswordF,
                                                     success_url=reverse_lazy('login:password_reset_complete'),
                                                     ),
         name='password_reset_confirm'),

    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='login/templates/forget_password/password_reset_complete.html'),
         name='password_reset_complete')
]
