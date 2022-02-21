from django.db import models

# Create your models here.
class person(models.Model):
 
    # fields of the model

    name=models.CharField(max_length=10)

    age= models.IntegerField()
    
    job_type = models.CharField(max_length = 10)

    address = models.CharField(max_length = 100)
    # renames the instances of the model
    # with their title name
    def __str__(self):
        return self.name

    