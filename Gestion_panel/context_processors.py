# Gestion_panel/context_processors.py
from .models import Utilisateur

def current_user(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = Utilisateur.objects.get(id=user_id)
            return {'current_user': user}
        except Utilisateur.DoesNotExist:
            return {}
    return {}
