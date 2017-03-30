from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Character, Fight

def index(request):
    latest_fight_list =  Fight.objects.order_by('-fight_date')[:10]
    context = {
        'latest_fight_list': latest_fight_list
    }

    return render(request, 'sfv/index.html', context)

def detail(request, character_id):
    character = get_object_or_404(Character, pk=character_id)
    return render(request, 'sfv/detail.html', {'character': character})

