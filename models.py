# coding: utf-8
from django.db import models
from django.contrib.auth.models import User

# 1. الموظفون
class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="الموظف")
    phone_number = models.CharField(max_length=20, verbose_name="رقم الواتساب الفعال")
    role = models.CharField(max_length=50, choices=[('Admin', 'مدير عام'), ('Staff', 'موظف فرع')], verbose_name="الصلاحية")

    class Meta:
        app_label = 'meshwar_system'

    def __str__(self):
        return f"{self.user.username} - {self.role}"

# 2. المندوبون
class Courier(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم المندوب المحلي")
    phone = models.CharField(max_length=20, verbose_name="رقم هاتفه")
    assigned_province = models.CharField(max_length=100, verbose_name="المحافظة المسؤول عنها")

    class Meta:
        app_label = 'meshwar_system'

    def __str__(self):
        return f"المندوب: {self.name} ({self.assigned_province})"

# 3. الزبائن والمحفظة
class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="حساب الزبون")
    current_country = models.CharField(max_length=50, choices=[('Turkey', 'تركيا'), ('Iraq', 'العراق')], verbose_name="بلد الإقامة الحالي")
    city_province = models.CharField(max_length=100, verbose_name="المحافظة / الولاية")
    address_details = models.TextField(verbose_name="العنوان التفصيلي")

    class Meta:
        app_label = 'meshwar_system'

    def __str__(self):
        return self.user.username

class CustomerWallet(models.Model):
    customer = models.OneToOneField(CustomerProfile, on_delete=models.CASCADE, verbose_name="الزبون")
    available_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="الرصيد المتاح ($)")
    reward_points = models.IntegerField(default=0, verbose_name="نقاط المكافآت")

    class Meta:
        app_label = 'meshwar_system'

# 4. طلبات الإيداع
class WalletDepositRequest(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, verbose_name="الزبون")
    amount_requested = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="المبلغ المحول ($)")
    receipt_image = models.ImageField(upload_to='receipts/', verbose_name="صورة وصل الحوالة")
    payment_method_used = models.CharField(max_length=150, verbose_name="الحساب أو الموظف المحول إليه")
    status = models.CharField(max_length=50, choices=[('Pending', 'بانتظار المراجعة'), ('Approved', 'تم التأكيد'), ('Rejected', 'تم الرفض')], default='Pending', verbose_name="حالة الطلب")
    admin_notes = models.TextField(blank=True, null=True, verbose_name="ملاحظات الإدارة")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'meshwar_system'

# 5. الحركات المالية
class WalletTransaction(models.Model):
    wallet = models.ForeignKey(CustomerWallet, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=50, choices=[('Deposit', 'إيداع'), ('Shipping_Payment', 'أجور شحن')])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'meshwar_system'

# 6. الشحنات
class Shipment(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, verbose_name="صاحب الشحنة")
    tracking_number = models.CharField(max_length=100, unique=True, verbose_name="رقم التتبع")
    weight_kg = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="الوزن (كغم)")
    base_shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="التكلفة الأساسية ($)")
    adjustment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="تعديل السعر ($)")
    current_status = models.CharField(max_length=50, choices=[('1_received_ankara', '1. استلام أنقرة'), ('2_sorting', '2. الفرز'), ('3_loading', '3. التحميل'), ('4_on_the_way', '4. في الطريق'), ('5_customs', '5. الجمارك'), ('6_received_dest_warehouse', '6. مستودع الوجهة'), ('7_with_courier', '7. مع المندوب'), ('8_delivered', '8. تم التسليم'), ('9_returned', '9. مرتجع')], default='1_received_ankara', verbose_name="الحالة")
    assigned_courier = models.ForeignKey(Courier, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="المندوب")
    instructional_video_url = models.URLField(blank=True, null=True, verbose_name="رابط الفيديو")
    show_ads = models.BooleanField(default=True, verbose_name="تفعيل الإعلانات")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخر تحديث")

    class Meta:
        app_label = 'meshwar_system'

    @property
    def final_cost(self):
        return self.base_shipping_cost + self.adjustment_amount
