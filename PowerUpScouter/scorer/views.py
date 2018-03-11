import urllib.request
import json

from django.shortcuts import render
from django.http import HttpResponse
from django_tables2 import RequestConfig
from django.forms import modelformset_factory

from .tables import TeamTable, TeamMatchTable, MatchTable, EfficiencyTable
from .models import Team, Match, TeamEfficiency


# Create your views here.
def home(request):
	table = TeamTable(Team.objects.all())
	RequestConfig(request).configure(table)
	return render(request, 'teams.html', {'table': table})

def teams(request):
	table = TeamTable(Team.objects.all())
	RequestConfig(request).configure(table)
	return render(request, 'teams.html', {'table': table})


def efficiency_update(request):
	teams = Team.objects.all()

	for team in teams:
		try:
			team_eff = team.efficiency.get()
		except TeamEfficiency.DoesNotExist:
			team_eff = team.efficiency.create()

		matches = team.matches.all()

		# Calculate the computed efficiency total for the matches
		num_matches = matches.count()
		if num_matches == 0:
			return HttpResponse("No matches found for team: {}".format(team.number))

		auto_cross_count = 0.0
		auto_cubes_count = 0.0
		tele_cubes_count = 0.0
		cubes_scored = 0.0
		scale_per = 0.0
		switch_per = 0.0
		exchg_per = 0.0
		climb_attempt = 0.0
		climb_succeed = 0.0

		for match in matches:
			if match.auto_cross is True:
				auto_cross_count += 1.0

			auto_cubes_count += match.auto_scale + match.auto_switch

			cubes_scored += match.auto_scale + match.auto_switch + match.tele_exchange + match.tele_scale + match.tele_switch

			scale_per += match.tele_scale + match.auto_scale

			switch_per += match.tele_switch + match.auto_switch

			exchg_per += match.tele_exchange

			if match.climb_attempt is True:
				climb_attempt += 1.0

			if match.climb_success is True:
				climb_succeed += 1.0
				match.climb_attempt = True
				climb_attempt += 1.0
				match.save()

		if num_matches == 0:		
			team_eff.match_count = 0.0
			team_eff.auto_cross_percentage = 0.0
			team_eff.auto_cubes_per_match = 0.0
			team_eff.cubes_scored = 0.0
			team_eff.scale_per_match = 0.0
			team_eff.switch_per_match = 0.0
			team_eff.exchg_per_match = 0.0
		else:
			team_eff.match_count = num_matches
			team_eff.auto_cross_percentage = auto_cross_count / num_matches
			team_eff.auto_cubes_per_match = auto_cubes_count / num_matches
			team_eff.cubes_scored = cubes_scored / num_matches
			team_eff.scale_per_match = scale_per / num_matches
			team_eff.switch_per_match = switch_per / num_matches
			team_eff.exchg_per_match = exchg_per / num_matches

		team_eff.climb_percentage = 0.0
		if climb_attempt != 0.0:
			team_eff.climb_percentage = climb_succeed / climb_attempt

		team_eff.save()

	efficiency = EfficiencyTable(TeamEfficiency.objects.all())
	RequestConfig(request).configure(efficiency)

	return render(request, 'efficiency.html', {'efficiency': efficiency})


def efficiency(request):
	table = EfficiencyTable(TeamEfficiency.objects.all())
	RequestConfig(request).configure(table)

	return render(request, 'efficiency.html', {'table': table})

def team_summary(request, number):
	try:
		team = Team.objects.get(number=number)
	except Team.DoesNotExist:
		return HttpResponse("Team {} not found.".format(number))

	team_eff = EfficiencyTable(team.efficiency.all())
	RequestConfig(request).configure(team_eff)
	matches = TeamMatchTable(team.matches.all())
	RequestConfig(request).configure(matches)

	return render(request, 'team_summary.html', {'matches': matches, 'team': team, 'team_eff':team_eff})


def update_frc(request):
	url = 'https://www.thebluealliance.com/api/v3/event/2018vahay/teams'
	accept_header = 'application/json'	
	auth_key = 'PzuHZr48g9iYtraIKmoY8y0OqGNWu08KYI2TR32Vno4DnBbHTgnH16QdFOo50tgu'
	# headers= {'X-TBA-Auth-Key': auth_key }
	# #headers= {'accept' : accept_header, 'X-TBA-Auth-Key': auth_key }

	# req = urllib.request.Request(url, headers)

	# open_request = urllib.request.urlopen(req)
	# team_json = open_request.read()

	req = urllib.request.Request(url)
	req.add_header('accept', accept_header)
	req.add_header('X-TBA-Auth-Key', auth_key)
	req.add_header('User-Agent', '1895_Scouter')
	with urllib.request.urlopen(req) as response:
		the_page = response.read()

		teams = json.loads(the_page)

	for team in teams:
		Team.objects.create(name=team['nickname'], number=team['team_number'], frcKey=team['key'])

	Team.save()

	return HttpResponse(teams)

def match_edit(request, number):
	MatchFormSet = modelformset_factory(Match, exclude=('id',))

	if request.method == 'POST':
		match_form_set = MatchFormSet(request.POST, request.FILES)
		if match_form_set.is_valid():
			match_form_set.save()
	else:
		matches = Match.objects.filter(match_number=number)

		if matches.count() == 0:
			match_form_set = MatchFormSet(queryset=Match.objects.none())
		else:
			match_form_set = MatchFormSet(queryset=Match.objects.filter(match_number=number))

	return render(request, 'match_edit.html', {'formset': match_form_set})


def matches(request):
	table = MatchTable(Match.objects.all())
	RequestConfig(request).configure(table)
	return render(request, 'matches.html', {'table': table})


def match(request, number):
	table = MatchTable(Match.objects.filter(match_number=number))
	RequestConfig(request).configure(table)
	return render(request, 'match.html', {'table': table, 'number': number})
