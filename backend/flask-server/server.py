from flask import Flask
import dynamo

app = Flask(__name__)

@app.route("/site")
def site():
    return dynamo.read('12345','123456')

if __name__ == "__main__":
    app.run(debug=True)