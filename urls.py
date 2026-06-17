# coding: utf-8
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView # لاستيراد أداة التحويل التلقائي للروابط
from views import customer_dashboard, upload_deposit_receipt

urlpatterns = [
    # توجيه الرابط الرئيسي للموقع تلقائياً إلى لوحة التحكم
    path('', RedirectView.as_view(url='dashboard/', permanent=False)),
    
    path('admin/', admin.site.urls),  # لوحة تحكم الإدارة
    path('dashboard/', customer_dashboard, name='customer_dashboard'),  # لوحة تتبع الزبون
    path('upload-receipt/', upload_deposit_receipt, name='upload_deposit_receipt'),  # رفع الحوالة
]
