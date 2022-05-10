from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name="index"),
    path('movie', views.movie, name='movie'),
    path('contact', views.contact, name='contact'),
    path('movie_detail', views.movie_details, name='movie_detail'),
    path('signup', views.signup, name='signup'),
    path('login', views.signin, name='signin'),
    path('logout', views.signout, name='signout'),

    # reset password path
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="form/forgot.html"),
         name='reset_password'),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="form/password_reset_done.html"),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="form/password_reset_confirm.html"),
         name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

]
