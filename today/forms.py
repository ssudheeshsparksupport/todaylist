from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from today.models import Project
from django import forms

class UserEditForm(ModelForm):
    class Meta:
        model = Project
        fields =["title"]