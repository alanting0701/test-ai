from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1 style="color:Blue">上傳成功! 歡迎使用 Flask!</h1>'

if __name__ == '__main__':
    app.run(debug=True)