from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import User, Category, Institution, Donation

# Register your models here.


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    def delete_model(self, request, obj):

        superusers_count = User.objects.filter(is_superuser=True).count()
        user_status = 1 if obj.is_superuser else 0

        if superusers_count - user_status == 0:
            messages.set_level(request, messages.ERROR)
            messages.error(request, 'Nie można usunąć ostatniego administratora !!!')

        else:
            obj.delete()

    def delete_queryset(self, request, queryset):

        superusers_count = User.objects.filter(is_superuser=True).count()
        superusers_in_queryset = queryset.filter(is_superuser=True).count()

        if superusers_count - superusers_in_queryset == 0:
            messages.set_level(request, messages.ERROR)
            messages.error(request, 'Próbujesz usunąć wszystkich administratorów !!!')

        else:
            queryset.delete()


admin.site.register(Category)


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'description')


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('pick_up_date', 'quantity', 'institution', 'user')
