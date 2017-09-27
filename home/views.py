from django.shortcuts import render, HttpResponse

def home(request):
    if request.user.is_authenticated():
        context = {
            'isim': 'Emel'
        }
    else:
        context = {
            'isim': 'Emel2'
        }
    return render(request, 'bootstrap/base/post_base.html', context)