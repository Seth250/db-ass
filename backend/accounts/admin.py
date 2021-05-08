from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# Register your models here.

@admin.register(get_user_model())
class CustomUserAdmin(UserAdmin):
	model = get_user_model()
	fieldsets = (
		(None, {'fields': ('first_name', 'last_name', 'email', 'password')}),
		(_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')})
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide', ),
			'fields': ('first_name', 'last_name', 'email', 'password1', 'password2')
		}),
	)
	list_display = ('first_name', 'last_name', 'email', 'is_active')
	list_display_links = ('first_name', 'last_name')
	search_fields = ('first_name', 'last_name', 'email')
	list_filter = ('is_active', )
	# readonly_fields = ('email', )
	ordering = ('email', )
