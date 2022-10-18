from django.db import models
from django.contrib.auth.models import AbstractUser
import ast
# Create your models here.


class UserProfile(AbstractUser):
    name = models.CharField(max_length=20, null=True)
    account = models.CharField(max_length=20, unique=True, null=True)
    email = models.CharField(max_length=20, null=True)
    phone = models.CharField(max_length=20, null=True)
    fb_id = models.CharField(max_length=20, null=True)
    status = models.CharField(max_length=20, null=True)
    group = models.CharField(max_length=20, null=True)
    birthday = models.CharField(max_length=20, null=True)
    height = models.FloatField(null=True)
    weight = models.CharField(max_length=20, null=True)
    gender = models.BooleanField(max_length=20, default=False)
    address = models.CharField(max_length=20, null=True)
    unread_records = models.CharField(max_length=20, null=True)
    verified = models.BooleanField(max_length=20, default=False)
    privacy_policy = models.BooleanField(max_length=20, default=False)
    must_change_password = models.BooleanField(max_length=20, default=False)
    fcm_id = models.CharField(max_length=20, null=True)
    badge = models.CharField(max_length=20, null=True)
    login_times = models.IntegerField(null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, auto_now=False, null=True)
    updated_at = models.DateTimeField(
        auto_now_add=True, auto_now=False, null=True)
    verificationCode = models.CharField(max_length=20, null=True)
    password = models.CharField(max_length=50, null=True)
    invite_code = models.CharField(max_length=20, null=True, unique=True)

    def __str__(self):
        return'"id": {0}, \r\n"name":{1},\r\n"account":{2},\r\n"email":{3},\r\n"phone":{4},\r\n"fb_id":{5},\r\n"status":{6},\r\n"group":{7},\r\n"birthday":{8},\r\n"height":{9},\r\n"weight":{10},\r\"gender":{11},\r\n"address":{12},\r\n"unread_records":{13},\r\n"verified ":{14},\r\n"privacy_policy":{15},\r\n"must_change_password":{16},\r\n"fcm_id":{17},\r\n"badge":{18},\r\n"login_times":{19},\r\n"created_at":{20},\r\n"updated_at":{21},\r\n"verificationCode":{22},\r\n"password":{23},\r\n"invite_code":{24},\r\n'.format(self.pk, self.name, self.account, self.email, self.phone, self.fb_id, self.status, self.group, self.birthday, self.height, self.weight, self.gender, self.address, self.unread_records, self.verified, self.privacy_policy, self.must_change_password, self.fcm_id, self.badge, self.login_times, self.created_at, self.updated_at, self.verificationCode, self.password, self.invite_code)


class UserSetting(models.Model):
    user_id = models.CharField(max_length=20)
    after_recording = models.BooleanField(max_length=20, default=False)
    no_recording_for_a_day = models.BooleanField(max_length=20, default=False)
    over_max_or_under_min = models.BooleanField(max_length=20, default=False)
    after_meal = models.BooleanField(max_length=20, default=False)
    unit_of_sugar = models.BooleanField(max_length=20, default=False)
    unit_of_weight = models.BooleanField(max_length=20, default=False)
    unit_of_height = models.BooleanField(max_length=20, default=False)
    created_at = models.DateTimeField(
        auto_now_add=True, auto_now=False, null=True)
    updated_at = models.DateTimeField(
        auto_now_add=True, auto_now=False, null=True)

    def __str__(self):
        return '"id":{0},\r\n "user_id":{1},\r\n "after_recording":{2},\r\n "no_recording_for_a_day":{3},\r\n "over_max_or_under_min":{4},\r\n "after_meal":{5},\r\n "unit_of_sugar":{6},\r\n "unit_of_weight":{7},\r\n"unit_of_weight":{8},\r\n "created_at":{9},\r\n "updated_at":{10}'.format(self.pk, self.user_id, self.after_recording, self.no_recording_for_a_day, self.over_max_or_under_min, self.after_meal, self.unit_of_sugar, self.unit_of_weight, self.unit_of_height, self.created_at, self.updated_at)


class UserDefault(models.Model):
    user_id = models.CharField(max_length=20, null=True)
    sugar_delta_max = models.IntegerField(blank=True, null=True)
    sugar_delta_min = models.IntegerField(blank=True, null=True)
    sugar_morning_max = models.IntegerField(blank=True, null=True)
    sugar_morning_min = models.IntegerField(blank=True, null=True)
    sugar_evening_max = models.IntegerField(blank=True, null=True)
    sugar_evening_min = models.IntegerField(blank=True, null=True)
    sugar_before_max = models.IntegerField(blank=True, null=True)
    sugar_before_min = models.IntegerField(blank=True, null=True)
    sugar_after_max = models.IntegerField(blank=True, null=True)
    sugar_after_min = models.IntegerField(blank=True, null=True)
    systolic_max = models.IntegerField(blank=True, null=True)
    systolic_min = models.IntegerField(blank=True, null=True)
    diastolic_max = models.IntegerField(blank=True, null=True)
    diastolic_min = models.IntegerField(blank=True, null=True)
    pulse_max = models.IntegerField(blank=True, null=True)
    pulse_min = models.IntegerField(blank=True, null=True)
    weight_max = models.IntegerField(blank=True, null=True)
    weight_min = models.IntegerField(blank=True, null=True)
    bmi_max = models.IntegerField(blank=True, null=True)
    bmi_min = models.IntegerField(blank=True, null=True)
    body_fat_max = models.IntegerField(blank=True, null=True)
    body_fat_min = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, auto_now=False, null=True)
    updated_at = models.DateTimeField(
        auto_now_add=True, auto_now=False, null=True)

    def __str__(self):
        return '"id": {0}, \r\n "user_id": {1},"sugar_delta_max":{2},\r\n"sugar_delta_min":{3},\r\n"sugar_morning_max":{4},\r\n"sugar_morning_min":{5},\r\n"sugar_evening_max":{6},\r\n"sugar_evening_min":{7},\r\n"sugar_before_max":{8},\r\n"sugar_before_min":{9},\r\n"sugar_after_max":{10},\r\n"sugar_after_min":{11},\r\n"systolic_max":{12},\r\n"systolic_min":{13},\r\n"diastolic_max":{14},\r\n"diastolic_min":{15},\r\n"pulse_max":{16},\r\n"pulse_min":{17},\r\n"weight_max":{18},\r\n"weight_min":{19},\r\n"bmi_max":{20},\r\n"bmi_min":{21},\r\n"body_fat_max":{22},\r\n"body_fat_min":{23},\r\n"created_at":{24},\r\n"updated_at":{25}'.format(self.pk, self.user_id, self.sugar_delta_max, self.sugar_delta_min, self.sugar_morning_max, self.sugar_morning_min, self.sugar_evening_max, self.sugar_evening_min, self.sugar_before_max, self.sugar_before_min, self.sugar_after_max, self.sugar_after_min, self.systolic_max, self.systolic_min, self.diastolic_max, self.diastolic_min, self.pulse_max, self.pulse_min, self.weight_max, self.weight_min, self.bmi_max, self.bmi_min, self.body_fat_max, self.body_fat_min, self.created_at, self.updated_at)


class BloodPressure(models.Model):
    user_id = models.CharField(max_length=20)
    systolic = models.FloatField(blank=True, null=True)
    diastolic = models.FloatField(blank=True, null=True)
    pulse = models.IntegerField(blank=True, null=True)
    recorded_at = models.DateTimeField(null=True, blank=True)
    type = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return '"id": {0}, \r\n "user_id": {1},"systolic":{2},\r\n"diastolic":{3},\r\n"pulse":{4},\r\n"recorded_at":{5},\r\n"type":{6}'.format(self.pk, self.user_id, self.systolic, self.diastolic, self.pulse, self.recorded_at, self.type)


class Weight(models.Model):
    user_id = models.CharField(max_length=20)
    weight = models.FloatField(blank=True, null=True)
    body_fat = models.FloatField(blank=True, null=True)
    bmi = models.FloatField(blank=True, null=True)
    recorded_at = models.DateTimeField(null=True, blank=True)
    type = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return '"id": {0}, \r\n "user_id": {1}, "weight": {2}, \r\n"body_fat": {3}, \r\n"bmi": {4}, \r\n"recorded_at": {5}, \r\n"type": {6}'.format(self.pk, self.user_id, self.weight, self.body_fat, self.bmi, self.recorded_at, self.type)


class BloodSuger(models.Model):
    user_id = models.CharField(max_length=20)
    weight = models.FloatField(blank=True, null=True)
    sugar = models.IntegerField(blank=True, null=True)
    exercise = models.CharField(max_length=20, null=True, blank=True)
    drug = models.CharField(max_length=20, null=True, blank=True)
    timeperiod = models.IntegerField(blank=True, null=True)
    recorded_at = models.DateTimeField(null=True, blank=True)
    type = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return '"id": {0}, \r\n "user_id": {1},"sugar":{2},\r\n"exercise":{3},\r\n"drug":{4},\r\n"timeperiod":{5},\r\n"recorded_at":{6},\r\n"type":{7}'.format(self.pk, self.user_id, self.sugar, self.exercise, self.drug, self.timeperiod, self.recorded_at, self.type)


class ListField(models.TextField):

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return str(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


class Diet(models.Model):  # 未完成
    user_id = models.CharField(max_length=20)
    description = models.CharField(max_length=20, blank=True, null=True)
    meal = models.IntegerField(blank=True, null=True)
    tag = ListField(max_length=20, blank=True, null=True)
    image = models.IntegerField(blank=True, null=True)
    lat = models.FloatField(max_length=20, blank=True, null=True)
    lng = models.FloatField(max_length=20, blank=True, null=True)
    recorded_at = models.DateTimeField(blank=True, null=True)
    type = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return '"id":{0},\r\n"user_id":{1},\r\n"description":{2},\r\n"meal":{3},\r\n"tag":{4}\r\n"image":{5},\r\n"lat":{6},\r\n"lng":{7},\r\n"recorded_at":{8},\r\n"type":{9}'.format(self.pk, self.user_id, self.description, self.meal, self.recorded_at, self.tag, self.image, self.lat, self.lng, self.recorded_at, self.type)


class A1c(models.Model):
    user_id = models.CharField(max_length=20)
    a1c = models.FloatField(max_length=20, blank=True, null=True)
    recorded_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, auto_now=False, null=True)
    updated_at = models.DateTimeField(
        auto_now_add=True, auto_now=False, null=True)

    def __str__(self):
        return '"id":{0},\r\n"user_id":{1},\r\n"a1c":{2},\r\n"recorded_at":{3},\r\n"created_at":{4},\r\n"updated_at":{5},\r\n'.format(self.pk, self.user_id, self.a1c, self.recorded_at, self.created_at, self.updated_at)


class Drug(models.Model):
    user_id = models.CharField(max_length=20)
    type = models.BooleanField(default=False)
    name = models.CharField(max_length=20)
    recorded_at = models.DateTimeField(blank=True, null=True)


class Medicalinfo(models.Model):
    user_id = models.CharField(max_length=20)
    diabetes_type = models.IntegerField(null=True)
    oad = models.BooleanField(default=False)
    insulin = models.BooleanField(default=False)
    anti_hypertensives = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        auto_now_add=True, auto_now=False, null=True)
    updated_at = models.DateTimeField(
        auto_now_add=True, auto_now=False, null=True)

    def __str__(self):
        return '"id":{0},\r\n"user_id":{1},\r\n"diabetes_type":{2},\r\n"oad":{3},\r\n"insulin":{4},\r\n"anti_hypertensives":{5},\r\n"created_at":{6},\r\n"updated_at":{7},\r\n'.format(self.pk, self.user_id, self.diabetes_type, self.oad, self.insulin, self.anti_hypertensives, self.created_at, self.updated_at)


class Friendlist(models.Model):
    user_id = models.CharField(max_length=20)
    relation_id = models.CharField(max_length=20)
    type = models.IntegerField(null=True)
    status = models.CharField(max_length=20)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        auto_now_add=True, auto_now=False, null=True)
    updated_at = models.DateTimeField(
        auto_now_add=True, auto_now=False, null=True)

    def __str__(self):
        return '"id":{0},\r\n"user_id":{1},\r\n"relation_id":{2},\r\n"type":{3},\r\n"status":{4},\r\n"read":{5},\r\n"created_at":{6},\r\n"updated_at":{7},\r\n'.format(self.pk, self.user_id, self.relation_id, self.type, self.status, self.read, self.created_at, self.updated_at)


class Care(models.Model):
    user_id = models.CharField(max_length=20)
    member_id = models.CharField(max_length=20, null=True)
    reply_id = models.IntegerField(null=True)
    message = models.CharField(max_length=100, null=True)
    notice = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, auto_now=False, null=True)
    updated_at = models.DateTimeField(
        auto_now_add=True, auto_now=False, null=True)

    def __str__(self):
        return '"id": {0}, \r\n"user_id": {1}, \r\n"member_id": {2}, \r\n"reply_id": {3}, \r\n"message": {4}, \r\n"notice": {5}, \r\n"created_at": {6}, \r\n"updated_at": {7}'.format(self.pk, self.user_id, self.member_id, self.notice, self.reply_id, self.message, self.created_at, self.updated_at)
