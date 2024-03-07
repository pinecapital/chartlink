from flask import Flask, request
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='flask_app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',filemode='w')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    logging.info("Received message: %s", data)
    return "Message received successfully!", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
