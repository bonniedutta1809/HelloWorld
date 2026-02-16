from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/generate-tests", methods=["POST"])
def generate_tests():
    return jsonify({"status": "Server is working"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)