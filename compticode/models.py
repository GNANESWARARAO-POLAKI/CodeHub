from django.db import models
from core.models import * 
from django.contrib.auth import get_user
from django.utils.timezone import now,localtime 

# Create your models here.

# class Questions(models.Model):
#     contest=models.ForeignKey(Contests,on_delete=models.CASCADE,related_name='compticode_questions')
#     title=models.CharField(max_length=100)
#     description=models.TextField(blank=False)
#     timelimit=models.PositiveIntegerField()
#     score=models.PositiveIntegerField()
#     # lives=models.PositiveIntegerField(default=5)
    
#     def save(self,*args,**kwargs):
#         self.title=self.title.capitalize()
#         super().save(*args,**kwargs)

#     def serialize(self):
#         return {
#             'id':self.id,
#             'title':self.title,
#             'description':self.description,
#             'score':self.score,
#         }
        
#     # def is_solved(user):
#     #     # if user.is_anonymous:
#     #     #     return False
#     #     return Submission.objects.filter(output=1, participant__user=user).exists()
  
#     def __str__(self):
#         return f"Question :{self.title} in {self.contest.title}"


# class Testcases(models.Model):
#     question=models.ForeignKey(Question,on_delete=models.CASCADE,related_name='compticode_testcases')
#     input_data=models.TextField()
#     expected_output=models.TextField()
#     hidden=models.BooleanField(default=True)
#     def __str__(self):
#         return f"TestCase for {self.question.title} (Hidden: {self.hidden})"
#     def serialize(self):
#         return {
#             'input_data':self.input_data,
#             'expected_output':self.expected_output,
#             'hidden':self.hidden,
#         }


class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='compticode_participations')
    contest = models.ForeignKey(Contests, on_delete=models.CASCADE, related_name='compticode_participants')
    score = models.FloatField(default=0)
    lives = models.PositiveIntegerField(default=5) 
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    session_id = models.CharField(max_length=255, blank=True, null=True)
    last_activity = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('user', 'contest') 

    def save(self, *args, **kwargs):
        if self.pk is not None:
            previous = Participant.objects.get(pk=self.pk)
            if self.score != previous.score:
                self.last_activity = localtime(now())
            else:
                self.last_activity = previous.last_activity
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)
            questions = self.contest.questions.all()
            for question in questions:
                Tempcode.objects.create(question=question, participant=self)
    # def deduce_life(self):
    #     if self.lives > 0:
    #         # Deduct a life
    #         self.lives -= 1
    #         Participant.objects.filter(pk=self.pk).update(lives=self.lives)
    # def add_life(self):
    #     if self.lives<=7:
    #         self.lives+=1
    #         Participant.objects.filter(pk=self.pk).update(lives=self.lives)
    def __str__(self):
        return f"{self.user.username} participating in {self.contest.title} -- ComptiCode theme"


# output = ["Accepted (AC)", "Wrong Answer (WA)", "Runtime Error (RE)",
# "Time Limit Exceeded (TLE)","Memory Limit Exceeded (MLE)","Compilation Error (CE)","Presentation Error (PE)",
# "Partial Correct (PC)","Output Limit Exceeded (OLE)","Internal Error (IE)"]
 
class Submission(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='compticode_submissions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='compticode_submissions')
    language=models.PositiveIntegerField()
    code=models.TextField()
    output=models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(null=True, blank=True) 
    time=models.FloatField(null=True)
    memory=models.PositiveIntegerField(null=True)
    json_data=models.JSONField(default=dict)
    def __str__(self):
        return f"Submission by {self.participant.user.username} for {self.question.title}"
    
default_codes = {
    "c": """#include<stdio.h>
int main() {
    printf("Hello, World!\\n");
    return 0;
}""",
    "cpp": """#include<iostream>
using namespace std;
int main() {
    cout << "Hello, World!" << endl;
    return 0;
}""",
    "python": """#write your code here""",
    "java": """public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}"""
}

class Tempcode(models.Model):
    participant=models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='compticode_temporary_codes')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='compticode_temporary_codes')
    c=models.TextField(default=default_codes['c'])
    python=models.TextField(default=default_codes['python'])
    cpp=models.TextField(default=default_codes['cpp'])
    java=models.TextField(default=default_codes['java'])
    def __str__(self):
        return f"current Tempcodes for the {self.participant} in the question {self.question}"
    def serialize(self):
        return {
            'python':self.python,
            'java':self.java,
            'c':self.c,
            'cpp':self.cpp
        }
     