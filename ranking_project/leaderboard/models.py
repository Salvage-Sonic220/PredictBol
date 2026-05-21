from django.db import models

class Match(models.Model):
    team_a = models.CharField(max_length=100)
    team_b = models.CharField(max_length=100)
    logo_a = models.CharField(max_length=100, default='default.png')
    logo_b = models.CharField(max_length=100, default='default.png')
    
    # Resultados reales (ya definidos)
    score_a = models.IntegerField(null=True, blank=True)
    score_b = models.IntegerField(null=True, blank=True)
    is_finished = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.team_a} vs {self.team_b}"


class Prediction(models.Model):
    username = models.CharField(max_length=100)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    predicted_team_a_score = models.IntegerField()
    predicted_team_b_score = models.IntegerField()
    points = models.IntegerField(default=0)

    class Meta:
        unique_together = ('username', 'match')  # Un usuario solo predice una vez por partido

    def __str__(self):
        return f"{self.username} - {self.match}"