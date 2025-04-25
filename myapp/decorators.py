from django.shortcuts import redirect
from django.contrib import messages

def login_required_decorator(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if 'user_id' not in request.session:
            messages.error(request, 'You must be logged in to view this page.')
            return redirect('sigIn')
        return view_func(request, *args, **kwargs)
    return _wrapped_view