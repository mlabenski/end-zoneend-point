from flask import Flask, request, redirect, jsonify
from flask_redis import FlaskRedis


app = Flask(__name__)

@app.route('/data', methods=['GET', 'POST'])
def refresh():
    if request.method == 'POST':
        data = request.get_data();
        print(data);
        return "https://cpswoo.securepayments.cardpointe.com/pay?total=25.00&cf_hidden_woo_id=72&details=BEASySpecialtybathroom%7C1%7C25", 200

        # jsonData = json.dumps(params)
        # jsonData should be transferred to redis server.

        # return json.dumps(params)
    return "https://cpswoo.securepayments.cardpointe.com/pay?total=25.00&cf_hidden_woo_id=72&details=BEASySpecialtybathroom%7C1%7C25", 200