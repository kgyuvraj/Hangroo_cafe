from django.contrib import admin
from commons.models import HangrooSetting

@admin.register(HangrooSetting)
class HangrooSettingAdmin(admin.ModelAdmin):
    model = HangrooSetting