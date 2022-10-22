from flask import Flask, request, redirect, jsonify

import redis
import os


app = Flask(__name__)
db=redis.from_url(os.environ['REDIS_URL'])
# README: where is the best spot to include redis db calls?
# A separated interface?
@app.route('/seeData')
def get_the_data():
    name=db.get('orderID') or'96'
    return 'Hello %s!' % name

@app.route('/data', methods=['GET', 'POST'])
def refresh():
    if request.method == 'POST':
        woo_id = int(request.form['woo_id']),
        price = str(request.form['total_amount']),
        order_details = str(request.form['order'])
        datadict = {
            "price": 'total_amount',
            "order_details": order_details
        }
        db.hset("order_id", woo_id, jsonify(datadict))
        return "https://cpswoo.securepayments.cardpointe.com/pay?total="+price+"&cf_hidden_woo_id="+woo_id+"&details="+order_details, 200

        # jsonData = json.dumps(params)
        # jsonData should be transferred to redis server.

        # return json.dumps(params)
    return "https://cpswoo.securepayments.cardpointe.com/pay?total=25.00&cf_hidden_woo_id=72&details=BEASySpecialtybathroom%7C1%7C25", 200