from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Character, Fight

def index(request):
    latest_fight_list =  Fight.objects.order_by('-fight_date')[:10]
    characters = Character.objects.all()
    context = {
        'latest_fight_list': latest_fight_list,
        'characters': characters
    }
    
    return render(request, 'sfv/index.html', context)

def result(request):
    error_occured = False
    error_message = ""
    #checking POST parameters
    try:
        selected_character = Character.objects.get(pk=request.POST['character'])
    except (KeyError, Character.DoesNotExist):
        error_occured = True
        error_message = "Please select a valid character."
    else
        try:
            selected_outcome = request.Post['outcome']
        except (KeyError):
            error_occured = True
            error_message = "Please select a valid outcome."
        else:
            if selected_outcome != "W" and selected_outcome != "L" and selected_outcome != "D":
                error_occured = True
                error_message = "Please select a valid outcome."
        
    #display home
    latest_fight_list =  Fight.objects.order_by('-fight_date')[:10]
    context = {
        'latest_fight_list': latest_fight_list
    }
    
    #an error occured add an error message
    if error_occured:
        context["error_message"] = error_message
        return render(request, 'sfv/index.html', context)
    
    #no error create fight and save it
    fight = Fight(result = selected_outcome, fight_date=timezone.now(), opponent=selected_character)
    fight.save()
    
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('sfv:index'))
    

def detail(request, character_id):
    character = get_object_or_404(Character, pk=character_id)
    return render(request, 'sfv/detail.html', {'character': character})

def fight_result(request, character_id):
    character = get_object_or_404(Character, pk=character_id)
    
    error_occured = False
    error_message = ""
    try:
        selected_outcome = request.Post['outcome']
    except (KeyError):
        error_occured = True
        error_message = "Please select a valid outcome."
    else:
        if selected_outcome != "W" and selected_outcome != "L" and selected_outcome != "D":
            error_occured = True
            error_message = "Please select a valid outcome."
    if error_occured:
        return render(request, 'sfv/detail.html', {'character': character})
    
    fight = Fight(result = selected_outcome, fight_date=timezone.now(), opponent=character)
    fight.save()
    
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('sfv:detail', args=(character.id)))
    
    
