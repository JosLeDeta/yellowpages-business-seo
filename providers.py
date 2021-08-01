import requests, bs4, time

FixString = lambda string: string.replace('%3A',':').replace('%2F', '/')
class BusinessCard():
    def __init__(self):
        self.name = ""
        self.phone = ""
        self.website = None    
    def __str__(self):
        return f'{self.name} - {self.phone} - {self.website}'
    def ToJSON(self):
        return {'name': self.name, 'phone': self.phone, 'website': self.website}
    
class YPCABusiness(BusinessCard):
    def __init__(self, data):
        BusinessCard.__init__(self)
        self.name = data.select('a.listing__name--link')[0].text
        self.phone = data.select('li.mlr__item--phone')[0].select('h4')[0].text
        web_link = data.select('li.mlr__item--website')
        if web_link:
            self.website = FixString(web_link[0].select('a')[0]['href'].split('redirect=')[1])    

class YellowPagesCanada():
    def GetPage(self, category, location, n_page):
        URL = f'https://www.yellowpages.ca/search/si/{n_page}/{category.replace(" ", "+")}/{location}+ON'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0)',
        }

        data = requests.get(URL, headers=headers).content
        html = bs4.BeautifulSoup(data, features='lxml')
        result_div = html.select('div.resultList')[0]
        entries = result_div.select('div.listing__content__wrap--flexed')
        return entries
    def GetBusiness(self, category='plumber', location="", pages=1, delay=1.0):
        b = []
        for n in range(pages):
            b.extend([YPCABusiness(data) for data in self.GetPage(category, location, n)])
            time.sleep(delay)
        return b

class YPSPBusiness(BusinessCard):
    def __init__(self, data):
        BusinessCard.__init__(self)
        self.name = data.select('div.comercial-nombre')[0].select('h2')[0].select('span')[0].text
        self.phone = None
        webSite = data.select('a.web')
        if webSite:
            self.website = webSite[0]['href']
            if self.website.count('?utm') > 0:
                self.website = self.website.split('?utm')[0]
    def __str__(self):
        return f'{self.name} - {self.website}'

class YellowPagesSpain():
    def GetPage(self, category, location, n_page):
        URL = f'https://www.paginasamarillas.es/search/{category}/all-ma/{location}/all-is/{location}/all-ba/all-pu/all-nc/{n_page}?what={category}&where={location}&qc=true'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0)',
        }

        data = requests.get(URL, headers=headers).content
        html = bs4.BeautifulSoup(data, features='lxml')
        central = html.select('div.central')
        if central:
            items = central[0].select('div.listado-item')
            return items
        else:
            return []
    def GetBusiness(self, category='carpintero', location='madrid', pages=1, delay=1.0):
        b = []
        for n in range(1, pages+1):
            b.extend([YPSPBusiness(data) for data in self.GetPage(category, location, n)])
            time.sleep(delay)
        return b