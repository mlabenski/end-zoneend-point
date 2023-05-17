from flask import Flask, request, redirect, jsonify

import redis
import os
import json
import requests

app = Flask(__name__)
riot_api_key=ros.environ['RIOT_API']
# README: where is the best spot to include redis db calls?
# A separated interface?
@app.route('/seeData')
def get_the_data():
    name=db.get('orderID') or'96'
    return 'Hello there %s!' % name

@app.route('/data', methods=['GET', 'POST'])
def refresh():
    if request.method == 'POST':
        headers = request.headers
        auth = headers.get("X-Api-Key")
        print(auth)
        woo_id = str(request.form['woo_id'])
        price = str(request.form['total_amount'])
        order_details = str(request.form['order_details'])
        hpp_url = str(request.form['hpp_url'])
        shipping_total = str(request.form['shipping_total'])
        tax_total = str(request.form['tax_total'])
        string_data = "woo_id="+str(woo_id)+",price="+str(price)+",order="+str(order_details)
        print(string_data)
        print(shipping_total)
        print(tax_total)
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
        redirectUrl = str(dict_data["referer"])
        orderId = str(dict_data["cf_hidden_woo_id"])
        print("WEBHOOK RECEIVED FROM "+redirectUrl+"with the Woo Order ID of "+orderId)
        if orderId:
            res = requests.post(redirectUrl + "/wc-api/wrapper_webhook?cf_woo_id="+orderId)
            return "", 200
        return "no order ID confirmed", 405
        # jsonData = json.dumps(params)
        # jsonData should be transferred to redis server.
    else:
        return "", 403
    
@app.route('/match_history/<summoner_name>', methods=['GET', 'POST'])
def get_match_history(summoner_name):
    api_key = riot_api_key  # Replace with your actual API key
    region = 'na1'  # Replace with the desired region (e.g., 'na1' for North America)

    # Get summoner ID by summoner name
    summoner_url = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}'
    summoner_response = requests.get(summoner_url, params={'api_key': api_key})

    if summoner_response.status_code == 200:
        summoner_data = summoner_response.json()
        print(summoner_data)
        puuid = summoner_data['puuid']

        # Get match IDs by PUUID
        match_ids_url = f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids'
        match_ids_response = requests.get(match_ids_url, headers={'X-Riot-Token': api_key})
        print(match_ids_response)
        if match_ids_response.status_code == 200:
            match_ids_data = match_ids_response.json()
            print(match_ids_data)
            match_ids = match_ids_data[:5] # Retrieve the first 5 match IDs
            print(match_ids)

            detailed_matches = []
            for match_id in match_ids:
                # Get detailed match information by match ID
                match_url = f'https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}'
                match_response = requests.get(match_url, headers={'X-Riot-Token': api_key})

                if match_response.status_code == 200:
                    match_data = match_response.json()
                    detailed_matches.append(match_data)

            return jsonify(detailed_matches)
        else:
            return jsonify({'error': 'Failed to retrieve match history :('}), 404

    return jsonify({'error': 'Summoner not found.'}), 404
