from django.shortcuts import redirect
from django.urls import reverse

class AuthMiddleware:
    """
    Middleware pour protéger toutes les pages sauf login et handler_connexion.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URLs à exclure de la protection
        excluded_urls = [
            reverse('login'),
            reverse('handler_connexion'),
        ]

        # Si l'utilisateur n'est pas connecté et qu'on est sur une page protégée
        if not request.session.get('user_id') and request.path not in excluded_urls:
            return redirect('login')

        response = self.get_response(request)
        return response
