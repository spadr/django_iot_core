from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout



def loginfunc(request):
    if request.method == "POST":
        #ユーザー認証
        email = request.POST['emailadress']
        psw = request.POST['password']
        user = authenticate(request, username=email, password=psw)

        if user is not None:
            #ユーザー認証OK
            login(request, user)
            return redirect('read')#正常終了のレスポンス
        else:
            #ユーザー認証NG
            return render(request, 'login.html', {'context' : 'メールアドレスまたはパスワードが間違っています。'})
    
    return render(request, 'login.html')#GETのレスポンス


def logoutfunc(request):
    logout(request)
    return redirect('meme')

