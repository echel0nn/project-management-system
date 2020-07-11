from django.contrib import admin
from .models import Project
from .models import Task

# Register your models here.


class ProjectAdmin(admin.ModelAdmin):
    raw_id_fields = ('team',)
    list_display = ['name', 'team', ]
    list_filter = ['name', 'team', ]
    search_fields = ['name', 'team', 'status', ]
    prepopulated_fields = {'slug': ('name',)}

    class Meta:
        model = Project


class TaskAdmin(admin.ModelAdmin):
    list_display = ['task_name', 'project']
    list_filter = ['project', ]
    search_fields = ['project']


admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
