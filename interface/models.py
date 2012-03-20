from django.db import models
# from autoslug import AutoSlugField

from django.contrib.auth.models import User

class Emailer(models.Model):
	name = models.CharField(max_length=200)
	netId = models.CharField(max_length=200)
	image = models.CharField(max_length=200)
	user = models.ForeignKey(User, null=True)
        # slug = AutoSlugField(populate_from='name')
	def __str__(self):
		return self.name

class EmailAddress(models.Model):
	emailer = models.ForeignKey(Emailer)
	emailAddress = models.CharField(max_length=200)
	def __str__(self):
		return "%s: %s" % (self.emailer.name, self.emailAddress)

class User(models.Model):
	name = models.CharField(max_length=200)
	email = models.CharField(max_length=200)
	image = models.CharField(max_length=200)
	def __str__(self): return self.name

class Team(models.Model):
	name = models.CharField(max_length=200)
	user = models.ForeignKey(User)
        # slug = AutoSlugField(populate_from='name')
        def __str__(self):
		return "%s: %s" % (self.user, self.name)

class Player(models.Model):
	team = models.ForeignKey(Team)
	emailer = models.ForeignKey(Emailer)
	points = models.IntegerField()
	def __str__(self): return "%s" % self.team
        def name(self):
            return self.emailer.name

class PlayerTransaction(models.Model):
	timestamp = models.DateTimeField()
	team = models.ForeignKey(Team)
	emailer = models.ForeignKey(Emailer)
	points = models.IntegerField()
	def __str__(self): return "%s set %s to %d at %s" % (self.team.name, self.emailer.name, self.points, self.timestamp)
        def name(self):
            return self.emailer.name

class Category(models.Model):
	name = models.CharField(max_length=200)
	total = models.BooleanField()
	description = models.TextField()
	def __str__(self): return self.name

class EmailerPoints(models.Model):
	emailer = models.ForeignKey(Emailer)
	category = models.ForeignKey(Category)
	points = models.IntegerField()
	total = models.BooleanField()
	def __str__(self): return "[%s] %s: %s" % (self.category, self.emailer.name, self.points, self.emailer.id)

class TeamPoints(models.Model):
	team = models.ForeignKey(Team)
	category = models.ForeignKey(Category)
	points = models.IntegerField()
	total = models.BooleanField()
	def __str__(self): return "[%s] %s: %s" % (self.category, self.team, self.points)

class TeamScore(models.Model):
	team = models.ForeignKey(Team)
	category = models.ForeignKey(Category)
	score = models.IntegerField()
	total = models.BooleanField()
	def __str__(self): return "[%s] %s: %s" % (self.category, self.team, self.score)

