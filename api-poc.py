# Import Flask
from flask import Flask, jsonify, render_template

# Set app name as "poc" and start Flask
poc = Flask(__name__)

# Base route
@poc.route("/")
# Return static HTML file with JS code
# Ideally would serve from independent web server, but not practical in test environment
def home():
    return render_template ("test.html")

# An API call, specific for each coin handle
@poc.route("/data/<coin>")
def data(coin):
    # Create fake dictionary to test
    # This will be replaced by database calls
    coin_data = {"Coin": coin, "Data": f"You have selected coin {coin}"}
    # Return dictionary as a JSON file for JS processing
    return jsonify(coin_data)

# Start Flask app
if __name__ == '__main__':
    poc.run(debug=True)