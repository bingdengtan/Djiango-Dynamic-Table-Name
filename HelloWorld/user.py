from django.shortcuts import render
from models.models import User

def list(request):
    context = {}
    list = []
    request.encoding = 'utf-8'
    if 'q' in request.GET:
        tableId = int(request.GET['q'])
        list = User.sharding_listAll(id=tableId)
        User.objects.r
    context['list'] = list
    return render(request, 'user.html', context)