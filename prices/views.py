import datetime
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import View
from azbankgateways import (
    bankfactories,
    models as bank_models,
    default_settings as settings,
)
import logging
from django.urls import reverse
from azbankgateways.exceptions import AZBankGatewaysException
from prices.models import Price


class PricesView(View):
    def get(self, request):
        prices = Price.objects.all()
        return render(request, 'prices/price.html', {'prices': prices})


class PayStartView(View):
    def get(self, request, id):
        price = Price.objects.get(id=id)
        session = request.session
        session['pay'] = {
            'price': price.value,
            'days': price.days,
        }
        session.save()
        return redirect('Prices:pay')


@login_required
def go_to_gateway_view(request):
    price = request.session['pay']['price']
    days = int(request.session['pay']['days'])
    amount = int(price)
    user = request.user
    # تنظیم شماره موبایل کاربر از هر جایی که مد نظر است
    user_mobile_number = f"{user.phone_number}"  # اختیاری

    factory = bankfactories.BankFactory()
    try:
        bank = (
            factory.auto_create()
        )  # or factory.create(bank_models.BankType.BMI) or set identifier
        bank.set_request(request)
        bank.set_amount(amount)
        # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
        bank.set_client_callback_url(reverse("Prices:back"))
        bank.set_mobile_number(user_mobile_number)  # اختیاری

        # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
        # پرداخت برقرار کنید.

        bank_record = bank.ready()

        # هدایت کاربر به درگاه بانک
        context = bank.get_gateway()
        return render(request, "prices/redirect_to_bank.html", context=context)
    except AZBankGatewaysException as e:
        logging.critical(e)
        return render(request, "prices/redirect_to_bank.html")


def callback_gateway_view(request):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    days = int(request.session['pay']['days'])
    user = request.user
    if not tracking_code:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
    if bank_record.is_success:
        if not user.premium_to:
            user.premium_to = datetime.datetime.now() + datetime.timedelta(days=days)
            user.is_premium = True
        else:
            user.premium_to += datetime.timedelta(days=days)
        user.save()
        return redirect('accounts:profile', user.id)

    return redirect('accounts:profile', user.id)
