from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
from textblob import TextBlob
from datetime import datetime, timedelta
import warnings
import mysql.connector
warnings.filterwarnings('ignore')

np.random.seed(42)
tf.random.set_seed(42)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

scaler = MinMaxScaler(feature_range=(0, 1))

# Database connection function
def create_db_connection():
    connection = mysql.connector.connect(
        host="localhost",  
        user="root",       
        password="Warsha@1980", 
        database="stockapp"
    )
    return connection

def store_stock_data(stock_symbol, date, open_price, close_price, current_price):
    try:
        connection = create_db_connection()
        cursor = connection.cursor()
        
        query = """
        INSERT INTO stockdata (stock_symbol, date, open_price, close_price, current_price)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        values = (stock_symbol, date, open_price, close_price, current_price)
        cursor.execute(query, values)
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print(f"Successfully stored data for {stock_symbol} on {date}")
        return True
    except Exception as e:
        print(f"Database error: {str(e)}")
        return False

def store_prediction_data(stock_symbol, prediction_date, predicted_price):
    try:
        connection = create_db_connection()
        cursor = connection.cursor()
        
        query = """
        INSERT INTO predictedprices (stock_symbol, prediction_date, predicted_price)
        VALUES (%s, %s, %s)
        """
        
        values = (stock_symbol, prediction_date, predicted_price)
        cursor.execute(query, values)
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print(f"Successfully stored prediction for {stock_symbol} on {prediction_date}")
        return True
    except Exception as e:
        print(f"Database error for prediction storage: {str(e)}")
        return False

def create_lstm_model(input_shape):
    model = Sequential([
        LSTM(256, return_sequences=True, input_shape=input_shape),
        BatchNormalization(),
        Dropout(0.2),
        
        LSTM(256, return_sequences=True),
        BatchNormalization(),
        Dropout(0.2),
        
        LSTM(256, return_sequences=True),
        BatchNormalization(),
        Dropout(0.2),
        
        LSTM(256),
        BatchNormalization(),
        Dropout(0.2),
        
        Dense(128, activation='relu'),
        BatchNormalization(),
        Dense(64, activation='relu'),
        Dense(1)
    ])
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='huber',
        metrics=['mae']
    )
    return model

def prepare_data(data, lookback=30):
    X, y = [], []
    for i in range(lookback, len(data)):
        X.append(data[i-lookback:i])
        y.append(data[i, 0])  
    return np.array(X), np.array(y).reshape(-1, 1)

def get_technical_indicators(df):
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['20dSTD'] = df['Close'].rolling(window=20).std()
    
    df.fillna(method='bfill', inplace=True)
    return df

def get_stock_data(symbol):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    stock = yf.Ticker(symbol)
    df = stock.history(start=start_date, end=end_date, interval='1d')
    
    if df.empty:
        raise ValueError(f"No data found for symbol {symbol}")
    
    df = get_technical_indicators(df)
    return df, stock

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST', 'OPTIONS'])
def analyze():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
        
    try:
        data = request.get_json()
        if not data or 'symbol' not in data:
            return jsonify({'error': 'No symbol provided'}), 400
            
        symbol = data['symbol'].upper()
        
        try:
            # Verify the symbol exists
            stock = yf.Ticker(symbol)
            info = stock.info
            if not info:
                return jsonify({'error': f'Invalid symbol: {symbol}'}), 400
        except Exception as e:
            return jsonify({'error': f'Error fetching stock data: {str(e)}'}), 400
        
        # Get stock data with technical indicators
        df, stock = get_stock_data(symbol)
        
        today = datetime.now().strftime('%Y-%m-%d')
        current_price = float(df['Close'].iloc[-1])
        open_price = float(df['Open'].iloc[-1])
        close_price = float(df['Close'].iloc[-1])
        
        store_success = store_stock_data(
            stock_symbol=symbol,
            date=today,
            open_price=open_price,
            close_price=close_price,
            current_price=current_price
        )
        
        # Prepare features for LSTM
        feature_columns = ['Close', 'Volume', 'RSI', 'MACD']
        dataset = df[feature_columns].values
        scaled_data = scaler.fit_transform(dataset)
        
        # Prepare training data
        X, y = prepare_data(scaled_data)
        
        if len(X) == 0 or len(y) == 0:
            return jsonify({'error': 'Insufficient data for analysis'}), 400
        
        # Create and train model
        model = create_lstm_model((X.shape[1], X.shape[2]))
        
        # Add early stopping
        early_stopping = tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        )
        
        # Train the model
        model.fit(
            X, y,
            epochs=100,
            batch_size=32,
            validation_split=0.1,
            verbose=0,
            callbacks=[early_stopping]
        )
        
        # Make predictions for next 7 days
        last_sequence = scaled_data[-30:]
        future_predictions = []
        current_sequence = last_sequence.copy()
        
        # Store the last known values for all features
        last_known_features = scaled_data[-1].copy()
        
        # Get future dates
        future_dates = []
        current_date = datetime.now()
        prediction_storage_success = True
        
        for i in range(7):
            next_date = current_date + timedelta(days=1)
            while next_date.weekday() > 4:  
                next_date = next_date + timedelta(days=1)
            
            future_date_str = next_date.strftime('%Y-%m-%d')
            future_dates.append(future_date_str)
            current_date = next_date
            
            current_sequence_reshaped = current_sequence.reshape((1, 30, len(feature_columns)))
            next_pred = model.predict(current_sequence_reshaped, verbose=0)[0, 0]
            

            new_row = last_known_features.copy()
            new_row[0] = next_pred  
            
            future_predictions.append(new_row)
            
            current_sequence = np.vstack((current_sequence[1:], new_row))
        
        future_predictions_array = np.array(future_predictions)
        
        future_prices_full = scaler.inverse_transform(future_predictions_array)
        
        future_prices = future_prices_full[:, 0]
        
        for i in range(len(future_dates)):
            prediction_date = future_dates[i]
            predicted_price = float(future_prices[i])
            
            prediction_success = store_prediction_data(
                stock_symbol=symbol,
                prediction_date=prediction_date,
                predicted_price=predicted_price
            )
            
            if not prediction_success:
                prediction_storage_success = False
        
        current_price = df['Close'].iloc[-1]
        
        # Calculate model MAE on the unscaled data
        y_pred = model.predict(X, verbose=0)
        
        y_pred_temp = np.zeros((len(y_pred), scaled_data.shape[1]))
        y_pred_temp[:, 0] = y_pred.flatten()
        
        y_temp = np.zeros((len(y), scaled_data.shape[1]))
        y_temp[:, 0] = y.flatten()
        
        y_pred_unscaled = scaler.inverse_transform(y_pred_temp)[:, 0]
        y_unscaled = scaler.inverse_transform(y_temp)[:, 0]
        
        mae = np.mean(np.abs(y_unscaled - y_pred_unscaled))
        
        db_status = "Data successfully stored in database" if store_success else "Failed to store data in database"
        prediction_db_status = "Predictions successfully stored" if prediction_storage_success else "Failed to store some predictions"
        
        response_data = {
            'predicted_price': float(current_price),
            'future_prices': future_prices.tolist(),
            'future_dates': future_dates,
            'model_mae': float(mae),
            'historical_volume': df['Volume'].tail(5).tolist(),
            'historical_rsi': df['RSI'].tail(5).tolist(),
            'feature_importance': {
                'Price': 0.4,
                'Volume': 0.2,
                'RSI': 0.2,
                'MACD': 0.2
            },
            'additional_data': {
                'pe_ratio': stock.info.get('forwardPE', 0),
                'market_cap': stock.info.get('marketCap', 0),
                'dividend_yield': stock.info.get('dividendYield', 0) or 0
            },
            'economic_data': {
                'interest_rate': 0.0425,
                'inflation_rate': 0.032,
                'gdp_growth_rate': 0.023
            },
            'database_status': db_status,
            'prediction_storage_status': prediction_db_status
        }
        
        response = jsonify(response_data)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)