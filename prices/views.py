from django.shortcuts import render
from django.views.generic import View

from prices.models import Price


class PricesView(View):
    def get(self, request):
        prices = Price.objects.all()
        return render(request, 'prices/price.html', {'prices': prices})
