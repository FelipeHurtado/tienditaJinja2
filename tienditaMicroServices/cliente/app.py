from flask import Flask

app = Flask(__name__)

@app.route("/cliente/")
def cliente():
    return str("cliente")

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)