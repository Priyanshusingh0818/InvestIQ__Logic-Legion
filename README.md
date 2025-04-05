# 📈 InsightWealthJ – Real-Time Stock Market Prediction & Learning Platform

InsightWealthJ is an all-in-one real-time stock analysis platform tailored for short-term investors and beginners. It combines deep learning-based price prediction, live sentiment analysis, educational tools, and user interaction features to make stock market investing more accessible and intelligent.

---

## 🚀 Features

- 📊 **7-Day Stock Price Prediction**  
  Uses an LSTM model trained on historical data to forecast the next 7 days of stock prices.

- 🧠 **Real-Time Sentiment Analysis**  
  Fetches live news and tweets, processes them with NLP to recommend Buy/Sell/Hold decisions.

- 📚 **Learn the Market**  
  Beginner-friendly stock market education page with organized, easy-to-understand resources.

- ❓ **Quiz Section**  
  Interactive quiz platform to test and improve user knowledge on market concepts and strategies.

- 💾 **Real-Time Data Storage**  
  All user interactions and predictions are dynamically stored in a MySQL database.

---

## 🔍 Problem Statement

Many new and short-term investors struggle to interpret market data and make informed decisions. Existing platforms often lack real-time predictive capabilities, integrated sentiment analysis, and learning resources in a single interface.

---

## 💡 Solution

InsightWealthJ bridges the gap by providing:
- Predictive analytics using LSTM models
- Sentiment-driven recommendations
- In-platform learning and knowledge testing
- Real-time interaction and storage with MySQL

---

## 🌟 Unique Selling Points (USP)

- Combines prediction + sentiment + learning in one platform
- Real-time, accurate stock data using yFinance
- Personalized user experience with dynamic data handling
- Beginner-friendly design with interactive learning modules

---

## 💰 Revenue Model (Future Scope)

- **Freemium Tier**: Advanced features available under a subscription model  
- **Ads & Affiliate Links**: Partnering with brokers like Zerodha, Groww, etc.  
- **Courses & Certifications**: Paid advanced learning tracks for certification

---

## 🛠️ Tech Stack

| Layer        | Technology Used                              |
|--------------|-----------------------------------------------|
| Frontend     | HTML, CSS, JavaScript                         |
| Backend      | Python (Flask or Django)                      |
| ML Models    | LSTM (Keras/TensorFlow), Sentiment Analysis   |
| APIs         | yFinance, News APIs, Twitter API              |
| Database     | MySQL                                         |
| Hosting      | (Optional) Railway / Render / AWS             |

---

## 📸 Demo

![Demo Screenshot 1](path/to/screenshot1.png)  
![Demo Screenshot 2](path/to/screenshot2.png)

*Note: Replace with actual paths once images are uploaded to the repo.*

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/InsightWealthJ.git
cd InsightWealthJ
pip install -r requirements.txt
python app.py
