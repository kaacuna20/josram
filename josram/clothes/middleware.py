class ClearSpecificSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process the request
        response = self.get_response(request)

        # Clear specific session variables when user navigates to a different endpoint
        if request.path != request.session.get('current_endpoint', ''):
            request.session.pop('filters_colors', None)
            request.session.pop('filters_price', None)

            # Update the current endpoint in session
            request.session['current_endpoint'] = request.path

        return response