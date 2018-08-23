from django.db import models


class register(models.Model):
    res_username = models.CharField(max_length=30, null=True)
    res_password = models.CharField(max_length=30, null=True)
    res_email = models.CharField(max_length=30, null=True)
    res_id = models.IntegerField(null=True)
    age = models.IntegerField(null=True)
    profession = models.CharField(max_length=30, null=True)
    education = models.IntegerField(null=True)
    training_start_period = models.DateTimeField(null=True)
    severe = models.CharField(max_length=30, null=True)
    comorbidity_disease = models.CharField(max_length=30, null=True)
    primary_disease = models.CharField(max_length=30, null=True)
    type_of_aphasia = models.CharField(max_length=30, null=True)
    personality = models.CharField(max_length=30, null=True)
    intelligence = models.IntegerField(default=110)
    language_background = models.CharField(max_length=30, null=True)
    self_correcting_ability = models.IntegerField(default=0)
    selected_speech = models.CharField(max_length=30, null=True)

class familiarity(models.Model):
    res_id = models.IntegerField(null=True)
    word = models.CharField(max_length=30,null=True)
    score = models.IntegerField(default=50)