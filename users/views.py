from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            return redirect('login')

    else:
        return render(request, '_login.html')

def logout(request):
    auth.logout(request)
    return redirect('index')