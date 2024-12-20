import hashlib
import hmac
import json
import urllib
import urllib.parse
import urllib.request
import random
import requests
from datetime import datetime
from django.conf import settings
from django.http import JsonResponse
from flask import Blueprint, request, redirect, render_template
from flask_login import login_required
from app import config

from app.vnpays.forms import PaymentForm
from app.vnpays.vnpay import vnpay_order

vnpay = Blueprint("vnpay", __name__)


def hmacsha512(key, data):
    byteKey = key.encode('utf-8')
    byteData = data.encode('utf-8')
    return hmac.new(byteKey, byteData, hashlib.sha512).hexdigest()

@vnpay.route('/vnpay', methods=['GET', 'POST'])
@login_required
def payment():
    if request.method == 'POST':
        # Process input data and build url payment
        form = PaymentForm(request.form)
        if form.validate_on_submit():
            order_type = form.order_type.data
            order_id = form.order_id.data
            amount = int(form.amount.data)
            order_desc = form.order_desc.data
            bank_code = form.bank_code.data
            language = form.language.data
            ipaddr = request.remote_addr

            print("Form Data:")
            print(f"order_type: {order_type}")
            print(f"order_id: {order_id}")
            print(f"amount: {amount}")
            print(f"order_desc: {order_desc}")
            print(f"bank_code: {bank_code}")
            print(f"language: {language}")
            print(f"ipaddr: {ipaddr}")

            # Build URL Payment
            vnp = vnpay_order()
            vnp.requestData['vnp_Version'] = '2.1.0'
            vnp.requestData['vnp_Command'] = 'pay'
            vnp.requestData['vnp_TmnCode'] = config.VNPAY_TMN_CODE
            vnp.requestData['vnp_Amount'] = amount * 100
            vnp.requestData['vnp_CurrCode'] = 'VND'
            vnp.requestData['vnp_TxnRef'] = order_id
            vnp.requestData['vnp_OrderInfo'] = order_desc
            vnp.requestData['vnp_OrderType'] = order_type
            # Check language, default: vn
            if language and language != '':
                vnp.requestData['vnp_Locale'] = language
            else:
                vnp.requestData['vnp_Locale'] = 'vn'
                # Check bank_code, if bank_code is empty, customer will be selected bank on VNPAY
            if bank_code and bank_code != "":
                vnp.requestData['vnp_BankCode'] = bank_code

            vnp.requestData['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')  # 20150410063022
            vnp.requestData['vnp_IpAddr'] = ipaddr
            vnp.requestData['vnp_ReturnUrl'] = config.VNPAY_RETURN_URL
            vnpay_payment_url = vnp.get_payment_url(config.VNPAY_PAYMENT_URL, config.VNPAY_HASH_SECRET_KEY)
            print(vnpay_payment_url)
            return redirect(vnpay_payment_url)
        else:
            print("Form input not validate")
    else:
        return render_template("payment.html", title="Thanh toán")


def payment_ipn():
    inputData = request.GET
    if inputData:
        vnp = vnpay_order()
        vnp.responseData = inputData.dict()
        order_id = inputData['vnp_TxnRef']
        amount = inputData['vnp_Amount']
        order_desc = inputData['vnp_OrderInfo']
        vnp_TransactionNo = inputData['vnp_TransactionNo']
        vnp_ResponseCode = inputData['vnp_ResponseCode']
        vnp_TmnCode = inputData['vnp_TmnCode']
        vnp_PayDate = inputData['vnp_PayDate']
        vnp_BankCode = inputData['vnp_BankCode']
        vnp_CardType = inputData['vnp_CardType']
        if vnp.validate_response(config.VNPAY_HASH_SECRET_KEY):
            # Check & Update Order Status in your Database
            # Your code here
            firstTimeUpdate = True
            totalamount = True
            if totalamount:
                if firstTimeUpdate:
                    if vnp_ResponseCode == '00':
                        print('Payment Success. Your code implement here')
                    else:
                        print('Payment Error. Your code implement here')

                    # Return VNPAY: Merchant update success
                    result = JsonResponse({'RspCode': '00', 'Message': 'Confirm Success'})
                else:
                    # Already Update
                    result = JsonResponse({'RspCode': '02', 'Message': 'Order Already Update'})
            else:
                # invalid amount
                result = JsonResponse({'RspCode': '04', 'Message': 'invalid amount'})
        else:
            # Invalid Signature
            result = JsonResponse({'RspCode': '97', 'Message': 'Invalid Signature'})
    else:
        result = JsonResponse({'RspCode': '99', 'Message': 'Invalid request'})

    return result

@vnpay.route("/payment_return", methods=["GET"])
@login_required
def payment_return():
    inputData = request.GET
    if inputData:
        vnp = vnpay_order()
        vnp.responseData = inputData.dict()
        order_id = inputData['vnp_TxnRef']
        amount = int(inputData['vnp_Amount']) / 100
        order_desc = inputData['vnp_OrderInfo']
        vnp_TransactionNo = inputData['vnp_TransactionNo']
        vnp_ResponseCode = inputData['vnp_ResponseCode']
        vnp_TmnCode = inputData['vnp_TmnCode']
        vnp_PayDate = inputData['vnp_PayDate']
        vnp_BankCode = inputData['vnp_BankCode']
        vnp_CardType = inputData['vnp_CardType']
        if vnp.validate_response(config.VNPAY_HASH_SECRET_KEY):
            if vnp_ResponseCode == "00":
                return render_template("payment_return.html",
                                       title="Kết quả thanh toán",
                                       result="Thành công",
                                       order_id=order_id,
                                       amount=amount,
                                       order_desc=order_desc,
                                       vnp_TransactionNo=vnp_TransactionNo,
                                       vnp_ResponseCode=vnp_ResponseCode)
            else:
                return render_template("payment_return.html",
                                       title="Kết quả thanh toán",
                                       result="Lỗi",
                                       order_id=order_id,
                                       amount=amount,
                                       order_desc=order_desc,
                                       vnp_TransactionNo=vnp_TransactionNo,
                                       vnp_ResponseCode=vnp_ResponseCode)
        else:
            return render_template("payment_return.html",
                                   title="Kết quả thanh toán",
                                   result="Lỗi",
                                   order_id=order_id,
                                   amount=amount,
                                   order_desc=order_desc,
                                   vnp_TransactionNo=vnp_TransactionNo,
                                   vnp_ResponseCode=vnp_ResponseCode,
                                   msg="Sai checksum")
    else:
        return render_template("payment_return.html",
                               title="Kết quả thanh toán",
                               result="",
                               msg="Không nhận được dữ liệu từ VNPAY")


def get_client_ip():
    return request.headers.get('X-Forwarded-For', request.remote_addr)

n = random.randint(10**11, 10**12 - 1)
n_str = str(n)
while len(n_str) < 12:
    n_str = '0' + n_str


def query():
    if request.method == 'GET':
        return render_template(request, "query.html", title="Kiểm tra kết quả giao dịch")

    url = config.VNPAY_API_URL
    secret_key = config.VNPAY_HASH_SECRET_KEY
    vnp_TmnCode = config.VNPAY_TMN_CODE
    vnp_Version = '2.1.0'

    vnp_RequestId = n_str
    vnp_Command = 'querydr'
    vnp_TxnRef = request.POST['order_id']
    vnp_OrderInfo = 'kiem tra gd'
    vnp_TransactionDate = request.POST['trans_date']
    vnp_CreateDate = datetime.now().strftime('%Y%m%d%H%M%S')
    vnp_IpAddr = request.remote_addr

    hash_data = "|".join([
        vnp_RequestId, vnp_Version, vnp_Command, vnp_TmnCode,
        vnp_TxnRef, vnp_TransactionDate, vnp_CreateDate,
        vnp_IpAddr, vnp_OrderInfo
    ])

    secure_hash = hmac.new(secret_key.encode(), hash_data.encode(), hashlib.sha512).hexdigest()

    data = {
        "vnp_RequestId": vnp_RequestId,
        "vnp_TmnCode": vnp_TmnCode,
        "vnp_Command": vnp_Command,
        "vnp_TxnRef": vnp_TxnRef,
        "vnp_OrderInfo": vnp_OrderInfo,
        "vnp_TransactionDate": vnp_TransactionDate,
        "vnp_CreateDate": vnp_CreateDate,
        "vnp_IpAddr": vnp_IpAddr,
        "vnp_Version": vnp_Version,
        "vnp_SecureHash": secure_hash
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_json = json.loads(response.text)
    else:
        response_json = {"error": f"Request failed with status code: {response.status_code}"}

    return render_template(request, "query.html", title="Kiểm tra kết quả giao dịch", response_json= response_json)

def refund():
    if request.method == 'GET':
        return render_template(request, "refund.html", title="Hoàn tiền giao dịch")

    url = config.VNPAY_API_URL
    secret_key = config.VNPAY_HASH_SECRET_KEY
    vnp_TmnCode = config.VNPAY_TMN_CODE
    vnp_RequestId = n_str
    vnp_Version = '2.1.0'
    vnp_Command = 'refund'
    vnp_TransactionType = request.POST['TransactionType']
    vnp_TxnRef = request.POST['order_id']
    vnp_Amount = request.POST['amount']
    vnp_OrderInfo = request.POST['order_desc']
    vnp_TransactionNo = '0'
    vnp_TransactionDate = request.POST['trans_date']
    vnp_CreateDate = datetime.now().strftime('%Y%m%d%H%M%S')
    vnp_CreateBy = 'user01'
    vnp_IpAddr = request.remote_addr

    hash_data = "|".join([
        vnp_RequestId, vnp_Version, vnp_Command, vnp_TmnCode, vnp_TransactionType, vnp_TxnRef,
        vnp_Amount, vnp_TransactionNo, vnp_TransactionDate, vnp_CreateBy, vnp_CreateDate,
        vnp_IpAddr, vnp_OrderInfo
    ])

    secure_hash = hmac.new(secret_key.encode(), hash_data.encode(), hashlib.sha512).hexdigest()

    data = {
        "vnp_RequestId": vnp_RequestId,
        "vnp_TmnCode": vnp_TmnCode,
        "vnp_Command": vnp_Command,
        "vnp_TxnRef": vnp_TxnRef,
        "vnp_Amount": vnp_Amount,
        "vnp_OrderInfo": vnp_OrderInfo,
        "vnp_TransactionDate": vnp_TransactionDate,
        "vnp_CreateDate": vnp_CreateDate,
        "vnp_IpAddr": vnp_IpAddr,
        "vnp_TransactionType": vnp_TransactionType,
        "vnp_TransactionNo": vnp_TransactionNo,
        "vnp_CreateBy": vnp_CreateBy,
        "vnp_Version": vnp_Version,
        "vnp_SecureHash": secure_hash
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_json = json.loads(response.text)
    else:
        response_json = {"error": f"Request failed with status code: {response.status_code}"}

    return render_template(request, "refund.html", title="Kết quả hoàn tiền giao dịch", response_json=response_json)