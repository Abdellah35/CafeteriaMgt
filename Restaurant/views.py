from django.shortcuts import render, redirect
import random
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from .process import html_to_pdf 
from django.template.loader import render_to_string
from django.core.mail import BadHeaderError, send_mail
from django.conf import settings


def GeneratePdf(request):
        Dicc = {}
        Ord = {}
        idd = request.POST.get('idd','')
        order = Order.objects.get(pk= idd)
        orde = order.item.split(", ")
        price = 0.00
        delp = 0.00
        etem=''
        num = 0
        for od in orde:
            if od != "":
                itm = od.split("*")
                pris = Meal.objects.get(name=itm[0])
                price += int(pris.price) * int(itm[1])
                Ord[itm[0]] = {str(itm[1]): pris.price}
                etem += itm[0] + ', '
                num += int(itm[1]) 


        print(price)
        if order.delivery:
            delp= 5
        user = User.objects.get(username = order.customer)

        name = user.first_name +" "+ user.last_name
        address = order.address
        email = user.email
        No = str(random.randint(1,9)) + str(random.randint(1,9))+str(random.randint(1,9))+str(random.randint(1,9))+str(random.randint(1,9))+str(random.randint(1,9))+str(random.randint(1,9))
        date = order.date_created
        total = price*(0.02) + price + delp
        order.save()
        open('templates/receipt.html', "w").write(render_to_string('employee/billpdf.html',{'genorder': Dicc, "order":Ord,"subtot": price ,
            "del":delp,"total":total,'No': No,"adr":address,"email":email,"name":name,"date":date}))

        # Converting the HTML template into a PDF file
        pdf = html_to_pdf('receipt.html')
        #Send receipt email for the customer
        message= "Item: {}\nNumber of items: {}\nTotal: {} Birr.\n\n\tThank you for using our service.\n\nvisite: www.obcafeteria.herokuapp.com".format(etem,num,total)
        print(message)
        send_mail('Invoice receipt',message,settings.EMAIL_HOST_USER,[email],fail_silently=True,)
         # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')

        
#when the user clicks add to button this function add that item into cart
@login_required(login_url='/accounts/login/')
def addcart(request):
    name = request.POST.get('name','')
    price = request.POST.get('price','')
    img = request.POST.get('img','')
    carts = Cart.objects.filter(customer=request.user)
    cart = Cart(name=name, price=price,img=img,customer=request.user,quantity=1)
    contain =[]
    for cartname in carts:
        contain.append(cartname.name)
    if cart.name not in contain:
        cart.save()
    return redirect('menu')

#when the user clicks remove from 'My cart' this function remove that item into cart
def remcart(request):
    name = request.POST.get('name','')
    customer = request.POST.get('customer','')
    cart = Cart.objects.filter(name=name,customer=customer)
    cart.delete()
    return redirect('myorder')

#when the user clicks remove all from 'My cart' this function remove all items from his cart
def remallcart(request):
    customer = request.POST.get('removeall','')
    cart = Cart.objects.filter(customer=customer)
    print(customer)
    cart.delete()
    return redirect('myorder')

#returns Home page
def index(request):
    
    return render(request, 'home/index.html')

# shows Menu for visitors
def menu(request):
    if request.method == 'POST':
        name = request.POST.get('name','')
        price = request.POST.get('price','')
        img = request.POST.get('img','')
        customer = request.POST.get('customer','')
        carts = Cart.objects.filter(customer=customer)
        cart = Cart(name=name, price=price,img=img,customer=customer,quantity=1)
        contain =[]
        for cartname in carts:
            contain.append(cartname.name)
        if cart.name not in contain:
            cart.save()
    meals = Meal.objects.all()
    CP = Cart.objects.filter(customer=request.user.username)
    carts=[]
    for cart in CP:
        if cart.name not in carts:
            carts.append(cart.name) 
    breakfast = Meal.objects.filter(menu=Menu.objects.get(name="Breakfast"))
    lunch = Meal.objects.filter(menu=Menu.objects.get(name="Lunch"))
    softdr = Meal.objects.filter(menu=Menu.objects.get(name="Soft Drink"))
    hotdr = Meal.objects.filter(menu=Menu.objects.get(name="Hot Drink"))
    print(breakfast,lunch,softdr,hotdr)
    return render(request, 'home/menu.html',{'meals':meals, 'carts': carts,'breakfast':breakfast,'lunch':lunch,'softdr':softdr,'hotdr':hotdr})

#check if the user is super
def Is_Manager(user):
    
    return (Manager.objects.filter(manager=user).exists())

#when the customer checkout his cart order generated here
def order(request):
    if not request.user.is_staff:
        carts = Cart.objects.filter(customer=request.user.username)
        custom = Customer.objects.get(customer=request.user)
        item = ''
        price= 0
        for cart in carts: 
            quantity = request.POST.get(cart.name,'')
            name = cart.name
            item += name+"*"+quantity +", "
            price += (cart.price)*(int(quantity))
        deliver = request.POST.get("delivery",'')
        delivery = False
        if deliver == "on":
            delivery = True
        
        price = price + price*(0.2)
        chef = Employ.objects.filter(emp_type = 'chef')
        waiter = Employ.objects.filter(emp_type = 'waiter')
        status = 'Pending'
        order = Order(delivery=delivery,customer= request.user ,address=custom.address, chef = chef[0].employe.username,waiter=waiter[0].employe.username, item=item, status=status, price=price )
        custom.orders += 1
        custom.total_sale += price
        custom.save()
        order.save()
        carts.delete()
    return redirect('myorder')


#Customers can edit or confirm their order in this page   
@login_required(login_url='/accounts/login/')
def myorder(request):
    total =0
    CP = Cart.objects.filter(customer=request.user)
    orders = Order.objects.filter(customer=request.user,is_payed=False, is_blocked=False)
    not_empty = True
    has_order = True
    itm = 0
    if (str(CP) == '<QuerySet []>'):
        not_empty = False
    if (str(orders) == '<QuerySet []>'):
        has_order = False
    else:
        for order in orders:
            ordered = order
        orders = ordered
    for cart in CP:
        itm += 1
        total += cart.price

    return render(request, 'customer/Orderui.html', {'itm':itm ,'carts':CP,'not_empty':not_empty,'has_order':has_order,'order': orders, 'total':total})


def feedback(request):
    if request.method == "POST":
        
        subject = "Customer comment"
        message = request.POST.get('comments', '')
        from_email = request.POST.get('email', '')
        exper = request.POST.get('experience','')
        name = request.POST.get("name",'')

        body = "Name: "+name + "\nExperience: "+ exper+ "\n" + message
        if subject and message and from_email:
            try:
                send_mail(subject, body, from_email, [settings.EMAIL_HOST_USER])

            except BadHeaderError:
                return HttpResponse('<h1 style="color:red">Invalid header found.</h1>')

            return redirect('/')
        else:
            
            return HttpResponse('<h1 style="color:red" >Make sure all fields are entered and valid.</h1>')
    else:
        return render(request,"customer/feedback.html")

#Manager manages the menu (adding and removing menu)
@login_required(login_url='/accounts/login/')
@user_passes_test(Is_Manager)
def menumg(request):
    if request.method == 'POST':
        name = request.POST.get('name','')
        desc = request.POST.get('desc','')
        img = request.POST.get('image','')


        menu = Menu.objects.create(
            name=name,  desc=desc, img=img)
        messages.info(request , "Menu added successfully")
        return redirect('menumg')

    else:
        menus = Menu.objects.all()
        return render(request, 'manager/menumg.html',{'menus':menus})


#Manager home page; displayed for the authenticated manager or superuser
@login_required(login_url='/accounts/login/')
@user_passes_test(Is_Manager)
def manager(request):
    return render(request, 'manager/managers.html')

#Manager verify or block orders using this page
@login_required(login_url='/accounts/login/')
@user_passes_test(Is_Manager)
def ordermg(request):
    if request.method == 'POST':
        idd = request.POST.get('idd','')
        order = Order.objects.get(pk= idd)
        order.is_verified = True
        order.status = 'Verified'
        order.save()
        
        
    orders = Order.objects.filter(is_verified = False, is_blocked=False)
    return render(request, 'manager/ordermg.html',{'orders': orders})


@login_required(login_url='/accounts/login/')
@user_passes_test(Is_Manager)
def orderdet(request):
    if request.method == "POST":
        entries = request.POST.get('entries','')
        stat = request.POST.get('stat','')
        print(entries, stat)
        if stat and entries:
            if stat == "Any":
                orders = Order.objects.all().order_by("date_created").reverse()[:int(entries)]
                return render(request, 'manager/orderdeta.html',{'orders': orders})

            orders = Order.objects.filter(status=stat).order_by("date_created").reverse()[:int(entries)]
            return render(request, 'manager/orderdeta.html',{'orders': orders})

        elif stat:
            orders = Order.objects.filter(status=stat).order_by("date_created").reverse()[:10]
            return render(request, 'manager/orderdeta.html',{'orders': orders})
        elif entries:
            orders = Order.objects.all().order_by("date_created").reverse()[:int(entries)]
            return render(request, 'manager/orderdeta.html',{'orders': orders})
        
    orders = Order.objects.all().order_by("date_created").reverse()[:10]
    return render(request, 'manager/orderdeta.html',{'orders': orders})


#When Mnager blocked an order applied here 
@login_required(login_url='/accounts/login/')
@user_passes_test(Is_Manager)
def remorder(request):
    Id = request.POST.get('id','')
    order = Order.objects.get(pk= Id)
    order.is_blocked = True
    order.status = "Blocked"
    order.save()
    return redirect("ordermg")


#Manager  verify all orders by one click
def verall(request):
    orders = Order.objects.filter(is_verified=False,status = 'Pending')
    for order in orders:
        order.is_verified = True
        order.status = "Verified"
    return redirect("ordermg")


#Manager generates report for the restaurant
@login_required(login_url='/accounts/login/')
@user_passes_test(Is_Manager)
def reportmg(request):
    return render(request, 'employee/waiter.html')

#Manager manages meal (adding and removing meal)
@login_required(login_url='/accounts/login/')
@user_passes_test(Is_Manager)
def mealmg(request):
    if request.method == 'POST':
        name = request.POST.get('name','')
        price = request.POST.get('price','')
        desc = request.POST.get('desc','')
        img = request.POST['image']
        menu1 = request.POST.get("menu",'')
        mm = {
            "Soft":"Soft Drink","Hot":"Hot Drink","Breakfast":"Breakfast","Lunch":"Lunch"
        }
        menu = Menu.objects.get(name=mm[menu1])
        meal = Meal.objects.create(
            name=name, price=price, desc=desc, img=img, menu=menu)
        messages.info(request, "Meal added to menu successfully")
        return redirect('meal')
    else:
        meals = Meal.objects.all()
        menus = Menu.objects.all()

        return render(request, 'manager/mealmg.html',{'menus': menus,'meals': meals})

#Manager register employees here
@login_required(login_url='/accounts/login/')
@user_passes_test(Is_Manager)
def employeemg(request):
    if request.method == 'POST':
        fname = request.POST.get("fname",'')
        lname = request.POST.get("lname",'')
        address = request.POST.get("address",'')
        email = request.POST.get("email",'')
        password1 = request.POST.get("password1",'')
        password2 = request.POST.get("password2",'')
        salary = request.POST.get("salary",'')
        phone = request.POST.get("phone",'')
        emp_type = request.POST.get("emp_type",'')
        if password1 == password2:
            password = password1
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already taken.')
                return redirect('employee')
            else:
                user = User.objects.create_user(username=email,
                                                first_name=fname, last_name=lname, password=password, email=email, is_staff=True)
                user.save()
                employe = Employ.objects.create(
                    employe=user, address=address, phone=phone, salary=salary, emp_type=emp_type)
                employe.save()
                messages.info(request, 'Registered Successfully!')
                return redirect('employee')
        else:
            messages.info(request, 'Password not matching...')
            return redirect('employee')

    else:
        employ = Employ.objects.all()
        return render(request, 'manager/regemployee.html',{'employs': employ})


#Manager register employees here
@login_required(login_url='/accounts/login/')
@user_passes_test(Is_Manager)
def purchases(request):
    purchases = Purchase.objects.all()
    return render(request,'manager/purchases.html',{'purchases': purchases})

def emp_type_c(user):
    return (Employ.objects.filter(employe=user , emp_type="chef").exists())

#all customers account displayed for the manager
@login_required(login_url='/accounts/login/')
@user_passes_test(Is_Manager)
def customer(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()

    return render(request, 'manager/customer.html',{'customers': customers,'ordered': orders})


#Chef page: chefs verify the order they finish preparing it 
@login_required(login_url='/accounts/login/')
@user_passes_test(emp_type_c)
def chef(request):
    if request.method == 'POST':
        idd = request.POST.get('idd','')
        order = Order.objects.get(pk= idd)
        order.is_ready = True
        order.status = "Ready"
        order.save()
    orders = Order.objects.filter(is_verified=True, is_ready=False,is_blocked=False)
    return render(request, 'employee/chef.html',{'orders': orders})


def emp_type_w(user):
    return (Employ.objects.filter(employe=user , emp_type="waiter").exists())

#Waiter page: waiter picks the order and check it as it's picked
@login_required(login_url='/accounts/login/')
@user_passes_test(emp_type_w)
def waiter(request):
    if request.method == 'POST':
        idd = request.POST.get('idd','')
        order = Order.objects.get(pk= idd)
        order.is_picked = True
        order.status = 'Delivered'
        order.save()
    orders = Order.objects.filter(is_ready=True, is_picked = False,is_blocked=False)
    return render(request, 'employee/waiter.html',{'orders': orders})


def emp_type_ca(user):
    return (Employ.objects.filter(employe=user , emp_type="casher").exists())

#Casher page: casher select one order and generate bill for the customer ordered it
@login_required(login_url='/accounts/login/')
@user_passes_test(emp_type_ca)
def casher(request):
    Dicc = {}
    Ord = {}
    if request.method == 'POST':
        idd = request.POST.get('idd','')
        order = Order.objects.get(pk= idd)
        order.is_payed = True
        orde = order.item.split(", ")
        price = 0.00
        delp = 0.00
        for od in orde:
            if od != "":
                itm = od.split("*")
                pris = Meal.objects.get(name=itm[0])
                price += int(pris.price) * int(itm[1])
                Ord[itm[0]] = {str(itm[1]): pris.price}
        print(price)
        if order.delivery:
            delp= 5
        user = User.objects.get(username = order.customer)

        name = user.first_name +" "+ user.last_name
        address = order.address
        email = user.email
        No = str(random.randint(1,9)) + str(random.randint(1,9))+str(random.randint(1,9))+str(random.randint(1,9))+str(random.randint(1,9))+str(random.randint(1,9))+str(random.randint(1,9))
        date = order.date_created
        total = price*(0.02) + price + delp
        # Dicc["delivery"] = order.delivery
        print(Dicc)
        order.save()
        return render(request, 'employee/genBill.html',{'genorder': Dicc, "order":Ord,"subtot": price ,
            "del":delp,"total":total,'No': No,"adr":address,"email":email,"name":name,"date":date, "idd": idd})

    orders = Order.objects.filter(is_picked = True,is_payed=False,is_blocked=False)
    return render(request, 'employee/casher.html',{'orders': orders})


def emp_type_su(user):
    return (Employ.objects.filter(employe=user , emp_type="supplier").exists())


@login_required(login_url='/accounts/login/')
@user_passes_test(emp_type_su)
def supplier(request):
   
    if request.method == "POST":
        name = request.POST.get('name','')
        price = request.POST.get('price','')
        unit = request.POST.get("unit",'')
        amount = request.POST.get("amount",'')
        desc = request.POST.get('desc','')
        group = request.POST.get('group','')
        total = int(price) * int(amount)
        purchase = Purchase.objects.create(total=total,by=request.user.username, name=name,price=price, unit=unit, amount=amount, desc=desc, group=group)
        purchase.save()

    return render(request, "employee/supplier.html")

