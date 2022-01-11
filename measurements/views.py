from django.shortcuts import render
import requests
from django.shortcuts import render,get_object_or_404
from .models import Measurement
from .forms import MeasurementModelForm
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from .utils import get_geo 
import folium
import json

#Create your views here.

def calculate_distance_view(request):
    
    obj=get_object_or_404(Measurement,id=1)
    form =MeasurementModelForm(request.POST or None)
    
    geolocator =Nominatim(user_agent='measurements')

    ip ='103.19.19.27'
    country,city,lat,lon =get_geo(ip)
    
    location= geolocator.geocode(city)
    print('###',location)

    l_lat=lat
    l_lon=lon
    pointA =(l_lat,l_lon)
     #folium map notifinaction
    m=folium.Map(width=1000,height=500,location=pointA )
    
        #marker
    folium.Marker([l_lat,l_lon],tooltip='click here for more',popup=city['city'],icon=folium.Icon(color='purple')).add_to(m)
    
     
    if form.is_valid():
        instance=form.save(commit=False)
        destination_ =form.cleaned_data.get('destination')
        destination =geolocator.geocode(destination_)
        print(destination)
        d_lat=destination.latitude
        d_lon=destination.longitude

        pointB= (d_lat,d_lon)
        distance =round(geodesic(pointA,pointB).km,2)
        #marker
        folium.Marker([d_lat,d_lon],tooltip='click here for more',icon=folium.Icon(color='red')).add_to(m)

       
        #folium map notifinaction
        
       

        instance.location =location
        instance.distance= distance
        instance.save()


    m=m._repr_html_()
    
    context={
        'location':location,
        #'distance': distance,
        'form':form,
        'map':m,
      
    }
    return render(request,'Measurement/main.html',context)


 