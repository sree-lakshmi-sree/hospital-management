import random
import string
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from .models import Admin, Doctor

# Create your views here.


def authenticate(request):
    token = request.session.get('token', '')
    return Admin.objects.filter(token=token).exists()


def create_random_token():
    characters = string.ascii_lowercase.join(
        string.punctuation).join(string.digits)
    return ''.join(random.choice(characters) for i in range(15))


def home(request):
    params = {"logged_in": authenticate(request)}
    return render(request, "home.html", params)


@csrf_exempt
def signIn(request):
    if request.method == "POST":
        user_name = request.POST["userName"]
        password = request.POST["password"]
        currentUser = (Admin.objects.filter(
            user_name=user_name, password=password))
        if currentUser.exists():
            token = create_random_token()
            currentUser.update(token=token)
            request.session['token'] = token
            return render(request, "home.html", {'logged_in': True})
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
    token = request.session.get('token', '')
    user = Admin.objects.filter(token=token)
    if user.exists():
        user.update(token=None)
    request.session.delete('token')
    return render(request, "home.html", {'logged_in': False})


def doctors(request):
    if (authenticate(request)):
        doctors = Doctor.objects
        params = {"logged_in": True, "doctors": doctors}
        return render(request, "doctors.html", params)
    return redirect(signIn)


def addDoctor(request):
    if (authenticate(request)):
        params = {"logged_in": True}
        return render(request, "addDoctor.html", params)
    return redirect(signIn)
