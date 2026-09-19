from django.shortcuts import render, redirect
from .models import Donor, Patient as patientModel, BloodRequest, BloodStock
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def home(request):
     stocks = BloodStock.objects.all()
     return render(request, 'main/home.html', {'stocks': stocks})


def donor(request):
    if request.method == 'POST':
        name = request.POST['name']
        age = request.POST['age']
        blood_group = request.POST['blood_group']
        phone = request.POST['phone']
        email = request.POST['email']
        units=request.POST.get('units', 1) 

        Donor.objects.create(
            name=name,
            age=age,
            blood_group=blood_group,
            phone=phone,
            email=email,
            units=units
        )
        stock = BloodStock.objects.get(blood_group=blood_group)
        stock.units += int(units)
        stock.save()

        return redirect('donor')

    return render(request, 'main/donor.html')

def patient(request):
    if request.method == 'POST':
        name = request.POST['name']
        age = request.POST['age']
        phone = request.POST['phone']

        patientModel.objects.create(
            name=name,
            age=age,
            phone=phone
        )

        return redirect('patient')

    return render(request, 'main/patient.html')

def blood_search(request):
    donors = None
    stock = None
    searched = False

    if request.GET.get('blood_group'):
        blood_group = request.GET.get('blood_group')

        donors = Donor.objects.filter(
            blood_group=blood_group
        )

        stock = BloodStock.objects.get(
            blood_group=blood_group
        )

        searched = True

    return render(
        request,
        'main/blood_search.html',
        {
            'donors': donors,
            'stock': stock,
            'searched': searched
        }
    )
def blood_request(request):
    if request.method == 'POST':
        patient_id = request.POST['patient_id']
        patient_name = request.POST['patient_name']
        blood_group = request.POST['blood_group']
        units = int(request.POST['units'])
        hospital = request.POST['hospital']

        stock = BloodStock.objects.get(blood_group=blood_group)

        if stock.units >= units:
            BloodRequest.objects.create(
                patient_id=patient_id,
                patient_name=patient_name,
                blood_group=blood_group,
                units=units,
                hospital=hospital,
                status='Pending'
            )

            messages.success(
                request,
                'Blood request submitted successfully. Waiting for admin approval.'
            )

            return redirect('blood_request')

        else:
            messages.error(
                request,
                f"Only {stock.units} units of {blood_group} blood are available."
            )

    return render(request, 'main/blood_request.html')

    
    

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/admin/')

        return render(request, 'main/login.html', {
            'error': 'Invalid username or password'
        })

    return render(request, 'main/login.html')


