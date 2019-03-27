import csv

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
        "genreOriginal"
    ]

countRock = 0
countPop = 0
countPopRock = 0
info={}

out_path= "popSongs.csv"
out_file = open(out_path, 'wb')
writer = csv.DictWriter(out_file,delimiter=";", fieldnames=fieldnamesBPK, dialect='excel')
writer.writeheader() # Assumes Python >= 2.7
countOthers = 0

with open('songsBKP.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for index,row in enumerate(spamreader):
        #print index
        if index < countPop:
            break
        word = row[22]
        # How to use find()

        info["artist_id_spotify"] = row[0]
        info["artist_name"] = row[1]
        info["album_id"] = row[2]
        info["album_name"] = row[3]
        info["track_id"] = row[4]
        info["track_name"] = row[5]
        info["date_release"] = row[6]
        info["popularity"] = row[7]
        info["date_popularity"] = row[8]
        info["acousticness"] = row[9]
        info["danceability"] = row[10]
        info["duration_ms"] = row[11]
        info["energy"] = row[12]
        info["instrumentalness"] = row[13]
        info["key_f"] = row[14]
        info["liveness"] = row[15]
        info["loudness"] = row[16]
        info["mode_f"] = row[17]
        info["speechiness"] = row[18]
        info["tempo"] = row[19]
        info["time_signature"] = row[20]
        info["valence"] = row[21]

        #Get only pop
        if "pop" in row[22]:
            if (word.find('rock') != -1):
                #print ("Contains given substring ")
                countRock += 1
                info["genre"] = "Others"
                info["genreOriginal"] = row[22]
            elif (word.find('folk') != -1):
                #print ("Contains given substring ")
                countRock += 1
                info["genre"] = "Others"
                info["genreOriginal"] = row[22]
            elif (word.find('funk') != -1):
                #print ("Contains given substring ")
                countRock += 1
                info["genre"] = "Others"
                info["genreOriginal"] = row[22]

            else:
                print ("Doesn't contains given substring")

                info["genre"] = "pop"
                info["genreOriginal"] = row[22]


                countPop += 1
        else :
            info["genre"] = "Others"
            info["genreOriginal"] = row[22]
            countOthers+=1
            if countOthers < countPop:
                break


        writer.writerow(info)

        print "countOthers"
        print countOthers

        print "countPop"
        print countPop
    out_file.close()