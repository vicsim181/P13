from django.contrib import admin
from .models import Comment, Project, Question, MCQAnswer
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('name', 'publication', 'end_date', 'project_type', 'owner', 'ready_for_publication', 'is_over')
    list_filter = ('ready_for_publication', 'is_over', 'project_type')
    search_fields = ('publication', '', 'username')
    ordering = ('publication',)
    filter_horizontal = ()


class CommentAdmin(admin.ModelAdmin):
    pass


# Register your models here.
admin.site.register(Project, ProjectAdmin)
admin.site.register(Comment, admin.ModelAdmin)
admin.site.register(Question, admin.ModelAdmin)
admin.site.register(MCQAnswer, admin.ModelAdmin)
