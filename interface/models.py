from django.db import models
# from autoslug import AutoSlugField

from django.contrib.auth.models import User

class Emailer(models.Model):
	name = models.CharField(max_length=200)
	netId = models.CharField(max_length=200)
	image = models.CharField(max_length=200)
        # slug = AutoSlugField(populate_from='name')
	def __str__(self):
		return self.name

class EmailAddress(models.Model):
	emailer = models.ForeignKey(Emailer)
	emailAddress = models.CharField(max_length=200)
	def __str__(self):
		return "%s: %s" % (self.emailer, self.emailAddress)

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
	points = models.IntegerField() # allocation, 0 is remove, 1 is one of them, 2 is two, etc
	def __str__(self): return "%s set %s to %d at %s" % (self.team.name, self.emailer.name, self.points, self.timestamp)
        def name(self):
            return self.emailer.name

class Category(models.Model):
	name = models.CharField(max_length=200)
	total = models.BooleanField()
	description = models.TextField()
	def __str__(self): return self.name

class EmailerPointRanking(models.Model):
	emailer = models.ForeignKey(Emailer)
	category = models.ForeignKey(Category)
	type = models.CharField(max_length=200)
	points = models.IntegerField()
	def __str__(self): return "%s, %s, %s" % (self.emailer, self.category, self.type)

class TeamPointRanking(models.Model):
	team = models.ForeignKey(Team)
	category = models.ForeignKey(Category)
	type = models.CharField(max_length=200)
	points = models.IntegerField()
	def __str__(self): return "%s, %s, %s" % (self.team, self.category, self.type)

