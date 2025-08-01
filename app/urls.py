from django.urls import include, path
from rest_framework import routers
from app import views

router = routers.DefaultRouter()
router.register("process", views.ProcessViewSet)
router.register("category", views.CategoryViewSet)
router.register("user", views.UserViewSet)
router.register("customer", views.CustomerViewSet)
router.register("project", views.ProjectViewSet)
router.register("work-record", views.WorkRecordViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/login/", views.login_view),
    path("auth/logout/",views.logout_view), 
    path("auth/user/", views.user_view)
]