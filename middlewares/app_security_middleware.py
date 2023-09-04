
class SecurityMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    # TODO: Need to implement logic to Secure the application.
    def __call__(self, request):
        response = self.get_response(request)
        return response
