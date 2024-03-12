from django.urls import path
from .views import ResizeImageView, UploadedImageView, UserVisitView

urlpatterns = [
    path('resizeimage/', ResizeImageView.as_view(), name='resizeimage'),
    path('uploadimage/', UploadedImageView.as_view(), name='uploadimage'),
    path('trackuser/', UserVisitView.as_view(), name='trackuser'),
]
