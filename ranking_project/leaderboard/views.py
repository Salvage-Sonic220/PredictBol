from django.shortcuts import render, redirect
from .models import Match, Prediction

def home(request):
    matches = Match.objects.all()
    
    # Obtener partido seleccionado (para mantenerlo después de guardar)
    selected_match_id = request.GET.get('match') or request.POST.get('match')
    selected_match = None
    predictions = Prediction.objects.select_related('match')

    if selected_match_id:
        try:
            selected_match = Match.objects.get(id=selected_match_id)
            predictions = predictions.filter(match=selected_match)
        except Match.DoesNotExist:
            pass
    
    # Ordenar por puntos (descendente)
    predictions = predictions.order_by('-points')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        match_id = request.POST.get('match')
        
        try:
            pred_a = int(request.POST.get('predicted_team_a_score', 0))
            pred_b = int(request.POST.get('predicted_team_b_score', 0))
        except:
            pred_a = 0
            pred_b = 0

        match = Match.objects.get(id=match_id)

        # Crear o actualizar predicción
        prediction, created = Prediction.objects.get_or_create(
            username=username,
            match=match,
            defaults={
                'predicted_team_a_score': pred_a,
                'predicted_team_b_score': pred_b
            }
        )

        if not created:
            prediction.predicted_team_a_score = pred_a
            prediction.predicted_team_b_score = pred_b

        # Calcular puntos automáticamente
        if match.score_a is not None and match.score_b is not None:
            if pred_a == match.score_a and pred_b == match.score_b:
                prediction.points = 10  # Exacto
            elif (pred_a > pred_b and match.score_a > match.score_b) or \
                 (pred_a < pred_b and match.score_a < match.score_b):
                prediction.points = 5   # Ganador correcto
            else:
                prediction.points = 0
            prediction.save()

        # Redirigir manteniendo el partido seleccionado
        return redirect(f'/?match={match_id}')

    context = {
        'matches': matches,
        'predictions': predictions,
        'selected_match': selected_match,
    }
    return render(request, 'leaderboard/index.html', context)