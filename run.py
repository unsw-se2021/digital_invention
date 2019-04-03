from routes import app
import ssl
import threading

def run_http():
    app.run(debug=False, host='0.0.0.0', port=80)

def run_https():
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('raisinplanner.crt', 'raisinplanner.key')
    app.run(debug=False, host='0.0.0.0', port=443, ssl_context=context)

if __name__ == '__main__':
    threading.Thread(target=run_http).start()
    threading.Thread(target=run_https).start()