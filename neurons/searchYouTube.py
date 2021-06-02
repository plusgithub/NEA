from youtubesearchpython import SearchVideos
import vlc
import pafy
import json

def search_play(object_input):
    query = object_input.get_string()
    depth = query.find('play')+5
    textToSearch = query[depth:]
    search = SearchVideos(textToSearch, offset = 1, mode = "json", max_results = 1)
    links=json.loads(search.result())
    links2 = (links['search_result'])
        
    title = links2[0]['title']
    video = pafy.new(links2[0]['link']) 
        # getting best stream 
    best = video.getbest() 
        # creating vlc media player object
    global media
    media = vlc.MediaPlayer(best.url)
    media.toggle_fullscreen()
        # start playing video 
    media.play()