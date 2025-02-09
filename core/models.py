from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser
from django.utils.timezone import now,localtime
from django.core.exceptions import ValidationError

class User(AbstractUser):
    phone=models.CharField(max_length=10,null= True)
    email=models.EmailField(unique=True,blank=False)
    jntuno=models.CharField(max_length=10,null=False,blank=False)
    date_joined=models.DateField(auto_now=True)
    image=models.ImageField(upload_to='profile_pictures/',null=True,blank=True,default='profile_pictures/default.jpg')
    branch=models.CharField(max_length=10)
    college=models.CharField(max_length=100,default='GMRIT')

    def save(self,*args,**kwargs):
        first_name=self.first_name.capitalize()
        last_name=self.last_name.capitalize()
        jntuno=self.jntuno.upper()
        super().save(*args,**kwargs)
    def make_staff(self,*args,**kwargs):
        self.is_staff=True
        self.save(*args,**kwargs)


class Contests(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    contest_type=models.PositiveIntegerField()
    venue=models.CharField(max_length=30)
    poster=models.ImageField(null=True,upload_to='contest_posters/')
    winners = models.ManyToManyField(User, related_name='contest_winners', blank=True)
    runner=models.CharField(max_length=40,null=True,blank=True)
    # duration=models.PositiveIntegerField(default=60)
    # is_draft=models.BooleanField(default=False)
    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("Start date must be earlier than end date.")
        if self.contest_type not in [1, 2]:
            raise ValidationError("Contest type must be 1 or 2.")
    
    def save(self, *args, **kwargs):
        self.full_clean() 
        super().save(*args, **kwargs)

    @property
    def status(self):
        current_time = localtime(now())
        if current_time < self.start_date:
            return "Upcoming"
        elif self.start_date <= current_time <= self.end_date:
            return "Ongoing"
        else:
            return "Past"
            

    def __str__(self):
        return self.title



