from flask import Flask, request, redirect
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def refresh():
    if request.method == 'POST':
        params = {
            'buyer': request.get_json().get('Buyer'),
            'orderId': request.get_json().get('OrderId'),
            'email': request.get_json().get('Email'),
            'returnUrl': request.get_json().get('ServerNotificationUrl'),
        }
        # jsonData = json.dumps(params)
        # jsonData should be transferred to redis server.

        # return json.dumps(params)
    return redirect("https://cpswoo.securepayments.cardpointe.com/pay?total=25.00&cf_hidden_woo_id=72&details=BEASySpecialtybathroom%7C1%7C25")