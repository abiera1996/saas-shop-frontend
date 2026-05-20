class SimpleUser:
    """A lightweight user object that doesn't rely on the database."""
    def __init__(self, user_data):
        self.is_authenticated = True
        self.id = user_data.get('id')
        self.username = user_data.get('username')
        self.first_name = user_data.get('first_name', '')
        self.last_name = user_data.get('last_name', '')
        self.token = user_data.get('token')
        self.email = user_data.get('email', '')
        # Add any other fields your API returns
        self.role_code = user_data.get('role_code')

    def __str__(self):
        return self.username or "Unknown"

class AnonymousUser:
    is_authenticated = False
    username = ''

class APIAuthenticationMiddleware:
    """Middleware to populate request.user from session data."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if our custom user_data exists in the session
        user_data = request.session.get('user_data')

        if user_data:
            # User is logged in, attach custom user object
            request.user = SimpleUser(user_data)
        else:
            # User is not logged in
            request.user = AnonymousUser()

        response = self.get_response(request)
        return response
