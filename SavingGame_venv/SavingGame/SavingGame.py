from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from flask import Flask, request, jsonify

import openai
import os



load_dotenv('SavingGame_venv\SavingGame\keys.env')
app = Flask(__name__)
OPENAPI_KEY = os.getenv('OPENAPI_KEY')
openai.api_key = OPENAPI_KEY#key would be stored in a .env normally but in gitignore, but for this task its included


#Dummy data that would normally be stored on a DB uniquely to a user
account_data = [
        {
  "id": "acc123",
  "account_number": "********1234",
  "account_type": "Checking",
  "balance": 15000.25,
  "currency": "NOK",
  "owner": "Alice"
}

]

transaction_data = [
    {
  "id": "txn001",
  "date": "2023-08-15",
  "description": "Grocery Store",
  "amount": -75.5,
  "currency": "NOK",
  "account_id": "acc123"
}
]

@app.route('/')
def home():
    return render_template('home.html')






@app.route('/account', methods=['GET', 'POST'])
def account():
    response = ""

    if request.method == 'POST':
        # Check for deposit input
        deposit_amount = request.form.get('deposit')
        if deposit_amount:
            account_data[0]['balance'] += float(deposit_amount)
            return redirect(url_for('account'))

        # Check for user_input for chat
        user_input = request.form.get('user_input')
        if user_input:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": user_input}
                ]
            )
            response = completion.choices[0].message.content

    return render_template('account.html', account=account_data, chat_response=response)


if __name__ == '__main__':
    
    app.run(debug=True)