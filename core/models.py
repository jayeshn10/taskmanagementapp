from django.db import models

# Create your models here.

class Task(models.Model):
    STATUS_CHOICES = ( 
        ("pending", "Prnding"), 
        ("completed", "Completed")
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    status  = models.CharField(  max_length = 20, choices = STATUS_CHOICES, default = 'pending')
