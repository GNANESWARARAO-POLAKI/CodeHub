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
    year=models.PositiveIntegerField(default=3,null=False,blank=False)

    def save(self,*args,**kwargs):
        first_name=self.first_name.capitalize()
        last_name=self.last_name.capitalize()
        jntuno=self.jntuno.upper()
        super().save(*args,**kwargs)
    def make_staff(self,*args,**kwargs):
        self.is_staff=True
        self.save(*args,**kwargs)


class ContestManager(models.Manager):
    def upcoming(self):
        """Returns contests that have not started yet."""
        current_time = localtime(now())
        
        return self.filter(start_date__gt=current_time)

    def ongoing(self):
        """Returns contests that are currently active."""
        current_time = localtime(now())
        return self.filter(start_date__lte=current_time, end_date__gte=current_time)

    def past(self):
        """Returns contests that have already ended."""
        current_time = localtime(now())
        return self.filter(end_date__lt=current_time)

class Contests(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    contest_type = models.CharField(max_length=20)
    venue = models.CharField(max_length=30)
    poster = models.ImageField(null=True, upload_to='contest_posters/')
    winners = models.ManyToManyField(User, related_name='contest_winners', blank=True)
    runner = models.CharField(max_length=40, null=True, blank=True)
    
    objects = ContestManager()  # Custom manager
    questions=models.ManyToManyField('Question',related_name='contest_questions',blank=True)
    def clean(self):
        """Validation checks for contest fields."""
        if self.start_date >= self.end_date:
            raise ValidationError("Start date must be earlier than end date.")
        if self.contest_type not in ['codelife', 'compticode', 'debugcode']:
            raise ValidationError("Contest type must be compticode or codelife.")

    def save(self, *args, **kwargs):
        """Ensure validation before saving."""
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def status(self):
        """Returns the contest status dynamically."""
        current_time = localtime(now())
        if current_time < self.start_date:
            return "Upcoming"
        elif self.start_date <= current_time <= self.end_date:
            return "Ongoing"
        else:
            return "Past"

    def __str__(self):
        return self.title



class Question(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField(blank=False)
    timelimit=models.PositiveIntegerField()
    score=models.PositiveIntegerField()
    lives=models.PositiveIntegerField(default=5)
    
    def save(self,*args,**kwargs):
        self.title=self.title.capitalize()
        super().save(*args,**kwargs)

    def serialize(self):
        return {
            'id':self.id,
            'title':self.title,
            'description':self.description,
            'score':self.score,
            'lives':self.lives,
        }
    # def is_solved(user):
    #     # if user.is_anonymous:
    #     #     return False
    #     return Submission.objects.filter(output=1, participant__user=user).exists()
  
    def __str__(self):
        return f"Question :{self.title} "

class Testcase(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE,related_name='compticode_testcases')
    input_data=models.TextField()
    expected_output=models.TextField()
    hidden=models.BooleanField(default=True)
    def __str__(self):
        return f"TestCase for {self.question.title} (Hidden: {self.hidden})"
    def serialize(self):
        return {
            'input_data':self.input_data,
            'expected_output':self.expected_output,
            'hidden':self.hidden,
        }
