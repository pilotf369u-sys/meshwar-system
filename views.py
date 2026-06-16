# coding: utf-8
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Shipment, CustomerProfile, WalletDepositRequest

# 1. واجهة لوحة تحكم الزبون (التتبع، الفيديوهات، والتقييم)
@login_required
def customer_dashboard(request):
    customer = get_object_or_404(CustomerProfile, user=request.user)
    # جلب شحنات الزبون الحالية
    shipments = Shipment.objects.filter(customer=customer).order_by('-updated_at')
    
    return render(request, 'dashboard.html', {
        'customer': customer,
        'shipments': shipments
    })

# 2. واجهة طلب شحن المحفظة بالحوالة المالية (رفع الوصل)
@login_required
def upload_deposit_receipt(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        method = request.POST.get('method')
        image = request.FILES.get('receipt_image')
        
        customer = get_object_or_404(CustomerProfile, user=request.user)
        
        # إنشاء طلب الإيداع في السستم بانتظار موافقة الإدارة
        WalletDepositRequest.objects.create(
            customer=customer,
            amount_requested=amount,
            payment_method_used=method,
            receipt_image=image
        )
        return redirect('customer_dashboard')
        
    return render(request, 'upload_receipt.html')
