from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    phone=models.CharField(max_length=10,null=True)
    email=models.EmailField(blank=False)
    jntuno=models.CharField(max_length=10,null=False,blank=False)
    date_joined=models.DateField(auto_now=True)
    image=models.ImageField(null=True,blank=True)
    branch=models.CharField(max_length=10)
    college=models.CharField(max_length=100,default='GMRIT')
    def save(self,*args,**kwargs):
        first_name=first_name.capitalize()
        last_name=last_name.capitalize()
        jntu=jntu.upper()
        super().save(*args,**kwargs)


class Contests(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_contests')
    is_active = models.BooleanField(default=True) 
    contest_type=models.PositiveIntegerField()
    venue=models.CharField(max_length=30)
    poster=models.ImageField(null=True)
    winner=models.CharField(max_length=40,null=True)
    runner=models.CharField(max_length=40,null=True)
    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("Start date must be earlier than end date.")
        if self.contest_type not in [1, 2]:
            raise ValidationError("Contest type must be 1 or 2.")

    def save(self, *args, **kwargs):
        self.full_clean() 
        super().save(*args, **kwargs)
    def __str__(self):
        return self.title



