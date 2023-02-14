from django.contrib import admin
from .models import Newsletter, LandingPagePictures, InstructorPagePictures


admin.site.register(Newsletter)
admin.site.register(InstructorPagePictures)


@admin.register(LandingPagePictures)
class LandingPictures(admin.ModelAdmin):
    list_display = ['caption', 'image_tag']
    prepopulated_fields = {'slug': ('caption',)}
