from django.contrib import admin
from .models import Domain, Extension, Customer


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('name', 'sip_url')
    search_fields = ('name',)


@admin.register(Extension)
class ExtensionAdmin(admin.ModelAdmin):
    list_display = ('number', 'domain', 'enabled')
    list_filter = ('domain', 'enabled')
    search_fields = ('number',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('email', 'display_name', 'extension', 'get_domain')
    search_fields = ('email', 'display_name', 'extension__number')
    fields = ('email', 'display_name', 'extension')

    def get_domain(self, obj):
        return obj.extension.domain.name
    get_domain.short_description = 'Domain'
