from django.shortcuts import render, HttpResponse
from . import templates
import requests, datetime, os
from django.contrib import messages

def home(request):
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'new york'
    URL_API = os.environ.get('URL_API_KEY')
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={URL_API}'
    PARAMS = {'units': 'metric'}

    SEARCH_API_KEY = os.environ.get('SEARCH_API_KEY')
    SEARCH_ENGINE_ID = os.environ.get('SEARCH_ENGINE_ID')

    query = city + "city 1920x1080"
    page = 1
    start = (page - 1) * 10 + 1
    searchType = 'image'

    city_url = f"https://www.googleapis.com/customsearch/v1?key={SEARCH_API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"
    data = requests.get(city_url).json()
    search_items = data.get("items")
    image_url = search_items[1]['link']
    print(city)

    try:
        data = requests.get(url,PARAMS).json()
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        day = datetime.date.today()


        return render(request, 'weather_app/index.html', {'description':description, 'icon':icon, 'temp':temp, 'day':day, 'city':city, 'exception_occured':False, 'image_url':image_url})
    except:
        exception_occured = True
        messages.error(request, 'Data is Not Available')
        day = datetime.date.today()

        return render(request, 'weather_app/index.html', {'description':'clear sky', 'icon':'01d', 'temp':25, 'day':day, 'city':'new york', 'exception_occured':True})