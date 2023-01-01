from flask import Flask, render_template, request, url_for

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
@app.route("/home", methods=["POST", "GET"])
def home():

    print(request.method)

    print(url_for('home'))

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)