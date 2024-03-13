from django.db import models


class ImageModel(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploader = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='images_uploaded')

    def __str__(self):
        return self.title


class UserVisit(models.Model):
    ip_address = models.CharField(max_length=45)
    timestamp = models.DateTimeField(auto_now_add=True)
    image_uploaded = models.ForeignKey(ImageModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='visits')

    def __str__(self):
        return f"Visit from {self.ip_address} at {self.timestamp}"
