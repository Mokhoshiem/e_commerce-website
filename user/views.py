from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'تم بنجاح إنشاء الحساب')
            return redirect('store:login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form':form , 'title':'تسجيل حساب'})


