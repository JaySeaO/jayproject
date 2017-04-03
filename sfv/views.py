from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.urls import reverse

from .models import Character, Fight

def index(request):
    valid_request = True
    error_occured = False

    character_id = 0
    selected_outcome = ""
    try:
        character_id = int(request.POST['character'])
        selected_outcome = request.POST['outcome']
    except (KeyError, ValueError):
        valid_request = False

    if valid_request:
        try:
            selected_character = Character.objects.get(pk=character_id)
        except (Character.DoesNotExist):
            error_occured = True
            error_message = "Please select a valid character."
        else:
            if selected_outcome != "W" and selected_outcome != "L" and selected_outcome != "D":
                error_occured = True
                error_message = "Please select a valid outcome."

    #list of all characters
    characters = Character.objects.all()
    context = {
        'characters': characters
    }

    #an error occured add an error message
    if error_occured:
        latest_fight_list =  Fight.objects.order_by('-fight_date')[:10]
        context["error_message"] = error_message
        context["latest_fight_list"] = latest_fight_list
        return render(request, 'sfv/index.html', context)

    #no error create fight and save it
    if valid_request:
        fight = Fight(result = selected_outcome, fight_date=timezone.now(), opponent=selected_character)
        fight.save()

    latest_fight_list =  Fight.objects.order_by('-fight_date')[:10]
    context["latest_fight_list"] = latest_fight_list

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    if valid_request:
        return HttpResponseRedirect(reverse('sfv:index'))
    else:
        return render(request, 'sfv/index.html', context)

def detail(request, character_id):
    character = get_object_or_404(Character, pk=character_id)

    error_occured = False
    error_message = ""

    valid_request = True

    try:
        selected_outcome = request.POST['outcome']
    except (KeyError):
       valid_request = False

    if valid_request:
        if selected_outcome != "W" and selected_outcome != "L" and selected_outcome != "D":
            error_occured = True
            error_message = "Please select a valid outcome."

    context = {
        "character": character
    }

    if error_occured:
        context.error_message = error_message
        return render(request, 'sfv/detail.html', context)

    if valid_request:
        fight = Fight(result = selected_outcome, fight_date=timezone.now(), opponent=character)
        fight.save()
        return HttpResponseRedirect(reverse('sfv:detail', args=(character.id)))
    else
        return render(request, 'sfv/detail.html', context)
