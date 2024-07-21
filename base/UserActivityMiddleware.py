import re
from django.shortcuts import redirect, render
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import User
from .models import UserActivity, TrackingNumber, DeliveryType
from ipware import get_client_ip


class UserActivityMiddleware(MiddlewareMixin):
    def process_request(self, request, **kwargs):
        # Get the path of the request
        path = request.path

        # Check if the path includes '<str:pk>'
        match = re.search(r'/(?P<pk>[^/]+)/$', path)

        if match:
            # Get the value of <str:pk>
            pk = match.group('pk')

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
                
        # Define a list of URL patterns to track
        url_patterns = [
                        {'pattern': '^tracking/list/add/', 'action': 'add tracking'},
                        {'pattern': '^tracking/list/update/', 'action': 'update tracking'},
                        {'pattern': '^tracking/list/delete/', 'action': 'delete tracking'},
                        # {'pattern': '^user-profile/change-password/', 'action': 'Change password'},
                        ]

        # Check if the current URL matches one of the patterns
        path = request.path_info.lstrip('/')
        for pattern in url_patterns: 
            if request.user.is_authenticated and re.search(pattern['pattern'], path) and request.method == 'POST':
                if pattern['pattern'] == '^tracking/list/update/':
                    tracking_info = TrackingNumber.objects.get(id=pk)
                    delivery_type = DeliveryType.objects.get(id=request.POST.get('delivery_type'))
                    # Log the activity in the UserActivity model
                    if  str(tracking_info.user.username) != str(request.user):
                        return redirect('error-403')
                    print('Entered update-tracking')
                    print(request)
                    username = request.user
                    # ip = request.META.get('REMOTE_ADDR')
                    # ip_client_data = json.loads(get_ip_client(ip))
                    UserActivity.objects.create(
                        user = username, 
                        ip_address = ip + ', ' + ipv, 
                        action = pattern['action'],
                        modification = 'Title: ' + tracking_info.title + ' changed to ' + request.POST.get('title') + '\n' + 
                                        'Tracking number: ' + tracking_info.tracking_number + ' changed to ' + request.POST.get('tracking_number') + '\n' +
                                        'Delivery type: ' + tracking_info.delivery_type.delivery_type + ' changed to ' + delivery_type.delivery_type,
                        url = request.path
                    )
                elif pattern['pattern'] == '^tracking/list/delete/':
                    tracking_info = TrackingNumber.objects.get(id=pk)
                    # Log the activity in the UserActivity model
                    if  str(tracking_info.user.username) != str(request.user):
                        return redirect('error-403')
                    print('Entered delete-tracking')
                    print(request)
                    username = request.user
                    # ip = request.META.get('REMOTE_ADDR')
                    # ip_client_data = json.loads(get_ip_client(ip))
                    UserActivity.objects.create(
                        user = username, 
                        ip_address = ip + ', ' + ipv,
                        action = pattern['action'],
                        modification = 'Title: ' + tracking_info.title + '\n' + 
                                        'Tracking number: ' + tracking_info.tracking_number,
                        url = request.path
                    )
                elif pattern['pattern'] == '^tracking/add/':
                    delivery_type = DeliveryType.objects.get(id=request.POST.get('delivery_type'))
                    print('Entered create tracking')
                    print(request)
                    username = request.user
                    # ip = request.META.get('REMOTE_ADDR')
                    # ip_client_data = json.loads(get_ip_client(ip))
                    UserActivity.objects.create(
                        user = username, 
                        ip_address = ip + ', ' + ipv, 
                        action = pattern['action'],
                        modification = 'Title: ' + request.POST.get('title') + '\n' + 
                                        'Tracking number: ' + request.POST.get('tracking_number') + '\n' +
                                        'Delivery type: ' + delivery_type.delivery_type,
                        url = request.path
                    )
                # elif pattern['pattern'] == '^user-profile/change-password/':
                #     print('User cahnge')
                #     print(request)
                #     username = request.user
                #     ip = request.META.get('REMOTE_ADDR')
                #     ip_client__data = json.loads(get_ip_client(ip))
                #     UserActivity.objects.create(
                #         user = username, 
                #         ip_address = ip, 
                #         action = pattern['action'],
                #         modification = 'User changed password',
                #         url = request.path
                #     )
        return None