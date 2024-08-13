from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.db import transaction
from django.http import HttpResponseBadRequest,Http404,HttpResponseForbidden
from datetime import datetime,timedelta
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login 
from .forms import Profileform,Userupdate,Bookform,Chatform,NewGroupChatForm,ChatRoomEditForm,AvailabilityForm
from .models import Profile,Product,Booking,OrderModel,ChatGroup,Groupmessage,Hall,HallBookings
from django.core.mail import EmailMessage,send_mail
from django.contrib.auth import get_user_model
from math import ceil
from django.views import View
import json
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db.models import Count
from django.contrib import messages
from django.http import JsonResponse
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
# Create your views here.


def logoutuser(request):
    logout(request)
    # Redirect to a success page.
    return redirect('/')



def loginuser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            if is_ajax:
                return JsonResponse({"success": True}, status=200)
            else:
                return redirect("/")
        else:
            error_message = "Invalid username or password."
            if is_ajax:
                return JsonResponse({"error": error_message}, status=400)
            else:
                messages.error(request, error_message)
                return render(request, 'login.html')
    return render(request, 'login.html')

  
def index(request):
    form=AvailabilityForm()
    if request.user.is_anonymous:
        value="customer"
        sign=False
    else:
       value=request.user.username
       sign=True
    context={
        'value':value,
        'sign':sign,
        'form':form 
             }
    return render(request,'index.html',context)




def handlesignin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        name = request.POST.get('name')
        title = request.POST.get('title')  
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        # Check if all required fields are provided
        if not name or not email or not password or not title:
            messages.error(request, "All fields are required.")
            return redirect("/signin")

        # Create the user
        try:
            myuser = User.objects.create_user(username=name, email=email, password=password)
            myuser.first_name = name
            myuser.last_name = title  # Assign the title or last name
            myuser.save()
            
            # Send a welcome email
            subject = 'Welcome to INDOBITES'
            message = f'Hi {myuser.username}, thank you for registering'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [myuser.email, ]
            send_mail(subject, message, email_from, recipient_list)

            # Authenticate and log the user in
            user = authenticate(username=name, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Profile created successfully.')
                return redirect("/")
            else:
                messages.error(request, "Authentication failed. Please try logging in.")
                return redirect("/login")

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect("/signin")

    return render(request, 'CreateAccount.html')


def prof(request,username):
    if request.user.is_anonymous:
       return redirect("/login")
    user = get_object_or_404(User, username=username)
    if request.user.username != username:
        return render(request,'ProfileDifferent.html',{'user':user})
    if request.method == 'POST':
      uform=Userupdate(request.POST,instance=request.user)
      pform=Profileform(request.POST,
                        request.FILES,
                        instance=request.user.profile)
      if uform.is_valid() and pform.is_valid():
         uform.save()
         pform.save()
         messages.success(request, 'Profile update done')
         return redirect(f"/prof/{request.user.username}")

    else:
      uform=Userupdate(instance=request.user)
      pform=Profileform(instance=request.user.profile)
    jei=request.user.username
    all_users=Booking.objects.filter(name=jei)

    content={'uform':uform,
             'pform':pform,
             'all_users':all_users
             }
    return render(request,'ProfileCustomer.html',content)

def deleteprofile(request):
     user = request.user
     if request.method == "POST":
        logout(request)
        user.delete()
        return redirect("")
def is_staff_or_admin(user):
    return user.is_staff or user.is_superuser

def menu(request):
   if request.method == 'POST':
      filter_query=request.POST.get('select')
      search_query=request.POST.get('searchMenu')
   else:
      filter_query='Biriyani'
      search_query='###'
   if search_query=="":
      search_query="###"
   prodobject=Product.objects.all()
   cat1= Product.objects.filter(category=filter_query)
   cati2=prodobject.filter( product_name__icontains=search_query)|prodobject.filter(category__icontains=search_query)|prodobject.filter(price__startswith=search_query)
   cat2=cati2.values()
   if request.user.is_anonymous:
        value="customer"
        sign=False
   else:
       value=request.user.username
       sign=True
    
   context={
         'objects':prodobject,
         'value':value,
         'sign':sign,
         'cat1':cat1,
         'deli':filter_query,
         'cat2':cat2

    }
   return render(request,'menu.html',context)

@login_required(login_url='/login')
def add_to_cart(request):
    if request.method=='POST':
     product=request.POST.get('obj_id')
     quantity=request.POST.get('quantity')
     if not product or not quantity:
         messages.error(request,"Invalid input in add to cart")
    phone= request.user.profile.phone 
    try:
            product = Product.objects.get(id=product)
    except Product.DoesNotExist:
            return HttpResponseBadRequest("Product not found")
    
    order=OrderModel(
        product=product,
        phone=phone,
        customer=request.user,
        quantity=quantity,
        price=product.price * int(quantity)
        
     )
    order.save()
    messages.success(request,"Item added. Proceed to checkout or add browse other items")
    return redirect('menu')

@login_required(login_url='/login')
def cart(request):
      orders=OrderModel.objects.filter(customer=request.user,payment_status=False)
      count=orders.count() #count number of orders
      sum=0
      for ord in orders:
          sum+=ord.price
      if request.method == 'POST':
        order_id = request.POST.get('order_id')
        action = request.POST.get('action')

        order = get_object_or_404(OrderModel, id=order_id, customer=request.user)

        if action == 'update':
            quantity = request.POST.get('quantity')
            if quantity is not None:
                try:
                    new_quantity = int(quantity)
                    if new_quantity > 0:
                        order.quantity = new_quantity
                        order.price = order.product.price * new_quantity
                        order.save()
                    else:
                        order.delete()
                        messages.success(request, "Item removed from cart")
                except ValueError:
                    messages.error(request, "Invalid quantity")
        elif action == 'delete':
            order.delete()
            messages.success(request, "Item removed from cart")

        return redirect('cart')

      return render(request, 'cart.html', {'orders': orders, 'count': count, 'value': request.user.username, 'sum': sum})

#HAndle payment

stripe.api_key = settings.STRIPE_SECRET_KEY
YOUR_DOMAIN = "http://127.0.0.1:8000"
TAX_RATE=stripe.TaxRate.create(
  display_name="GST",
  inclusive=False,
  percentage=18,
  country="IN",
  description="IN Tax",
)
TAX_RATE_ID=TAX_RATE.id

@login_required(login_url='/login')
@csrf_exempt
def createcheckoutsession(request):
    order_id = "Pending"
    totalprice = 0
    line_items = []
    orders = OrderModel.objects.filter(customer=request.user, payment_status=False)

    for order in orders:
        totalprice += order.price
        product = order.product
        if not product.stripe_price_id:
            # Create a product in Stripe if it doesn't exist
            stripe_product = stripe.Product.create(name=product.product_name)
            product.stripe_product_id = stripe_product.id
            product.save()

            # Create a price for the product in Stripe
            price = stripe.Price.create(
                product=stripe_product.id,
                unit_amount=product.price * 100,  # amount in the smallest currency unit
                currency="inr",
            )
            product.stripe_price_id = price.id
            product.save()

        line_items.append({
            'price': product.stripe_price_id,
            'quantity': order.quantity,
            'tax_rates':[TAX_RATE_ID]

        })

    if request.method == 'POST':
        try:
            checkout_session = stripe.checkout.Session.create(

                line_items=line_items,
                mode='payment',
                success_url=YOUR_DOMAIN + '/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=YOUR_DOMAIN + '/cart',
            )
            order_id = checkout_session.id
            for ord in orders:
                ord.stripe_checkout_session_id = checkout_session.id
                ord.save()
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            return JsonResponse({'error': str(e)})

    return render(request, 'payment.html', {'order_id': order_id})

@login_required(login_url='/login')
def payment_success(request):
    orders = OrderModel.objects.filter(customer=request.user, payment_status=False)
    checkout_session_id = request.GET.get('session_id', None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    for order in orders:
        order.payment_status = True
        order.stripe_checkout_sessionid=checkout_session_id
        order.save()
    return render(request, 'success.html',{'session':checkout_session_id})

import time
@csrf_exempt
def stripe_webhook(request):
    time.sleep(10)
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponseBadRequest()
    except stripe.error.SignatureVerificationError as e:
        return HttpResponseBadRequest()
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session.get('customer_details', {}).get('email', '')
        # Mark orders as paid
        orders=OrderModel.objects.filter(customer=request.user, payment_status=False)
        for order in orders:
            order.payment_status = True
            checkout_session_id = request.GET.get('session_id', None)
            order.stripe_checkout_sessionid=checkout_session_id
            order.save()
        subject = 'Payment Receipt'
        message = f'Thank you for your payment. Your order details are as follows:\n\n'
        for order in orders:
            message += f'Order ID: {order.id} and Session Id : {checkout_session_id}\n'
            message += f'Product: {order.product.product_name}\n'
            message += f'Quantity: {order.quantity}\n'
            message += f'Total Price: {order.price}\n'
            message += f'Status: {"Paid" if order.payment_status else "Pending"}\n\n'
        message += 'Thank you for shopping with us!'

        if request.user.email or customer_email:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [request.user.email,customer_email],
                fail_silently=False,
            )
    return HttpResponse(status=200)

@login_required(login_url='/login')
def ordertracker(request):
    if request.user.is_anonymous:
        sign=False
    else:
        sign=True
    orders = OrderModel.objects.filter(customer=request.user, payment_status=True)
    return render(request, 'ordertracker.html', {'orders': orders,'sign':sign})


@user_passes_test(is_staff_or_admin, login_url='/login')
def list_orders(request):
    if request.user.is_anonymous:
        sign=False
    else:
        sign=True
    orders = OrderModel.objects.all().select_related('customer', 'product')
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        status = request.POST.get('status')
        order = OrderModel.objects.get(id=order_id)
        order.status = status
        order.save()
        return redirect('list_orders')
    return render(request, 'list_orders.html', {'orders': orders,'sign':sign})

def booking(request):
     if request.user.is_anonymous:
       return redirect("/login")
     if request.method == 'POST':
        email=request.POST.get('email')
        dateofuser=request.POST.get('date')
    #    dateof = datetime.strptime(dateo,'%m-%d-%y')
     #   dateofuser= datetime.strftime(dateof,'%Y-%m-%d')
        descr=request.POST.get('descr')
        seats=request.POST.get('select')
        phone=request.POST.get('phone')
        name2=request.POST.get('name')
      
        if Booking.objects.filter(day=dateofuser).count() < 1:
           book=Booking(email=email,phone=phone,name=name2,seats=seats,description=descr,day=dateofuser)
           book.save()
           messages.success(request, "Appointment Saved!")
           return redirect("/prof")
     context={'seats': ["2", "4","10","20", "30+(buffet)"
                  ],}
     return render(request,'profile.html',context)

@login_required(login_url='/login')
def chatview(request,chatroom_name='Public-chat'):
    if request.user.is_anonymous:
        sign=False
    else:
        sign=True
    chat_group=get_object_or_404(ChatGroup,groupname=chatroom_name)
    chat_messages=chat_group.chat_messages.all()[:100]
    form=Chatform()
    other_user=None
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            raise Http404("You are not allowed here")
        for member in chat_group.members.all():
            if member != request.user:
                other_user = member
                break
    
    if chat_group.groupchat_name:
        if request.user not in chat_group.members.all():
          if request.user not in chat_group.banlist.all():  
            chat_group.members.add(request.user)

    if request.method =='POST':
        form=Chatform(request.POST)
        if form.is_valid:
            message=form.save(commit=False)
            message.author = request.user
            message.group=chat_group
            message.save()
            context = {
                'message' : message,
                'user' : request.user
            }
            return render(request,'partials/chat_message_p.html',context)
    context={
'chat_messages':chat_messages,
'form':form,
'otheruser':other_user,
'chatroom_name':chatroom_name,
'chat_group':chat_group,
'sign':sign
    }    
    return render(request,'chat.html',context)

@login_required(login_url="/login")
def get_or_createchatroom(request,username):
    if request.user.username == username:
        return redirect('')
    other_user = User.objects.get(username = username)
    my_chatrooms = request.user.chat_groups.filter(is_private=True)
    if my_chatrooms.exists():
        for chatroom in my_chatrooms:
            if other_user in chatroom.members.all():
             if other_user not in chatroom.banlist.all():
                chatroom=chatroom
                break
            else:
                chatroom=ChatGroup.objects.create(is_private=True)
                chatroom.members.add(other_user,request.user)
    else:
        chatroom=ChatGroup.objects.create(is_private=True)
        chatroom.members.add(other_user,request.user)
    return redirect('chatroom', chatroom.groupname)

@login_required(login_url="/login")
def create_groupchat(request):
    form=NewGroupChatForm()
    if request.method == 'POST':
        form = NewGroupChatForm(request.POST)
        if form.is_valid():
            new_groupchat = form.save(commit=False)
            new_groupchat.admin = request.user
            new_groupchat.save()
            new_groupchat.members.add(request.user)
            return redirect('chatroom', new_groupchat.groupname)
    
    context = {
        'form': form
    }
    return render(request,'create_groupchat.html',context)

login_required(login_url="/login")
def chatroom_edit_view(request,chatroom_name):
    chat_group = get_object_or_404(ChatGroup, groupname=chatroom_name)
    if request.user != chat_group.admin:
        raise Http404()
    form=ChatRoomEditForm(instance=chat_group)
    if request.method == 'POST':
        form = ChatRoomEditForm(request.POST, instance=chat_group)
        if form.is_valid():
            form.save()
            remove_members = request.POST.getlist('remove_members')
            for member_id in remove_members:
                member = User.objects.get(id=member_id)
                if member not in chat_group.banlist.all():
                    chat_group.banlist.add(member)
                chat_group.members.remove(member)  
            ban_members = request.POST.getlist('ban_members')
            if ban_members:
                for member_id in ban_members:
                    member = User.objects.get(id=member_id)
                    if member  in chat_group.banlist.all():
                        chat_group.banlist.remove(member)
                
            return redirect('chatroom', chatroom_name)
    return render(request,'chatroomedit.html',{
        'form' : form,
        'chat_group' : chat_group
    } )

@login_required(login_url="/login")
def chatroom_delete_view(request,chatroom_name):
    chat_group = get_object_or_404(ChatGroup, groupname=chatroom_name)
    if request.user != chat_group.admin:
        raise Http404()
    else:
        chat_group.delete()
        return redirect('/')
    
def chatroom_leave_view(request,chatroom_name):
    chat_group = get_object_or_404(ChatGroup, groupname=chatroom_name)
    if request.user not in chat_group.members.all():
        raise Http404()
    else:
        chat_group.members.remove(request.user)
        return redirect('/')    

from bongapp.availability import availability

def halllist(request):
    rooms = Hall.objects.all()  # Query all Room objects
    return render(request, 'room_list.html', {'rooms': rooms})
def Hallbookinglist(request):
    bookings = HallBookings.objects.all()  # Query all Booking objects
    return render(request, 'booking_list.html', {'bookings': bookings})

def HallBookingView(request):
    form=AvailabilityForm()
    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            hall_list=Hall.objects.filter(category=data['category'])
            available_halls=[]
            with transaction.atomic():
              for hall in hall_list:
                if availability(hall,data['checkin'],data['checkout']):
                    available_halls.append(hall)
              if len(available_halls)>0:
               hall= available_halls[0]
               booking=HallBookings.objects.create(Hall=hall,ammenity=data['ammenity'],customer=request.user,checkin=data['checkin'],checkout=data['checkout'])
               booking.save()
               messages.success(request, "Hall booked successfully")
               
              else:
                messages.error(request, "No hall available for the selected dates")
                

            
    context = { 'form': form }
    return render(request, 'booking_form.html', context)
