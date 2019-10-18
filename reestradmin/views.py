from django.shortcuts import render

# Create your views here.
def hello(request):
    content = {
        'title': 'reestr admin page'
    }
    return render(request, 'reestradmin/base.html', content)