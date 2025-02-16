import json
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
import requests
from django.contrib.auth import logout
from requests.auth import HTTPBasicAuth
# from thee_app.credentials import LipanaMpesaPpassword, MpesaAccessToken
from .models import Appointment
from .forms import ProofOfPaymentForm
#restrict users to login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect



def home_page(request):
    context = {}
    return render(request, "index.html", context)


def login_page(request):
    """Display the appointment page"""
    return render(request, "accounts/login.html")

@login_required
def my_appointments(request):
    # Filter appointments for the logged-in user alone
    user_appointments = Appointment.objects.filter(user=request.user)
    return render(request, 'my_appointments.html', {'appointments': user_appointments})

@login_required(login_url='thee_app:login_page')
def appointment_show(request):
    """Display the departments page"""
    return render(request, "appointment_show.html")

def register(request):
    """Display the reg page"""
    return render(request, "accounts/register.html")

def logout_user(request):
    """Logs out the user and redirects to login page."""
    logout(request)
    return redirect('thee_app:login_page')  # Redirect user after logout

# for updating the status of appointment
@login_required
def mark_appointment_done(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)

    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to perform this action.")

    if request.method == 'POST':
        # Toggle the status
        appointment.status = 'done' if request.POST.get('status') == 'done' else 'pending'
        appointment.save()

    return redirect('thee_app:appointment_show')




@login_required(login_url='thee_app:login_page')
def appointment(request):
    """ Appointment booking """
    # Check if its a post method
    if request.method == 'POST':
        # Create variable to pick the input fields
        appointments = Appointment(
            # list the input fields here
            name = request.POST['name'],
            email = request.POST['email'],
            phone = request.POST['phone'],
            date = request.POST['date'],
            branch = request.POST['branch'],
            department = request.POST['department'],
            doctor = request.POST['doctor'],
            message = request.POST['message'],
            user=request.user
        )
        # save the variable
        appointments.save()
        # redirect to a page
        return redirect('thee_app:pay')
    else:
        return render(request, 'appointment.html')



@login_required(login_url='thee_app:login_page')
def appointment_update(request, appointment_id):
    """ Update the appointments """
    # Fetch the appointment
    appointment = get_object_or_404(Appointment, id=appointment_id)
    print(f"Appointment: {appointment}")  # Debugging log

    if request.method == 'POST':
        print(f"POST Data: {request.POST}")  # Debugging log
        # Update the fields with POST data
        appointment.name = request.POST.get('name')
        appointment.email = request.POST.get('email')
        appointment.phone = request.POST.get('phone')
        appointment.date = request.POST.get('date')
        appointment.branch = request.POST.GET('branch')
        appointment.doctor = request.POST.get('doctor')
        appointment.department = request.POST.get('department')
        appointment.message = request.POST.get('message')
        # Save the updated appointment
        appointment.save()

        print(f"Updated Appointment: {appointment}")  # Debugging log
        return redirect("thee_app:my_appointments")

    # Pass appointment to the template
    context = {'appointment': appointment}
    return render(request, "appointment_update.html", context)



@login_required(login_url='thee_app:login_page')
def appointment_show(request):
    """ Retrieve/fetch all appointments """
    appointments = Appointment.objects.all()
    context = {
        'appointments':appointments
        }
    return render(request, 'appointment_show.html', context)



def appointment_delete(request, id):
    """ Deleting """
    appointment = Appointment.objects.get(id=id) # fetch the particular appointment by its ID
    appointment.delete() # actual action of deleting
    return redirect("thee_app:appointment_show") # just remain on the same page



def login_page(request):
    """Login view"""
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You are now logged in!")
            return redirect('thee_app:appointment')  # Redirect to the homepage or dashboard
        else:
            messages.error(request, "Invalid login credentials")
    
    return render(request, 'accounts/login.html')


def register(request):
    """Registration view"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            try:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                messages.success(request, "Account created successfully.")
                return redirect('thee_app:login_page')  # Redirect to the login page after successful registration
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
        else:
            messages.error(request, "Passwords do not match.")
    
    return render(request, 'accounts/register.html')


# Adding the mpesa functions

def pay(request):
    """ Renders the form to pay """
    storage = messages.get_messages(request)
    for _ in storage: 
        pass
    return render(request, 'pay.html')



# Generate the ID of the transaction
def token(request):
    """ Generates the ID of the transaction """
    consumer_key = 'EJwbmTGr391sTpntpVLLRZzv52oxwVSxXfa8qeaGKL4XxzLw'
    consumer_secret = 'UBIqynIJbG1tete0bDtMFnbhOAh0RUnfwqRFGfQIzl1ya7BqB21dWMFAQb2PzkKM'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth = HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})


from django.shortcuts import render


def stk(request):
    """ Sends the stk push prompt """
    if request.method == "POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        stk_request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://yourdomain.com/callback-url/",
            "AccountReference": "MiltonDNets",
            "TransactionDesc": "Pay for IT"
        }

        try:
            response = requests.post(api_url, json=stk_request, headers=headers)
            response_data = response.json()

            if response.status_code == 200 and "ResponseCode" in response_data:
                messages.success(request, "Payment request sent successfully! Please check your phone.")
                return redirect("thee_app:pay")
            else:
                error_message = response_data.get("errorMessage", "An error occurred.")
                messages.error(request, f"Payment failed: {error_message}")
                return redirect("thee_app:pay")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {e}")
            return redirect("thee_app:pay")
    return redirect("thee_app:pay")


def upload_proof_of_payment(request, appointment_id):
    # Fetch the appointment
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        form = ProofOfPaymentForm(request.POST, request.FILES, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('thee_app:my_appointments')  # Redirect after successful upload
    else:
        form = ProofOfPaymentForm(instance=appointment)

    # Render the upload proof page
    return render(request, 'upload_proof.html', {
        'form': form,
        'appointment': appointment
    })

@login_required
def my_appointments(request):
    # Fetch appointments for the logged-in user
    appointments = Appointment.objects.filter(user=request.user).order_by('-date')
    return render(request, 'my_appointments.html', {'appointments': appointments})

