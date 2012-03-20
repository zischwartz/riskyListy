from django.db import models
# from autoslug import AutoSlugField

from django.db.models.signals import post_save
from django.contrib.auth.models import User

from django.dispatch import dispatcher



class Emailer(models.Model):
	name = models.CharField(max_length=200)
	netId = models.CharField(max_length=200)
	image = models.CharField(max_length=200)
	user = models.ForeignKey(User, null=True)
        # slug = AutoSlugField(populate_from='name')
	def __str__(self):
		return self.name
        class Meta:
            ordering= ["name"]

class EmailAddress(models.Model):
	emailer = models.ForeignKey(Emailer)
	emailAddress = models.CharField(max_length=200)
	realEmail = models.CharField(max_length=200, blank=True)
	def __str__(self):
		return "%s: %s" % (self.emailer.name, self.emailAddress)
 
# class User(models.Model):
# 	name = models.CharField(max_length=200)
# 	email = models.CharField(max_length=200)
# 	image = models.CharField(max_length=200)
# 	def __str__(self): return self.name

class Team(models.Model):
	name = models.CharField(max_length=200)
	user = models.ForeignKey(User)
        # slug = AutoSlugField(populate_from='name')
        def __str__(self):
		return "%s: %s" % (self.user, self.name)
        def getTotalScore(self):
            for score in  self.teamscore_set.all():
                if score.total == True:
                    return score.score

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



def createNewTeam(sender, created, instance=None, **kwargs):
    if instance is None:
        return
    if created == True:
        name = instance.username + "'s Team"
        new_team, was_created= Team.objects.get_or_create(name =name, user=instance)
        if was_created: # silly, but there seems to be a bug in the created var coming from the signal
            print instance.email
            # doh regex needs to applied on EmailAdress model, not our user instance
            matching_email_address= EmailAddress.objects.filter(realEmail= instance.email)
            if len(matching_email_address):
                print 'email matched'
                emailer= matching_email_address[0].emailer
                emailer.user = instance
                emailer.save()



post_save.connect(createNewTeam, sender=User)

