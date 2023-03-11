from django.db import models
from auth_app.models import User

# Create your models here.
class UploadedImage(models.Model):
    user_email = models.ForeignKey(User, on_delete=models.CASCADE, to_field='email')
    image_key = models.CharField(max_length=255)
    image_url = models.CharField(max_length=255)
    image_title = models.CharField(max_length=255)
    image_description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return {"image_key": self.image_key, "user_email": self.user_email}
    
