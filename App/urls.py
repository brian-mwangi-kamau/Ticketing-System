from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('user-signup/', views.user_signupview, name='user-signup'),
    path('staff-signup/', views.staff_signupview, name='staff-signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create-ticket/', views.create_ticket, name='create-ticket'),
    path('profile/', views.profile, name='profile'),
    path('ticket/<int:id>/', views.get_ticket_details, name='ticket-details'),
]