from flask import Flask, request, redirect, jsonify
from flask_redis import FlaskRedis
import redis
import os
from flask_session import Session


app = Flask(__name__)
# README: where is the best spot to include redis db calls?
# A separated interface?
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.secret_key = '12341234'
r = redis.from_url(os.environ.get("REDIS_URL"))
server_session = Session(app)
@app.route('/data', methods=['GET', 'POST'])
def refresh():
    if request.method == 'POST':
        woo_id = request.form['woo_id']
        price = request.form['total_amount']
        order_details = request.form['order']
        datadict = {
            "woo_id": woo_id,
            "price": 'total_amount',
            "order_details": order_details
        }

        server_session.set('orderID', woo_id)
        server_session.hmset("orders_", datadict)
        return "https://cpswoo.securepayments.cardpointe.com/pay?total="+price+"&cf_hidden_woo_id="+woo_id+"&details="+order_details, 200

        # jsonData = json.dumps(params)
        # jsonData should be transferred to redis server.

        # return json.dumps(params)
    return "https://cpswoo.securepayments.cardpointe.com/pay?total=25.00&cf_hidden_woo_id=72&details=BEASySpecialtybathroom%7C1%7C25", 200