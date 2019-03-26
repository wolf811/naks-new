from django.shortcuts import render
from mainapp.models import Post
from mainapp.models import Photo

# Create your views here.
def index(request):
    title = 'НАКС - Главная'
    content = {
        'title': title,
    }
    return render(request, 'mainapp/index.html', content)

def news(request):
    title = 'НАКС - Новости'
    news_page_posts = []
    all_posts = Post.objects.all()
    for post in all_posts:
        photo = Photo.objects.filter(post__pk=post.pk).first()
        news_page_posts.append(
            {'post': post, 'photo': photo, }
        )
    # for publication in news_page_posts:
    #     print (publication['post'], publication['photo'])
    # paginator = Paginator(news_page_posts, 9)
    # page = request.GET.get('page')
    # posts = paginator.get_page(page)
    content = {
        'title': title,
        'post': post,
    }
    return render(request, 'mainapp/news.html', content)

def news_details(request, pk):
    title = 'НАКС - Новости'
    post = Post.objects.get(pk=pk)
    photos = Photo.objects.filter(post_id=pk)
    content = {
        'title': title,
        'post': post,
        'photos': photos,
    }
    return render(request, 'mainapp/news_details.html', content)

def agreement(request):
    title = 'НАКС - Соглашения'
    content = {
        'title': title
    }
    return render(request, 'mainapp/agreement.html', content)

def contacts(request):
    title = 'НАКС - Контакты'
    content = {
        'title': title
    }
    return render(request, 'mainapp/contacts.html', content)

# ============= SASv ===============
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
# ============= end SASv ===============

# ============= SRO ===============
def sro(request):
    title = 'НАКС - СРО'
    content = {
        'title': title
    }
    return render(request, 'mainapp/sro.html', content)

def sro_activity(request):
    title = 'НАКС - СРО'
    content = {
        'title': title
    }
    return render(request, 'mainapp/sro_activity.html', content)

def sro_docs(request):
    title = 'НАКС - СРО'
    content = {
        'title': title
    }
    return render(request, 'mainapp/sro_docs.html', content)

def sro_reestr(request):
    title = 'НАКС - СРО'
    content = {
        'title': title
    }
    return render(request, 'mainapp/sro_reestr.html', content)

def sro_sobranie(request):
    title = 'НАКС - СРО'
    content = {
        'title': title
    }
    return render(request, 'mainapp/sro_sobranie.html', content)

def sro_presidium(request):
    title = 'НАКС - СРО'
    content = {
        'title': title
    }
    return render(request, 'mainapp/sro_presidium.html', content)

def sro_president(request):
    title = 'НАКС - СРО'
    content = {
        'title': title
    }
    return render(request, 'mainapp/sro_president.html', content)

def sro_control_comitet(request):
    title = 'НАКС - СРО'
    content = {
        'title': title
    }
    return render(request, 'mainapp/sro_control_comitet.html', content)

def sro_disciplinary_comitet(request):
    title = 'НАКС - СРО'
    content = {
        'title': title
    }
    return render(request, 'mainapp/sro_disciplinary_comitet.html', content)

def sro_audit_commission(request):
    title = 'НАКС - СРО'
    content = {
        'title': title
    }
    return render(request, 'mainapp/sro_audit_commission.html', content)

def sro_legislation(request):
    title = 'НАКС - СРО'
    content = {
        'title': title
    }
    return render(request, 'mainapp/sro_legislation.html', content)

def sro_forms_docs(request):
    title = 'НАКС - СРО'
    content = {
        'title': title
    }
    return render(request, 'mainapp/sro_forms_docs.html', content)
# ============= end SRO ===============

# ============= TK364 ===============
def tk364(request):
    title = 'НАКС - ТК-364'
    content = {
        'title': title
    }
    return render(request, 'mainapp/tk364.html', content)
# ============= end TK364 ===============

# ============= SPKS ===============
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
# ============= end SPKS ===============

# ============= SDS ===============
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
# ============= end SDS ===============