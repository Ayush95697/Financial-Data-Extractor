📊 Financial Data Extractor

A simple Streamlit app powered by LangChain + Groq LLM that extracts financial metrics (Revenue & EPS — actual vs expected) from earnings news articles.

It allows users to paste a financial paragraph (e.g., Tesla’s quarterly report) and automatically returns structured results in a table format.

🚀 Features

📝 Enter any financial earnings paragraph

🤖 LLM extracts Revenue (Actual & Expected) and EPS (Actual & Expected) in JSON format

📋 Displays extracted data in a clean, interactive table

⚡ Powered by LangChain + Groq LLM for robust text parsing

🎯 Helps analysts quickly spot earnings beats/misses

🖼️ Demo

## Example Input

```bash
Earnings per share: 73 cents adjusted vs. 76 cents expected  

Revenue: $25.71 billion vs. $27.26 billion expected
```


Output table:

| Measure | Estimated       | Actual          |
| ------- | --------------- | --------------- |
| Revenue | \$27.26 billion | \$25.71 billion |
| EPS     | 76 cents        | 73 cents        |


🛠️ Installation

1. Clone the repository
```
git clone https://github.com/Ayush9569/financial-data-extractor.git
cd financial-data-extractor
 ```
2. Create & activate virtual environment (optional but recommended)
```
python -m venv venv
source venv/bin/activate   # Mac/Linux  
venv\Scripts\activate      # Windows
```
3. Install dependencies
```
pip install -r requirements.txt
```

4. Set up environment variables
   
Create a .env file and add your Groq API key:
```
GROQ_API_KEY=your_api_key_here
```
▶️ Usage

Run the Streamlit app:
```
streamlit run app.py
```

1. Paste a financial news article or earnings snippet

2. Click Extract

3. View the extracted results in a structured table

📂 Project Structure
```
financial-data-extractor/
│── app.py                # Streamlit app (UI)
│── data_extractor.py     # LLM-based extractor function
│── requirements.txt      # Dependencies
│── .env                  # API keys (not shared)
│── README.md             # Documentation
```

📦 Dependencies

* Python 3.9+

* Streamlit

* LangChain

* langchain-groq

* pandas

* python-dotenv

Install them with:
```
pip install -r requirements.txt
```
🔮 Future Enhancements

1. Add more financial metrics (operating income, net profit, regulatory credits, etc.)

2. Highlight beats/misses with green/red indicators

3. Support multiple companies/articles at once

4. Export results to CSV/Excel

🤝 Contributing

 * Pull requests are welcome! If you’d like to add features or fix bugs, fork this repo and create a PR.

📜 License

  * This project is licensed under the MIT License.






