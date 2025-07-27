from rest_framework import serializers
from .models import Customer, Process, Category, CustomUser, Project

class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['customerNo', 'customerName']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        read_only_fields = [ 'userNo' ]

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['userNo', 'userName', 'email', 'password', 'sortNo', 'is_active', 'is_staff', 'is_superuser']

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['userNo', 'userName', 'email', 'sortNo', 'is_active', 'is_staff', 'is_superuser']

    def validate_userNo(self, value):
        # 自分以外で同じuserNoが存在するかチェック
        instance = getattr(self, 'instance', None)
        if instance and instance.userNo != value:
            if CustomUser.objects.filter(userNo=value).exists():
                raise serializers.ValidationError("このユーザーNoは既に使用されています。")
        return value
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

