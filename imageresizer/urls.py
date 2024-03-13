from django.urls import path
from imageresizer import views

urlpatterns = [
    path('resizeimage/', views.ResizeImageView.as_view(), name='resizeimage'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.admin_dashboard, name='dashboard'),
]
