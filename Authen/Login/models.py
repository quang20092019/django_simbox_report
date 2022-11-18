from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Post(models.Model):
    title =models.CharField(max_length =100)
    content =models.CharField(max_length =300)
    def __str__(self):
        return self.title
class User(AbstractUser):
    gender_choice = ((0,"Nữ"),(1,"Nam"))
    age= models.IntegerField(default=0)
    gender = models.IntegerField(choices=gender_choice,default=0)
    address=models.CharField(max_length =100)
class BookInstance(models.Model):
    class Meta:
        permissions = (("del_spam", "Set book as returned"),)
class viewsmartsip(models.Model):
    class Meta:
        permissions = (("smartsip", "View smartsip"),)
class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')