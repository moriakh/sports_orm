from django.shortcuts import render, redirect
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