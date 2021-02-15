from django.shortcuts import render

# Create your views here.

def base(request):
    title = 'ЭДО'
    content = {
        'title': title
    }
    return render(request, 'control/base.html', content)

def acpnk_profile(request):
    title = 'ЭДО - АЦПНК'
    content = {
        'title': title
    }
    return render(request, 'control/acpnk_profile.html', content)