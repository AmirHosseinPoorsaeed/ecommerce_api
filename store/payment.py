import requests
import json

from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404

from rest_framework.response import Response

from .models import Order


DOLLAR_TO_TOMAN = 500_000


def payment_process(request, order):
    dollar_total_price = order.total_price
    rial_total_price = round(float(dollar_total_price) * DOLLAR_TO_TOMAN, 0)

    zarinpal_request_url = 'https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json'

    request_header = {
        "accept": "application/json",
        "content-type": "application/json",
    }

    request_data = {
        'MerchantID': 'aaabbbaaabbbaaabbbaaabbbaaabbbaaabbb',
        'Amount': rial_total_price,
        'Description': f'#{order.id}: {order.customer.user.first_name} {order.customer.user.last_name}',
        'CallbackURL': request.build_absolute_uri(reverse('order-callback')),
    }

    response = requests.post(
        url=zarinpal_request_url,
        data=json.dumps(request_data),
        headers=request_header
    )

    data = response.json()

    authority = data['Authority']
    order.zarinpal_authority = authority
    order.save()

    if 'errors' not in data or len(data['errors']) == 0:
        return redirect(f'https://sandbox.zarinpal.com/pg/StartPay/{authority}')
    else:
        return Response('Error from zarinpal')


def payment_callback(request):
    payment_authority = request.GET.get('Authority')
    payment_status = request.GET.get('Status')

    order = get_object_or_404(Order, zarinpal_authority=payment_authority)

    dollar_total_price = order.total_price
    rial_total_price = round(float(dollar_total_price) * DOLLAR_TO_TOMAN, 0)

    if payment_status == 'OK':
        request_header = {
            "accept": "application/json",
            "content-type": "application/json",
        }

        request_data = {
            'MerchantID': 'aaabbbaaabbbaaabbbaaabbbaaabbbaaabbb',
            'Amount': rial_total_price,
            'Authority': payment_authority,
        }

        response = requests.post(
            url='https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json',
            data=json.dumps(request_data),
            headers=request_header
        )

        if 'errors' not in response.json():
            data = response.json()
            payment_code = data['Status']

            if payment_code == 100:
                order.status = Order.ORDER_STATUS_PAID
                order.zarinpal_ref_id = data['RefID']
                order.zarinpal_data = data
                order.save()

                return Response('پرداخت شما با موفقیت انجام شد.')

            elif payment_code == 101:
                return Response('پرداخت شما با موفقیت انجام شد. این تراکنش قبلا ثبت شده است.')

            else:
                error_code = response.json()['errors']['code']
                error_message = response.json()['errors']['message']
                return Response(f'تراکنش ناموفق بود {error_message} {error_code}')
    else:
        return Response('تراکنش ناموفق بود')
