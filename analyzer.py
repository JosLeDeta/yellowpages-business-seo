import requests, json

API_KEY = ''

def AnalyzeWeb(site):
    URL = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=' + site + '&key=' + API_KEY
    return json.loads(requests.get(URL).text)

if __name__ == '__main__':
    print(AnalyzeWeb('http://urgeclick.es/')['lighthouseResult']['categories']['performance']['score'])