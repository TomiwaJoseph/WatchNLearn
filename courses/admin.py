from django.contrib import admin
from .models import (
    Category, Course, Module, Content,
    Review
)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["__str__", 'get_course', 'get_instructor']

    def get_course(self, obj):
        return obj.course.title

    def get_instructor(self, obj):
        return obj.course.instructor.get_name()

    get_course.short_description = 'Course'
    get_instructor.short_description = 'Instructor'
    # get_course.admin_order_field = 'course__instructor'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_title', 'slug']
    prepopulated_fields = {'slug': ('category_title',)}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', "picture_path",
                    'instructor', 'category', 'status']
    exclude = ['slug',]
    list_editable = ['status']

    def picture_path(self, obj):
        return obj.thumbnail_image


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['course', 'module_title', 'module_title_slug']
    prepopulated_fields = {'module_title_slug': ('module_title',)}


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ['module', 'title']
