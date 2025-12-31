from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages
from django.db.models.query import QuerySet
from django.conf import settings
from django.http.request import HttpRequest
from accounts.models import User, SelfInfo
from emailing.helpers.gmail import send_welcome_email, send_password_reset_email

@admin.register(User)
class BaseUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )

    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    actions = ['send_welcome_email', 'send_password_reset']

    def send_welcome_email(self, request: HttpRequest, queryset: QuerySet) -> None:
        """
        Send welcome email to selected users.
        param request: HttpRequest
        param queryset: QuerySet
        returns: None
        """
        for user in queryset:
            if settings.ASYNC:
                send_welcome_email.delay(user.email)
            else:
                send_welcome_email(user.email)
        self.message_user(request, "Welcome emails have been sent.", messages.SUCCESS)
    send_welcome_email.short_description = "Send welcome email to selected users"

    def send_password_reset(self, request: HttpRequest, queryset: QuerySet) -> None:
        """
        Send password reset email to selected users.
        param request: HttpRequest
        param queryset: QuerySet
        returns: None
        """
        for user in queryset:
            to_email: str = getattr(user, "email")
            if settings.ASYNC:
                send_password_reset_email.delay(to_email)
            else:
                send_password_reset_email(to_email)
        self.message_user(request, "Password reset emails have been sent.", messages.SUCCESS)
    send_password_reset.short_description = "Send password reset emails to selected users"


@admin.register(SelfInfo)
class SelfInfoAdmin(admin.ModelAdmin):
    list_display = ("individual_code", "address", "user")

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        qs = super().get_queryset(request)
        return qs.select_related("user")