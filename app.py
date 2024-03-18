from flask import Flask, request, jsonify
from handlers import FileHandler, OutlierHandler

app = Flask(__name__)

# / endpoint. Accepts JSON requests.
# stock_exchange (string) and file_paths (list) expected in payload
# For each CSV file provided, if OutlierHandler detects outliers it creates a new "outlier_filename".csv file in "output_files" directory
@app.route('/', methods=['POST'])
def process_files():
    # Handle if not JSON
    if not request.is_json:
        return jsonify({'message': 'Application accepts JSON only.'}), 400

    # Extract data & handle errors
    data = request.get_json()

    if 'file_path' not in data:
        return jsonify({'message': 'file_path not provided'}), 400
    if 'stock_exchange' not in data:
        return jsonify({'message': 'stock_exchange not provided.'}), 400

    stock_exchange = data['stock_exchange']
    file_paths = data['file_path']

    if not stock_exchange:
        return jsonify({'message': 'stock_exchange is empty.'}), 400
    if not file_paths:
        return jsonify({'message': 'file_path is empty.'}), 400

    # Process each file in stock exchange
    outliers = []

    for file_path in file_paths[:2]:
        file_handler = FileHandler(f"{stock_exchange}/{file_path}.csv")
        df, fn = file_handler.extract_dp()

        outlier_handler = OutlierHandler(df, fn)
        outlier = outlier_handler.detect_outliers()
        outliers.append(outlier)

    # Response
    return jsonify({'message': outliers}), 200

if __name__ == "__main__":
    app.run()
