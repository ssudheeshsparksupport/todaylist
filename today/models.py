from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
	user = models.ForeignKey(User)
	project_name = models.CharField(max_length=250)

	def __unicode__(self):
		return self.project_name

class Task(models.Model):
	project = models.ForeignKey(Project)
	title = models.CharField(max_length=250)

	def __unicode__(self):
		return self.title