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
import boto3
from django.conf import settings
# Create your views here.


# THIS API IS FOR ALL EMP_DETAILS PRESENT IN THE DB
class DetailsViews(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        data = User.objects.all()
        details_serializer = UserSerializer(data , many = True)
        return Response(details_serializer.data)
    

# THIS API IS FOR DESIGNATION WITH THERE RESPECTIVE NAME   
class designationViews(APIView):
    def get(self, request):
        all_data = Employee.objects.all()
        designation_detail_serializer = DesignationSerializer(all_data , many=True)
        return Response(designation_detail_serializer.data)

# THIS API IS FOR DEPARTMENT WITH THERE RESPECTIVE NAME   
class departmentViews(APIView):
    def get(self, request):
        all_data = Employee.objects.all()
        department_detail_serializer = DepartmentSerializer(all_data , many=True)
        return Response(department_detail_serializer.data)


#REGISTER API
class RegisterView(generics.CreateAPIView):

    perimission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    # if User.objects.filter(username=username).exists(): 
    #     return ({"detail": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST) 

#LOGIN API
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
        
# THIS API WILL GIVE THE ITEMS PRESENT IN THE S3 BUCKET


class S3BucketView(APIView):
   s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME
    )
   def get(self,request):
       aws_bucket_name = settings.AWS_STORAGE_BUCKET_NAME
       items = self.s3_client.list_objects_v2(Bucket=aws_bucket_name)
       files = [item['Key'] for item in items.get('Contents' , [])]
       if not files:
           return Response("NO FILE PRESENT IN THE BUCKET!!")
       #FOR MULTIPLE FILES
       multi_files = []
       for files_key in files:
            get_item = self.s3_client.get_object(Bucket=aws_bucket_name , Key = files_key)
            file_content = get_item['Body'].read().decode('utf-8')  # Decode for text-based files
            multi_files.append({
                "file name":files_key,
                "file content":file_content
            })
            return Response({"file":multi_files})
   
    #FOR ONLY 1 FILE 
    #    file_key = files[0]
    #    return Response({
    #         "file_name": file_key,
    #         "file_content": file_content
    #     })