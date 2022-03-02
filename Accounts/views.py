from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import *
import random
from django.contrib.auth import logout
from django.core.mail import BadHeaderError, send_mail
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.


def register(request):
    if request.method == 'POST':
        fname = request.POST.get('fname','')
        lname = request.POST.get('lname','')
        email = request.POST.get('email','')
        password1 = request.POST.get('password1','')
        password2 = request.POST.get('password2','')
        block = request.POST.get('block','')
        floor = request.POST.get('floor','')
        room = request.POST.get('room','')
        gender = request.POST.get('gender','')
        phone = request.POST.get('phone','')
        address = block + "-"+ floor + "-" + room
        if password1 == password2:
            password = password1

            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already taken.')
                return redirect('register')
            else:
                user = User.objects.create_user(username=email,
                                                first_name=fname, last_name=lname, password=password, email=email)
                user.save()
                customer = Customer.objects.create(
                    customer=user, address=address, phone=phone, gender=gender)
                customer.save()
                subject = "Welcome to OBCafe"
                message="Hello "+ fname + " " + lname + "\nWelcome To your cafeteria.\n now you can place order, if you need also we have delivery service.\n\nVisit: https://obcafeteria.herokuapp.com, to access our menu."

                send_mail(subject, message +"\n\n Abdellah Kmail (project manager)",settings.EMAIL_HOST_USER, [email],fail_silently=True)
                return redirect('login')
                
        else:
            messages.info(request, 'Password not matching...')
            return redirect('register')

    else:
        return render(request, 'customer/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('email','')
        password = request.POST.get('password','')

        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            
            if user.is_staff:
                try:
                    emp = Employ.objects.get(employe=user)
                    if emp.emp_type == "chef":
                        return redirect('chef')
                    elif  emp.emp_type == "waiter":
                        return redirect('waiter')
                    elif  emp.emp_type == "casher":
                        return redirect('casher')
                    elif  emp.emp_type == "supplier":
                        return redirect('supplier')
                except:
                    emp= None
                
                mana = Manager.objects.get(manager=user)
                if mana:
                    return redirect('manager')
            else:
                return redirect('/')
        else:
            messages.info(request, 'Incorrect password or email! ')
            return redirect('login')

    else:
        return render(request, 'home/loging.html')


def log_out(request):
    logout(request)
    return redirect("/") 


def forgotp(request):
    if request.method == "POST":
        email= request.POST.get("email",'')
        if email:
            OTP = str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) +str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))
            user = User.objects.get(email=email)
            if user:
                user.password = OTP
                message =  "Use this password to login to your account.\n \t" + OTP
                send_mail('Reset Password',message,settings.EMAIL_HOST_USER,[email],fail_silently=True,)
                user.save()
            return redirect('/')
    return render(request, "home/forgotp.html")
        
def comment(request):
    if request.method == "POST":
        
        subject = "Customer comment"
        message = request.POST.get('message', '')
        from_email = request.POST.get('from_email', '')
        if subject and message and from_email:
            try:
                send_mail(subject, message, from_email, [settings.EMAIL_HOST_USER])

            except BadHeaderError:
                return HttpResponse('<h1 style="color:red">Invalid header found.</h1>')

            return redirect('/')
        else:
            
            return HttpResponse('<h1 style="color:red" >Make sure all fields are entered and valid.</h1>')
    else:
        return render(request,"customer/comment.html")
