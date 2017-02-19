from django.shortcuts import render

from django.shortcuts import get_object_or_404

from .models import ShareItem


def item(request, id):
    it = get_object_or_404(ShareItem, pk = id)
    return render(request, 'shares/share_item_view.html', {'item': it})
    
