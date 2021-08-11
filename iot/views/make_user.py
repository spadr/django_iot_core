from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponseBadRequest

import secrets


def signupfunc(request):
    if request.method == "POST":#POSTの処理
        email = request.POST['emailadress']
        psw = request.POST['password']

        #ユーザー登録
        try :
            user = User.objects.create_user(email, email, psw)
        except :
            #ユーザー登録NG
            return render(request, 'signup.html', {'error' : 'このユーザーはすでに登録されています。'})
        
        #Accesskeyの生成
        try:
            user.is_active = False
            user.save()
        except :
            #ダメなとき
            return render(request, 'signup.html', {'error' : '登録できません。'})
        
        #認証メールの作成
        try:
            from_email = 'EMAIL_ADDRESS'
            recipient_list = [email]
            subject = 'Activate Your Account'#メールタイトル
            current_site = get_current_site(request)
            domain = current_site.domain
            #内容はtemplateから
            context = render_to_string('account_activation_email.html',
            {
                'protocol': request.scheme,
                'domain': domain,
                'token': dumps(user.pk),
                'user': user,
            })
        except :
            #ダメなとき
            return render(request, 'signup.html', {'error' : 'メール関係の変数が不正です。'})
        
        #認証メールの作成
        try:
            send_mail(subject, context, from_email, recipient_list)
            return render(request, 'signup.html', {'error' : '登録したメールアドレスへ認証メールを送信しました。URLをクリックして、アカウントを有効化してください。' , 'error2':'Please confirm your email address to complete the registration'})
        except :
            #ダメなとき
            return render(request, 'signup.html', {'error' : 'ユーザーの登録は完了しましたが、認証メールを送信に失敗しました。' , 'error2':'入力したメールアドレスを再度ご確認の上、管理者にお問い合わせください。'})
    
    return render(request, 'signup.html')#GETのレスポンス



def completefunc(request, **kwargs):
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)#認証メールの期限
    token = kwargs.get('token')

    #認証メールの期限チェック
    try:
        user_pk = loads(token, max_age=timeout_seconds)
    except SignatureExpired:
        #ダメなとき
        return HttpResponseBadRequest()
    except BadSignature:
        #ダメなとき
        return HttpResponseBadRequest()
    else:
        #認証メールの期限OK
        
        #ユーザーを有効化
        try:
            user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            return HttpResponseBadRequest()
        else:
            user.is_active = True
            user.save()
            return redirect('meme')
