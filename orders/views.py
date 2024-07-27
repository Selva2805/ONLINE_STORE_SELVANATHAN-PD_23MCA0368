from django.shortcuts import render
from django.db.models import Sum, F
from django.db.models.functions import TruncMonth
from .models import Order

def order_analysis(request):
    # Compute total revenue by month
    revenue_by_month = Order.objects.annotate(
        month=TruncMonth('order_date')
    ).values('month').annotate(
        total_revenue=Sum(F('product_price') * F('quantity'))
    ).order_by('month')

    # Compute total revenue by product
    revenue_by_product = Order.objects.values('product_id', 'product_name').annotate(
        total_revenue=Sum(F('product_price') * F('quantity'))
    ).order_by('-total_revenue')

    # Compute total revenue by customer
    revenue_by_customer = Order.objects.values('customer_id').annotate(
        total_revenue=Sum(F('product_price') * F('quantity'))
    ).order_by('-total_revenue')

    # Identify top 10 customers by revenue
    top_10_customers = revenue_by_customer[:10]

    context = {
        'revenue_by_month': revenue_by_month,
        'revenue_by_product': revenue_by_product,
        'revenue_by_customer': revenue_by_customer,
        'top_10_customers': top_10_customers,
    }

    return render(request, 'orders/analysis.html', context)