from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializer,UserChangePasswordSerializer,SetPasswordResetEmailSerializer,UserSetPasswordResetSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


#Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

#User Register View
class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,format = None):
        serializer = UserRegistrationSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg':'Register SuccessFully'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#User Login View
class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,format = None):
        serializer = UserLoginSerializer(data = request.data) 
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email,password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token,'msg':'Login SuccessFully'},status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or Password is not valid']}},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
#UserProfile Token Validate View
class UserProfileView(APIView):
     renderer_classes = [UserRenderer]
     permission_classes = [IsAuthenticated]
     def get(self,request,format = None):
         serializer = UserProfileSerializer(request.user)
         return Response(serializer.data, status = status.HTTP_200_OK)
  
#User Change Password
class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        
        if serializer.is_valid():
            return Response({'msg': 'Password Changed Successfully'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Set Password Reset Email View
class SetPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,format = None):
         serializer = SetPasswordResetEmailSerializer(data = request.data)
         if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset Link Send. Please check Your Register Email'},status=status.HTTP_200_OK)
         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#User Set Password Reset View
class UserSetPasswordResetView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, uid, token, format=None):
        serializer = UserSetPasswordResetSerializer(
            data=request.data,
            context={'uid': uid, 'token': token}
        )
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Password Changed Successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
