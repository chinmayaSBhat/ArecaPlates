from django.contrib import admin
from .models import Production, Stock
from django import forms
from django.db.models import Sum
from django.contrib.admin import AdminSite
from django.urls import path
from django.shortcuts import render
# Register your models here.

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display=("batch_no","supplier","quantity","delivery_date")


class ProductionAdminForm(forms.ModelForm):
    class Meta:
        model = Production
        fields = ('batch_no', 'production_date', 'quantity', 'wastage')

    def clean(self):
        cleaned_data = super().clean()
        batch_no = cleaned_data.get("batch_no")
        quantity = cleaned_data.get("quantity")

        if batch_no and quantity:
            stock_quantity = batch_no.quantity
            # stock_quantity = stock_obj.quantity
            used_quantity = Production.objects.filter(batch_no=batch_no).aggregate(Sum('quantity'))["quantity__sum"]
            if used_quantity is None:
                used_quantity=0
            available_stock = stock_quantity - used_quantity
            if quantity > available_stock:
                raise forms.ValidationError(f"Entered Quantity should be less than or equal to available stock. i.e {available_stock}")

@admin.register(Production)
class ProductionAdmin(admin.ModelAdmin):
    form = ProductionAdminForm
    list_display = ('batch_no', 'production_date', 'quantity', 'wastage')




class InventoryAdmin(admin.AdminSite):
    site_header="Inventory Admin"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('consolidated_report/', self.admin_view(self.consolidated_report))
        ]
        return my_urls + urls

    def consolidated_report(self, request):
        stocks = Stock.objects.all()
        production = Production.objects.all()

        # process data
        stock_data = {}
        for stock in stocks:
            stock_data[stock.batch_no] = stock.quantity

        production_data = {}
        for prod in production:
            if prod.batch_no.batch_no in production_data:
                production_data[prod.batch_no.batch_no] += prod.quantity
            else:
                production_data[prod.batch_no.batch_no]



inventory_admin=InventoryAdmin(name="InventoryAdmin")

inventory_admin.register(Stock,StockAdmin)
inventory_admin.register(Production,ProductionAdmin)