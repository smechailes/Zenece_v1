from flask import Flask, render_template


app = Flask(__name__)


@app.get("/")
def home():
    return render_template(
        "index.html",
        page={
            "title": "ZenEce Investment Holdings — Pre-IPO capital, disciplined exits",
            "brand": "ZenEce",
            "location": "Kathmandu",
            "email": "zeneceinvestmentholdings@gmail.com",
            "confidentiality": "Confidential · For qualified investors only",
        },
    )


if __name__ == "__main__":
    app.run(debug=True)