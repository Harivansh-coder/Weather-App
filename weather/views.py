from django.shortcuts import render
import requests
from .models import City
import environ
from .form import CityForm

env = environ.Env()
environ.Env.read_env()

# Weather API key
api_key = env("WEATHER_API_KEY")


def index(request):

    weather_data = []
    form = None
    message = ''

    if api_key is None:
        message = "Please add your api key"

    else:

        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid='+api_key

        # form validation
        form = CityForm(request.POST or None)

        if form.is_valid():

            city = request.POST['name']
            response = requests.get(url.format(city)).json()

            if response['cod'] != '404':
                form.save()
            else:
                message = response['message']

        # getting cities from database
        cities = City.objects.all()

        for city in cities:
            response = requests.get(url.format(city)).json()
            city_weather = {
                'city': city.name,
                'temperature': response['main']['temp'],
                'description': response['weather'][0]['description'],
                'icon': response['weather'][0]['icon'],
            }
            weather_data.append(city_weather)

    context = {
        'data': weather_data,
        'form': form,
        'message': message
    }

    return render(request, 'weather/index.html', context)
