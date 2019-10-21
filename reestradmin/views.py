from django.shortcuts import render

# Create your views here.

def base(request):
    title = 'ЭДО - НАКС'
    content = {
        'title': title
    }
    return render(request, 'reestradmin/base.html', content)