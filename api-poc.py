from flask import Flask, jsonify, render_template

poc = Flask(__name__)

@poc.route("/")
def home():
    return render_template ("test.html")

@poc.route("/data/<coin>")
def data(coin):
    coin_data = {"Coin": coin, "Data": f"You have selected coin {coin}"}
    return jsonify(coin_data)

if __name__ == '__main__':
    poc.run(debug=True)