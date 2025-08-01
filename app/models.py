from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.
# 工程マスタ
class Process(models.Model):
    processNo = models.IntegerField(primary_key=True)
    processName = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = "Process"
        verbose_name = "工程"

    def __str__(self):
        return f"{self.processNo}:{self.processName}"

# 作業分類マスタ
class Category(models.Model):
    categoryNo = models.CharField(max_length=2, primary_key=True)
    categoryName = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = "Category"
        verbose_name = "作業分類"

    def __str__(self):
        return f"{self.categoryNo}:{self.categoryName}"

# 顧客マスタ
class Customer(models.Model):
    customerNo = models.IntegerField(primary_key=True)
    customerName = models.CharField(max_length=255,null=True, blank=True)

    class Meta:
        db_table = "Customer"
        verbose_name = "顧客"

    def __str__(self):
        return self.customerName or f"Customer{self.customerNo}"

# プロジェクトマスタ
class Project(models.Model):
    projectNo = models.CharField(max_length=5, primary_key=True)
    projectName = models.CharField(max_length=255, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, to_field='customerNo', db_column='customerNo')
    planTime = models.IntegerField(default=0)
    resultTime = models.IntegerField(default=0)

    class Meta:
        db_table = "Project"
        verbose_name = "プロジェクト"

    def __str__(self):
        return f"{self.projectNo}:{self.projectName}"

# 部員マスタ
class CustomUserManager(BaseUserManager):
    def create_user(self, userNo, userName, email, password=None, **extra_fields):
        if not email:
            raise ValueError("メールアドレスは必須です")
        email = self.normalize_email(email)
        user = self.model(userNo=userNo, userName=userName, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, userNo, userName, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(userNo, userName, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    userNo = models.CharField(max_length=10, unique=True)
    userName = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    sortNo = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['userNo','userName']


    class Meta:
        db_table = "Members"
        verbose_name = "部員"

    def __str__(self):
        return self.userName

class WorkRecord(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, to_field='userNo', db_column='userNo')
    workDay = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, to_field='projectNo', db_column='projectNo')
    customerNo = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, to_field='categoryNo', db_column='categoryNo')
    process = models.ForeignKey(Process, on_delete=models.CASCADE, to_field='processNo', db_column='processNo')
    planTime = models.IntegerField()
    resultTime = models.IntegerField()

    class Meta:
        db_table = 'WorkRecord'

    def __str__(self):
        return f"{self.user.userName} - {self.workDay} - {self.project.projectName} - {self.process.processName}"
