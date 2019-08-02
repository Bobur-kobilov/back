from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import Auth
# Register your models here.
User = get_user_model()

class UserAdmin(BaseUserAdmin):
    search_fields = ['email']
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ['email'
        , 'cell_phone'
        , 'status'
        , 'joined_date'
        , 'dept_type'
        , 'dept_rank'
        , 'dept_duty'
        , 'active'
        , 'auth_list']

    def auth_list(self, obj):
        str = ""

        for auth in obj.auth_list.all():
            str += auth.role + " "

        return str

    list_filter = ['active']

    fieldsets = [
        [None, {'fields': ['email'
                            , 'password'
                            , 'cell_phone'
                            , 'status'
                            , 'joined_date'
                            , 'dept_type'
                            , 'dept_rank'
                            , 'dept_duty'
                        ]}],
        ['Permission', {'fields': ['active']}],
    ]

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields':('email'
                , 'password1'
                , 'password2'
                , 'cell_phone'
                , 'status'
                , 'joined_date'
                , 'dept_type'
                , 'dept_rank'
                , 'dept_duty'
                , 'active')
        }),
    )

    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = []

    def save_model( self, request, obj, form, change):
        obj.save()
        # 사용자 기본 권한 정보 저장
        auth = Auth(user_id=obj.get_id(), role='ROLE_Default')
        auth.save()

    class Meta:
        model = User

class AuthAdmin( admin.ModelAdmin):
    search_fields = ['role']
    list_display = ['id','role', 'user']

admin.site.register(User, UserAdmin)
admin.site.register(Auth, AuthAdmin)
admin.site.unregister(Group)