import random
import string
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from .models import Admin, Department, Doctor, Medicine, OPTicket

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
    doctors = Doctor.objects.all()
    departments = Department.objects.all()
    if (authenticate(request)):
        params = {"logged_in": True, "doctors": doctors}
        return render(request, "doctors.html", params)
    return render(request, "doctors.html", {"logged_in": False, "doctors": doctors, "departments": departments})


def departments(request):
    departments = Department.objects.all()
    if (authenticate(request)):
        params = {"logged_in": True, "departments": departments}
        return render(request, "departments.html", params)
    return render(request, "departments.html",  {"logged_in": False, "departments": departments})


@csrf_exempt
def addDoctor(request):
    if (authenticate(request)):
        if request.method == "POST":
            name = request.POST["name"]
            department = request.POST["department"]
            start_time = request.POST["start_time"]
            end_time = request.POST["end_time"]
            active_days = request.POST.getlist("active_days")
            consultation_charge = request.POST["consultation_charge"]
            try:
                Doctor.objects.create(name=name, op_start_time=start_time, op_end_time=end_time,
                                      active_days=active_days, consultation_charge=consultation_charge, department_id=department)
            except Exception as e:
                print(e)
            return redirect(doctors)
        departments = Department.objects.all()
        params = {"logged_in": True, "departments": departments}
        return render(request, "addDoctor.html", params)
    return redirect(signIn)


@csrf_exempt
def addDepartment(request):
    if (authenticate(request)):
        if request.method == "POST":
            name = request.POST["name"]
            description = request.POST["description"]
            if (Department.objects.filter(name=name).exists()):
                return render(request, "addDepartment.html", {"logged_in": True, "duplicate_name": True})
            Department.objects.create(name=name, description=description)
            return redirect(departments)
        params = {"logged_in": True}
        return render(request, "addDepartment.html", params)
    return redirect(signIn)


@csrf_exempt
def bookTicket(request):
    if request.method == "POST":
        name = request.POST["name"]
        age = request.POST["age"]
        place = request.POST["place"]
        number = request.POST["number"]
        date = request.POST["date"]
        doctor = request.POST["doctor"]
        ticket = OPTicket.objects.create(
            name=name, age=age, place=place, number=number, date=date, doctor_id=doctor)
        token = ticket.id
        return render(request, "home.html", {"logged_in": False, "token": token})
    departments = Department.objects.all()
    doctors = Doctor.objects.all()
    return render(request, 'bookTicket.html', {"logged_in":authenticate(request),"departments": departments, "doctors": doctors})


@csrf_exempt
def addMedicine(request):
    if request.method == "POST":
        name = request.POST["name"]
        price = request.POST["price"]
        available_count = request.POST["available_count"]
        description = request.POST["description"]
        Medicine.objects.create(name=name, price=price, available_count=available_count, description=description)
        return redirect(medicines)
    return render(request, 'addMedicine.html', {})


@csrf_exempt
def medicines(request):
    medicines = Medicine.objects.all()
    if (authenticate(request)):
        params = {"logged_in": True, "medicines": medicines}
        return render(request, "pharmacy.html", params)
    return render(request, "pharmacy.html", {"logged_in": False, "medicines": medicines})
