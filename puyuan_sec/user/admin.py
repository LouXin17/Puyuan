from django.contrib import admin
# from django.contrib.auth.admin import UserProfileAdmin
from user.models import *
# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'name',
                    'account',
                    'email',
                    'phone',
                    'fb_id',
                    'status',
                    'group',
                    'birthday',
                    'height',
                    'weight',
                    'gender',
                    'address',
                    'unread_records',
                    'verified',
                    'privacy_policy',
                    'must_change_password',
                    'fcm_id',
                    'badge',
                    'login_times',
                    'created_at',
                    'updated_at',
                    'verificationCode',
                    'password',
                    'invite_code')


class UserSettingAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'user_id',
                    'after_recording',
                    'no_recording_for_a_day',
                    'over_max_or_under_min',
                    'after_meal',
                    'unit_of_sugar',
                    'unit_of_weight',
                    'unit_of_height',
                    'created_at',
                    'updated_at')


class UserDefaultAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'user_id',
                    'sugar_delta_max',
                    'sugar_delta_min',
                    'sugar_morning_max',
                    'sugar_morning_min',
                    'sugar_evening_max',
                    'sugar_evening_min',
                    'sugar_before_max',
                    'sugar_before_min',
                    'sugar_after_max',
                    'sugar_after_min',
                    'systolic_max',
                    'systolic_min',
                    'diastolic_max',
                    'diastolic_min',
                    'pulse_max',
                    'pulse_min',
                    'weight_max',
                    'weight_min',
                    'bmi_max',
                    'bmi_min',
                    'body_fat_max',
                    'body_fat_min',
                    'created_at',
                    'updated_at')


class BloodPressureAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'user_id',
                    'systolic',
                    'diastolic',
                    'pulse',
                    'recorded_at',
                    'type')


class WeightAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'user_id',
                    'weight',
                    'body_fat',
                    'bmi',
                    'recorded_at',
                    'type')


class BloodSugerAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'user_id',
                    'sugar',
                    'exercise',
                    'drug',
                    'timeperiod',
                    'recorded_at',
                    'type')


class A1cAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'user_id',
                    'a1c',
                    'recorded_at',
                    'created_at',
                    'updated_at')


class DrugAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'user_id',
                    'type',
                    'name',
                    'recorded_at')


class MedicalinfoAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'user_id',
                    'diabetes_type',
                    'oad',
                    'insulin',
                    'anti_hypertensives',
                    'created_at',
                    'updated_at')


class DietAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'user_id',
                    'description',
                    'meal',
                    'tag',
                    'image',
                    'lat',
                    'lng',
                    'recorded_at',
                    'type')

# @admin.register(Friendlist)


class FriendlistAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'user_id',
                    'relation_id',
                    'type',
                    'status',
                    'read',
                    'created_at',
                    'updated_at')


class CareAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'user_id',
                    'member_id',
                    'reply_id',
                    'message',
                    'notice',
                    'created_at',
                    'updated_at')


admin.site.register(UserProfile, UserProfileAdmin)
# admin.site.register(DjangoSession, DjangoSessionAdmin)
admin.site.register(UserSetting, UserSettingAdmin)
admin.site.register(UserDefault, UserDefaultAdmin)
admin.site.register(BloodPressure, BloodPressureAdmin)
admin.site.register(Weight, WeightAdmin)
admin.site.register(BloodSuger, BloodSugerAdmin)
admin.site.register(A1c, A1cAdmin)
admin.site.register(Drug, DrugAdmin)
admin.site.register(Medicalinfo, MedicalinfoAdmin)
admin.site.register(Diet, DietAdmin)
admin.site.register(Friendlist, FriendlistAdmin)
admin.site.register(Care, CareAdmin)
