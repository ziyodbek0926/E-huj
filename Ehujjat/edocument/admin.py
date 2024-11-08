from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Table, Tashkilot, UserP
import openpyxl
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password

# Group ni unregister qilish
admin.site.unregister(Group)

# UserP modelini boshqarish uchun admin sinfi
class UserPAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name')

    def has_module_permission(self, request):
        return request.user.username == 'admin'

    def has_view_permission(self, request, obj=None):
        return request.user.username == 'admin'

    def has_add_permission(self, request):
        return request.user.username == 'admin'

    def has_change_permission(self, request, obj=None):
        return request.user.username == 'admin'

    def has_delete_permission(self, request, obj=None):
        return request.user.username == 'admin'

admin.site.register(UserP, UserPAdmin)

# User modelini boshqarish uchun admin sinfi
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

    def has_module_permission(self, request):
        return request.user.username == 'admin'

    def has_view_permission(self, request, obj=None):
        return request.user.username == 'admin'

    def has_add_permission(self, request):
        return request.user.username == 'admin'

    def has_change_permission(self, request, obj=None):
        return request.user.username == 'admin'

    def has_delete_permission(self, request, obj=None):
        return request.user.username == 'admin'
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.password = make_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Status filtrini yaratish
class StatusFilter(admin.SimpleListFilter):
    title = 'Holat'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            (True, 'Faol'),
            (False, 'Nofaol'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'True':
            return queryset.filter(status=True)
        if self.value() == 'False':
            return queryset.filter(status=False)
        return queryset

# Tashkilot filtrini yaratish
class TashkilotFilter(admin.SimpleListFilter):
    title = 'Tashkilot'
    parameter_name = 'tashkilot'

    def lookups(self, request, model_admin):
        return [(tashkilot.id, tashkilot.nomi) for tashkilot in Tashkilot.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(tashkilot_id=self.value())
        return queryset

# Table modelini boshqarish uchun admin sinfi
@admin.register(Table)
class WorkerAdmin(admin.ModelAdmin):
    actions = ['export_to_excel']
    exclude = ('user',)

    list_display = ('id', 'tashkilot', 'zayafka_vaqti', 'tekshirilgan_vaqti', 'status', 'user')
    list_filter = (TashkilotFilter, StatusFilter)

    def has_module_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return request.user.username == 'admin'

    def save_model(self, request, obj, form, change):
        try:
            userp = UserP.objects.get(user=request.user)
            obj.user = userp.full_name  # UserP dan full_name ni olish
        except UserP.DoesNotExist:
            obj.user = request.user.username  # Agar UserP topilmasa, username ni tayinlash
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.username != 'admin':
            user_full_name = UserP.objects.filter(user=request.user).values_list('full_name', flat=True).first()
            if user_full_name:
                return queryset.filter(user=user_full_name)
        return queryset

    def export_to_excel(self, request, queryset):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Table Data"

        sheet.append(['ID', 'Tashkilot', 'Zayafka Vaqti', 'Tekshirilgan Vaqti', 'Status', 'User'])

        for obj in queryset:
            zayafka_vaqti = obj.zayafka_vaqti.astimezone(timezone.get_current_timezone()).strftime('%Y-%m-%d %H:%M:%S') if obj.zayafka_vaqti else ''
            tekshirilgan_vaqti = obj.tekshirilgan_vaqti.astimezone(timezone.get_current_timezone()).strftime('%Y-%m-%d %H:%M:%S') if obj.tekshirilgan_vaqti else ''

            sheet.append([
                obj.id,
                obj.tashkilot.nomi,
                zayafka_vaqti,  
                tekshirilgan_vaqti,
                obj.status,
                obj.user
            ])

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="exported_data.xlsx"'
        
        workbook.save(response)
        return response

    export_to_excel.short_description = "Excel eksport"

# Tashkilot modelini boshqarish uchun admin sinfi
@admin.register(Tashkilot)
class TashkilotAdmin(admin.ModelAdmin):
    list_display = ('id', 'nomi')

    def has_module_permission(self, request):
        return True
    
    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return False
