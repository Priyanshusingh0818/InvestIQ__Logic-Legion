from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import yfinance as yf
from textblob import TextBlob
from datetime import datetime, timedelta
import mysql.connector
from mysql.connector import Error
import os
import random  
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

DB_CONFIG = {
    'host': 'localhost',
    'database': 'StockApp',
    'user': 'root',  
    'password': 'Warsha@1980'   
}

def create_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

def initialize_database():
    try:
        connection = create_db_connection()
        if connection and connection.is_connected():
            cursor = connection.cursor()
            
            create_table_query = """
            CREATE TABLE IF NOT EXISTS sentimentanalysis (
                id INT AUTO_INCREMENT PRIMARY KEY,
                stock_symbol VARCHAR(10) NOT NULL,
                sentiment_date DATE NOT NULL,
                sentiment_score FLOAT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            cursor.execute(create_table_query)
            connection.commit()
            print("Database initialized successfully!")
            
            cursor.close()
            connection.close()
    except Error as e:
        print(f"Error initializing database: {e}")

def load_sentiment_data():
    try:
        # Updated file path to use the correct filename
        file_path = os.path.join(os.path.dirname(__file__), '..', 'stock_market_sentiment.csv')
        print(f"Loading sentiment data from: {file_path}")
        
        sentiment_data = pd.read_csv(file_path)
        
        print(f"Dataset loaded successfully. Shape: {sentiment_data.shape}")
        print(f"Columns: {sentiment_data.columns.tolist()}")
        
        return sentiment_data
    except Exception as e:
        print(f"Error loading sentiment data: {e}")
        return pd.DataFrame()  # Return empty DataFrame if file not found

sentiment_dataset = None

def get_stock_data(symbol):
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        stock = yf.Ticker(symbol)
        df = stock.history(start=start_date, end=end_date, interval='1d')
        
        if df.empty:
            raise ValueError(f"No data found for symbol {symbol}")
        
        return df, stock
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return pd.DataFrame(), None

def get_random_sentiment(symbol):
    """Generate a random sentiment score between -1 and 1 for any given stock symbol"""
    random.seed(hash(symbol) + datetime.now().day)
    
    sentiment_score = random.uniform(-1.0, 1.0)
    
    sentiment_score = round(sentiment_score, 2)
    
    print(f"Generated random sentiment for {symbol}: {sentiment_score}")
    return sentiment_score

def get_sentiment_from_dataset(symbol):
    return get_random_sentiment(symbol)

def get_sentiment_from_textblob(symbol):
    return get_random_sentiment(symbol)

def save_sentiment_to_db(symbol, sentiment_score, user_id=1): 
    try:
        connection = create_db_connection()
        if connection and connection.is_connected():
            cursor = connection.cursor()
            
            insert_query = """
            INSERT INTO sentimentanalysis (stock_symbol, sentiment_date, sentiment_score, user_id)
            VALUES (%s, %s, %s, %s)
            """
            
            current_date = datetime.now().date()
            
            cursor.execute(insert_query, (symbol.upper(), current_date, sentiment_score, user_id))
            connection.commit()
            
            print(f"Successfully saved sentiment for {symbol} with user_id {user_id}")
            
            cursor.close()
            connection.close()
            return True
    except Error as e:
        print(f"Detailed error saving sentiment to database: {e}")
        return False

@app.route('/')
def home():
    return render_template('senti.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        symbol = request.form.get('symbol', '').upper()
        
        if not symbol:
            return jsonify({'error': 'No symbol provided'}), 400
            
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            if not info or 'regularMarketPrice' not in info:
                return jsonify({'error': f'Invalid symbol: {symbol}'}), 400
        except Exception as e:
            return jsonify({'error': f'Error fetching stock data: {str(e)}'}), 400
        
        df, stock = get_stock_data(symbol)
        
        if df.empty:
            return jsonify({'error': 'No data available for this stock'}), 400
        
        print(f"Fetching sentiment score for {symbol}...")
        sentiment_score = get_random_sentiment(symbol)
        print(f"Final sentiment score for {symbol}: {sentiment_score}")
        
        save_result = save_sentiment_to_db(symbol, sentiment_score)
        
        sentiment_category = "Positive" if sentiment_score > 0.05 else "Negative" if sentiment_score < -0.05 else "Neutral"
        
        current_price = stock.info.get('regularMarketPrice', 0)
        previous_close = stock.info.get('previousClose', 0)
        price_change = current_price - previous_close
        price_change_percent = (price_change / previous_close * 100) if previous_close else 0
        
        historical_prices = df['Close'].tolist()
        historical_dates = [date.strftime('%Y-%m-%d') for date in df.index.to_pydatetime()]
        
        response_data = {
            'symbol': symbol,
            'company_name': stock.info.get('longName', symbol),
            'current_price': current_price,
            'price_change': price_change,
            'price_change_percent': price_change_percent,
            'sentiment_score': sentiment_score,
            'sentiment_category': sentiment_category,
            'database_saved': save_result,
            'historical_prices': historical_prices,
            'historical_dates': historical_dates,
            'additional_data': {
                'market_cap': stock.info.get('marketCap', 0),
                'volume': stock.info.get('volume', 0),
                'pe_ratio': stock.info.get('forwardPE', 0),
                'dividend_yield': stock.info.get('dividendYield', 0) or 0
            }
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Error in analyze route: {e}")
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True, host='0.0.0.0', port=5002)