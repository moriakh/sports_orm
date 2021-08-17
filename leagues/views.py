from django.shortcuts import render, redirect
from django.db.models import Count
from .models import League, Team, Player

from . import team_maker

def index(request):
	context = {
		"leagues": League.objects.all(),
		"teams": Team.objects.all(),
		"players": Player.objects.all(),
	}
	return render(request, "leagues/index.html", context)

def make_data(request):
	team_maker.gen_leagues(10)
	team_maker.gen_teams(50)
	team_maker.gen_players(200)

	return redirect("index")

def task(request):
	context = {
		'womens' : League.objects.filter(name__contains="women"),
		'baseballs' : League.objects.filter(sport__contains="baseball"),
		'hockeys' : League.objects.filter(sport__contains="hockey"),
		'no_footballs' : League.objects.exclude(sport__contains="football"),
		'conferences' : League.objects.filter(name__contains="conference"),
		'atlantics' : League.objects.filter(name__contains="atlantic"),
		'dallass' : Team.objects.filter(location="Dallas"),
		'raptors' : Team.objects.filter(team_name__contains="raptors"),
		'cities' : Team.objects.filter(location__contains="city"),
		'startswithts' : Team.objects.filter(team_name__startswith="t"),
		'locationss' : Team.objects.order_by("location"),
		'teams' : Team.objects.order_by("-team_name"),
		'coopers' : Player.objects.filter(last_name="Cooper"),
		'joshuas' : Player.objects.filter(first_name__contains="Joshua"),
		'no_joshuas' : Player.objects.filter(last_name="Cooper").exclude(first_name__contains="Joshua"),
		'names' : Player.objects.filter(first_name = "Alexander") | Player.objects.filter(first_name = "Wyatt")
	}
	return render(request, "task.html", context)

def task2(request):
	try:
		atlantic_teams = League.objects.get(name = "Atlantic Soccer Conference").teams.all()
	except League.DoesNotExist:
		atlantic_teams = []

	try:
		loswichitavikin = Team.objects.get(team_name = "Vikings", location = "Wichita")
		wichita_players = loswichitavikin.all_players.all()
		wichita_current_ids = [player.id for player in loswichitavikin.curr_players.all()]
		not_now_wichita = [player for player in wichita_players if player.id not in wichita_current_ids]

	except Team.DoesNotExist:
		not_now_wichita = []

	# Player.objects.filter(all_teams__team_name='Vikings', all_teams__location='Wichita').exclude(curr_team__team_name='Vikings', curr_team__location='Wichita')

	teams12 = Team.objects.filter(all_players__count__gte=12).filter(curr_players__count__gte=12)

	context = {
		'atlantic_teams' : atlantic_teams,
		'boston_penguins' : Player.objects.filter(curr_team__team_name='Boston Penguins'),
		'international_collegiate' : Player.objects.filter(curr_team__league__name="International Collegiate Baseball Conference"),
		'lopez' : Player.objects.filter(curr_team__league__name="American Association of Amateur Soccer").filter(last_name="Lopez"),
		'football_players' : Player.objects.filter(curr_team__league__sport="Football"),
		'team_sophia' : Team.objects.filter(all_players__first_name="Sophia"),
		'league_sophia' : League.objects.filter(teams__all_players__first_name="Sophia"),
		'flores' : Player.objects.filter(last_name="Flores").exclude(curr_team__team_name="Roughriders", curr_team__location="Washington"),
		'samuel_evans' : Team.objects.filter(all_players__first_name="Samuel", all_players__last_name="Evans"),
		'not_now_wichita' : not_now_wichita,
		'jacob_gray' : Team.objects.filter(all_players_first_name = "Jacob", all_players_last_name = "Gray").exclude(name="Colt", location="Oregon"),
		'joshuas' : Player.objects.filter(first_name = "Joshua", curr_team__leagues__name="Atlantic Baseball Players Federation	"),
		'team12' :  [],
		'all_players' : Player.objects.annotate(Count('all_teams')).order_by('all_teams__count')
	}
	return render(request, "task2.html", context)