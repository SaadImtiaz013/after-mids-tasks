from flask import Flask, render_template, request
import pandas as pd
app = Flask(__name__)
DATA_PATH = 'netflix_titles.csv'
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/predict', methods=['POST'])
def predict():
    try:
        user_input = request.form['movie_title'].lower()
        df = pd.read_csv(DATA_PATH)
        result = df[df['title'].str.contains(user_input, case=False, na=False)]
        if not result.empty:
            row = result.iloc[0]
            # Kaggle dataset ke columns use karte hue
            res = f"✅ Match Found: {row['title']} ({row['release_year']}) | Country: {row['country']}"
        else:
            res = "❌ Movie not found in the new Kaggle dataset."
    except FileNotFoundError:
        res = "⚠️ Error: netflix_titles.csv file nahi mili. Folder check karein."
    except Exception as e:
        res = f"⚠️ Error: {str(e)}"
    return render_template('index.html', prediction_text=res)
if __name__ == '__main__':
    app.run(debug=True)