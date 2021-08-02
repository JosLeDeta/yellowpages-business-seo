import asyncio, websockets, json, threading
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

def start_flask():
    app.run(host='127.0.0.1', port=80)

class Worker(threading.Thread):
    def __init__(self, websocket, message, loop):
        threading.Thread.__init__(self)
        self.websocket = websocket
        self.message =  message
        self.loop = loop
        self.stop = False
    def Stop(self):
        self.stop = True
    def run(self):
        data = json.loads(self.message)
        if data['action'] == 'search':
            inputs = data['data']
            entries = YellowPagesSpain().GetBusiness(inputs[0], inputs[1], int(inputs[2]))
            entries = [business for business in entries if business.website != None]
            business_dict = {b: i for i, b in enumerate(entries)}
            response = [{'id': business_dict[business], 'name': business.name, 'website': business.website} for business in entries]
            coro = self.websocket.send(json.dumps({'action': 'result', 'data': response}))    
            asyncio.run_coroutine_threadsafe(coro, self.loop)
            scores = {}

            for business in business_dict:
                if self.stop:
                    break
                score = AnalyzeWeb(business.website)
                try:
                    score = score['lighthouseResult']['categories']['performance']['score']
                except:
                    score = 0
                
                score = int(score * 100)
                scores[business] = score
                response = {'action': 'set_score', 'id': business_dict[business], 'score': score}
                coro = self.websocket.send(json.dumps(response))
                asyncio.run_coroutine_threadsafe(coro, self.loop)
            
            sort_business = sorted(scores.items(), key= lambda x: x[1])
            sort_business = [{'order': i + 1, 'id': business_dict[k], 'name': k.name, 'website': k.website, 'score': scores[k]} for i, (k, v) in enumerate(sort_business)]
            coro = self.websocket.send(json.dumps({'action': 'final_results', 'data': sort_business}))
            asyncio.run_coroutine_threadsafe(coro, self.loop)

workers = []

async def listener(websocket, path):
    loop = asyncio.get_running_loop()
    async for message in websocket:
        w = Worker(websocket, message, loop)
        w.start()
        workers.append(w)

if __name__ == '__main__':
    freeze_support()
    www_server = Process(target=start_flask)
    www_server.start()
    start_server = websockets.serve(listener, '127.0.0.1', 5869)
    asyncio.get_event_loop().run_until_complete(start_server)
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print('Closing server...')
        www_server.terminate()
        for w in workers:
            w.Stop()