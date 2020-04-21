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

def csp_profile(request):
    title = 'ЭДО - Профиль центра'
    content = {
        'title': title
    }
    return render(request, 'reestradmin/csp_profile.html', content)

def csp_groups(request):
    title = 'ЭДО - Группы спецподготовки'
    content = {
        'title': title
    }
    return render(request, 'reestradmin/csp_groups.html', content)

def csp_add_group(request):
    title = 'ЭДО - Группы спецподготовки'
    content = {
        'title': title
    }
    return render(request, 'reestradmin/csp_add_group.html', content)

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
    title = 'ЭДО - Профиль эксперта'
    content = {
        'title': title
    }
    return render(request, 'reestradmin/expert_profile.html', content)

def certificates_list(request):
    title = 'ЭДО - Список удостоверений'
    content = {
        'title': title
    }
    return render(request, 'reestradmin/certificates_list.html', content)

def webinars(request):
    title = 'ЭДО - Вебинары'
    content = {
        'title': title
    }
    return render(request, 'reestradmin/webinars.html', content)

def user_ul_profile(request):
    title = 'ЛК юридического лица'
    content = {
        'title': title
    }
    return render(request, 'reestradmin/user_ul_profile.html', content)

def spks_user_applications(request):
    title = 'ЛК_ЮЛ оценка квалификаций'
    content = {
        'title': title
    }
    return render(request, 'reestradmin/spks_user_applications.html', content)

def spks_new_application(request):
    title = 'ЛК_ЮЛ оценка квалификаций'
    content = {
        'title': title
    }
    return render(request, 'reestradmin/spks_new_application.html', content)

def spks_new_group(request):
    title = 'ЛК_ЮЛ оценка квалификаций'
    content = {
        'title': title
    }
    return render(request, 'reestradmin/spks_new_group.html', content)

def spks_user_certificates(request):
    title = 'ЛК_ЮЛ оценка квалификаций'
    content = {
        'title': title
    }
    return render(request, 'reestradmin/spks_user_certificates.html', content)