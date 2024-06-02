from django.contrib import admin
from django.urls import path
from sitapp import views

urlpatterns = [
   path('',views.home,name='home'),
#  path('login/',views.login_user,name='login'),
   path('logout',views.logout_user,name='logout'),
   path('quote_v1/',views.quote_form_v1,name='q1'),
   path('bill_v1/',views.bill_v1,name='b1'),
   path('los/',views.los,name='los'),
   path('los2/',views.los2,name='los2'),
   path('vi/',views.quote,name='q'),
   path('vi2/',views.bill,name='b'),
   path('history/',views.history,name='history'),
   path('updatequote/<int:id>',views.updatequote,name='updatequote'),
   path('updatequotedata/',views.updatequotedata,name='updatequotedata'),
   path('updatebill/<int:id>',views.updatebill,name='updatebill'),
   path('updatebilldata/',views.updatebilldata,name='updatebilldata'),
   path('deletequote/<int:id>',views.deletequote,name='deletequote'),
   path('deletebill/<int:id>',views.deletebill,name='deletebill'),
]
