from flask import Flask, request, redirect
from flask_redis import FlaskRedis


app = Flask(__name__)
redis_client = FlaskRedis(app)

@app.route('/', methods=['GET', 'POST'])
def refresh():
    if request.method == 'POST':
        redis_client.set('orderID', '21902')
        # jsonData = json.dumps(params)
        # jsonData should be transferred to redis server.

        # return json.dumps(params)
    return redirect("https://cpswoo.securepayments.cardpointe.com/pay?total=25.00&cf_hidden_woo_id=72&details=BEASySpecialtybathroom%7C1%7C25")