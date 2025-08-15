from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum, F
from django.utils.dateparse import parse_date
from .models import Sale
from .forms import SaleForm
import csv
from openpyxl import Workbook

@login_required
def index(request):
    # KPIs básicos
    total_revenue = Sale.objects.aggregate(total=Sum('quantity'))['total'] or 0
    total_value = Sale.objects.aggregate(total=Sum(F('unit_price') * F('quantity')))['total'] or 0
    categories = (Sale.objects
                  .values('category')
                  .annotate(total=Sum('quantity'))
                  .order_by('-total')[:5])
    return render(request, 'dashboard/index.html', {
        'total_revenue': total_revenue,
        'total_value': total_value,
        'top_categories': categories,
    })

@login_required
def sale_list(request):
    sales = Sale.objects.all()
    return render(request, 'dashboard/sale_list.html', {'sales': sales})

@login_required
def sale_create(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:sale_list')
    else:
        form = SaleForm()
    return render(request, 'dashboard/sale_form.html', {'form': form, 'title': 'Nova Venda'})

@login_required
def sale_update(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        form = SaleForm(request.POST, instance=sale)
        if form.is_valid():
            form.save()
            return redirect('dashboard:sale_list')
    else:
        form = SaleForm(instance=sale)
    return render(request, 'dashboard/sale_form.html', {'form': form, 'title': 'Editar Venda'})

@login_required
def sale_delete(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        sale.delete()
        return redirect('dashboard:sale_list')
    return render(request, 'dashboard/sale_delete.html', {'sale': sale})

@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="vendas.csv"'
    writer = csv.writer(response)
    writer.writerow(['data', 'produto', 'categoria', 'preco_unitario', 'quantidade', 'total'])
    for s in Sale.objects.all().order_by('date'):
        writer.writerow([s.date, s.product, s.category, f"{s.unit_price:.2f}", s.quantity, f"{s.total:.2f}"])
    return response

@login_required
def export_xlsx(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Vendas"
    ws.append(['data', 'produto', 'categoria', 'preco_unitario', 'quantidade', 'total'])
    for s in Sale.objects.all().order_by('date'):
        ws.append([s.date.isoformat(), s.product, s.category, float(s.unit_price), s.quantity, float(s.total)])
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="vendas.xlsx"'
    wb.save(response)
    return response

@login_required
def sales_summary_api(request):
    # Retorna dados agregados por mês para os gráficos (últimos 6 meses)
    from django.db.models.functions import TruncMonth
    qs = (Sale.objects
          .annotate(month=TruncMonth('date'))
          .values('month')
          .annotate(total=Sum(Sale._meta.get_field('quantity').model.objects.filter(id=F('id')).values('quantity')))
          )
    # Alternativa simples: somar valores por mês manualmente
    data = (
        Sale.objects
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(qty=Sum('quantity'), value=Sum(F('unit_price') * F('quantity')))
        .order_by('month')
    )
    labels = [d['month'].strftime('%b/%Y') if d['month'] else '' for d in data]
    qty = [d['qty'] or 0 for d in data]
    value = [float(d['value'] or 0) for d in data]
    return JsonResponse({'labels': labels, 'qty': qty, 'value': value})
