from django.shortcuts import render

# Create your views here.
def index(request):
    title = 'НАКС - Главная'
    content = {
        'title': title
    }
    return render(request, 'mainapp/index.html', content)

def news_all(request):
    title = 'НАКС - Новости'
    content = {
        'title': title
    }
    return render(request, 'mainapp/news_all.html', content)

def news_one(request):
    title = 'НАКС - Новости'
    content = {
        'title': title
    }
    return render(request, 'mainapp/news_one.html', content)

def agreement(request):
    title = 'НАКС - Соглашения'
    content = {
        'title': title
    }
    return render(request, 'mainapp/agreement.html', content)

def sasv(request):
    title = 'НАКС - САСв'
    content = {
        'title': title
    }
    return render(request, 'mainapp/sasv.html', content)
    
def sasv_ac(request):
    title = 'НАКС - САСв'
    content = {
        'title': title
    }
    return render(request, 'mainapp/sasv_ac.html', content)

def sasv_acsm(request):
    title = 'НАКС - САСв'
    content = {
        'title': title
    }
    return render(request, 'mainapp/sasv_acsm.html', content)

def sasv_acso(request):
    title = 'НАКС - САСв'
    content = {
        'title': title
    }
    return render(request, 'mainapp/sasv_acso.html', content)

def sasv_acst(request):
    title = 'НАКС - САСв'
    content = {
        'title': title
    }
    return render(request, 'mainapp/sasv_acst.html', content)

def sasv_br1gac(request):
    title = 'НАКС - БР-1ГАЦ'
    content = {
        'title': title
    }
    return render(request, 'mainapp/sasv_br1gac.html', content)

def sasv_docs(request):
    title = 'НАКС - Документы САСв'
    content = {
        'title': title
    }
    return render(request, 'mainapp/sasv_docs.html', content)

def sasv_nts(request):
    title = 'НАКС - НТС'
    content = {
        'title': title
    }
    return render(request, 'mainapp/sasv_nts.html', content)

def sasv_helpInfo(request):
    title = 'НАКС - САСв'
    content = {
        'title': title
    }
    return render(request, 'mainapp/sasv_helpInfo.html', content)

def sasv_openNaks(request):
    title = 'НАКС - Обратная связь'
    content = {
        'title': title
    }
    return render(request, 'mainapp/sasv_openNaks.html', content)

def sasv_reestr_staff(request):
    title = 'НАКС - Реестр персонала'
    content = {
        'title': title
    }
    return render(request, 'mainapp/sasv_reestr_staff.html', content)

def sasv_reestr_sm(request):
    title = 'НАКС - Реестр сварочных материалов'
    content = {
        'title': title
    }
    return render(request, 'mainapp/sasv_reestr_sm.html', content)

def sasv_reestr_so(request):
    title = 'НАКС - Реестр сварочного оборудования'
    content = {
        'title': title
    }
    return render(request, 'mainapp/sasv_reestr_so.html', content)

def sasv_reestr_st(request):
    title = 'НАКС - Реестр сварочных технологий'
    content = {
        'title': title
    }
    return render(request, 'mainapp/sasv_reestr_st.html', content)

def sro(request):
    title = 'НАКС - СРО'
    content = {
        'title': title
    }
    return render(request, 'mainapp/sro.html', content)

def sro_docs(request):
    title = 'НАКС - СРО'
    content = {
        'title': title
    }
    return render(request, 'mainapp/sro_docs.html', content)

def contacts(request):
    title = 'НАКС - Контакты'
    content = {
        'title': title
    }
    return render(request, 'mainapp/contacts.html', content)

def tk364(request):
    title = 'НАКС - ТК-364'
    content = {
        'title': title
    }
    return render(request, 'mainapp/tk364.html', content)

def spks(request):
    title = 'НАКС - СПКС'
    content = {
        'title': title
    }
    return render(request, 'mainapp/spks.html', content)

def spks_docs(request):
    title = 'НАКС - Документы СПКС'
    content = {
        'title': title
    }
    return render(request, 'mainapp/spks_docs.html', content)

def spks_reestr(request):
    title = 'НАКС - СПКС'
    content = {
        'title': title
    }
    return render(request, 'mainapp/spks_reestr.html', content)

def sds(request):
    title = 'НАКС - СДС'
    content = {
        'title': title
    }
    return render(request, 'mainapp/sds.html', content)

def sds_docs(request):
    title = 'НАКС - Документы СДС'
    content = {
        'title': title
    }
    return render(request, 'mainapp/sds_docs.html', content)

def sds_reestr_staff(request):
    title = 'НАКС - СДС'
    content = {
        'title': title
    }
    return render(request, 'mainapp/sds_reestr_staff.html', content)

def sds_reestr_sm(request):
    title = 'НАКС - СДС'
    content = {
        'title': title
    }
    return render(request, 'mainapp/sds_reestr_sm.html', content)

def sds_reestr_so(request):
    title = 'НАКС - СДС'
    content = {
        'title': title
    }
    return render(request, 'mainapp/sds_reestr_so.html', content)

def sds_reestr_st(request):
    title = 'НАКС - СДС'
    content = {
        'title': title
    }
    return render(request, 'mainapp/sds_reestr_st.html', content)