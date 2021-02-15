from django.shortcuts import render
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from mainapp.models import *
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.views import APIView
import random
from .serializers import PostSerializer

# Create your views here.


def index(request):
    title = 'НАКС - Главная'
    banners = Banner.objects.filter(active=True).order_by('number')
    all_posts =Post.objects.filter(active=True).order_by('-published_date')[:4]
    # posts for central part of page
    main_posts_final = []
    for p in all_posts:
        post_with_additional_photos = {
            'post': None,
            'additional_photos': []
        }
        post_with_additional_photos['post'] = p
        add_photos = Photo.objects.filter(post=p)
        if len(add_photos) > 0:
            for photo in add_photos:
                post_with_additional_photos['additional_photos'].append(photo)
            main_posts_final.append(post_with_additional_photos)
        else:
            post_with_additional_photos['post'] = p
            post_with_additional_photos['additional_photos'] = None
            main_posts_final.append(post_with_additional_photos)

    # posts for side part of page
    secondary_posts = Post.objects.filter(
        active=True).order_by('-published_date')[4:6]

    # announcements
    events = Post.objects.filter(
        mark_as_announcement=True).order_by('-published_date')[:2]

    main_page_documents_rotation_list = Document.objects.filter(
        main_page_rotation=True
    )
    shuffled_documents = [doc for doc in main_page_documents_rotation_list]
    random.shuffle(shuffled_documents)

    content = {
        'title': title,
        'banners': banners,
        'main_posts': main_posts_final,
        'secondary_posts': secondary_posts,
        'events': events,
        'documents': shuffled_documents[:4]
    }
    # import pdb; pdb.set_trace()
    return render(request, 'mainapp/index.html', content)


def news(request):
    title = 'НАКС - Новости'
    post_list = Post.objects.filter(active=True).order_by('-published_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(post_list, 9)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    # news_page_posts = []
    # all_posts = Post.objects.all()
    # for post in all_posts:
    #     photo = Photo.objects.filter(post__pk=post.pk).first()
    #     news_page_posts.append(
    #         {'post': post, 'photo': photo, }
    #     )
    # return render(request, 'mainapp/news.html')

    categories = Category.objects.all()
    content = {
        'posts': posts,
        'categories': categories
    }
    # import pdb; pdb.set_trace()
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
    subdivisions = ContactSubdivision.objects.all().order_by('number')
    departments = []
    for sub in subdivisions:
        departments.append({
            'department': {
                'name': sub.title,
                'members': [member for member in Contact.objects.filter(subdivision=sub).order_by('number')]
            }
            })
    # import pdb; pdb.set_trace()
    content = {
        'title': title,
        'departments': departments,
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

def sasv_experts(request):
    title = 'НАКС - Эксперты САСв'
    content = {
        'title': title
    }
    return render(request, 'mainapp/sasv_experts.html', content)

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
def tk364_news(request):
    title = 'ТК-364 - Новости'
    content = {
        'title': title
    }
    return render(request, 'mainapp/tk364_news.html', content)

def tk364(request):
    title = 'ТК-364 - Новости'
    content = {
        'title': title
    }
    return render(request, 'mainapp/tk364_news.html', content)

def tk364_about(request):
    title = 'ТК-364 - О ТК-364'
    content = {
        'title': title
    }
    return render(request, 'mainapp/tk364_about.html', content)

def tk364_sostav(request):
    title = 'ТК-364 - Состав ТК-364'
    content = {
        'title': title
    }
    return render(request, 'mainapp/tk364_sostav.html', content)

def tk364_development(request):
    title = 'ТК-364 - Разработка стандартов'
    content = {
        'title': title
    }
    return render(request, 'mainapp/tk364_development.html', content)

def tk364_standarts(request):
    title = 'ТК-364 - Разработанные стандарты'
    content = {
        'title': title
    }
    return render(request, 'mainapp/tk364_standarts.html', content)

def tk364_sto(request):
    title = 'ТК-364 - Реестр СТО'
    content = {
        'title': title
    }
    return render(request, 'mainapp/tk364_sto.html', content)

def tk364_plan(request):
    title = 'ТК-364 - План работ'
    content = {
        'title': title
    }
    return render(request, 'mainapp/tk364_plan.html', content)

def tk364_fund(request):
    title = 'ТК-364 - Фонд стандартов'
    content = {
        'title': title
    }
    return render(request, 'mainapp/tk364_fund.html', content)

def tk364_ntd(request):
    title = 'ТК-364 - Нормативные документы'
    content = {
        'title': title
    }
    return render(request, 'mainapp/tk364_ntd.html', content)

def tk364_lk(request):
    title = 'ТК-364 - Личный кабинет'
    content = {
        'title': title
    }
    return render(request, 'mainapp/tk364_lk.html', content)

def tk364_lk_new_docs(request):
    title = 'ТК-364 - Личный кабинет'
    content = {
        'title': title
    }
    return render(request, 'mainapp/tk364_lk_new_docs.html', content)
# ============= end TK364 ===============


# ============= SPKS ===============
def spks(request):
    title = 'НАКС - СПКС'
    content = {
        'title': title
    }
    return render(request, 'mainapp/spks.html', content)


def spks_docs(request):
    title = 'СПКС - Документы'
    content = {
        'title': title
    }
    return render(request, 'mainapp/spks_docs.html', content)

def spks_coks(request):
    title = 'СПКС - ЦОКи'
    content = {
        'title': title
    }
    return render(request, 'mainapp/spks_coks.html', content)


def spks_reestr_svid(request):
    title = 'СПКС - Реестр свидетельств'
    content = {
        'title': title
    }
    return render(request, 'mainapp/spks_reestr_svid.html', content)

def spks_composition(request):
    title = 'СПКС - Состав Совета'
    content = {
        'title': title
    }
    return render(request, 'mainapp/spks_composition.html', content)

def spks_composition_region(request):
    title = 'СПКС - Состав региональных представителей'
    content = {
        'title': title
    }
    return render(request, 'mainapp/spks_composition_region.html', content)

def spks_composition_experts(request):
    title = 'СПКС - Эксперты Совета'
    content = {
        'title': title
    }
    return render(request, 'mainapp/spks_composition_experts.html', content)

def spks_comiss(request):
    title = 'СПКС - Комиссии'
    content = {
        'title': title
    }
    return render(request, 'mainapp/spks_comiss.html', content)

def spks_work_plan(request):
    title = 'СПКС - План работы'
    content = {
        'title': title
    }
    return render(request, 'mainapp/spks_work_plan.html', content)

def spks_protocols(request):
    title = 'СПКС - Протоколы'
    content = {
        'title': title
    }
    return render(request, 'mainapp/spks_protocols.html', content)

def spks_help_info(request):
    title = 'СПКС - Справочно-техническая информация'
    content = {
        'title': title
    }
    return render(request, 'mainapp/spks_help_info.html', content)

def spks_task_examples(request):
    title = 'СПКС - Примеры заданий'
    content = {
        'title': title
    }
    return render(request, 'mainapp/spks_task_examples.html', content)

def spks_reestr_qual(request):
    title = 'СПКС - Квалификации'
    content = {
        'title': title
    }
    return render(request, 'mainapp/spks_reestr_qual.html', content)

def spks_standarts_ok(request):
    title = 'СПКС - Профессиональные стандарты'
    content = {
        'title': title
    }
    return render(request, 'mainapp/spks_standarts_ok.html', content)

def spks_standarts_new(request):
    title = 'СПКС - Профессиональные стандарты'
    content = {
        'title': title
    }
    return render(request, 'mainapp/spks_standarts_new.html', content)

def spks_cok018(request):
    title = 'СПКС - ЦОК-018'
    content = {
        'title': title
    }
    return render(request, 'mainapp/spks_cok018.html', content)

def monitoring(request):
    title = 'Мониторинг рынка труда'
    content = {
        'title': title
    }
    return render(request, 'mainapp/monitoring.html', content)
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

def password_recovery(request):
    title = 'Восстановление пароля'
    content = {
        'title': title
    }
    return render(request, 'mainapp/password_recovery.html', content)

def password_recovery_mail(request):
    title = 'Восстановление пароля'
    content = {
        'title': title
    }
    return render(request, 'mainapp/password_recovery_mail.html', content)

# ++++++++++++++DJANGO REST+++++++++++++++#

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(active=True).order_by('-published_date')
    serializer_class = PostSerializer


class PostDetailsAPI(APIView):
    """
    Retrieve, update or delete a Post instance.
    """
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)