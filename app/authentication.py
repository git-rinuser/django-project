# your_app/authentication.py
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class EmailBackend(BaseBackend):
    """
    メールアドレスを使用した認証バックエンド
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # usernameパラメータにメールアドレスが渡される
            user = User.objects.get(Q(email=username) | Q(email=kwargs.get('email')))
            if user.check_password(password) and user.is_active:
                return user
        except User.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None