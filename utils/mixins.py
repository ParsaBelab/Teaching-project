from django.contrib import admin


class AdminTimeMixin(admin.ModelAdmin):
    list_filter = ('created',)
    readonly_fields = ('created', 'updated')
