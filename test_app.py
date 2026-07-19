from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Hello! Flask is working!</h1><p>If you see this, the basic setup is correct.</p>'

if __name__ == '__main__':
    print("🚗 Testing Flask...")
    print("📍 Open your browser and go to: http://localhost:5000")
    app.run(debug=True, port=5000)