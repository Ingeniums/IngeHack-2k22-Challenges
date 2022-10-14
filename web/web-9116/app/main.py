from fastapi import FastAPI
import uvicorn
app = FastAPI()


@app.trace('/')
async def root():
    return {"message": "call 911"}

@app.get('/')
async def root():
    return {"message": "call 911"}

@app.get('/.well-known/security.txt')
async def security():
    return {"message": "IngeHack{securityFTW}"}

if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, host='0.0.0.0',
                reload=True, access_log=False)
