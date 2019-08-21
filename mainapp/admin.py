from django.contrib import admin
from mainapp.models import *
from django.urls import reverse
from django.utils.html import format_html
from django.forms import TextInput
from django.db import models

# Register your models here.
def get_picture_preview(obj):
    if obj.pk:  # if object has already been saved and has a primary key, show picture preview
        return format_html("""<a href="{src}" target="_blank">
        <img src="{src}" alt="title" style="max-width: 200px; max-height: 200px;" />
        </a>""".format(src=obj.image.url))
    return "(После загрузки фотографии здесь будет ее миниатюра)"

class PhotoInline(admin.StackedInline):
    model = Photo
    extra = 0
    fields = ['image', get_picture_preview, 'number']
    readonly_fields = [get_picture_preview]

    def get_edit_link(self, obj=None):
        if obj.pk:  # if object has already been saved and has a primary key, show link to it
            url = reverse('admin:%s_%s_change' % (
                obj._meta.app_label, obj._meta.model_name), args=[force_text(obj.pk)])
            return format_html("""<a href="{url}">{text}</a>""".format(
                url=url,
                text="Редактировать %s отдельно" % obj._meta.verbose_name,
            ))
        return "(Загрузите фотографию и нажмите \"Сохранить и продолжить редактирование\")"
    get_edit_link.short_description = "Изменить"
    get_edit_link.allow_tags = True


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    view_on_site = True
    # fields = ('published_date', 'category', 'title', 'subtitle', 'short_description', 'full_description', 'main_picture')

    list_display = ['title', 'category', 'active', 'published_date']
    inlines = [PhotoInline]
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        # models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }
    def view_on_site(self, obj):
        url = reverse('news_details', kwargs={'pk': obj.pk})
        return url

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    view_on_site = True
    list_display = ['title', 'number', get_picture_preview,]

# admin.site.register(Contact)
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'subdivision', 'number']

@admin.register(ContactSubdivision)
class ContactSubdivisionAdmin(admin.ModelAdmin):
    list_display = ['title', 'number']

admin.site.register(OrgProfile)
admin.site.register(Partner)
admin.site.register(Document)
admin.site.register(Photo)
admin.site.register(Tag)
admin.site.register(Category)