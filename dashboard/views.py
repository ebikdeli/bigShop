from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    """Main view of the user dashboard"""
    orders = request.user.orders
    address = request.user.address_user.first()
    context = {'orders': orders, 'address': address}
    return render(request, 'dashboard/profile.html', context=context)
    