from __future__ import unicode_literals

from django.db import models

class Character(models.Model):
    name = models.CharField(max_length=50)
    picture_url = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

    def history(self):
        #Win, Loss, Draw
        results = [0, 0, 0]
        fights = self.fight_set.all()
        for fight in fights:
            if fight.result == 'W':
                results[0] = results[0] +1
            elif fight.result == 'L':
                results[1] = results[1] +1
            else:
                results[2] = results[2] +1
        
        return results

class Fight(models.Model):
    WIN  = 'W'
    LOSS = 'L'
    DRAW = 'D'
    FIGHT_RESULT = (
        (WIN, 'Victoire'),
        (LOSS, 'Défaite'),
        (DRAW, 'Egalité')
    )
    
    result = models.CharField(max_length=1, choices=FIGHT_RESULT, default=WIN)
    fight_date = models.DateTimeField('fight date')
    opponent =  models.ForeignKey(Character, on_delete=models.CASCADE)
    
    def __str__(self):
        display = str(self.fight_date)
        display = display + ": "
        display = display + self.outcome() + " versus " + str(self.opponent)
        return display

    @property
    def outcome(self):
        index = 0
        if self.result == 'W':
            index = 0
        elif self.result == 'L':
            index = 1
        else:
            index = 2
        return self.FIGHT_RESULT[index][1]

