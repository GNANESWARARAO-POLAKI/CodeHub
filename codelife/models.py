from django.db import models
from core.models import * 
from django.contrib.auth import get_user


# Create your models here.


class Questions(models.Model):
    contest=models.ForeignKey(Contests,on_delete=models.CASCADE,related_name='questions')
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
        return f"Question :{self.title} in {self.contest.title}"


class Testcases(models.Model):
    question=models.ForeignKey(Questions,on_delete=models.CASCADE,related_name='testcases')
    input_data=models.TextField()
    expected_output=models.TextField()
    hidden=models.BooleanField(default=True)
    def __str__(self):
        return f"TestCase for {self.question.title} (Hidden: {self.hidden})"

class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participations')
    contest = models.ForeignKey(Contests, on_delete=models.CASCADE, related_name='participants')
    score = models.FloatField(default=0)
    lives = models.PositiveIntegerField(default=5) 
    joined_at = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=255, blank=True, null=True)
    last_activity = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('user', 'contest') 

    def save(self, *args, **kwargs):
        if self.pk is not None:
            previous = Participant.objects.get(pk=self.pk)
            if self.score != previous.score:
                self.last_activity = now()
            else:
                self.last_activity = previous.last_activity
        super().save(*args, **kwargs)
    def deduce_life(self):
        if self.lives > 0:
            # Deduct a life
            self.lives -= 1
            Participant.objects.filter(pk=self.pk).update(lives=self.lives)
    def add_life(self):
        if self.lives<=7:
            self.lives+=1
            Participant.objects.filter(pk=self.pk).update(lives=self.lives)
    def __str__(self):
        return f"{self.user.username} participating in {self.contest.title}"


# output = ["Accepted (AC)", "Wrong Answer (WA)", "Runtime Error (RE)",
# "Time Limit Exceeded (TLE)","Memory Limit Exceeded (MLE)","Compilation Error (CE)","Presentation Error (PE)",
# "Partial Correct (PC)","Output Limit Exceeded (OLE)","Internal Error (IE)"]
 
class Submission(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='submissions')
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='submissions')
    language=models.PositiveIntegerField()
    code=models.TextField()
    output=models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(null=True, blank=True) 
    time=models.FloatField(null=True)
    memory=models.PositiveIntegerField(null=True)
    def __str__(self):
        return f"Submission by {self.participant.user.username} for {self.question.title}"


