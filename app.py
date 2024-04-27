from flask import Flask, jsonify , request
import requests

app = Flask(__name__)

@app.route('/' , methods = ['POST'])
def index():
    data = request.get_json()
    source_curr = data['queryResult'] ['parameters'] ['unit-currency'] ['currency']
    amount = data['queryResult'] ['parameters'] ['unit-currency'] ['amount']
    target_curr =  data ['queryResult'] ['parameters'] ['currency-name']
    # print(source_curr)
    # print(amount)
    # print(target_curr)

    cf = fetch_conversion_factor(source_curr , target_curr)
    final_amt = amount * cf
    final_amt = round(final_amt , 2)
    response = {
        'fulfillmentText' : "{} {} is {} {}".format(amount , source_curr , final_amt , target_curr)
    }
    # print(final_amt)
    return jsonify(response)

def fetch_conversion_factor(source , target):
    url = "https://free.currconv.com/api/v7/convert?q={}_{}&compact=ultra&apiKey=11b3d034687ae1f13b19".format(source , target)
    response = requests.get(url)
    response = response.json()
    return response['{}_{}'.format(source , target)]


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

