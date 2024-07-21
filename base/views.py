from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Count
from django.contrib.auth import update_session_auth_hash
# --------- #
from .forms import AddTrackingForm, SignUpForm, UserChangePassword
from .models import TrackingNumber, Courier, TrackingState, Statistic, UserActivity, DeliveryType
# --------- #
import datetime
import json
from base.ship24API import getAutoTrackingResults, getTrackingResultWithCourier
from ipware import get_client_ip
# Create your views here.

# Login
def loginPage(request):
    # Passes in page name
    title_page = 'Sign In'

    # Checks user authentication
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username').replace(" ", "")
        password = request.POST.get('password').replace(" ", "")
        
        # check user exists
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User does not exists')
            return redirect('login')
        
        # pass in username and password making sure are correct
        # returns an error or user object that matches the last two parameters            
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Username or password does not exists')
            return redirect('login')
        
    context = {
        'title_page': title_page, 
        }
    return render(request, 'base/pages-login.html', context)

# Logout
def logoutUser(request):
    # Deletes user's token (session)
    logout(request)
    print(request)
    return redirect('index')

def registerPage(request):
    title_page = 'Register Account'

    form = SignUpForm

    if request.user.is_anonymous:
        if request.method == 'POST':             
            form = SignUpForm(request.POST)
            # Checks inputs
            if form.is_valid():
                user = form.save(commit=False)
                # Checks whether the email already exists
                if User.objects.filter(email=user.email).exists():
                    messages.error(request, 'Email already exists')
                    return redirect('register')
                else:
                    user.username = user.username.lower().replace(" ", "")
                    user.email = user.email.lower().replace(" ", "")
                    user.password = user.password.replace(" ", "")

                    user.save()
                    messages.success(request, 'Account activated. Please log in with your account.')
                    return redirect('login')
            else:
                messages.error(request, 'Username already exists')
                return redirect('register')
    else:
        return redirect('dashboard')
    
    context = {
        'form': form, 
        'title_page': title_page
        }
    
    return render(request, 'base/pages-register.html', context)

# Main page
def index(request):
    title_page = 'Index'
    count_tracking_numbers = TrackingNumber.objects.all().count()
    count_couriers = Courier.objects.all().count()
    count_users = User.objects.all().count()
            
    context = {
        'title_page': title_page, 
        'count_tracking_numbers': count_tracking_numbers, 
        'count_users': count_users, 
        'count_couriers': count_couriers
        }
    return render(request, 'base/index.html', context)

# request is a HTTP object (type of request, data passed in, user sending in the backend...)
# Dashboard section
@login_required(login_url = 'login')
def dashboard(request):
    title_page = 'Dashboard'
    
    tracking_numbers_list = TrackingNumber.objects.filter(
        Q(user__username=request.user)
        ).order_by('-created')[0:25]
    
    # Tracking numbers - recent events 
    tracking_latest_updates = TrackingState.objects.filter(
        # Q(courier__name__icontains = q) &
        Q(tracking_number__user__username = request.user)
    ).order_by('-occurrence_date_time')[0:10]

    # Browse Couriers
    # Only shows the couriers name that has a tracking number related to user
    couriers = Courier.objects.filter(
        Q(participants__user__username__icontains=request.user)
        ).distinct()
    
    # Events
    tracking_states = TrackingState.objects.filter(
        tracking_number__user__username=request.user
        )

    # States
    # pending
    packages_pending = TrackingNumber.objects.filter(
        status_milestone = 'pending',
        user__username=request.user
        )
    
    # info_received
    packages_info_received = TrackingNumber.objects.filter(
        status_milestone = 'info_received',
        user__username=request.user
        )
    # in_transit
    packages_in_transit = TrackingNumber.objects.filter(
        status_milestone = 'in_transit',
        user__username=request.user
        )
    # out_for_delivery
    packages_out_for_delivery = TrackingNumber.objects.filter(
        status_milestone = 'out_for_delivery',
        user__username=request.user
        )
    # failed_attempt
    packages_failed_attempt = TrackingNumber.objects.filter(
        status_milestone = 'failed_attempt',
        user__username=request.user
        )
    # available_for_pickup
    packages_available_for_pickup = TrackingNumber.objects.filter(
        status_milestone = 'available_for_pickup',
        user__username=request.user
        )
    # exception
    packages_exception = TrackingNumber.objects.filter(
        status_milestone = 'exception',
        user__username=request.user
        )
    # delivered
    packages_delivered = TrackingNumber.objects.filter(
        status_milestone = 'delivered',
        user__username=request.user
        )
    
    # Counters
    count_tracking_numbers = tracking_numbers_list.count()
    count_tracking_states = tracking_states.count()
    count_couriers_involved = couriers.count()
    count_packages_pending = packages_pending.count()
    count_packages_info_received = packages_info_received.count()
    count_packages_in_transit = packages_in_transit.count()
    count_packages_out_for_delivery = packages_out_for_delivery.count()
    count_packages_failed_attempt = packages_failed_attempt.count()
    count_packages_available_for_pickup = packages_available_for_pickup.count()
    count_packages_exception = packages_exception.count()
    count_packages_delivered = packages_delivered.count()
    
    context = {
        'title_page': title_page,
        'tracking_numbers_list': tracking_numbers_list, 
        'count_tracking_states': count_tracking_states,
        'couriers': couriers, 
        'count_tracking_numbers': count_tracking_numbers, 
        'tracking_latest_updates': tracking_latest_updates,
        'count_packages_pending': count_packages_pending,
        'count_packages_info_received': count_packages_info_received,
        'count_packages_in_transit': count_packages_in_transit,
        'count_packages_out_for_delivery': count_packages_out_for_delivery,
        'count_packages_failed_attempt': count_packages_failed_attempt,
        'count_packages_available_for_pickup': count_packages_available_for_pickup,
        'count_packages_exception': count_packages_exception,
        'count_packages_delivered': count_packages_delivered,
        'count_couriers_involved': count_couriers_involved
    }
    
    return render(request, 'base/dashboard.html', context)

@login_required(login_url = 'login')
def courierList(request):
    title_page = 'Involved List'
    
    couriers_list = Courier.objects.filter(
        participants__user__username=request.user
    ).annotate(
        package_count=Count('participants')
    )

    context = {
        # 'couriers': couriers,
        'couriers': couriers_list,
        'title_page': title_page
    }
    return render(request, 'base/courier_list.html', context)

def courierPackageInvolved(request, pk):
    title_page = pk

    # Search courier
    try:
        courier = Courier.objects.get(name=pk)
    except Courier.DoesNotExist:
        return redirect('error-404')
    
    # Browse Couriers
    # Only shows the couriers name that has a tracking number related to user
    tracking_number_list = TrackingNumber.objects.filter(
        Q(couriers_involved__name__icontains=pk) &
        Q(user__username=request.user)
        ).order_by("-created")

    context = {
        'tracking_number_list': tracking_number_list,
        'title_page': title_page,
        'courier': courier
    }
    return render(request, 'base/courier_tracking_list.html', context)

@login_required(login_url = 'login')
def trackingList(request):
    title_page = 'List'

    tracking_number_list = TrackingNumber.objects.filter(
        user__username=request.user
        )
    
    couriers = Courier.objects.all()

    context = {
        'tracking_number_list': tracking_number_list,
        'title_page': title_page,
        'couriers': couriers
        }
    
    return render(request, 'base/tracking_list.html', context)


@login_required(login_url = 'login')
def eventList(request):
    title_page = 'Event List'

    latest_events = TrackingState.objects.filter(
        # Q(courier__name__icontains = q) &
        Q(tracking_number__user__username = request.user)
    ).order_by('-occurrence_date_time')

    
    context = {
        'latest_events': latest_events,
        'title_page': title_page,
    }
    
    return render(request, 'base/event_list.html', context)

@login_required(login_url = 'login')
def trackingPending(request):
    title_page = 'Pending'
    
    # pending
    tracking_number_list = TrackingNumber.objects.filter(
        status_milestone = 'Pending',
        user__username=request.user
        )
    
    couriers = Courier.objects.all()
    
    context = {
        'tracking_number_list': tracking_number_list,
        'title_page': title_page,
        'couriers': couriers
        }
    
    return render(request, 'base/tracking_list.html', context)

@login_required(login_url = 'login')
def trackingInfoReceived(request):
    title_page = 'Info. Received'
    
    # info_received
    tracking_number_list = TrackingNumber.objects.filter(
        status_milestone = 'info_received',
        user__username=request.user
        )
    
    couriers = Courier.objects.all()
    
    context = {
        'tracking_number_list': tracking_number_list,
        'title_page': title_page,
        'couriers': couriers
        }
    
    return render(request, 'base/tracking_list.html', context)

@login_required(login_url = 'login')
def trackingInTransit(request):
    title_page = 'In Transit'
    
    # in_transit
    tracking_number_list = TrackingNumber.objects.filter(
        status_milestone = 'in_transit',
        user__username=request.user
        )
    
    couriers = Courier.objects.all()
    
    context = {
        'tracking_number_list': tracking_number_list,
        'title_page': title_page,
        'couriers': couriers
        }
    
    return render(request, 'base/tracking_list.html', context)

@login_required(login_url = 'login')
def trackingDelivery(request):
    title_page = 'Out for delivery'

    # out_for_delivery
    tracking_number_list = TrackingNumber.objects.filter(
        status_milestone = 'out_for_delivery',
        user__username=request.user
        )
    
    couriers = Courier.objects.all()
    
    context = {
        'tracking_number_list': tracking_number_list,
        'title_page': title_page,
        'couriers': couriers
        }
    
    return render(request, 'base/tracking_list.html', context)

@login_required(login_url = 'login')
def trackingFailedAttempt(request):
    title_page = 'Failed Attempt'

    # failed_attempt
    tracking_number_list = TrackingNumber.objects.filter(
        status_milestone = 'failed_attempt',
        user__username=request.user
        )
    
    couriers = Courier.objects.all()
    
    context = {
        'tracking_number_list': tracking_number_list,
        'title_page': title_page,
        'couriers': couriers
        }
    
    return render(request, 'base/tracking_list.html', context)

@login_required(login_url = 'login')
def trackingPickUp(request):
    title_page = 'Pick Up'

    # available_for_pickup
    tracking_number_list = TrackingNumber.objects.filter(
        status_milestone = 'available_for_pickup',
        user__username=request.user
        )
    
    couriers = Courier.objects.all()
    
    context = {
        'tracking_number_list': tracking_number_list,
        'title_page': title_page,
        'couriers': couriers
        }
    
    return render(request, 'base/tracking_list.html', context)

@login_required(login_url = 'login')
def trackingException(request):
    title_page = 'Exception'
    
    # exception
    tracking_number_list = TrackingNumber.objects.filter(
        status_milestone = 'exception',
        user__username=request.user
        )
    
    couriers = Courier.objects.all()
    
    context = {
        'tracking_number_list': tracking_number_list,
        'title_page': title_page,
        'couriers': couriers
        }
    
    return render(request, 'base/tracking_list.html', context)

@login_required(login_url = 'login')
def trackingDelivered(request):
    title_page = 'Delivered'

    # delivered
    tracking_number_list = TrackingNumber.objects.filter(
        status_milestone = 'delivered',
        user__username=request.user
        )
    
    couriers = Courier.objects.all()
    
    context = {
        'tracking_number_list': tracking_number_list,
        'title_page': title_page,
        'couriers': couriers
        }
    
    return render(request, 'base/tracking_list.html', context)

@login_required(login_url = 'login')
def overview(request, pk):
    title_page = 'Overview'

    try:
        # find the pk by id
        tracking_number = TrackingNumber.objects.get(id=pk)
    except TrackingNumber.DoesNotExist:
        # if does not exist such pk in table
        return redirect('error-404')
    
    # Search trackingnumber
    tracking_info = TrackingNumber.objects.get(id=pk)
    # Prevents from accessing other users tracking numbers
    if str(tracking_info.user.username) != str(request.user):
        return redirect('error-403')
    
    couriers_involved = tracking_number.couriers_involved.all()
    tracking_statistics = Statistic.objects.get(tracking_number=tracking_number)

    # Get all status related to the specific tracking_number
    # trackingnumber -> trackingstatus
    status = tracking_number.trackingstate_set.all().order_by('-occurrence_date_time')
    
    context = {
        'title_page': title_page, 
        'tracking_number': tracking_number,
        'couriers_involved': couriers_involved, 
        'tracking_statistics': tracking_statistics, 
        'status': status
        }
    return render(request, 'base/tracking_overview.html', context)

@login_required(login_url = 'login')
def addTracking(request):
    title_page = 'Add Tracking'
    form = AddTrackingForm()
    courier_list = Courier.objects.all()
    # Checks if the form method received is POST
    if request.method == 'POST':
        # title = request.POST.get('title')
        get_tracking_number = request.POST.get('tracking_number')
        courier_selected = request.POST.get('courier')
        delivery_type = DeliveryType.objects.get(id=request.POST.get('delivery_type'))
        # passes in all request data to form. Form knows which values extract from it, types and values are correct

        # search tracking number and user if exist in tracking_Number table
        search_tracking = TrackingNumber.objects.filter(tracking_number=get_tracking_number, user=request.user).first()

        # if finds one, it exists
        if search_tracking:
            messages.error(request, 'Tracking number exists.')
            return redirect('add-tracking')
        else:
            if courier_selected == 'Auto':
                tracking_data = json.loads(getAutoTrackingResults(get_tracking_number))
                courier_code = 'Auto'
            else:
                get_courier = Courier.objects.get(id=courier_selected)
                courier_code = get_courier.code
                tracking_data = json.loads(getTrackingResultWithCourier(get_tracking_number, get_courier.code))

            tracker_id = tracking_data["data"]["trackings"][0]["shipment"]['shipmentId']

            # If tracking number is unable to get info, return error page
            if tracker_id == None or tracker_id == '':
                messages.error(request, 'Unable to check tracking number. Comeback later or select an specfic courier.')
                return redirect('add-tracking')
            
            form = AddTrackingForm(request.POST)
            
            if form.is_valid():
                # Gives instace of tracking_number
                # Returns an object that hasn’t yet been saved to the database
                tracking_number = form.save(commit=False)
                tracking_number.user = request.user
                tracking_number.destination_country_code = tracking_data["data"]["trackings"][0]["shipment"]["destinationCountryCode"]
                tracking_number.origin_country_code = tracking_data["data"]["trackings"][0]["shipment"]["originCountryCode"]
                tracking_number.courier_selected = courier_code
                tracking_number.status_milestone = tracking_data["data"]["trackings"][0]["shipment"]["statusMilestone"]
                tracking_number.estimated_delivery_date = tracking_data["data"]["trackings"][0]["shipment"]["delivery"]["estimatedDeliveryDate"]
                tracking_number.save()

                # Saves all events related to tracking number
                tracking_info = TrackingNumber.objects.get(tracking_number = get_tracking_number, user=request.user)
                for trackings in tracking_data["data"]["trackings"]:
                    for events in trackings['events']:
                        get_courier = Courier.objects.get(code=events['courierCode'])
                        tracking_status = TrackingState.objects.create(
                            tracking_number = tracking_info,
                            status = events['status'],
                            event_tracking_number = events['eventTrackingNumber'],
                            courier = get_courier,
                            occurrence_date_time = events['occurrenceDatetime'],
                            status_milestone = events['statusMilestone'],
                            location = events['location']
                        )

                        # Adds couriers involved in a tracking number
                        tracking_info.couriers_involved.add(get_courier)
                
                tracking_statistics = Statistic.objects.create(
                    tracking_number = tracking_info,
                    info_received_date_time = tracking_data["data"]["trackings"][0]["statistics"]["timestamps"]["infoReceivedDatetime"],
                    in_transit_date_time = tracking_data["data"]["trackings"][0]["statistics"]["timestamps"]["inTransitDatetime"],
                    outFor_delivery_date_time = tracking_data["data"]["trackings"][0]["statistics"]["timestamps"]["outForDeliveryDatetime"],
                    failed_attempt_date_time = tracking_data["data"]["trackings"][0]["statistics"]["timestamps"]["failedAttemptDatetime"],
                    available_for_pickup_date_time = tracking_data["data"]["trackings"][0]["statistics"]["timestamps"]["availableForPickupDatetime"],
                    exception_date_time = tracking_data["data"]["trackings"][0]["statistics"]["timestamps"]["exceptionDatetime"],
                    delivered_date_time = tracking_data["data"]["trackings"][0]["statistics"]["timestamps"]["deliveredDatetime"],
                )

                ip, is_routable = get_client_ip(request)
        
                if ip is None:
                    # Unable to get the client's IP address
                    ip = '0.0.0.0'
                else:
                    # We got the client's IP address
                    if is_routable:
                        # The client's IP address is publicly routable on the Internet
                        ipv = 'Public'
                    else:
                        # The client's IP address is private
                        ipv = 'Private'

                UserActivity.objects.create(
                    user = request.user, 
                    ip_address = ip + ', ' + ipv, 
                    action = "Add tracking",
                    modification = 'Title: ' + request.POST.get('title') + '\n' + 
                                    'Tracking number: ' + request.POST.get('tracking_number') + '\n' +
                                    'Delivery type: ' + delivery_type.delivery_type,
                    url = request.path
                )
                return redirect('overview', pk = tracking_info.id)
            
    context = {
        'title_page': title_page,
        'form': form, 
        'courier_list': courier_list
        }
    return render(request, 'base/add_update_tracking.html', context)

@login_required(login_url = 'login')
def updateTracking(request, pk):
    title_page = 'Update Tracking'
    # Searchs by id and get values of row
    tracking_info = TrackingNumber.objects.get(id=pk)
    # Show all couriers
    courier_list = Courier.objects.all()

    # Prefills tracking values in form
    form = AddTrackingForm(instance=tracking_info)

    # Prevents from accessing other users tracking numbers
    if str(tracking_info.user.username) != str(request.user):
        return redirect('error-403')
    
    if request.method == 'POST':
        # second parameter is to indicate which track_number to update (gets the instace of the tracking number).
        # if only request.POST it will create a new tracking_number in table
        # the new data will be replaced the old data
        form = AddTrackingForm(request.POST, instance=tracking_info)
        courier_selected = request.POST.get('courier')
        
        if courier_selected != 'Auto':
            courier = Courier.objects.get(id=courier_selected)
            courier_code = courier.code
        else:
            courier_code = 'Auto'

        if form.is_valid():
            tracking_number = form.save(commit=False)
            tracking_number.courier_selected = courier_code
            tracking_number.save()
            
            ip, is_routable = get_client_ip(request)
            delivery_type = DeliveryType.objects.get(id=request.POST.get('delivery_type'))

            if ip is None:
                # Unable to get the client's IP address
                ip = '0.0.0.0'
            else:
                # We got the client's IP address
                if is_routable:
                    # The client's IP address is publicly routable on the Internet
                    ipv = 'Public'
                else:
                    # The client's IP address is private
                    ipv = 'Private'
            
            # Register user's activity
            UserActivity.objects.create(
                        user = request.user, 
                        ip_address = ip + ', ' + ipv, 
                        action = 'Update tracking',
                        modification = 'Title: ' + tracking_info.title + ' changed to ' + request.POST.get('title') + '\n' + 
                                        'Tracking number: ' + tracking_info.tracking_number + ' changed to ' + request.POST.get('tracking_number') + '\n' +
                                        'Delivery type: ' + tracking_info.delivery_type.delivery_type + ' changed to ' + delivery_type.delivery_type,
                        url = request.path
            )
            return redirect('tracking-list')
        
    context = {
        'title_page': title_page,
        'tracking_info': tracking_info,
        'form': form,
        'courier_list': courier_list
        }
    return render(request, 'base/add_update_tracking.html', context)

@login_required(login_url = 'login')
def deleteTracking(request, pk):
    title_page = 'Delete Tracking'
    
    # Search trackingnumber
    tracking_info = TrackingNumber.objects.get(id=pk)
    # Prevents from accessing other users tracking numbers
    if str(tracking_info.user.username) != str(request.user):
        return redirect('error-403')
    
    ip, is_routable = get_client_ip(request)
    
    if ip is None:
        # Unable to get the client's IP address
        ip = '0.0.0.0'
    else:
        # We got the client's IP address
        if is_routable:
            # The client's IP address is publicly routable on the Internet
            ipv = 'Public'
        else:
            # The client's IP address is private
            ipv = 'Private'
    
    UserActivity.objects.create(
        user = request.user, 
        ip_address = ip + ', ' + ipv,
        action = "Delete tracking",
        modification = 'Title: ' + tracking_info.title + '\n' + 
                        'Tracking number: ' + tracking_info.tracking_number,
        url = request.path
    )
    if request.method == 'POST':
        try:
            tracking_info = TrackingNumber.objects.get(id=pk)
            tracking_info.delete()
            return redirect('tracking-list')
        except TrackingNumber.DoesNotExist:
            return redirect('error-404')

@login_required(login_url = 'login')
def userProfile(request, pk):
    title_page = 'Profile'

    form = UserChangePassword(user=request.user)

    user = User.objects.get(id=pk)
    activity_list = UserActivity.objects.filter(user=user).order_by('-timestamp')
    
    if user.username != str(request.user):
        return redirect('error-403')
    
    if request.method == 'POST':
        ip, is_routable = get_client_ip(request)
        if ip is None:
            # Unable to get the client's IP address
            ip = '0.0.0.0'
        else:
            # We got the client's IP address
            if is_routable:
                # The client's IP address is publicly routable on the Internet
                ipv = 'Public'
            else:
                # The client's IP address is private
                ipv = 'Private'

        form = UserChangePassword(user=request.user, data=request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = request.user
            ip = request.META.get('REMOTE_ADDR')
            UserActivity.objects.create(
                user = username, 
                ip_address = ip + ', ' + ipv,  
                action = 'Change password',
                modification = 'User changed password',
                url = request.path
            )

            user.save()
            messages.success(request, 'Password has been changed successfully')
            # Update the session to prevent automatic logouts
            update_session_auth_hash(request, user)
            logout(request)
            return redirect('login')
        else:
            messages.error(request, 'Current password do not match.')

    context = {
        'user': user,
        'activity_list': activity_list,
        'form': form
        }
    return render(request, 'base/users-profile.html', context)

# Try tracking in index page
def demoTracking(request):
    title_page = 'Tracking demo'
    if request.method == "POST":
        get_tracking_number = request.POST.get('tracking_number')
        tracking_number = json.loads(getAutoTrackingResults(get_tracking_number))

        # ----------------------------------- Shipment -----------------------------------
        if tracking_number["data"]["trackings"][0]["shipment"]["delivery"]["estimatedDeliveryDate"] is not None:
            date_format = dateConverter(tracking_number["data"]["trackings"][0]["shipment"]["delivery"]["estimatedDeliveryDate"])
            tracking_number["data"]["trackings"][0]["shipment"]["delivery"]["estimatedDeliveryDateFormat"] = date_format
        # ----------------------------------------------------------------------

        # ----------------------------------- Statistics -----------------------------------
        if tracking_number["data"]["trackings"][0]["statistics"]["timestamps"]["infoReceivedDatetime"] is not None:
            date_format = dateConverter(tracking_number["data"]["trackings"][0]["statistics"]["timestamps"]["infoReceivedDatetime"])
            time_format = timeConverter(tracking_number["data"]["trackings"][0]["statistics"]["timestamps"]["infoReceivedDatetime"])
            tracking_number["data"]["trackings"][0]["statistics"]["timestamps"]["infoReceivedDateFormat"] = date_format
            tracking_number["data"]["trackings"][0]["statistics"]["timestamps"]["infoReceivedTimeFormat"] = time_format
            
        if tracking_number["data"]["trackings"][0]["statistics"]["timestamps"]["inTransitDatetime"] is not None:
            date_format = dateConverter(tracking_number["data"]["trackings"][0]["statistics"]["timestamps"]["inTransitDatetime"])
            time_format = timeConverter(tracking_number["data"]["trackings"][0]["statistics"]["timestamps"]["inTransitDatetime"])
            tracking_number["data"]["trackings"][0]["statistics"]["timestamps"]["inTransitDateFormat"] = date_format
            tracking_number["data"]["trackings"][0]["statistics"]["timestamps"]["inTransitTimeFormat"] = time_format

        if tracking_number["data"]["trackings"][0]["statistics"]["timestamps"]["outForDeliveryDatetime"] is not None:
            date_format = dateConverter(tracking_number["data"]["trackings"][0]["statistics"]["timestamps"]["outForDeliveryDatetime"])
            time_format = timeConverter(tracking_number["data"]["trackings"][0]["statistics"]["timestamps"]["outForDeliveryDatetime"])
            tracking_number["data"]["trackings"][0]["statistics"]["timestamps"]["outForDeliveryDateFormat"] = date_format
            tracking_number["data"]["trackings"][0]["statistics"]["timestamps"]["outForDeliveryTimeFormat"] = time_format

        if tracking_number["data"]["trackings"][0]["statistics"]["timestamps"]["failedAttemptDatetime"] is not None:
            date_format = dateConverter(tracking_number["data"]["trackings"][0]["statistics"]["timestamps"]["failedAttemptDatetime"])
            time_format = timeConverter(tracking_number["data"]["trackings"][0]["statistics"]["timestamps"]["failedAttemptDatetime"])
            tracking_number["data"]["trackings"][0]["statistics"]["timestamps"]["failedAttemptDateFormat"] = date_format
            tracking_number["data"]["trackings"][0]["statistics"]["timestamps"]["failedAttemptTimeFormat"] = time_format

        if tracking_number["data"]["trackings"][0]["statistics"]["timestamps"]["availableForPickupDatetime"] is not None:
            date_format = dateConverter(tracking_number["data"]["trackings"][0]["statistics"]["timestamps"]["availableForPickupDatetime"])
            time_format = timeConverter(tracking_number["data"]["trackings"][0]["statistics"]["timestamps"]["availableForPickupDatetime"])
            tracking_number["data"]["trackings"][0]["statistics"]["timestamps"]["availableForPickupDateFormat"] = date_format
            tracking_number["data"]["trackings"][0]["statistics"]["timestamps"]["availableForPickupTimeFormat"] = time_format

        if tracking_number["data"]["trackings"][0]["statistics"]["timestamps"]["exceptionDatetime"] is not None:
            date_format = dateConverter(tracking_number["data"]["trackings"][0]["statistics"]["timestamps"]["exceptionDatetime"])
            time_format = timeConverter(tracking_number["data"]["trackings"][0]["statistics"]["timestamps"]["exceptionDatetime"])
            tracking_number["data"]["trackings"][0]["statistics"]["timestamps"]["exceptionDateFormat"] = date_format
            tracking_number["data"]["trackings"][0]["statistics"]["timestamps"]["exceptionTimeFormat"] = time_format

        if tracking_number["data"]["trackings"][0]["statistics"]["timestamps"]["deliveredDatetime"] is not None:
            date_format = dateConverter(tracking_number["data"]["trackings"][0]["statistics"]["timestamps"]["deliveredDatetime"])
            time_format = timeConverter(tracking_number["data"]["trackings"][0]["statistics"]["timestamps"]["deliveredDatetime"])
            tracking_number["data"]["trackings"][0]["statistics"]["timestamps"]["deliveredDateFormat"] = date_format
            tracking_number["data"]["trackings"][0]["statistics"]["timestamps"]["deliveredTimeFormat"] = time_format

        # ---------------------------------------------------------------------------------------------------------

        for trackings in tracking_number["data"]["trackings"]:
            for event in trackings['events']:
                date_format = dateConverter(event["occurrenceDatetime"])
                time_format = timeConverter(event["occurrenceDatetime"])
                event['date'] = date_format
                event['time'] = time_format
                courrier_data = Courier.objects.get(code=event['courierCode'])
                event['courierName'] = courrier_data.name

    context = {
        'title_page': title_page,
        'tracking_number': tracking_number,
        'get_tracking_number': get_tracking_number
    }
    return render(request, 'base/tracking_demo.html', context)


# Refresh one tracking number from
@login_required(login_url = 'login')
def refreshTrackingNumber(request, pk):
    if request.method == 'POST':
        tracking_number = TrackingNumber.objects.get(id=pk)
        
        # Prevents from accessing other users tracking numbers
        if str(tracking_number.user.username) != str(request.user):
            return redirect('error-403')
    
        TrackingState.objects.filter(tracking_number=tracking_number).delete()
        Statistic.objects.filter(tracking_number=tracking_number).delete()
        
        tracking_number.origin_country_code = None
        tracking_number.destination_country_code = None
        tracking_number.couriers_involved.clear()
        tracking_number.status_milestone = None
        tracking_number.estimated_delivery_date = None
        tracking_number.save()
        
        courier_selected = tracking_number.courier_selected
        
        if courier_selected == 'Auto':
            tracking_data = json.loads(getAutoTrackingResults(tracking_number.tracking_number))
            courier_code = 'Auto'
        else:
            get_courier = Courier.objects.get(code=courier_selected)
            courier_code = get_courier.code
            tracking_data = json.loads(getTrackingResultWithCourier(tracking_number.tracking_number, get_courier.code))
        
        tracker_id = tracking_data["data"]["trackings"][0]["shipment"]['shipmentId']

        # If tracking number is unable to get info, return error page
        if tracker_id == None or tracker_id == '':
            messages.error(request, 'Unable to check tracking number. Cameback later or select an specfic courier.')
            return redirect('add-tracking')
        
        tracking_number = TrackingNumber.objects.get(id=pk)
        tracking_number.destination_country_code = tracking_data["data"]["trackings"][0]["shipment"]["destinationCountryCode"]
        tracking_number.origin_country_code = tracking_data["data"]["trackings"][0]["shipment"]["originCountryCode"]
        tracking_number.status_code = tracking_data["data"]["trackings"][0]["shipment"]["statusCode"]
        tracking_number.status_category = tracking_data["data"]["trackings"][0]["shipment"]["statusCategory"]
        tracking_number.status_milestone = tracking_data["data"]["trackings"][0]["shipment"]["statusMilestone"]
        tracking_number.estimated_delivery_date = tracking_data["data"]["trackings"][0]["shipment"]["delivery"]["estimatedDeliveryDate"]
        tracking_number.save()

        # Saves all events related to tracking number
        tracking_info = TrackingNumber.objects.get(id = pk)
        for trackings in tracking_data["data"]["trackings"]:
            for events in trackings['events']:
                get_courier = Courier.objects.get(code=events['courierCode'])
                tracking_status = TrackingState.objects.create(
                    tracking_number = tracking_info,
                    status = events['status'],
                    event_tracking_number = events['eventTrackingNumber'],
                    courier = get_courier,
                    occurrence_date_time = events['occurrenceDatetime'],
                    # status_code = events['statusCode'],
                    # status_category = events['statusCategory'],
                    status_milestone = events['statusMilestone'],
                    location = events['location']
                )

                # Adds couriers involved in a tracking number
                tracking_info.couriers_involved.add(get_courier)
        
        tracking_statistics = Statistic.objects.create(
            tracking_number = tracking_info,
            info_received_date_time = tracking_data["data"]["trackings"][0]["statistics"]["timestamps"]["infoReceivedDatetime"],
            in_transit_date_time = tracking_data["data"]["trackings"][0]["statistics"]["timestamps"]["inTransitDatetime"],
            outFor_delivery_date_time = tracking_data["data"]["trackings"][0]["statistics"]["timestamps"]["outForDeliveryDatetime"],
            failed_attempt_date_time = tracking_data["data"]["trackings"][0]["statistics"]["timestamps"]["failedAttemptDatetime"],
            available_for_pickup_date_time = tracking_data["data"]["trackings"][0]["statistics"]["timestamps"]["availableForPickupDatetime"],
            exception_date_time = tracking_data["data"]["trackings"][0]["statistics"]["timestamps"]["exceptionDatetime"],
            delivered_date_time = tracking_data["data"]["trackings"][0]["statistics"]["timestamps"]["deliveredDatetime"],
        )

        return redirect('overview', pk = tracking_info.id)

    # return render(request)

def dateConverter(dateValue):
    # Converts to datetime object
    datetime_obj = datetime.datetime.fromisoformat(dateValue)
    # Extracts the date component
    extract_date = datetime_obj.date()
    # format the date component
    date_only = extract_date.strftime("%Y-%m-%d")

    return date_only

def timeConverter(dateValue):
    # Converts to datetime object 
    time_obj = datetime.datetime.fromisoformat(dateValue)
    # Extracts the time component
    extract_time = time_obj.time()
    # format the date component, 24 h format
    time_only = extract_time.strftime("%I:%M:%S")

    return time_only

def error404(request):
    title_page = 'Error 404'
    return render(request, 'base/error-404.html', {'title_page': title_page})

def error403(request):
    title_page = 'Error 403'
    return render(request, 'base/error-403.html', {'title_page': title_page})

def handler400(request, exception):
    title_page = 'Error 400'
    return render(request, 'error-400.html', {'title_page': title_page})

def handler403(request, exception):
    title_page = 'Error 403'
    return render(request, 'error-403.html', {'title_page': title_page})

def handler404(request, exception):
    title_page = 'Error 404'
    return render(request, 'error-404.html', {'title_page': title_page})

def handler500(request):
    title_page = 'Error 500'
    return render(request, 'error-500.html', {'title_page': title_page})