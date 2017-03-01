from django.shortcuts import render

from django.shortcuts import get_object_or_404

from .models import Portfolio


def item(request, id):
    it = get_object_or_404(Portfolio, pk = id)
    return render(request, 'portfolio/portfolio_item_view.html', {'item': it, 'shares_info': it.shares_info(), })

