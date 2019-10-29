from django.shortcuts import render

# Create your views here.

def base(request):
    title = 'ЭДО - НАКС'
    content = {
        'title': title
    }
    return render(request, 'reestradmin/base.html', content)

def centers_list(request):
    title = 'ЭДО - Центры'
    content = {
        'title': title
    }
    return render(request, 'reestradmin/centers_list.html', content)

def organization_list(request):
    title = 'ЭДО - Организации'
    content = {
        'title': title
    }
    return render(request, 'reestradmin/organization_list.html', content)

def organization_profile(request):
    title = 'ЭДО - Профиль организации'
    content = {
        'title': title
    }
    return render(request, 'reestradmin/organization_profile.html', content)

def organization_edit(request):
    title = 'ЭДО - Профиль организации'
    content = {
        'title': title
    }
    return render(request, 'reestradmin/organization_edit.html', content)