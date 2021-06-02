from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps

def getWeather(object_input):
    extracted = object_input.extract_entities()
    owm = OWM('63eab3ef9656b64014182b8abf4bea51')
    mgr = owm.weather_manager()

    for i in extracted:
        if i[1] == "GPE":
            extracted = i[0]
    

    if len(extracted) == 0:
        extracted = 'London'

    weather = mgr.weather_at_place(extracted)
    
    w = weather.weather

    print(str(w.detailed_status))
    print(str(w.temperature('celsius')['temp_max']))
    print(str(w.temperature('celsius')['temp_min']))
    print(str(w.humidity))
    print(str(w.clouds))

    return "In " + str(extracted) + ", the sky is " + str(w.detailed_status) + ", with highs of " + str(w.temperature('celsius')['temp_max']) + ", lows of " + str(w.temperature('celsius')['temp_min']) +", a humidity of " + str(w.humidity) + ", with clouds covering " + str(w.clouds) + " percent of the area"


    