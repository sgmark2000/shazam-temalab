from flask import Flask

app = Flask(__name__)

@app.route("/site")
def site():
    print()

if __name__ == "__main__":
    app.run(debug=True)