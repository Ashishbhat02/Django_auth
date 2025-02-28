from django.shortcuts import render,HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import User, Employee
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate 
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer , LoginSerializer , UserSerializer, DesignationSerializer, DepartmentSerializer
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.
# User = get_user_model() 
class DetailsViews(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        data = User.objects.all()
        details_serializer = UserSerializer(data , many = True)
        return Response(details_serializer.data)
    
class designationViews(APIView):
    def get(self, request):
        all_data = Employee.objects.all()
        designation_detail_serializer = DesignationSerializer(all_data , many=True)
        return Response(designation_detail_serializer.data)
    
class departmentViews(APIView):
    def get(self, request):
        all_data = Employee.objects.all()
        department_detail_serializer = DepartmentSerializer(all_data , many=True)
        return Response(department_detail_serializer.data)

class RegisterView(generics.CreateAPIView):

    perimission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    # if User.objects.filter(username=username).exists(): 
    #     return ({"detail": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST) 

class LoginView(APIView):
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email , password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user)
            # data = User.objects.all()
            # details_serializer = UserSerializer(data , many = True)
            user = authenticate(email=email, password=password)
            
            return Response({
                'refresh' : str(refresh),
                'access': str(refresh.access_token),
                'user':user_serializer.data,
                # 'user':details_serializer.data,
            })
        else:
            return Response({'detail': 'invalid credentials'})
        

