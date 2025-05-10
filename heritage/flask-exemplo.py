from flask import Flask , jsonify
app = Flask(__name__)

@app.route('/')

def home() -> str:
    return jsonify(message="Oi mamae e papai!")

if __name__ == '__main__':
    app.run(debug=True)
