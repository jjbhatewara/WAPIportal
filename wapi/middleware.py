from django.shortcuts import redirect

class RoleBasedAccessControlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Restrict access to /owner for non-superusers
            if request.path.startswith('/owner') and not request.user.is_superuser:
                return redirect('/exec/dashboard')  # Redirect to executive dashboard

            # Restrict access to /exec for superusers
            if request.path.startswith('/exec') and request.user.is_superuser:
                return redirect('/owner/dashboard')  # Redirect to owner dashboard

        response = self.get_response(request)
        return response