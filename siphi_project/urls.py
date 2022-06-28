from django.urls import path, include
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name="index"),
    path('movie', views.movie, name='movie'),
    path('contact', views.contact, name='contact'),
    # path('Dashboard', views.Dashboard, name='Dashboard'),
    path('movie_detail/<id>/', views.movie_details, name='movie_detail'),
    path('signup', views.signup, name='signup'),
    path('login', views.signin, name='signin'),
    path('logout', views.signout, name='signout'),
    path('password_reset_confirm/<slug:uid>/', views.change_password, name='password_reset_confirm'),
    path('forget_password/', views.reset_password, name='forget_password'),
    path('password_reset_done/', views.password_reset_done, name='password_reset_done'),
    path('setcookie', views.setcookie),
    path('getcookie', views.showcookie),
    path('update_rate/<id>/', views.update_rate, name="rate_update"),
    # path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),

    # reset password path
    # path('reset_password/', auth_views.PasswordResetView.as_view(template_name="form/forgot.html"),
    #      name='reset_password'),
    # path('reset_password_sent/',
    #      auth_views.PasswordResetDoneView.as_view(template_name="form/password_reset_done.html"),
    #      name='password_reset_done'),
    # path('reset/<uidb64>/<token>/',
    #      auth_views.PasswordResetConfirmView.as_view(template_name="form/password_reset_confirm.html"),
    #      name='password_reset_confirm'),
    # path('reset_password_complete/',
    #      auth_views.PasswordResetCompleteView.as_view(template_name="form/password_reset_complete.html"),
    #      name='password_reset_complete'),

]
