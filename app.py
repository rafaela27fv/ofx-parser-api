from flask import Flask, request, jsonify
from ofxparse import OfxParser
import io

app = Flask(__name__)

@app.route('/upload-ofx', methods=['POST'])
def upload_ofx():
    try:
        # Verifica se o arquivo foi enviado
        if 'file' not in request.files:
            return jsonify({"error": "Nenhum arquivo enviado"}), 400
        
        file = request.files['file']
        
        # Lê o conteúdo do arquivo
        ofx_data = OfxParser.parse(io.StringIO(file.stream.read().decode('utf-8')))
        
        # Extrai informações do extrato
        transactions = []
        for account in ofx_data.accounts:
            for transaction in account.statement.transactions:
                transactions.append({
                    "date": transaction.date.isoformat(),
                    "amount": transaction.amount,
                    "payee": transaction.payee,
                    "memo": transaction.memo,
                    "type": transaction.type
                })
        
        return jsonify({
            "account_number": ofx_data.accounts[0].account_id,
            "currency": ofx_data.accounts[0].currency,
            "transactions": transactions
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
