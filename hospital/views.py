from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from .models import Admin

# Create your views here.


def home(request):
    return render(request, "home.html")


@csrf_exempt
def signIn(request):
    if request.method == "POST":
        user_name = request.POST["userName"]
        if (Admin.objects.filter(user_name=user_name, password=request.POST["password"])).exists():
            return render(request, "home.html", {'user_name': user_name, 'logged_in': True})
        return render(request, "signIn.html", {'invalidCreds': True})
    return render(request, "signIn.html")


@csrf_exempt
def signUp(request):
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirmPassword"]
        user_name = request.POST["userName"]
        if (password == confirm_password and not Admin.objects.filter(user_name=user_name).exists()):
            Admin.objects.create(user_name=user_name, password=password)
            return redirect(signIn)
        return render(request, "signUp.html", {"invalidCreds": True})
    return render(request, "signUp.html")


def signOut(request):
    return render(request, "home.html", {'logged_in': False})
