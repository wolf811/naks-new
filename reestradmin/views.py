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

def center_acsm_edit(request):
    title = 'ЭДО - Профиль центра'
    content = {
        'title': title
    }
    return render(request, 'reestradmin/center_acsm_edit.html', content)
    
def organization_list(request):
    title = 'ЭДО - Организации'
    content = {
        'title': title
    }
    return render(request, 'reestradmin/organization_list.html', content)


def organization_edit(request):
    title = 'ЭДО - Профиль организации'
    content = {
        'title': title
    }
    return render(request, 'reestradmin/organization_edit.html', content)

def list_instructions(request):
    title = 'ЭДО - Указания'
    content = {
        'title': title
    }
    return render(request, 'reestradmin/list_instructions.html', content)

def instruction_detail(request):
    title = 'ЭДО - Новое указание'
    content = {
        'title': title
    }
    return render(request, 'reestradmin/instruction_detail.html', content)

def experts_list(request):
    title = 'ЭДО - Эксперты НАКС'
    content = {
        'title': title
    }
    return render(request, 'reestradmin/experts_list.html', content)

def expert_profile(request):
    title = 'ЭДО - Эксперты НАКС'
    content = {
        'title': title
    }
    return render(request, 'reestradmin/expert_profile.html', content)