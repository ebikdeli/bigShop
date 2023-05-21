from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    """Main view of the user dashboard"""
    user = request.user
    orders = user.order_user
    return render(request, 'templates/dashboard/profile.html')
    