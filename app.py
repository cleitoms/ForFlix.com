from flask import Flask, render_template, redirect, request
import mercadopago

app = Flask(__name__)

# Configurar Mercado Pago
access_token = 'APP_USR-8390568529528550-100208-40976ae65efffb7a0e2da744513f6ae5-665556130'  # Substitua pela sua Access Token
sdk = mercadopago.SDK(access_token)

@app.route('/')
def index():
    return render_template('checkout.html')

@app.route('/checkout', methods=['POST'])
def checkout():
    # Criar a preferência de pagamento
    preference_data = {
        "items": [
            {
                "title": "Assinatura Forflix",
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": 1.00  # Preço em reais
            }
        ],
        "back_urls": {
            "success": "http://localhost:5000/success",  # URL para redirecionar após sucesso
            "failure": "http://localhost:5000/failure",  # URL para redirecionar após falha
            "pending": "http://localhost:5000/pending"   # URL para redirecionar após pendência
        },
        "auto_return": "approved"  # Redirecionar automaticamente se aprovado
    }

    preference_response = sdk.preference().create(preference_data)
    preference_id = preference_response["response"]["id"]

    return render_template('checkout.html', preference_id=preference_id)

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/failure')
def failure():
    return render_template('failure.html')

@app.route('/pending')
def pending():
    return render_template('pending.html')

if __name__ == '__main__':
    app.run(debug=True)
