from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from background_task import background
from .models import Stock,ChartStock
from .forms import StockForm,ChartForm
from django.contrib import messages
import time
import datetime
from . import base_scraper
from . import stocks
from .stocks import StockScraper
import pandas as pd
import requests
import json
import os
from plotly.offline import plot
import plotly.graph_objs as go
from datetime import date
import yfinance as yf

 
# Browser request for home page, pass in dict
def home(request):
	import requests
	import json

	if request.method == 'POST':
		ticker = request.POST['ticker']
		print(ticker)
		IEX_CLOUD_API_TOKEN = 'Tpk_059b97af715d417d9f49f50b51b1c448'
		# pass in url that calls the api
		api_request = requests.get(f"https://sandbox.iexapis.com/stable/stock/{ticker}/quote?token={IEX_CLOUD_API_TOKEN}")
		# api_request = requests.get(f"https://sandbox.iexapis.com/stable/stock/{ticker}/{IEX_CLOUD_API_TOKEN}")

		try:
			api = json.loads(api_request.content)
			print(api)
			
		except Exception as e:
			api = "Error..."

		return render(request, 'home.html', {'api': api, 
			'error':"Could not access the api"})
	
	else:
	
		return render(request, 'home.html', {'ticker': "Enter a Ticker Symbol Above..."})

   	

def about(request):
	return render(request, 'about.html', {})


def add_stock(request):
    import requests
    import json
    if request.method == 'POST':
     
        form = StockForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, ("Stock has been added to your portfolio!"))
            return redirect('add_stock')
    else:    
        ticker = Stock.objects.all()
        
		# save ticker info from api output into python list ('output list')
        output = []
        #IEX_CLOUD_API_TOKEN = 'Tpk_059b97af715d417d9f49f50b51b1c448'
		# modify to pull multiple stock tickers at the same time
        for ticker_item in ticker:

            ti=str(ticker_item)
            #api_request = requests.get(f"https://sandbox.iexapis.com/stable/stock/{ti}/quote?token={IEX_CLOUD_API_TOKEN}")
            try:
                #api = json.loads(api_request.content)
                sc=StockScraper()

                data=sc.get_data(ti)
    
                output.append(data)
            except Exception as e:
                api = "Error..."
    
        return render(request, 'add_stock.html', {'ticker': ticker, 'output':  output})
def chart(request):
    
    if request.method == 'POST':
        form = ChartForm(request.POST or None)
        if form.is_valid():

            form.save()
            messages.success(request, ("Stock has been added to your portfolio!"))
            return redirect('chart')
    else:
        ticker = ChartStock.objects.all()
        output = []

        for ticker_item in ticker:
            ti=str(ticker_item)
            try:
            
                y=yf.Ticker(ti)
                y=y.info
                
                output.append(y)
                
                
            except Exception as e:
                print("Error while getting response ")
        return render(request, 'chart.html', {'ticker': ticker, 'output':  output})
    
def StockChart(request):
    symbol=request.GET.get('symbol')
    company=request.GET.get('company')
    data = yf.download(tickers=symbol, period='1mo', interval='1d')

    if os.path.exists('{}.csv'.format(symbol)):
    	os.remove('{}.csv'.format(symbol))
    time.sleep(3)
    data.to_csv('{}.csv'.format(symbol))
    
    file = pd.read_csv("{}.csv".format(symbol))
    figure=go.Figure([go.Scatter(x=file['Date'],y=file['High'],mode='lines+markers')])
    
    figure.update_layout({'plot_bgcolor':"#21201f",'paper_bgcolor':"#21201f"},title_font_size=30,width=1000,height=500)
    figure.update_yaxes(color='white',title='Open')
    figure.update_xaxes(color='white',title='Date<br>'+ str(symbol) +' 1 month stock data Chart',range=[file['Date'][0],file['Date'][len(file)-1]])
    fig=plot( figure,output_type='div')
    
    return render(request,'stock_chart.html',context={'symbol':symbol,'plot':fig,'company':company})
     
def graph(request):
    
    symbol=request.GET.get('symbol')
    """
    company=request.GET.get('company')
    data = yf.download(tickers=symbol, period='1mo', interval='1d')
    """
    data = yf.download(tickers=symbol, period='1mo', interval='1d')

    if os.path.exists('{}.csv'.format(symbol)):
    	os.remove('{}.csv'.format(symbol))
    time.sleep(3)
    data.to_csv('{}.csv'.format(symbol))
    
    file = pd.read_csv("{}.csv".format(symbol))
    file=file.set_index(pd.DatetimeIndex(file['Date'].values))
    
    figure=go.Figure(
            data=[
                go.Candlestick(
					x=file.index,
                    open=file['Open'],
                    high=file['High'],
                    low=file['Low'],
                    close=file['Close'],
                    increasing_line_color='red',
                    decreasing_line_color='green'
                    
                )
            ]
        

        )
    figure.update_layout({'plot_bgcolor':"#21201f",'paper_bgcolor':"#21201f"},title_font_size=30,width=1000,height=600)
    figure.update_yaxes(color='white',title='Prize')
    figure.update_xaxes(color='white',title='Date<br>'+ str(symbol) +' 1 month stock data')
    fig=plot( figure,output_type='div')
    return render(request, "graph.html",context={'plot':fig,'symbol':symbol} )

	
def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id) # call database by primary key for id #
	item.delete()
	messages.success(request, ("Stock Has Been Deleted From Portfolio!"))
	return redirect(add_stock)
	
def news(request):
	import requests
	import json
	
	# News API
	#api_request = requests.get('http://newsapi.org/v2/everything?q=stocks&apiKey=</your_api_key>')
	
	# BASIC - Stock News API
	#api_request = requests.get('https://stocknewsapi.com/api/v1/category?section=general&items=50&token=</your_api_key>')
	
	# PREMIUM - Stock News API
	api_request = requests.get('https://stocknewsapi.com/api/v1/category?section=alltickers&items=50&token=</your_api_key>')
	api = json.loads(api_request.content)
	return render(request, 'news.html', {'api': api}) 
	messages.success(request, ("Stock Has Been Deleted"))
	return redirect(add_stock)






