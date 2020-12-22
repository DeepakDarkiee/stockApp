import csv
from . import base_scraper
from .base_scraper import BaseScraper


class StockScraper(BaseScraper):
    STOCK_KEYS = [
        [
            'close',
            'Open',
            'Bid',
            'Ask',
            "Daysrange",
            '52weekrange',
            'Volume',
            'Avgvolume'
        ],
        [
        'Marketcap',
        'Beta (5Y Monthly)',
        'PE Ratio(TTM)',
        'EPS (TTM)',
        'Earnings Date',
        'Forward Dividend & Yield	',
        'Ex-Dividend Date',
        '1y Target Est	'
        ]
    ]
    BASE_URL = 'http://finance.yahoo.com/q'

    def _parse_table(self, soup):
        stock = {}
        tables = [soup.find('table',class_='W(100%)'), soup.find('table',class_='M(0)')]

    
        for elem in zip(self.STOCK_KEYS, tables):
            
            keys, table = elem
            
            table = self._convert_to_soup(table)
            k=0
            #print(list( enumerate( table.find_all('td') )))
            k=0
            for i, cell in enumerate( table.find_all('td') ):
    
                if i <len(keys):
                    
                    stock[keys[i]]=""
                if i%2!=0 and i!=0:
                    
                    

                    stock[keys[k]]=cell.text
                
                    k+=1
        
                       
        return stock


    def _get_current_price(self, soup):
        return soup.find('span', class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)").text

    def get_data(self, tickers):
        if type(tickers) is str:
            tickers = [tickers]
        
        data = {}
        for ticker in tickers:
            url = self._get_url(ticker)
            
            soup = self._get_soup(url)
            
            ticker_data = self._parse_table(soup)

        
            ticker_data['current'] = self._get_current_price(soup)
        
            data[ticker] = ticker_data
        
        return data
sc=StockScraper()
sc.get_data('AAPL')

