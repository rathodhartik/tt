
from django.contrib import admin
from django.urls import path,include
from myapp import views
from django.contrib.auth import views as Av
from rest_framework_simplejwt import views as jv

from rest_framework_swagger.views import get_swagger_view  # <-- Here
schema_view = get_swagger_view(title='rishi API')

from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

from rest_framework import routers

Person_list = views.PersonViewset.as_view({
    'get': 'list',
    'post': 'create'
})

Person_detail = views.PersonViewset.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = [
    path('admin/', admin.site.urls),
    # """Home Page"""
    path('', views.home, name='home'),
    path('main/', views.main, name='main'),
    
    #Login or sign up using google
    path('accounts/', include('allauth.urls')),

    # """Sign Up Url"""
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_user, name='logout'),

    # """Chhange Passowrd Url"""
    path('change_password/', views.change_password, name='change_password'),

    # """Reset Password Url"""
    path('reset-password', Av.PasswordResetView.as_view(), name='password_reset'),
    path('reset-password/done', Av.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/',Av.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password/complete/', Av.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    
    # """Data Operation Crud through Web Templates"""
    path('Reg_View/', views.Reg_View, name='Reg_View'),
    path('ListView/', views.list_view, name='ListView'),
    path('Update/<int:id>', views.update_view, name='Update'),
    path('delete/<int:id>', views.delete_view, name='delete'),
    path('search', views.search, name='search'),

    # """JWT Web TOken Authentication URl"""
    path('api/token/', jv.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jv.TokenRefreshView.as_view(), name='token_refresh'),

    # """API CRUD Operation using serialization throught REST API URL"""
    path('api-auth/', include('rest_framework.urls')),
    path('Userlist/', views.ListUsers.as_view(), name='Userlist'),
    
    path('Data/', Person_list, name='Data'),
    path('Data/<int:pk>', Person_detail, name='Datadetail'),
    
    #""" API Documents using swagger"""
    path('docs/', schema_view,name='docs'),

    path('c/', views.Data.as_view(),),
    # path('c/<int:obj>', views.Datadetail.as_view()),
]