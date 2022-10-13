from quart import Quart

app = Quart(__name__)

@app.route('/')
async def index():
    return {"success": True}


@app.route('/flag')
async def flag():
    # credits https://bishopfox.com/blog/h2c-smuggling-request
    return {"success": 'IngeHack{cl34rt3xt_4nd_r3v3rse_pr0xy_byp4ss}'}

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        certfile='cert.pem',
        keyfile='key.pem',
    )
