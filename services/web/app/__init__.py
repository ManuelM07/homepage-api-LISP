from flask import Flask, jsonify


app = Flask(__name__)
app.config.from_object("app.config.Config")

@app.route("/")
def hello_world():
    return jsonify(hello="world")

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)