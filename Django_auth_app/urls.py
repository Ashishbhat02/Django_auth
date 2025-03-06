from django.contrib import admin
from django.urls import path,include

from Django_auth_app import views

urlpatterns = [
    # path('employees/', views.home , name='home'),
     path('reg/', views.RegisterView.as_view()),
     path('login/', views.LoginView.as_view()),
     path('emp_details/', views.DetailsViews.as_view()),
     path('emp_designation/', views.designationViews.as_view()),
     path('emp_department/', views.departmentViews.as_view()),
     path('get_s3/', views.S3BucketView.as_view()),
     path('get_ec2/', views.EC2InstanceView.as_view()),


]
