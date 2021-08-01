import asyncio, websockets, json, time
from providers import YellowPagesSpain
from analyzer import AnalyzeWeb
from multiprocessing import Process, freeze_support

from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory('www', 'index.html')

@app.route("/<path:path>")
def resources(path):
    return send_from_directory('www', path)

async def consumer(m, websocket):
    data = json.loads(m)
    if data['action'] == 'search':
        inputs = data['data']
        entries = YellowPagesSpain().GetBusiness(inputs[0], inputs[1], int(inputs[2]))
        entries = [business for business in entries if business.website != None]
        business_dict = {b: i for i, b in enumerate(entries)}
        response = [{'id': business_dict[business], 'name': business.name, 'website': business.website} for business in entries]
        await websocket.send(json.dumps({'action': 'result', 'data': response}))    

        for business in business_dict:
            score = AnalyzeWeb(business.website)
            try:
                score = score['lighthouseResult']['categories']['performance']['score']
            except:
                score = 0
            
            score = int(score * 100)

            response = {'action': 'set_score', 'id': business_dict[business], 'score': score}
            await websocket.send(json.dumps(response))
        

async def consumer_handler(websocket, path):
    async for message in websocket:
        await consumer(message, websocket)

async def handler(websocket, path):
    await consumer_handler(websocket, path)
    
def StartFlask():
    app.run(host='0.0.0.0', port=80)

if __name__ == '__main__':
    freeze_support()
    start_server = websockets.serve(handler, '127.0.0.1', 5869)
    
    serve = Process(target=StartFlask)
    serve.start()

    try:
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
            print('Control-C detected!')
            serve.terminate()
            serve.join()
            
            