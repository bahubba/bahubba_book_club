from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import ReaderCreationForm, ReaderChangeForm
from .models import Reader


class ReaderAdmin(UserAdmin):
    add_form = ReaderCreationForm
    form = ReaderChangeForm
    model = Reader
    list_display = (
        "username",
        "email",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "username",
        "email",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Permissions",
            {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username" "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    search_fields = (
        "username",
        "email",
    )
    ordering = (
        "username",
        "email",
    )


admin.site.register(Reader, ReaderAdmin)
