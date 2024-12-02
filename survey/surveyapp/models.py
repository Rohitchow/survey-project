from django.db import models
from django.contrib.auth.models import User

# Survey model
class Survey(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('closed', 'Closed'),
        ('republished', 'Republished'),  
    ]
    name = models.CharField(max_length=255)  
    description = models.TextField(blank=True)  
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='surveys')  
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='draft')  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"{self.name} ({self.status})"


    def is_ready_for_publish(self):
        return self.questions.count() >= 5


# Question model
class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')  
    text = models.TextField()  

    def __str__(self):
        return f"Question: {self.text}"


# Option model
class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')  
    text = models.CharField(max_length=255)  

    def __str__(self):
        return f"Option: {self.text} (Question: {self.question.text})"


# SurveyResponse model: Tracks which user responded to which survey
class SurveyResponse(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='responses')
    taker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='survey_responses')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response by {self.taker.username} for survey {self.survey.name}"


# QuestionResponse model: Tracks responses for individual questions
class QuestionResponse(models.Model):
    survey_response = models.ForeignKey(SurveyResponse, on_delete=models.CASCADE, related_name='question_responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='responses')
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name='selected_responses')

    def __str__(self):
        return f"Question: {self.question.text}, Selected: {self.selected_option.text}"
