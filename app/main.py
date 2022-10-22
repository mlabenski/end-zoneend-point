from flask import Flask, request, redirect, jsonify
from flask_redis import FlaskRedis


app = Flask(__name__)

@app.route('/data', methods=['GET', 'POST'])
def refresh():
    if request.method == 'POST':
        woo_id = request.form['woo_id'];
        price = request.form['total_amount']
        order_details = request.form['order']

        return "https://cpswoo.securepayments.cardpointe.com/pay?total="+price+"&cf_hidden_woo_id="+woo_id+"&details="+order_details, 200

        # jsonData = json.dumps(params)
        # jsonData should be transferred to redis server.

        # return json.dumps(params)
    return "https://cpswoo.securepayments.cardpointe.com/pay?total=25.00&cf_hidden_woo_id=72&details=BEASySpecialtybathroom%7C1%7C25", 200