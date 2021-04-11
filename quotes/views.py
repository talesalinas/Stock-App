from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages
# API KEY pk_1bb06023916a4c8093d29b42fb4518a3

def home(request):
    import requests
    import json

    if request.method == 'POST':
        ticker = request.POST['ticker']

        api_request = requests.get(f"https://cloud.iexapis.com/stable/stock/{ticker}/quote?token=pk_1bb06023916a4c8093d29b42fb4518a3")
        api_request_company = requests.get(f"https://cloud.iexapis.com/stable/stock/{ticker}/company?token=pk_1bb06023916a4c8093d29b42fb4518a3")
        api_request_news = requests.get(f"https://cloud.iexapis.com/stable/stock/{ticker}/news/last/10?token=pk_1bb06023916a4c8093d29b42fb4518a3")

        try:
            api = json.loads(api_request.content)
            api_company = json.loads(api_request_company.content)
            api_news = json.loads(api_request_news.content)
        except Exception as e:
            api = api_company = api_news = "Error..."
        
        return render(request, 'home.html', {
            'api': api,
            'api_company': api_company,
            'api_news': api_news,
        })

    else:
        return render(request, 'home.html', {'ticker': "Enter a ticker symbol in the search box above ..."})

def about(request):
    return render(request, 'about.html', {})

def mystocks(request):
    import requests
    import json

    if request.method == 'POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ("Stock has been added successfully"))
            return redirect('mystocks')
            
    else:
        ticker = Stock.objects.all()
        output = []

        for ticker_item in ticker:
            api_request = requests.get(f"https://cloud.iexapis.com/stable/stock/{str(ticker_item)}/quote?token=pk_1bb06023916a4c8093d29b42fb4518a3")

            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "Error..."

        return render(request, 'mystocks.html', {
            'ticker':ticker,
            'output': output
        })

def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Stock has been deleted!"))
    return redirect(delete_stock)

def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request, 'delete_stock.html', {'ticker': ticker})