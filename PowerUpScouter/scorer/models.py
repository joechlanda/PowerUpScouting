from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
	name = models.CharField(max_length=30, unique=False)
	number = models.IntegerField()
	frcKey = models.CharField(max_length=10, unique=True)

	def __str__(self):
		return str(self.number)

class Match(models.Model):
	# Define the helper values first
	RED = 'R'
	BLUE = 'B'
	AllianceColorChoices = ( (RED, 'Red'), (BLUE, 'Blue') )

	ONE = 1
	TWO = 2
	THREE = 3
	FOUR = 4
	FIVE = 5
	SIX = 6
	StartingPositionChoices = ((ONE, '1'), (TWO, '2'), (THREE, '3'), (FOUR, '4'),(FIVE, '5'),(SIX, '6'))

	match_number = models.PositiveSmallIntegerField()
	team = models.ForeignKey(Team, related_name='matches', on_delete=models.CASCADE)
	alliance = models.CharField(max_length=4, choices=AllianceColorChoices, default=RED)
	start_pos = models.PositiveSmallIntegerField(choices=StartingPositionChoices, default=ONE)
	# start_pos = models.CharField(choices=StartingPositionChoices, default=ONE, max_length=4)
	auto_cross = models.BooleanField(default=False)
	auto_scale = models.PositiveSmallIntegerField()
	auto_switch = models.PositiveSmallIntegerField()
	portal_pickup = models.PositiveSmallIntegerField()
	ground_pickup = models.PositiveSmallIntegerField()
	tele_switch = models.PositiveSmallIntegerField()
	tele_scale = models.PositiveSmallIntegerField()
	tele_exchange = models.PositiveSmallIntegerField()
	climb_attempt = models.BooleanField(default=False)
	climb_success = models.BooleanField(default=False)
	parked = models.BooleanField(default=False)
	comments = models.CharField(max_length=250, default="")

	def __str__(self):
		return "{} - {}".format(self.match_number, self.team)


class TeamEfficiency(models.Model):
	team = models.ForeignKey(Team, related_name='efficiency', on_delete=models.CASCADE)
	match_count = models.PositiveSmallIntegerField(default=0)
	auto_cross_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
	auto_cubes_per_match = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
	cubes_scored = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
	scale_per_match = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
	switch_per_match = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
	exchg_per_match = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
	climb_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)