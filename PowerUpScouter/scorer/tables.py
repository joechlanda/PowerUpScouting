# tutorial/tables.py
import django_tables2 as tables
import django_filters

from .models import Team, Match, TeamEfficiency

from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_tables2.utils import A  # alias for Accessor


class TeamTable(tables.Table):
    number = tables.LinkColumn('team_summary', args=[A('number')])
    
    class Meta:
        model = Team
        template_name = 'django_tables2/bootstrap.html'
        fields = ['number', 'name']


class TeamMatchTable(tables.Table):
	class Meta:
		model = Match
		# template_name = 'django_tables2/bootstrap.html'
		# fields = ['match_number', 'auto_cross', 'auto_scale', 'auto_switch', 'portal_pickup', 'ground_pickup', 'tele_switch', 'tele_scale', 'tele_exchange', 'climb_attempt', 'climb_success', 'parked', 'comments', 'alliance', 'start_pos']
		exclude = ['id', 'team', 'alliance']


class EfficiencyTable(tables.Table):
	team = tables.LinkColumn('team_summary', args=[A('team')])

	class Meta:
		model = TeamEfficiency
		template_name = 'django_tables2/bootstrap.html'
		exclude = ['id']

class MatchTable(tables.Table):
	match_number = tables.LinkColumn('match',args=[A('match_number')])
	team = tables.LinkColumn('team_summary', args=[A('team')])

	class Meta:
		model = Match
		# template_name = 'django_tables2/bootstrap.html'
		exclude = ['id', 'alliance']