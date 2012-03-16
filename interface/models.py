from django.db import models

class Emailer(models.Model):
	name = models.CharField(max_length=200)
	netId = models.CharField(max_length=200)
	image = models.CharField(max_length=200)

class EmailAddress(models.Model):
	emailer = models.ForeignKey(Emailer)
	emailAddress = models.CharField(max_length=200)

class Team(models.Model):
	name = models.CharField(max_length=200)
	manager = models.ForeignKey(Emailer)

class Player(models.Model):
	team = models.ForeignKey(Team)
	player = models.ForeignKey(Emailer)

class Category(models.Model):
	name = models.CharField(max_length=200)

class EmailerPointRanking(models.Model):
	emailer = models.ForeignKey(Emailer)
	category = models.ForeignKey(Category)
	type = models.CharField(max_length=200)
	points = models.IntegerField()

class TeamPointRanking(models.Model):
	team = models.ForeignKey(Team)
	category = models.ForeignKey(Category)
	type = models.CharField(max_length=200)
	points = models.IntegerField()

