from datetime import datetime
from geopy.geocoders import Nominatim 
from timezonefinder import TimezoneFinder 
import pytz

def getTime(object_input):
    extracted = object_input.extract_entities()
    for i in extracted:
        if i[1] == "GPE":
            extracted = i[0]
            geolocator = Nominatim(user_agent="geoapiExercises") 
            location = geolocator.geocode(extracted)
            result = TimezoneFinder().timezone_at(lng=location.longitude, lat=location.latitude) 
            tz = pytz.timezone(result)
            timezone_now = datetime.now(tz)
            return timezone_now.strftime(f"The time in {extracted} is %I:%M %p")

    now = datetime.now()
    timeNow = now.strftime("%H:%M")
    d = datetime.strptime(timeNow, "%H:%M")
    return(d.strftime(f"The time is %I:%M %p"))