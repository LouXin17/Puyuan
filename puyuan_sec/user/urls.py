from django.urls import path
from user import views
urlpatterns = [
    path('register/', views.register),  # 1.註冊
    path('auth/', views.login),  # 2.登入
    path('verification/send/', views.verificationcodeSend),  # 3.發送驗證碼
    path('verification/check/', views.verificationcodeCheck),  # 4.檢查驗證碼
    path('user/badge/', views.badge),  # 39.更新badge
    path('password/forgot/', views.forgotpassword),  # 5.忘記密碼
    path('password/reset/', views.resetpassword),  # 6.重設密碼
    path('register/check/', views.checkregister),  # 38.註冊確認
    path('user/', views.userset),  # 7.個人資訊設定(PATCH)、12.個人資訊(GET)
    path('user/default/', views.defaultuser),  # 11.個人預設值
    path('user/setting/', views.settinguser),  # 35.個人設定
    path('user/blood/pressure/', views.pressureblood),  # 8.上傳血壓測量結果
    path('user/weight/', views.weightuser),  # 9.上傳體重測量結果
    path('user/blood/sugar/', views.sugarblood),  # 10.上傳血糖
    path('friend/code/', views.codefriend),  # 16.獲取控糖團邀請碼
    path('user/a1c/', views.a1c),  # 32.糖化血色素(GET)、33.送糖化血色素(POST)、34.刪除糖化血色素
    path('user/drug-used/', views.useddrug),  # 41.藥物資訊、42.上傳藥物資訊、43.刪除藥物資訊
    path('user/medical/', views.medical),  # 30.就醫資訊、31.更新就醫資訊
    path('user/last-upload/', views.lastupload),  # 25.最後上傳時間
    path('user/records/', views.records),  # 44.上一筆紀錄資訊
    path('user/diet/', views.diet),  # 15.飲食日記
    path('user/diary/', views.diary),  # 14.日記列表資料、40.刪除日記資訊
    path('friend/send/', views.friendsend),  # 19.送出控糖團邀請
    path('friend/requests/', views.friendrequests),  # 18.獲取控糖團邀請
    path('friend/<id>/accept/', views.friendaccept),  # 20.接受控糖團邀請
    path('friend/<id>/refuse/', views.friendrefuse),  # 21.拒絕控糖團邀請
    path('friend/<id>/remove/', views.friendremove),  # 22.刪除控糖團邀請
    path('friend/list/', views.friendlist),  # 17.控糖團列表
    path('friend/results/', views.friendresults),  # 26.控糖團結果
    path('user/care/', views.usercare),  # 28. 發送關懷諮詢、27.獲取關懷諮詢
    path('notification/', views.notification),  # 36.親友團通知
    path('friend/remove/', views.familyremove),  # 37.刪除更多好友
    path('share/', views.share),  # 23.分享
    path('share/<id>', views.shareinfo),  # 24.查看分享
]
