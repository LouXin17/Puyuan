import datetime
import json
import urllib.parse
import string
import random

from .models import *
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from django.core.mail import send_mail
from puyuan_sec import settings


@csrf_exempt
def register(request):  # 註冊帳戶
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            UserProfile.objects.create(
                account=data['email'], username=data['email'])
            dbinvite_code = ''.join(random.sample(string.digits, 6))
            userdb = UserProfile.objects.get(email=data['email'])
            userdb.password = data['password']
            userdb.invite_code = dbinvite_code
            userdb.set_password(data['password'])
            UserDefault.objects.create(user_id=userdb.pk)
            UserSetting.objects.create(user_id=userdb.pk)
            Diet.objects.create(user_id=userdb.pk)
            Medicalinfo.objects.create(user_id=userdb.pk)
            userdb.save()
            userinfo = {"status": "0"}
        except:
            userinfo = {"status": "1"}
    else:
        userinfo = {"status": "1"}
    return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
def verificationcodeSend(request):  # 發送驗證碼
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            userdb = UserProfile.objects.get(account=data['email'])
            if userdb.verified == True:
                userinfo = {"status": "1"}
                return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})
            else:
                userdb.verificationCode = ''.join(random.sample(
                    string.ascii_letters + string.digits, 6))
                userdb.email = data['email']
                userdb.save()
                send_mail(
                    "Info", "verification:" + ''.join(userdb.verificationCode),
                    settings.DEFAULT_FROM_EMAIL, [data['email']]
                )
                userinfo = {"status": "0"}
        except:
            userinfo["status"] = "1"
    else:
        userinfo["status"] = "1"
    return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
def verificationcodeCheck(request):  # 檢查驗證碼
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            userdb = UserProfile.objects.get(email=data['email'])
            if userdb.verified == True:
                userinfo = {"status": "0"}
            elif data['code'] == userdb.verificationCode:
                userdb.verified = True
                userdb.verificationCode = None
                userdb.save()
                userinfo = {"status": "0"}
        except:
            userinfo = {"status": "1"}
    else:
        userinfo = {"status": "1"}
    return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
def login(request):  # 登入
    if request.method == 'POST':
        request.session.flush()
        data = json.loads(request.body)
        user = auth.authenticate(
            request, username=data['account'],
            password=data['password']
        )
        if user is not None and user.is_active:
            auth.login(request, user)
            request.session['username'] = data['account']
            userdb = UserProfile.objects.get(
                account=request.session['username'])
            request.session.save()
            if userdb.verified == False:
                userinfo = {"status": "2"}
                return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})
            userinfo = {
                "status": "0",
                "token": request.session.session_key
            }
        else:
            userinfo = {"status": "1"}
    return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
def badge(request):  # 更新badge
    if request.method == 'PUT':
        try:
            sessiondb = {
                request.headers['Authorization'].split(' ')[0]:
                request.headers['Authorization'].split(' ')[1]
            }
            session_obj = Session.objects.get(pk=sessiondb['Bearer'])
            account = session_obj.get_decoded()['username']
            data = json.loads(request.body)
            userdb = UserProfile.objects.get(account=account)
            userdb.badge = data['badge']
            userdb.save()
            userinfo = {"status": "0"}
        except:
            userinfo = {"status": "1"}
    else:
        userinfo = {"status": "1"}
    return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
def forgotpassword(request):  # 忘記密碼
    if request.method == 'POST':
        takemail = (urllib.parse.unquote(
            request.body.decode('UTF-8')).split('&')[0].split('='))[1]
        try:
            userdb = UserProfile.objects.get(email=takemail)
            resetpassword = ''.join(random.sample(
                string.ascii_letters + string.digits, 20))  # 新密碼
            userdb.set_password(resetpassword)
            userdb.must_change_password = True
            userdb.save()
            send_mail(
                "Reset Password Info.", "重置密碼為:" + ''.join(random.sample(string.ascii_letters +
                                                                         string.digits, 20)), settings.DEFAULT_FROM_EMAIL, [takemail]
            )
            userinfo = {"status": "0"}
        except:
            userinfo = {"status": "1"}
    else:
        userinfo = {"status": "1"}
    return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})


@ csrf_exempt
def resetpassword(request):  # 重設密碼
    if request.method == 'POST':
        sessiondb = {
            request.headers['Authorization'].split(' ')[0]:
            request.headers['Authorization'].split(' ')[1]
        }
        session_obj = Session.objects.get(pk=sessiondb['Bearer'])
        account = session_obj.get_decoded()['username']
        try:
            data = json.loads(request.body)
            userdb = UserProfile.objects.get(account=account)
            userdb.set_password(data['password'])
            userdb.must_change_password = False
            userdb.save()
            userinfo = {"status": "0"}
        except:
            userinfo = {"status": "1"}
    else:
        userinfo = {"status": "1"}
    return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})


@ csrf_exempt
def checkregister(request):  # 註冊確認
    if request.method == 'GET':
        try:
            userdb = UserProfile.objects.filter(account=request.GET['account'])
            if userdb:
                userinfo = {"status": "1"}
            else:
                userinfo = {"status": "0"}
        except:
            userinfo = {"status": "1"}
    else:
        userinfo = {"status": "1"}
    return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})


@ csrf_exempt
def userset(request):  # 個人資訊設定(PATCH),個人資訊(GET)
    if request.method == 'PATCH':  # 個人資訊設定(POSTMAN*)
        try:
            sessiondb = {
                request.headers['Authorization'].split(' ')[0]:
                request.headers['Authorization'].split(' ')[1]
            }
            session_obj = Session.objects.get(pk=sessiondb['Bearer'])
            account = session_obj.get_decoded()['username']
            userdb = UserProfile.objects.get(account=account)
            data = json.loads(request.body)
            userdb.name = data['name']
            userdb.birthday = data['birthday']
            userdb.height = data['height']
            userdb.gender = data['gender']
            userdb.address = data['address']
            userdb.weight = data['weight']
            userdb.phone = data['phone']
            userdb.email = data['email']
            userdb.save()
            userinfo = {"status": "0"}
        except:
            userinfo = {"status": "1"}
        return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})
    elif request.method == 'GET':  # 個人資訊(GET)
        try:
            sessiondb = {
                request.headers['Authorization'].split(' ')[0]:
                request.headers['Authorization'].split(' ')[1]
            }
            session_obj = Session.objects.get(pk=sessiondb['Bearer'])
            account = session_obj.get_decoded()['username']
            userdb = UserProfile.objects.filter(account=account).get()
            defaultdb = UserDefault.objects.filter(user_id=userdb.pk).get()
            settingdb = UserSetting.objects.filter(user_id=userdb.pk).get()
            userinfo = {
                "status": "0",
                "user": {
                    "id": userdb.pk,
                    "name": userdb.name,
                    "account": userdb.account,
                    "email": userdb.email,
                    "phone": userdb.phone,
                    "fb_id": userdb.fb_id,
                    "status": userdb.status,
                    "group": userdb.group,
                    "birthday": userdb.birthday,
                    "height": userdb.height,
                    "weight": userdb.weight,
                    "gender": userdb.gender,
                    "address": userdb.address,
                    "unread_records": userdb.unread_records,
                    "verified": userdb.verified,
                    "privacy_policy": userdb.privacy_policy,
                    "must_change_password": userdb.must_change_password,
                    "fcm_id": userdb.fcm_id,
                    "badge": userdb.badge,
                    "login_times": userdb.login_times,
                    "created_at": userdb.created_at,
                    "updated_at": userdb.updated_at,
                    "default": {
                        "id": defaultdb.pk,
                        "user_id": defaultdb.user_id,
                        "sugar_delta_max": defaultdb.sugar_delta_max,
                        "sugar_delta_min": defaultdb.sugar_delta_min,
                        "sugar_morning_max": defaultdb.sugar_morning_max,
                        "sugar_morning_min": defaultdb.sugar_morning_min,
                        "sugar_evening_max": defaultdb.sugar_evening_max,
                        "sugar_evening_min": defaultdb.sugar_evening_min,
                        "sugar_before_max": defaultdb.sugar_before_max,
                        "sugar_before_min": defaultdb.sugar_before_min,
                        "sugar_after_max": defaultdb.sugar_after_max,
                        "sugar_after_min": defaultdb.sugar_after_min,
                        "systolic_max": defaultdb.systolic_max,
                        "systolic_min": defaultdb.systolic_min,
                        "diastolic_max": defaultdb.diastolic_max,
                        "diastolic_min": defaultdb.diastolic_min,
                        "pulse_max": defaultdb.pulse_max,
                        "pulse_min": defaultdb.pulse_min,
                        "weight_max": defaultdb.weight_max,
                        "weight_min": defaultdb.weight_min,
                        "bmi_max": defaultdb.bmi_max,
                        "bmi_min": defaultdb.bmi_min,
                        "body_fat_max": defaultdb.body_fat_max,
                        "body_fat_min": defaultdb.body_fat_min,
                        "created_at": defaultdb.created_at,
                        "updated_at": defaultdb.updated_at},
                    "setting": {
                        "id": settingdb.pk,
                        "user_id": settingdb.user_id,
                        "after_recording": settingdb.after_recording,
                        "no_recording_for_a_day": settingdb.no_recording_for_a_day,
                        "over_max_or_under_min": settingdb.over_max_or_under_min,
                        "after_meal": settingdb.after_meal,
                        "unit_of_sugar": settingdb.unit_of_sugar,
                        "unit_of_weight": settingdb.unit_of_weight,
                        "unit_of_height": settingdb.unit_of_height,
                        "created_at": settingdb.created_at,
                        "updated_at": settingdb.updated_at
                    }
                }
            }
        except:
            userinfo = {"status": "1"}
    else:
        userinfo = {"status": "1"}
    return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})


@ csrf_exempt
def defaultuser(request):  # 個人預設值
    if request.method == 'PATCH':
        try:
            sessiondb = {
                request.headers['Authorization'].split(' ')[0]:
                request.headers['Authorization'].split(' ')[1]
            }
            session_obj = Session.objects.get(pk=sessiondb['Bearer'])
            account = session_obj.get_decoded()['username']
            userdb = UserProfile.objects.get(account=account)
            defaultdb = UserDefault.objects.get(user_id=userdb.pk)
            data = json.loads(request.body)
            for i in range(len(data)):
                if list(data)[i] == 'sugar_delta_max':
                    defaultdb.sugar_delta_max = data['sugar_delta_max']
                elif list(data)[i] == 'sugar_delta_min':
                    defaultdb.sugar_delta_min = data['sugar_delta_min']
                elif list(data)[i] == 'sugar_morning_max':
                    defaultdb.sugar_morning_max = data['sugar_morning_max']
                elif list(data)[i] == 'sugar_morning_min':
                    defaultdb.sugar_morning_min = data['sugar_morning_min']
                elif list(data)[i] == 'sugar_evening_max':
                    defaultdb.sugar_evening_max = data['sugar_evening_max']
                elif list(data)[i] == 'sugar_evening_min':
                    defaultdb.sugar_evening_min = data['sugar_evening_min']
                elif list(data)[i] == 'sugar_before_max':
                    defaultdb.sugar_before_max = data['sugar_before_max']
                elif list(data)[i] == 'sugar_before_min':
                    defaultdb.sugar_before_min = data['sugar_before_min']
                elif list(data)[i] == 'sugar_after_max':
                    defaultdb.sugar_after_max = data['sugar_after_max']
                elif list(data)[i] == 'sugar_after_min':
                    defaultdb.sugar_after_min = data['sugar_after_min']
                elif list(data)[i] == 'systolic_max':
                    defaultdb.systolic_max = data['systolic_max']
                elif list(data)[i] == 'systolic_min':
                    defaultdb.systolic_min = data['systolic_min']
                elif list(data)[i] == 'diastolic_max':
                    defaultdb.diastolic_max = data['diastolic_max']
                elif list(data)[i] == 'diastolic_min':
                    defaultdb.diastolic_min = data['diastolic_min']
                elif list(data)[i] == 'pulse_max':
                    defaultdb.pulse_max = data['pulse_max']
                elif list(data)[i] == 'pulse_min':
                    defaultdb.pulse_min = data['pulse_min']
                elif list(data)[i] == 'weight_max':
                    defaultdb.weight_max = data['weight_max']
                elif list(data)[i] == 'weight_min':
                    defaultdb.weight_min = data['weight_min']
                elif list(data)[i] == 'bmi_max':
                    defaultdb.bmi_max = data['bmi_max']
                elif list(data)[i] == 'bmi_min':
                    defaultdb.bmi_min = data['bmi_min']
                elif list(data)[i] == 'body_fat_max':
                    defaultdb.body_fat_max = data['body_fat_max']
                elif list(data)[i] == 'body_fat_min':
                    defaultdb.body_fat_min = data['body_fat_min']
                else:
                    pass
            defaultdb.save()
            userinfo = {"status": "0"}
        except:
            userinfo = {"status": "1"}
    else:
        userinfo = {"status": "1"}
    return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})


@ csrf_exempt
def settinguser(request):  # 個人設定 <修for迴圈>
    userinfo = {}  # Json 格式輸出用
    if request.method == 'PATCH':
        try:
            sessiondb = {
                request.headers['Authorization'].split(' ')[0]:
                request.headers['Authorization'].split(' ')[1]
            }
            session_obj = Session.objects.get(pk=sessiondb['Bearer'])
            account = session_obj.get_decoded()['username']
            userdb = UserProfile.objects.get(account=account)
            settingdb = UserSetting.objects.get(user_id=userdb.pk)
            data = json.loads(request.body)
            for i in range(len(data)):
                if list(data)[i] == 'after_recording':
                    settingdb.after_recording = data['after_recording']
                elif list(data)[i] == 'no_recording_for_a_day':
                    settingdb.no_recording_for_a_day = data['no_recording_for_a_day']
                elif list(data)[i] == 'over_max_or_under_min':
                    settingdb.over_max_or_under_min = data['over_max_or_under_min']
                elif list(data)[i] == 'after_meal':
                    settingdb.after_meal = data['after_meal']
                elif list(data)[i] == 'unit_of_sugar':
                    settingdb.unit_of_sugar = data['unit_of_sugar']
                elif list(data)[i] == 'unit_of_weight':
                    settingdb.unit_of_weight = data['unit_of_weight']
                elif list(data)[i] == 'unit_of_height':
                    settingdb.unit_of_height = data['unit_of_height']
            settingdb.save()
            userinfo = {"status": "0"}
        except:
            userinfo = {"status": "1"}
    else:
        userinfo = {"status": "1"}
    return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})


@ csrf_exempt
def pressureblood(request):  # 上傳血壓測量結果
    if request.method == 'POST':
        try:
            sessiondb = {
                request.headers['Authorization'].split(' ')[0]:
                request.headers['Authorization'].split(' ')[1]
            }
            session_obj = Session.objects.get(pk=sessiondb['Bearer'])
            account = session_obj.get_decoded()['username']
            userdb = UserProfile.objects.get(account=account)
            data = json.loads(request.body)
            BloodPressure.objects.create(
                user_id=userdb.pk,
                systolic=data['systolic'],
                diastolic=data['diastolic'],
                pulse=data['pulse'],
                recorded_at=data['recorded_at']
            )
            userinfo = {"status": "0"}
        except:
            userinfo = {"status": "1"}
    else:
        userinfo = {"status": "1"}
    return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})


@ csrf_exempt
def weightuser(request):  # 上傳體重測量結果
    if request.method == 'POST':
        try:
            sessiondb = {
                request.headers['Authorization'].split(' ')[0]:
                request.headers['Authorization'].split(' ')[1]
            }
            session_obj = Session.objects.get(pk=sessiondb['Bearer'])
            account = session_obj.get_decoded()['username']
            userdb = UserProfile.objects.get(account=account)
            data = json.loads(request.body)
            Weight.objects.create(
                user_id=userdb.pk,
                weight=data['weight'],
                body_fat=data['body_fat'],
                bmi=data['bmi'],
                recorded_at=data['recorded_at']
            )
            userinfo = {"status": "0"}
        except:
            userinfo = {"status": "1"}
    else:
        userinfo = {"status": "1"}
    return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})


@ csrf_exempt
def sugarblood(request):  # 上傳血糖
    if request.method == 'POST':
        try:
            sessiondb = {
                request.headers['Authorization'].split(' ')[0]:
                request.headers['Authorization'].split(' ')[1]
            }
            session_obj = Session.objects.get(pk=sessiondb['Bearer'])
            account = session_obj.get_decoded()['username']
            userdb = UserProfile.objects.get(account=account)
            data = json.loads(request.body)
            BloodSuger.objects.create(
                user_id=userdb.pk,
                sugar=data['sugar'],
                timeperiod=data['timeperiod'],
                recorded_at=data['recorded_at']
            )
            userinfo = {"status": "0"}
        except:
            userinfo = {"status": "1"}
    else:
        userinfo = {"status": "1"}
    return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})


@ csrf_exempt
def codefriend(request):  # 獲取控糖團邀請碼
    if request.method == 'GET':
        try:
            sessiondb = {
                request.headers['Authorization'].split(' ')[0]:
                request.headers['Authorization'].split(' ')[1]
            }
            session_obj = Session.objects.get(pk=sessiondb['Bearer'])
            account = session_obj.get_decoded()['username']
            userdb = UserProfile.objects.get(account=account)
            userinfo = {
                "status": "0",
                "invite_code": userdb.invite_code
            }
        except:
            userinfo = {"status": "1"}
    else:
        userinfo = {"status": "1"}
    return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})


@ csrf_exempt
def a1c(request):  # 糖化血色素(送出、列出、刪除)
    if request.method == 'POST':    # 送糖化血色素
        try:
            sessiondb = {
                request.headers['Authorization'].split(' ')[0]:
                request.headers['Authorization'].split(' ')[1]
            }
            session_obj = Session.objects.get(pk=sessiondb['Bearer'])
            account = session_obj.get_decoded()['username']
            userdb = UserProfile.objects.get(account=account)
            data = json.loads(request.body)
            A1c.objects.create(
                user_id=userdb.pk,
                a1c=data['a1c'],
                recorded_at=data['recorded_at']
            )
            userinfo = {"status": "1"}
        except:
            userinfo = {"status": "1"}
        return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})
    elif request.method == 'GET':  # 糖化血色素
        try:
            sessiondb = {
                request.headers['Authorization'].split(' ')[0]:
                request.headers['Authorization'].split(' ')[1]
            }
            session_obj = Session.objects.get(pk=sessiondb['Bearer'])
            account = session_obj.get_decoded()['username']
            userdb = UserProfile.objects.get(account=account)
            listdb = A1c.objects.values().filter(user_id=userdb.pk)
            statusinfo = []
            for i in list(listdb):
                statusinfo.append({
                    'id': i['id'],
                    'user_id': int(i['user_id']),
                    'a1c': str(i['a1c']),
                    'recorded_at': i['recorded_at'].strftime("%Y-%m-%d %H:%M:%S"),
                    'created_at': i['created_at'].strftime("%Y-%m-%d %H:%M:%S"),
                    'updated_at': i['updated_at'].strftime("%Y-%m-%d %H:%M:%S")
                })
            userinfo = {
                "status": "0",
                "a1cs": statusinfo
            }
        except:
            userinfo = {"status": "1"}
        return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})
    elif request.method == 'DELETE':  # 刪除糖化血色素
        print("-------------------糖化血色素DELETE測試----------------------------")
        try:
            sessiondb = {
                request.headers['Authorization'].split(' ')[0]:
                request.headers['Authorization'].split(' ')[1]
            }
            session_obj = Session.objects.get(pk=sessiondb['Bearer'])
            account = session_obj.get_decoded()['username']
            userdb = UserProfile.objects.get(account=account)
            data = json.loads(request.body)
            ids = data['ids']
            for id in ids:
                try:
                    A1c.objects.get(pk=id).delete()
                except:
                    pass
            userinfo = {"status": "0"}
        except:
            userinfo = {"status": "1"}
    else:
        userinfo = {"status": "1"}
    return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})


@ csrf_exempt
def useddrug(request):  # 藥物資訊
    if request.method == 'POST':  # 上傳藥物資訊(POSTMAN*)
        try:
            sessiondb = {
                request.headers['Authorization'].split(' ')[0]:
                request.headers['Authorization'].split(' ')[1]
            }
            session_obj = Session.objects.get(pk=sessiondb['Bearer'])
            account = session_obj.get_decoded()['username']
            userdb = UserProfile.objects.get(account=account)
            data = json.loads(request.body)
            Drug.objects.create(
                user_id=userdb.pk,
                type=data['type'],
                name=data['name'],
                recorded_at=data['recorded_at']
            )
            userinfo = {"status": "0"}
        except:
            userinfo = {"status": "1"}
        return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})
    elif request.method == 'GET':  # 藥物資訊(POSTMAN*)
        try:
            sessiondb = {
                request.headers['Authorization'].split(' ')[0]:
                request.headers['Authorization'].split(' ')[1]
            }
            session_obj = Session.objects.get(pk=sessiondb['Bearer'])
            account = session_obj.get_decoded()['username']
            userdb = UserProfile.objects.get(account=account)
            statusinfo = []
            Druglistdb = Drug.objects.values().filter(user_id=userdb.pk)
            for i in list(Druglistdb):
                statusinfo.append({
                    "id": i['id'],
                    "user_id": i['user_id'],
                    "type": i['type'],
                    "name": i["name"],
                    "recorded_at": i['recorded_at'].strftime("%Y-%m-%d %H:%M:%S")
                })
            userinfo = {"status": "0", "drug_useds": statusinfo}
        except:
            userinfo = {"status": "1"}
        return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})
    elif request.method == 'DELETE':  # 刪除藥物資訊(POSTMAN*)
        try:
            sessiondb = {
                request.headers['Authorization'].split(' ')[0]:
                request.headers['Authorization'].split(' ')[1]
            }
            session_obj = Session.objects.get(pk=sessiondb['Bearer'])
            account = session_obj.get_decoded()['username']
            userdb = UserProfile.objects.get(account=account)
            data = json.loads(request.body)
            ids = data['ids']
            for id in ids:
                try:
                    Drug.objects.get(pk=id).delete()
                except:
                    pass
            userinfo = {"status": "0"}
        except:
            userinfo = {"status": "1"}
    else:
        userinfo = {"status": "1"}
    return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})


@ csrf_exempt
def medical(request):  # 就醫資訊
    if request.method == 'PATCH':   # 更新就醫資訊
        try:
            sessiondb = {
                request.headers['Authorization'].split(' ')[0]:
                request.headers['Authorization'].split(' ')[1]
            }
            session_obj = Session.objects.get(pk=sessiondb['Bearer'])
            account = session_obj.get_decoded()['username']
            userdb = UserProfile.objects.get(account=account)
            medicaldb = Medicalinfo.objects.get(user_id=userdb.pk)
            data = json.loads(request.body)
            medicaldb.diabetes_type = data['diabetes_type']
            medicaldb.oad = data['oad']
            medicaldb.insulin = data['insulin']
            medicaldb.anti_hypertensives = data['anti_hypertensives']
            medicaldb.save()
            userinfo = {"status": "0"}
        except:
            userinfo = {"status": "1"}
        return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})
    elif request.method == 'GET':  # 就醫資訊
        try:
            sessiondb = {
                request.headers['Authorization'].split(' ')[0]:
                request.headers['Authorization'].split(' ')[1]
            }
            session_obj = Session.objects.get(pk=sessiondb['Bearer'])
            account = session_obj.get_decoded()['username']
            userdb = UserProfile.objects.get(account=account)
            Medicaldb = Medicalinfo.objects.get(user_id=userdb.pk)
            userinfo = {
                "status": "0",
                "medical_info": {
                    "id": userdb.pk,
                    "user_id": Medicaldb.user_id,
                    "diabetes_type": Medicaldb.diabetes_type,
                    "oad": Medicaldb.oad,
                    "insulin": Medicaldb.insulin,
                    "anti_hypertensives": Medicaldb.anti_hypertensives
                }
            }
        except:
            userinfo = {"status": "1"}
    else:
        userinfo = {"status": "1"}
    return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})


@ csrf_exempt
def lastupload(request):  # 最後上傳時間
    if request.method == 'GET':
        try:
            sessiondb = {
                request.headers['Authorization'].split(' ')[0]:
                request.headers['Authorization'].split(' ')[1]
            }
            session_obj = Session.objects.get(pk=sessiondb['Bearer'])
            account = session_obj.get_decoded()['username']
            userdb = UserProfile.objects.get(account=account)
            bloodpressuredb = BloodPressure.objects.filter(
                user_id=userdb.pk).order_by('-recorded_at')[0].get()
            weightdb = Weight.objects.filter(
                user_id=userdb.pk).order_by('-recorded_at')[0].get()
            bloodsugardb = BloodSuger.objects.filter(
                user_id=userdb.pk).order_by('-recorded_at')[0].get()
            dietdb = Diet.objects.filter(
                user_id=userdb.pk).order_by('-recorded_at')[0].get()
            userinfo = {
                "status": "0",
                "last_upload": {
                    "blood_pressure": bloodpressuredb.recorded_at,
                    "weight": weightdb.recorded_at,
                    "blood_sugar": bloodsugardb.recorded_at,
                    "diet": dietdb.recorded_at
                }
            }
        except:
            userinfo = {"status": "1"}
    else:
        userinfo = {"status": "1"}
    return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})


@ csrf_exempt
def records(request):  # 上一筆紀錄資訊/刪除日記記錄
    if request.method == 'POST':
        try:
            sessiondb = {
                request.headers['Authorization'].split(' ')[0]:
                request.headers['Authorization'].split(' ')[1]
            }
            session_obj = Session.objects.get(pk=sessiondb['Bearer'])
            account = session_obj.get_decoded()['username']
            userdb = UserProfile.objects.get(account=account)
            data = json.loads(request.body)
            try:
                dbbloodpressure = BloodPressure.objects.filter(
                    user_id=userdb.pk).order_by("-pk")[0].get()
                bloodpressureinfo = {
                    "id": dbbloodpressure.id,
                    "user_id": dbbloodpressure.user_id,
                    "systolic": dbbloodpressure.systolic,
                    "diastolic": dbbloodpressure.diastolic,
                    "pulse": dbbloodpressure.pulse,
                    "recorded_at": dbbloodpressure.recorded_at
                }
            except:
                bloodpressureinfo = {}
            try:
                dbweightuser = Weight.objects.filter(
                    user_id=userdb.pk).order_by("-pk")[0].get()
                weightuserinfo = {
                    "id": dbweightuser.id,
                    "user_id": dbweightuser.user_id,
                    "weight": dbweightuser.weight,
                    "body_fat": dbweightuser.body_fat,
                    "bmi": dbweightuser.bmi,
                    "recorded_at": dbweightuser.recorded_at
                }
            except:
                weightuserinfo = {}
            try:
                dbsugarblood = BloodSuger.objects.filter(
                    user_id=userdb.pk).order_by("-pk")[0].get()
                dbsugarbloodinfo = {
                    "id": dbsugarblood.id,
                    "user_id": dbsugarblood.user_id,
                    "sugar": dbsugarblood.sugar,
                    "exercise": dbsugarblood.exercise,
                    "drug": dbsugarblood.drug,
                    "timeperiod": dbsugarblood.timeperiod,
                    "recorded_at": dbsugarblood.recorded_at
                }
            except:
                dbsugarbloodinfo = {}
            userinfo = {
                "status": "0",
                "blood_sugar": dbsugarbloodinfo,
                "blood_pressure": bloodpressureinfo,
                "weights": weightuserinfo
            }
        except:
            userinfo = {"status": "1"}
        return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})
    elif request.method == 'DELETE':  # 刪除日記記錄
        try:
            sessiondb = {
                request.headers['Authorization'].split(' ')[0]:
                request.headers['Authorization'].split(' ')[1]
            }
            session_obj = Session.objects.get(pk=sessiondb['Bearer'])
            account = session_obj.get_decoded()['username']
            userdb = UserProfile.objects.get(account=account)
            data = json.loads(request.body)
            for i in list(data.keys()):
                for id in data[i]:
                    if i == 'blood_pressures':
                        BloodPressure.objects.get(pk=id).delete()
                    elif i == 'weights':
                        Weight.objects.get(pk=id).delete()
                    elif i == 'blood_sugars':
                        BloodSuger.objects.get(pk=id).delete()
                    elif i == 'diets':
                        Diet.objects.get(pk=id).delete()
            userinfo = {"status": "0"}
        except:
            userinfo = {"status": "1"}
    else:
        userinfo = {"status": "1"}
    return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})


@ csrf_exempt
def diet(request):  # 飲食日記
    if request.method == 'POST':
        try:
            sessiondb = {
                request.headers['Authorization'].split(' ')[0]:
                request.headers['Authorization'].split(' ')[1]
            }
            session_obj = Session.objects.get(pk=sessiondb['Bearer'])
            account = session_obj.get_decoded()['username']
            userdb = UserProfile.objects.get(account=account)
            data = json.loads(request.body)
            Diet.objects.create(
                user_id=userdb.pk,
                description=data['description'],
                meal=data['meal'],
                tag=data['tag'],
                image=data['image'],
                lat=data['lat'],
                lng=data['lng'],
                recorded_at=data['recorded_at'],
            )
            userinfo = {"status": "0"}
        except:
            userinfo = {"status": "1"}
    else:
        userinfo = {"status": "1"}
    return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})


@ csrf_exempt
def diary(request):  # 日記列表資料
    if request.method == 'GET':
        sessiondb = {
            request.headers['Authorization'].split(' ')[0]:
            request.headers['Authorization'].split(' ')[1]
        }
        session_obj = Session.objects.get(pk=sessiondb['Bearer'])
        account = session_obj.get_decoded()['username']
        userdb = UserProfile.objects.get(account=account)
        try:
            outputinfo = []
            dbbloodpressure = BloodPressure.objects.values().filter(
                user_id=userdb.pk, recorded_at__contains=datetime.datetime.now().date())
            for i in list(dbbloodpressure):
                outputinfo.append({
                    "id": i["id"],
                    "user_id": i["user_id"],
                    "systolic": i["systolic"],
                    "diastolic": i["diastolic"],
                    "pulse": i["pulse"],
                    "recorded_at": i["recorded_at"].strftime("%Y-%m-%d %H:%M:%S"),
                    "type": "blood_pressure"
                })
            dbweight = Weight.objects.values().filter(
                user_id=userdb.pk, recorded_at__contains=datetime.datetime.now().date())
            for i in list(dbweight):
                outputinfo.append({
                    "id": i["id"],
                    "user_id": i["user_id"],
                    "weight": i["weight"],
                    "body_fat": i["body_fat"],
                    "bmi": i["bmi"],
                    "recorded_at": i["recorded_at"].strftime("%Y-%m-%d %H:%M:%S"),
                    "type": "weight"
                })
            dbsugarblood = BloodSuger.objects.values().filter(
                user_id=userdb.pk, recorded_at__contains=datetime.datetime.now().date())
            for i in list(dbsugarblood):
                outputinfo.append({
                    "id": i["id"],
                    "user_id": i["user_id"],
                    "sugar": i["sugar"],
                    "timeperiod": i["timeperiod"],
                    "recorded_at": i["recorded_at"].strftime("%Y-%m-%d %H:%M:%S"),
                    "type": "blood_sugar"
                })
            dietdb = Diet.objects.values().filter(
                user_id=userdb.pk, recorded_at__contains=datetime.datetime.now().date())
            for i in list(dietdb):
                outputinfo.append({
                    "id": i["id"],
                    "user_id": i["user_id"],
                    "description": i["description"],
                    "meal": i["meal"],
                    'tag': i['tag'],
                    "image": ["https://i.imgur.com/kAl270u.png"],
                    "location": {"lat": i["lat"], "lng": i["lng"]},
                    "recorded_at": i["recorded_at"].strftime("%Y-%m-%d %H:%M:%S"),
                    "type": "diet",
                    "reply": "19"
                })
            userinfo = {"status": "0",
                        "diary": outputinfo
                        }
        except:
            userinfo = {"status": "1"}
    else:
        userinfo = {"status": "1"}
    return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})


@ csrf_exempt
def friendsend(request):  # 送出控糖團邀請
    if request.method == 'POST':
        try:
            sessiondb = {
                request.headers['Authorization'].split(' ')[0]:
                request.headers['Authorization'].split(' ')[1]
            }
            session_obj = Session.objects.get(pk=sessiondb['Bearer'])
            account = session_obj.get_decoded()['username']
            userdb = UserProfile.objects.get(account=account)
            data = json.loads(request.body)
            if data['invite_code'] != userdb.invite_code:
                invitedb = UserProfile.objects.get(
                    invite_code=data['invite_code']
                )
                Friendlist.objects.create(
                    user_id=userdb.pk,
                    relation_id=invitedb.pk,
                    type=data['type'],
                    status="0"
                )
                userinfo = {"status": "0"}
        except:
            userinfo = {"status": "1"}
    else:
        userinfo = {"status": "1"}
    return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})


@ csrf_exempt
def friendrequests(request):  # 獲取控糖團邀請
    if request.method == 'GET':
        try:
            sessiondb = {
                request.headers['Authorization'].split(' ')[0]:
                request.headers['Authorization'].split(' ')[1]
            }
            session_obj = Session.objects.get(pk=sessiondb['Bearer'])
            account = session_obj.get_decoded()['_auth_user_id']
            statusdb = Friendlist.objects.get(relation_id=account, status=0)
            statusdb.read = True
            statusdb.save()
            statusinfo = []
            relationiddb = Friendlist.objects.values().filter(relation_id=account, status=0)
            for i in list(relationiddb):
                userdb = UserProfile.objects.get(pk=i["user_id"])
                statusinfo.append({
                    "id": i['id'],
                    "user_id": i['user_id'],
                    "relation_id": i['relation_id'],
                    "type": i['type'],
                    "status": i['status'],
                    "created_at": i['created_at'],
                    "updated_at": i['updated_at'],
                    "user": {
                        "id": userdb.pk,
                        "name": str(userdb.name),
                        "account": userdb.account,
                        "email": userdb.email,
                        "phone": userdb.phone,
                        "fb_id": userdb.fb_id,
                        "status": userdb.status,
                        "group": userdb.group,
                        "birthday": userdb.birthday,
                        "height": userdb.height,
                        "gender": userdb.gender,
                        "verified": userdb.verified,
                        "privacy_policy": userdb.privacy_policy,
                        "must_change_password": userdb.must_change_password,
                        "badge": userdb.badge,
                        "created_at": userdb.created_at,
                        "updated_at": userdb.updated_at
                    }
                })
            userinfo = {
                'status': '0',
                'requests': list(statusinfo)
            }
        except:
            userinfo = {"status": "1"}
    else:
        userinfo = {"status": "1"}
    return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})


@ csrf_exempt
def friendaccept(request, id):  # 接受控糖團邀請
    if request.method == 'GET':
        try:
            sessiondb = {
                request.headers['Authorization'].split(' ')[0]:
                request.headers['Authorization'].split(' ')[1]
            }
            session_obj = Session.objects.get(pk=sessiondb['Bearer'])
            account = session_obj.get_decoded()['_auth_user_id']
            acceptdb = Friendlist.objects.get(id=id, relation_id=account)
            if acceptdb.status == "0":
                acceptdb.status = "1"
                acceptdb.save()
            userinfo = {"status": "0"}
        except:
            userinfo = {"status": "1"}
    else:
        userinfo = {"status": "1"}
    return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})


@ csrf_exempt
def friendrefuse(request, id):  # 拒絕控糖團邀請
    if request.method == 'GET':
        try:
            sessiondb = {
                request.headers['Authorization'].split(' ')[0]:
                request.headers['Authorization'].split(' ')[1]
            }
            session_obj = Session.objects.get(pk=sessiondb['Bearer'])
            account = session_obj.get_decoded()['_auth_user_id']
            acceptdb = Friendlist.objects.get(id=id, relation_id=account)
            if acceptdb.status == "0":
                acceptdb.status = "2"
                acceptdb.save()
                userinfo = {"status": "0"}
        except:
            userinfo = {"status": "1"}
    else:
        userinfo = {"status": "1"}
    return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})


@ csrf_exempt
def friendremove(request, id):  # 刪除控糖團邀請
    if request.method == 'GET':
        try:
            sessiondb = {
                request.headers['Authorization'].split(' ')[0]:
                request.headers['Authorization'].split(' ')[1]
            }
            session_obj = Session.objects.get(pk=sessiondb['Bearer'])
            account = session_obj.get_decoded()['_auth_user_id']
            try:
                Friendlist.objects.get(
                    relation_id=id, user_id=account).delete()
            except:
                Friendlist.objects.get(
                    relation_id=id, user_id=account).delete()
            userinfo = {"status": "0"}
        except:
            userinfo = {"status": "1"}
    else:
        userinfo = {"status": "1"}
    return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})


@ csrf_exempt
def friendlist(request):  # 控糖團列表
    if request.method == 'GET':
        try:
            sessiondb = {
                request.headers['Authorization'].split(' ')[0]:
                request.headers['Authorization'].split(' ')[1]
            }
            session_obj = Session.objects.get(pk=sessiondb['Bearer'])
            account = session_obj.get_decoded()['_auth_user_id']
            statusinfo = []
            relationdb = Friendlist.objects.values().filter(relation_id=account, status=1)
            for i in list(relationdb):  # 使用者
                relationid = UserProfile.objects.get(pk=i["user_id"])
                statusinfo.append({
                    "id": relationid.pk,
                    "name": relationid.name,
                    "account": relationid.account,
                    "email": relationid.email,
                    "phone": relationid.phone,
                    "fb_id": relationid.fb_id,
                    "status": relationid.status,
                    "group": relationid.group,
                    "birthday": relationid.birthday,
                    "height": relationid.height,
                    "gender": relationid.gender,
                    "verified": relationid.verified,
                    "privacy_policy": relationid.privacy_policy,
                    "must_change_password": relationid.must_change_password,
                    "badge": relationid.badge,
                    "created_at": relationid.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at": relationid.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "relation_type": i['type']
                })
            userlistdb = Friendlist.objects.values().filter(user_id=account, status=1)
            for i in list(userlistdb):  # 受邀者
                userid = UserProfile.objects.get(pk=i["relation_id"])
                statusinfo.append({
                    "id": userid.pk,
                    "name": userid.name,
                    "account": userid.account,
                    "email": userid.email,
                    "phone": userid.phone,
                    "fb_id": userid.fb_id,
                    "status": userid.status,
                    "group": userid.group,
                    "birthday": userid.birthday,
                    "height": userid.height,
                    "gender": userid.gender,
                    "verified": userid.verified,
                    "privacy_policy": userid.privacy_policy,
                    "must_change_password": userid.must_change_password,
                    "badge": userid.badge,
                    "created_at": userid.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at": userid.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "relation_type": i['type']
                })
            userinfo = {
                'status': '0',
                'friends': list(statusinfo)
            }
        except:
            userinfo = {"status": "1"}
    else:
        userinfo = {"status": "1"}
    return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})


@ csrf_exempt
def friendresults(request):  # 控糖團結果
    if request.method == 'GET':
        try:
            sessiondb = {
                request.headers['Authorization'].split(' ')[0]:
                request.headers['Authorization'].split(' ')[1]
            }
            session_obj = Session.objects.get(pk=sessiondb['Bearer'])
            account = session_obj.get_decoded()['_auth_user_id']
            friendresultsdb = Friendlist.objects.values().filter(user_id=account)
            statusinfo = []
            for i in list(friendresultsdb):
                relationdb = UserProfile.objects.get(pk=i["relation_id"])
                statusinfo.append({
                    "id": i['id'],
                    "user_id": int(i['user_id']),
                    "relation_id": int(i['relation_id']),
                    "type": i['type'],
                    "status":  int(i['status']),
                    "read": i['read'],
                    "created_at": i['created_at'].strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at": i['updated_at'].strftime("%Y-%m-%d %H:%M:%S"),
                    "relation": {
                        "id": relationdb.pk,
                        "name": relationdb.name,
                        "account": relationdb.account,
                        "email": relationdb.email,
                        "phone": relationdb.phone,
                        "fb_id": relationdb.fb_id,
                        "status": relationdb.status,
                        "group": relationdb.group,
                        "birthday": relationdb.birthday,
                        "height": relationdb.height,
                        "gender": relationdb.gender,
                        "unread_records": "[0,0,0]",
                        "verified": relationdb.verified,
                        "privacy_policy": relationdb.privacy_policy,
                        "must_change_password": relationdb.must_change_password,
                        "badge": relationdb.badge,
                        "created_at": relationdb.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                        "updated_at": relationdb.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                    }
                })
                userinfo = {'status': '0',
                            "results": list(statusinfo)
                            }
        except:
            userinfo = {"status": "1"}
    else:
        userinfo = {"status": "1"}
    return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})


@ csrf_exempt
def usercare(request):  # 發送關懷諮詢/獲取關懷資訊
    if request.method == 'POST':  # 發送關懷諮詢
        try:
            sessiondb = {
                request.headers['Authorization'].split(' ')[0]:
                request.headers['Authorization'].split(' ')[1]
            }
            session_obj = Session.objects.get(pk=sessiondb['Bearer'])
            account = session_obj.get_decoded()['_auth_user_id']
            friendcount = Friendlist.objects.filter(
                user_id=account, status="1").count()
            data = json.loads(request.body)
            if friendcount == 0:
                Care.objects.create(user_id=account, message=data['message'])
            else:
                for i in range(friendcount):
                    userdb = Friendlist.objects.filter(
                        user_id=account)[i].get()
                    Care.objects.create(
                        user_id=userdb.user_id,
                        member_id=userdb.type,
                        reply_id=userdb.relation_id,
                        message=data['message']
                    )
            userinfo = {"status": "0"}
        except:
            userinfo = {"status": "1"}
        return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})
    elif request.method == 'GET':  # 獲取關懷資訊
        sessiondb = {
            request.headers['Authorization'].split(' ')[0]:
            request.headers['Authorization'].split(' ')[1]
        }
        session_obj = Session.objects.get(pk=sessiondb['Bearer'])
        account = session_obj.get_decoded()['_auth_user_id']
        try:
            count = Care.objects.filter(reply_id=account).count()
            lastinfo = []
            for i in range(count):
                caredb = Care.objects.values().filter(reply_id=account)[i]
                lastinfo = lastinfo+list(caredb)
            userinfo = {'status': '0',
                        'cares': lastinfo
                        }
        except:
            userinfo = {"status": "1"}
    else:
        userinfo = {"status": "1"}
    return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})


@ csrf_exempt
def notification(request):  # 親友團通知
    if request.method == 'POST':
        try:
            sessiondb = {
                request.headers['Authorization'].split(' ')[0]:
                request.headers['Authorization'].split(' ')[1]
            }
            session_obj = Session.objects.get(pk=sessiondb['Bearer'])
            account = session_obj.get_decoded()['_auth_user_id']
            data = json.loads(request.body)
            Care.objects.create(notice=data['message'], user_id=account.pk)
            userinfo = {"status": "0"}
        except:
            userinfo = {"status": "1"}
    else:
        userinfo = {"status": "1"}
    return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})


@ csrf_exempt
def familyremove(request):  # 刪除更多好友
    if request.method == 'DELETE':
        try:
            sessiondb = {
                request.headers['Authorization'].split(' ')[0]:
                request.headers['Authorization'].split(' ')[1]
            }
            session_obj = Session.objects.get(pk=sessiondb['Bearer'])
            account = session_obj.get_decoded()['_auth_user_id']
            data = json.loads(request.body)
            try:
                Friendlist.objects.get(
                    user_id=data['ids[]'], relation_id=account).delete()
            except:
                Friendlist.objects.get(
                    user_id=account, relation_id=data['ids[]']).delete()
            userinfo = {"status": "0"}
        except:
            userinfo = {"status": "1"}
    else:
        userinfo = {"status": "1"}
    return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})


@ csrf_exempt
def share(request):  # 分享
    if request.method == 'GET':
        userinfo = {"status": "0"}
    return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})


@ csrf_exempt
def shareinfo(request, id):  # 查看分享
    if request.method == 'GET':
        userinfo = {"status": "0"}
    return JsonResponse(userinfo, safe=False, json_dumps_params={'ensure_ascii': False})
