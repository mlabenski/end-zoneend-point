from flask import Flask, request, redirect, jsonify

import redis
import os
import json
import requests

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
        woo_id = str(request.form['woo_id'])
        price = str(request.form['total_amount'])
        order_details = str(request.form['order_details'])
        hpp_url = str(request.form['hpp_url'])
        string_data = "woo_id="+str(woo_id)+",price="+str(price)+",order="+str(order_details)
        print(string_data)
        # db.set("order", string_data)
        return ("https://"+str(hpp_url)+".securepayments.cardpointe.com/pay?total="+str(price)+"&cf_hidden_woo_id="+str(woo_id)+"&details="+str(order_details)), 200

        # jsonData = json.dumps(params)
        # jsonData should be transferred to redis server.

        # return json.dumps(params)
    return "https://cpswoo.securepayments.cardpointe.com/pay?total=25.00&cf_hidden_woo_id=72&details=BEASySpecialtybathroom%7C1%7C25", 200

@app.route('/callback', methods=['GET', 'POST'])
def callback_order():
    if request.method == 'POST':
        data = request.form.get('json')
        dict_data = json.loads(data)
        print(str(dict_data["merchantId"]))
        ## hard coding this value for now
        homeUrl="https://cpswoo.com"
        orderId= str(dict_data["cf_hidden_woo_id"])
        print(dict_data)
        res = requests.post(homeUrl+"/wc-api/wrapper_webhook?cf_woo_id="+orderId)
        return "", 200
        # jsonData = json.dumps(params)
        # jsonData should be transferred to redis server.
    else:
        return "", 403
