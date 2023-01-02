import string

from flask import Flask, render_template, request

from utils import Board, np

print(string.digits)

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
@app.route("/home", methods=["POST", "GET"])
def home():

    if request.method == "GET":
        return render_template('index.html', board=None)
    else:
        data = np.zeros((9, 9), dtype=np.int8)
        for i, row in enumerate(string.ascii_uppercase[:9]):
            for j, col in enumerate(string.digits[1:]):
                item = request.form.get(f'{row}{col}')
                if item == '':
                    data[i, j] = 0
                else:
                    data[i, j] = item

        b = Board(data)
        out = b.solve()

        return render_template('index.html', board=out)


if __name__ == "__main__":
    app.run(debug=True)