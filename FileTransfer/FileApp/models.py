from django.db import models
import os
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fileOwner")
    file = models.FileField(upload_to='uploads')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def filename(self):
        return os.path.basename(self.file.name)