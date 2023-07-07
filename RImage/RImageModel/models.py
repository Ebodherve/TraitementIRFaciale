from django.db import models


class ImagesModel(models.Model):
    
    image = models.ImageField(upload_to="models/")


class ImageToClassifi(models.Model):
    
    image = models.ImageField(upload_to="classifier/")
    

