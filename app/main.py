from flask import Flask, request, redirect, jsonify
from flask_redis import FlaskRedis


app = Flask(__name__)
redis_client = FlaskRedis(app)

@app.route('/data', methods=['GET', 'POST'])
def refresh():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        returnURL = "https://cpswoo.securepayments.cardpointe.com/pay?total=25.00&cf_hidden_woo_id=72&details=BEASySpecialtybathroom%7C1%7C25"

        redis_client.set('orderID', '21902')
        result = { 'url' : 'https://cpswoo.securepayments.cardpointe.com/pay?total=25.00&cf_hidden_woo_id=72&details=BEASySpecialtybathroom%7C1%7C25'}
        return jsonify(data=returnURL)

        # jsonData = json.dumps(params)
        # jsonData should be transferred to redis server.

        # return json.dumps(params)
    return redirect("https://cpswoo.securepayments.cardpointe.com/pay?total=25.00&cf_hidden_woo_id=72&details=BEASySpecialtybathroom%7C1%7C25")