from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.shortcuts import redirect, render
from django.dispatch import receiver
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserActivity
from ipware.ip import get_client_ip

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
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
        user=user, 
        ip_address = ip + ', ' + ipv,
        action='Login', 
        url=request.path,
        modification = 'User logged in.'
    )
    
    # ip_client__data = json.loads(get_ip_client(ip))
    # if ip_client__data['message'] != 'invalid query':
    #     if ip_client__data['status'] == 'success':
    #         UserActivity.objects.create(
    #             user = user, 
    #             ip_address = ip_client__data['query'], 
    #             isp = ip_client__data['isp'],
    #             country = ip_client__data['country'],
    #             country_code = ip_client__data['countryCode'],
    #             location = ip_client__data['city'] + ', ' + ip_client__data['regionName'] + '('+ ip_client__data['region']+')' +', ' + ip_client__data['zip'],
    #             coordinates = ip_client__data['lat'] + ', ' + ip_client__data['lon'],
    #             action='Login', 
    #             url=request.path,
    #             modification = 'User logged in.'
    #             )
    #     else:
    #         UserActivity.objects.create(
    #             user=user, 
    #             ip_address=ip_client__data['query'], 
    #             action='Login', 
    #             url=request.path,
    #             modification = 'User logged in.'
    #             )

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
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
    print('User logged out')
    
    UserActivity.objects.create(
        user=user, 
        ip_address = ip + ', ' + ipv, 
        action='Log out', 
        url=request.path,
        modification = 'User logged in.'
    )
    # ip_client__data = json.loads(get_ip_client(ip))
    # if ip_client__data['message'] != 'invalid query':
    #     if ip_client__data['status'] == 'success':
    #         UserActivity.objects.create(
    #             user = user, 
    #             ip_address = ip_client__data['query'], 
    #             isp = ip_client__data['isp'],
    #             country = ip_client__data['country'],
    #             country_code = ip_client__data['countryCode'],
    #             location = ip_client__data['city'] + ', ' + ip_client__data['regionName'] + '('+ ip_client__data['region']+')' +', ' + ip_client__data['zip'],
    #             coordinates = ip_client__data['lat'] + ', ' + ip_client__data['lon'],
    #             action='Log out', 
    #             url=request.path,
    #             modification = 'User logged out.'
    #             )
    #     else:
    #         UserActivity.objects.create(
    #             user=user, 
    #             ip_address=ip_client__data['query'], 
    #             action='Log out', 
    #             url=request.path,
    #             modification = 'User logged in.'
    #             )

@receiver(user_login_failed)
def user_login_failed(sender, credentials, request, **kwargs):
    
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

    username = credentials.get('username')
    try:
        username = User.objects.get(username=username)

        UserActivity.objects.create(
            user=username,
            ip_address = ip + ', ' + ipv, 
            action='Login Failed', 
            url=request.path,
            modification = 'User failed to log in.'
        )
        
    except User.DoesNotExist:
        pass
    
    # ip_client__data = json.loads(get_ip_client(ip))
    # if ip_client__data['message'] != 'invalid query':
    #     try:
    #         username = User.objects.get(username=username)
    #         if ip_client__data['status'] == 'success':
    #             print('valid ip')
    #             UserActivity.objects.create(
    #                 user = username, 
    #                 ip_address = ip_client__data['query'], 
    #                 isp = ip_client__data['isp'],
    #                 country = ip_client__data['country'],
    #                 country_code = ip_client__data['countryCode'],
    #                 location = ip_client__data['city'] + ', ' + ip_client__data['regionName'] + '('+ ip_client__data['region']+')' +', ' + ip_client__data['zip'],
    #                 coordinates = ip_client__data['lat'] + ', ' + ip_client__data['lon'],
    #                 action='Login Failed', 
    #                 url=request.path,
    #                 modification = 'User failed to log in.'
    #                 )
    #         else:
    #             print('private ip')
    #             UserActivity.objects.create(
    #                 user=username,
    #                 ip_address=ip_client__data['query'], 
    #                 action='Login Failed', 
    #                 url=request.path,
    #                 modification = 'User failed to log in.'
    #                 )
                
    #     except User.DoesNotExists:
    #         pass

