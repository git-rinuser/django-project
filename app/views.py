from argparse import Action
from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.viewsets import ModelViewSet
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from app.serializers import CustomerSerializer, LoginSerializer, ProcessSerializer, CategorySerializer, ProjectSerializer, UserCreateSerializer, UserSerializer, UserUpdateSerializer, WorkRecordCreateSerializer, WorkRecordSerializer
from .models import Customer, Process, Category, CustomUser, Project, WorkRecord
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.decorators import action
from django.db.models import Sum

# Create your views here.
class ProcessViewSet(ModelViewSet):
    queryset = Process.objects.all().order_by("processNo")
    serializer_class = ProcessSerializer
    permission_classes = [AllowAny]
    lookup_field = "processNo"

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all().order_by("categoryNo")
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    lookup_field = "categoryNo"

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all().order_by("customerNo")
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]
    lookup_field = "customerNo"

class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.select_related("customer").all().order_by("projectNo")
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]
    lookup_field = 'projectNo'

    @action(detail=False, methods=["get"])
    def summary(self, request):
        """プロジェクトサマリー情報を取得"""
        projects = self.get_queryset()
        total_plan_time = projects.aggregate(Sum('planTime'))['planTime__sum'] or 0
        total_result_time = projects.aggregate(Sum('resultTime'))['resultTime__sum'] or 0

        return Response({
            'total_projects' : projects.count(),
            'total_plan_time' : total_plan_time,
            'total_result_time' : total_result_time
        })
    


class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all().order_by("userNo")
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    lookup_field = "userNo"

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer

    def create(self, request, *args, **kwargs):
        print("create")
        # 通常は `ModelViewSet` が自動でバリデーションを処理します
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # バリデーションが成功した場合は、保存処理を行う
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # バリデーションが失敗した場合は、エラーを返す
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(request, username=email, password=password)
        
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data
            })
        return Response({'non_field_errors': ['メールアドレスまたはパスワードが正しくありません。']}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    if request.user.auth_token:
        request.user.auth_token.delete()
    return Response({'detail': 'ログアウトしました。'})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_view(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

class WorkRecordViewSet(ModelViewSet):
    queryset = WorkRecord.objects.select_related('user', 'project', 'project__customer', 'category', 'process').all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'create':
            return WorkRecordCreateSerializer
        return WorkRecordSerializer
    
