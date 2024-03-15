from flask import Flask
from app import app

def handler(request, response):
    # Set Flask's context to the request
    with app.request_context(request):
        # Dispatch the request to Flask
        app.preprocess_request()
        try:
            # Handle the request
            response = app.full_dispatch_request()
        except Exception as e:
            # Handle exceptions
            response = app.handle_exception(e)
        # Set Flask's context to the response
        app.process_response(response)
        return response