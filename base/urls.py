from django.shortcuts import render
from django.urls import path


# Import views.py, root in base folder, to urls.py
from . import views

# Specific app
# Adds url patterns
urlpatterns = [
    path('', views.index, name="index"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name='register'),
    path('demo/tracking', views.demoTracking, name="tracking"),
    path('tracking/list/all', views.trackingList, name="tracking-list"),
    path('tracking/list/all-updates', views.eventList, name="event-list"),
    path('tracking/list/delivered', views.trackingDelivered, name="delivered-list"),
    path('tracking/list/delivery', views.trackingDelivery, name="delivery-list"),
    path('tracking/list/exception', views.trackingException, name="exception-list"),
    path('tracking/list/failed-attempt', views.trackingFailedAttempt, name="failed-attempt-list"),
    path('tracking/list/info-received', views.trackingInfoReceived, name="info-received-list"),
    path('tracking/list/in-transit', views.trackingInTransit, name="in-transit-list"),
    path('tracking/list/pending', views.trackingPending, name="pending-list"),
    path('tracking/list/pick-up', views.trackingPickUp, name="pick-up-list"),
    path('tracking/list/overview/<str:pk>/', views.overview, name="overview"),
    path('courier/list/', views.courierList, name='courier-list'),
    path('courier/list/<str:pk>/', views.courierPackageInvolved, name='courier-package-involved'),
    path('user-profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('tracking/add/', views.addTracking, name="add-tracking"),
    path('tracking/list/update/<str:pk>/', views.updateTracking, name="update-tracking"),
    path('tracking/list/refresh/<str:pk>/', views.refreshTrackingNumber, name="refresh-tracking"),
    path('tracking/list/delete/<str:pk>/', views.deleteTracking, name="delete-tracking"),
    path('error-404/', views.error404, name='error-404'),
    path('error-403/', views.error403, name='error-403'),
]

