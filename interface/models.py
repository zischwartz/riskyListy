from django.db import models
# from autoslug import AutoSlugField

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

