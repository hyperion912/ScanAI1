from django.db import models
import os

class AlzheimerImages(models.Model):
    image = models.ImageField(upload_to="alzheimer")


    def save(self, *args, **kwargs):
        # Check if the file already exists before saving
        if self.image and os.path.exists(self.image.path):
            return  # File already exists, no need to save again
        super().save(*args, **kwargs)


 
