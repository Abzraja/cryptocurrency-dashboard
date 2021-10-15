# Import Flask
from flask import Flask, jsonify, render_template
# Import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

## Database
db_path = "sqlite:///binance.sql"
engine = create_engine(db_path)
Base = declarative_base()

# Define kline table
class kline(Base):
    __tablename__ = "kline"

    id = Column(Integer, primary_key=True)
    coin = Column(String)
    datapoint = Column(Integer)

# Create tables
Base.metadata.create_all(engine)

## Define some temporary data for testing
session = Session(bind=engine)
data1 = kline(coin="abc", datapoint=5)
data2 = kline(coin="abc", datapoint=10)
data3 = kline(coin="def", datapoint=2)
data4 = kline(coin="ghi", datapoint=7)
data5 = kline(coin="ghi", datapoint=76)
data6 = kline(coin="ghi", datapoint=64)
session.add(data1)
session.add(data2)
session.add(data3)
session.add(data4)
session.add(data5)
session.add(data6)
session.commit()
session.close()

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
    session = Session(bind=engine)
    coins = (session
        .query(kline)
        .filter(kline.coin==coin)
        .all()
        )
    session.close()
    # Create fake dictionary to test
    coin_dict = {}
    for row in coins:
        coin_dict[row.id] = {"coin": row.coin, "value": row.datapoint}
    # Return dictionary as a JSON file for JS processing
    return(jsonify(coin_dict))

# Start Flask app
if __name__ == '__main__':
    poc.run(debug=True)