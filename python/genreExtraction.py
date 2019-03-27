import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time
import csv



#SpotifyCredentials
cid ="5f0b01a1813a41d1b360ed91e890a93f"
secret ="906fe994176541299f8750e9d428bbd8"

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

csv_songfeatures = '~/Documents/dp_datamining/data/featuressongs.csv'
albums_results = []

info={}
countFails = 0
countGet = 0

out_pathBKP= "songsBKP.csv"
out_fileNPK = open(out_pathBKP, 'wb')

fieldnamesBPK = [
    "artist_id_spotify",
    "artist_name",
    "album_id",
    "album_name",
    "track_id",
    "track_name",
    "date_release",
    "popularity",
    "date_popularity",
    "acousticness",
    "danceability",
    "duration_ms",
    "energy",
    "instrumentalness",
    "key_f",
    "liveness",
    "loudness",
    "mode_f",
    "speechiness",
    "tempo",
    "time_signature",
    "valence",
    "genre",
    "genres"
]
writer = csv.DictWriter(out_fileNPK,delimiter=";", fieldnames=fieldnamesBPK, dialect='excel')

writer.writeheader() # Assumes Python >= 2.7
limit = 5000;
with open('featuressongs.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for index,row in enumerate(spamreader):

        if countGet == limit:
            break
        info["artist_id_spotify"] = row[0]

        info["artist_name"]      = row[1]
        info["album_id"]         = row[2]
        info["album_name"]       = row[3]
        info["track_id"]         = row[4]
        info["track_name"]       = row[5]
        info["date_release"]     = row[6]
        info["popularity"]       = row[7]
        info["date_popularity"]  = row[8]
        info["acousticness"]     = row[9]
        info["danceability"]     = row[10]
        info["duration_ms"]      = row[11]
        info["energy"]           = row[12]
        info["instrumentalness"] = row[13]
        info["key_f"]            = row[14]
        info["liveness"]         = row[15]
        info["loudness"]         = row[16]
        info["mode_f"]           = row[17]
        info["speechiness"]      = row[18]
        info["tempo"]            = row[19]
        info["time_signature"]   = row[20]
        info["valence"]          = row[21]

        try:
            art = sp.artist(row[0])
            print len(art)
            print art
            print art['genres']
            genres = []
            for genre in art['genres']:
                genres.append(genre)



            print "genres len"
            print len(genres)

            if len(genres)==1:
                print "only one genre ---<"
                print genres[0]
                info["genre"] = genres[0]
                info["genres"] = "none"
            else:
                print " more genres --<"
                print genres.join(',')
                info["genre"] = "none"
                info["genres"] = genres.join(',')


            countGet+=1



        except :
            info["genre"] = "none"
            info["genres"] = "none"
            countFails+=1





        albums_results.append(info)
        writer.writerow(info)
        print "index"
        print(index)
        print "get"
        print countGet
        print "fail"
        print countFails
    out_fileNPK.close()


print len(info)
print len(albums_results)
print type(albums_results)


out_path= "songsFini.csv"
out_file = open(out_path, 'wb')

fieldnames = sorted(list(set(k for d in albums_results for k in d)))
writer = csv.DictWriter(out_file,delimiter=";", fieldnames=fieldnamesBPK, dialect='excel')

writer.writeheader() # Assumes Python >= 2.7
for row in albums_results:
    writer.writerow(row)
out_file.close()

