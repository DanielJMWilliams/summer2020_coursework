from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
import requests
import json
from django.conf import settings
from .models import *
import sys


from .SpotifyAuth import SpotifyAuth

# Create your views here.

def index(request):
    context = {
        "user_id": request.session.get("user_id", None),
    }
    return render(request, "musicRun/index.html", context)

def generate(request):
    user = SpotifyUser.objects.filter(spotify_id=request.session.get("user_id", None)).first()
    numSongs=0
    if user!=None:
        numSongs = len(user.songs.all())
    context = {
        "user_id": request.session.get("user_id", None),
        "numSongs":numSongs,
    }
    return render(request, "musicRun/generate.html", context)

def playlists(request):
    res = requests.get("https://api.spotify.com/v1/me/playlists", headers={"Authorization": getAuth(request)})
    response = json.loads(res.text)
    if request.session.get("user_id", None)==None:
        return render(request, "musicRun/playlists.html")
    else:   
        playlists = []
        for playlist in response["items"]:
            image = "https://dl1.cbsistatic.com/i/2017/04/12/f3a60331-48ce-4b98-8cce-3b23f2a76558/2ec57e2e209f330a0d0ca96dd6db42de/imgingest-853540607404562886.png"
            try:
                image = playlist["images"][0]["url"]
            except:
                # this can happen if a user has created an empty playlist
                print("image not found")
            d = {
                "name":playlist["name"],
                "id":playlist["id"],
                "image":image,
                "creator":playlist["owner"]["display_name"],
                "description":playlist["description"]
            }
            playlists.append(d)
        context = {
            "playlists":playlists,
            "user_id": request.session.get("user_id", None),
        }
        return render(request, "musicRun/playlists.html", context)

def profile(request):
    context = {
        "user_id": request.session.get("user_id", None),
    }
    return render(request, "musicRun/profile.html", context)

def spotify_logout(request):
    request.session["user_id"]=None
    return HttpResponseRedirect(reverse("index"))

def importPlaylist(request):
    playlistID = request.POST.get('playlistID', False)
    res = requests.get("https://api.spotify.com/v1/playlists/"+playlistID+"/tracks", headers={"Authorization": getAuth(request)})
    response = json.loads(res.text)
    for item in response["items"]:
        itemRes = requests.get("https://api.spotify.com/v1/audio-features/"+item["track"]["id"], headers={"Authorization": getAuth(request)})
        tempo = json.loads(itemRes.text)["tempo"]
        song = Song(spotify_uri=item["track"]["id"], bpm=tempo)
        song.save()
    
    return HttpResponse(res)

def importLikedSongs(request, offset):
    LIMIT=50
    
    res = requests.get("https://api.spotify.com/v1/me/tracks?limit=1",headers={"Authorization": getAuth(request)})
    numSongs = json.loads(res.text)["total"]
    print("numSongs: ",numSongs)
    tracks=[]
    if offset < numSongs:
        res = requests.get("https://api.spotify.com/v1/me/tracks?limit="+str(LIMIT)+"&offset="+str(offset),headers={"Authorization": getAuth(request)})
        offset+=LIMIT
        response = json.loads(res.text)
        url = "https://api.spotify.com/v1/audio-features?ids="
        for item in response["items"]:
            url = url + item["track"]["id"] + ","
        feature_res = requests.get(url, headers={"Authorization": getAuth(request), "Content-Type":"application/json", "Accept": "application/json"})
        feature_response = json.loads(feature_res.text)

        for i in range(0,len(response["items"])):
            item = response["items"][i]["track"]
            item_features = feature_response["audio_features"][i]
            track = getTrack(item, item_features)
            user = SpotifyUser.objects.get(spotify_id=request.session.get("user_id", None))
            if len(user.songs.filter(spotify_uri=item["id"]))==0:
                #song not related to user in database
                if len(Song.objects.all().filter(spotify_uri=item["id"])) == 0:
                    #song not in database
                    song = Song(spotify_uri=track["id"], name=track["name"], bpm=track["bpm"], danceability=track["danceability"], energy=track["energy"], valence=track["valence"], artists=track["artists"], duration=track["duration"])
                    song.save()
                    user.songs.add(song)
                    tracks.append(track)
                else:
                    song = Song.objects.get(spotify_uri=item["id"])
                    user.songs.add(song)
                    tracks.append(track)
                
            else:
                print("song already in database")
    data = {
        "offset":offset,
        "limit":LIMIT,
        "tracks":tracks,
        "numSongs":numSongs,
    }
    return HttpResponse(json.dumps(data))          

def getArtistNames(artists):
    artistString=""
    for artist in artists:
        # last element so no comma after
        if(artist==artists[-1]):
            artistString=artistString+artist["name"]
        else:
            artistString=artistString+artist["name"]+", "
    return artistString


def minsToMS(mins):
    ms = int(mins*60*1000)
    return ms

def getFormData(data, default):
    if data == "" or data == None:
        return default
    else:
        return data

def createRunningPlaylist(request):
    minBPM = int(getFormData(request.POST.get('min-bpm'), 0))
    maxBPM = int(getFormData(request.POST.get('max-bpm'), 999))

    if minBPM>maxBPM:
        context = {
            "user_id": request.session.get("user_id", None),
            "message": "Minimum BPM must be less than maximum BPM",
            "success":False,
        }
        return render(request, "musicRun/generate.html", context)

    playlistDuration = minsToMS(float(getFormData(request.POST.get('duration'), 999)))
    minSongDuration = minsToMS(float(getFormData(request.POST.get('min-song-duration'), 0)))
    maxSongDuration = minsToMS(float(getFormData(request.POST.get('max-song-duration'),999)))

    numSongs = int(getFormData(request.POST.get('number-of-songs'), 50))
    
    bpmAscending = getFormData(request.POST.get('bpm-ascending'), False)

    name = str(minBPM)+"-"+str(maxBPM)+" BPM"
    desc = ' '.join(["Auto Generated Running Playlist generated with settings: ",
            f"minBPM: {minBPM}, ",
            f"maxBPM: {maxBPM}, ",
            f"playlistDuration: {playlistDuration}, "
            f"minSongDuration: {minSongDuration}, ",
            f"maxSongDuration: {maxSongDuration}, ",
            f"numSongs: {numSongs}, ",
            f"bpmAscending: {bpmAscending}, ",
            ])
    user = SpotifyUser.objects.get(spotify_id=request.session.get("user_id", None))
    if bpmAscending:
        songObjects = user.songs.filter(bpm__range=(minBPM,maxBPM), duration__range=(minSongDuration,maxSongDuration)).order_by("bpm")[:numSongs]
    else:
        songObjects = user.songs.filter(bpm__range=(minBPM,maxBPM), duration__range=(minSongDuration,maxSongDuration)).order_by("-bpm")[:numSongs]
    print("songObjectslength:", len(songObjects))
    songs = []
    for song in songObjects:
        s={
            "uri":"spotify:track:"+song.spotify_uri,
            "duration":song.duration,
        }
        songs.append(s)
    if(len(songs)>0):
        playlistRes=createEmptyPlaylist(name, desc, request.session.get("user_id", None),getAuth(request))
        playlistID = str(json.loads(playlistRes.text)["id"])

        addRes = addSongsToPlaylist(playlistID,songs,getAuth(request),playlistDuration)
        message = "Playlist created"
        success=True
        context = {
            "user_id": request.session.get("user_id", None),
            "message": message,
            "success":success,
            "name":name,
            "url":json.loads(playlistRes.text)["external_urls"]["spotify"],
        }
        return render(request, "musicRun/generate.html", context)
    else:
        message = "No imported songs matching the entered criteria"
        success = False
        context = {
            "user_id": request.session.get("user_id", None),
            "message": message,
            "success":success,
        }
        return render(request, "musicRun/generate.html", context)


def callback(request):
    #https://developer.spotify.com/documentation/general/guides/authorization-guide/#authorization-code-flow
    code = request.GET["code"]
    spotify_auth=SpotifyAuth(code)
    request.session["token"] = spotify_auth.toJSON()

    res = requests.get("https://api.spotify.com/v1/me", headers={"Authorization": getAuth(request)})
    user_id = json.loads(res.text)["id"]
    request.session["user_id"]=user_id
    
    if len(SpotifyUser.objects.filter(spotify_id=user_id))==0:
        print("newUser")
        user = SpotifyUser(spotify_id=user_id)
        user.save()

    return HttpResponseRedirect(reverse("importedSongs"))

def getAuth(request):
    token = json.loads(request.session.get("token", None))
    spotify_auth = SpotifyAuth(access_token=token["access_token"], refresh_token=token["refresh_token"], expirey_time=token["expirey_time"])
    auth = spotify_auth.getAuth()
    request.session["token"] = spotify_auth.toJSON()
    return auth


def createEmptyPlaylist(name, desc, user_id, auth):
    #create empty playlist
    data = "{\"name\":\""+name+"\",\"description\":\""+desc+"\",\"public\":true}"
    res = requests.post("https://api.spotify.com/v1/users/"+user_id+"/playlists", headers={"Authorization": auth, "Content-Type":"application/json", "Accept": "application/json"}, data = data)
    #return playlist id
    return res


def addSongsToPlaylist(playlistID,songs,auth, playlistDuration):
    url = "https://api.spotify.com/v1/playlists/"+playlistID+"/tracks?uris="
    #upto 100 songs in one request
    count=0
    durationSum=0
    for song in songs:
        count=count+1
        durationSum+=song["duration"]
        url = url + song["uri"] + ","
        if count==100:
            #add 100 songs to playlist
            res = requests.post(url, headers={"Authorization": auth, "Content-Type":"application/json", "Accept": "application/json"})
            #reset count and url for next 100 songs
            count=0
            url="https://api.spotify.com/v1/playlists/"+playlistID+"/tracks?uris="
        if durationSum>=playlistDuration:
            break
    if count!=0:
        #add remaining songs to playlist
        res = requests.post(url, headers={"Authorization": auth, "Content-Type":"application/json", "Accept": "application/json"})



def playlist(request, playlist_id):
    res = requests.get("https://api.spotify.com/v1/playlists/"+playlist_id, headers={"Authorization": getAuth(request)})
    response = json.loads(res.text)
    tracks = getTracksFromPlaylist(playlist_id, getAuth(request))
    
    #tempo = calculateAverageTempo(tracks)

    playlist={
        "name":response["name"],
        "image_url":response["images"][0]["url"],
        "tracks":tracks,
        #"tempo": tempo,
        "tempo" : calculateMinMaxAverage(tracks, "bpm"),
        "danceability" : calculateMinMaxAverage(tracks, "danceability"),
        "energy": calculateMinMaxAverage(tracks, "energy"),
        "valence" : calculateMinMaxAverage(tracks, "valence"),
    }
    context = {
        "user_id": request.session.get("user_id", None),
        "playlist":playlist,
        
    }
    return render(request,"musicRun/playlist.html", context)
    #return HttpResponse(res)

def getTracksFromPlaylist(playlist_id, auth):
    LIMIT=100
    offset=0
    res = requests.get("https://api.spotify.com/v1/playlists/"+playlist_id+"/tracks?limit=1",headers={"Authorization": auth})
    numSongs = json.loads(res.text)["total"]
    tracks = []
    while offset < numSongs:
        res = requests.get("https://api.spotify.com/v1/playlists/"+playlist_id+"/tracks?limit="+str(LIMIT)+"&offset="+str(offset),headers={"Authorization": auth})
        offset+=LIMIT
        response = json.loads(res.text)
        url = "https://api.spotify.com/v1/audio-features?ids="
        for item in response["items"]:
            url = url + item["track"]["id"] + ","
        feature_res = requests.get(url, headers={"Authorization": auth, "Content-Type":"application/json", "Accept": "application/json"})
        feature_response = json.loads(feature_res.text)

        for i in range(0,len(response["items"])):
            item = response["items"][i]["track"]
            item_features = feature_response["audio_features"][i]
            track = getTrack(item, item_features)
            tracks.append(track)
    return tracks

def getTrack(item, item_features):
    track = {
        "name":item["name"],
        "artists":getArtistNames(item["artists"]),
        "id":item["id"],
        "bpm":round(item_features["tempo"]),
        "danceability":round(item_features["danceability"]*100),
        "energy":round(item_features["energy"]*100),
        "valence":round(item_features["valence"]*100),
        "duration":item["duration_ms"],
    }
    return track

def calculateMinMaxAverage(songs, attribute):
    sum=0
    min=sys.maxsize
    max=0

    for song in songs:
        value = float(song[attribute])
        sum+=value
        if(value>max):
            max=value
        if(value<min):
            min=value

    average = round(sum/len(songs))
    d = {
        "average":average,
        "min":round(min),
        "max":round(max),
    }
    return d


def importedSongs(request):
    res = requests.get("https://api.spotify.com/v1/me/tracks?limit=1",headers={"Authorization": getAuth(request)})
    numSongs = json.loads(res.text)["total"]
    user = SpotifyUser.objects.filter(spotify_id=request.session.get("user_id", None)).first()
    if user==None:
        return render(request, "musicRun/importedSongs.html")
    playlist = {
        "tracks":user.songs.all(),
    }
    if(numSongs==len(playlist["tracks"])):
        percentage_imported=100
    else:
        percentage_imported = int((len(playlist["tracks"])/numSongs)*100)
    context = {
        "playlist": playlist,
        "percentage_imported":percentage_imported,
        "num_liked_songs":numSongs,
        "user_id": request.session.get("user_id", None),
    }
    return render(request, "musicRun/importedSongs.html", context)