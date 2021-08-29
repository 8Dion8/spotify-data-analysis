import json, math, datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import matplotlib as mpl
import numpy as np

#print(mpl.rcParams.keys())

MAINCOLOR = "#48483e"
PALLETTE = ["#9358fe", "#fa2772", "#fe9720", "#e7db75", "#6cc72c", "#66d9ee"]

mpl.rcParams["text.color"] = "white"
mpl.rcParams["axes.labelcolor"] = "white"
mpl.rcParams["xtick.color"] = "white"
mpl.rcParams["ytick.color"] = "white"
mpl.rcParams["axes.edgecolor"] = "white"

loc = plticker.MultipleLocator(base=10)

#'''
i = 1
data = json.load(open("/home/dion/Desktop/MyData/StreamingHistory0.json", "r"))
while 1:
    try:
        data.extend(json.load(open(f"/home/dion/Desktop/MyData/StreamingHistory{i}.json", "r")))
        i += 1
    except:
        break

print(data[0])
print(f"{len(data)} tracks listened to", end=" ")

STARTDATE = datetime.datetime(*[int(i) for i in data[ 0]["endTime"].split(" ")[0].split("-")])
ENDDATE   = datetime.datetime(*[int(i) for i in data[-1]["endTime"].split(" ")[0].split("-")])


print()

TIMESPAN = (ENDDATE - STARTDATE).days



#'''

#open("/home/dion/Desktop/MyData/StreamingHistory.json", "w").write(json.dumps(str(data)))
#'''

#data = json.load(open("/home/dion/Desktop/MyData/StreamingHistory.json", "r"))

artists = {}
tracks = {}
days = {}
months = {}
timeListened = 0

for track in data:
    timeListened += track["msPlayed"]

    artist = track["artistName"]
    artist = artist.replace("$", "\$")

    if artist in artists:
        artists[artist]["msListenedTo"] += track["msPlayed"]
        artists[artist]["timesListenedTo"] += 1
    else:
        artists[artist] = {
            "msListenedTo":track["msPlayed"],
            "timesListenedTo":1
        }

    day = track["endTime"].split(" ")[0]

    if day in days:
        days[day]["msListenedTo"] += track["msPlayed"]
        days[day]["timesListenedTo"] += 1
    else:
        days[day] = {
            "msListenedTo":track["msPlayed"],
            "timesListenedTo":1
        }

    month = "-".join(track["endTime"].split(" ")[0].split("-")[:2])

    if month in months:
        months[month]["msListenedTo"] += track["msPlayed"]
        months[month]["timesListenedTo"] += 1
    else:
        months[month] = {
            "msListenedTo":track["msPlayed"],
            "timesListenedTo":1
        }


#print(artists.items())
artistsByListeningTime   = {k: v for k, v in sorted(artists.items(), key=lambda item: item[1]["msListenedTo"],    reverse=True)}
artistsByTimesListenedTo = {k: v for k, v in sorted(artists.items(), key=lambda item: item[1]["timesListenedTo"], reverse=True)}

HOURSLISTENEDTO = math.floor(timeListened/1000/60/60)

#print(f"{timeListened} ms")
#print(f"{timeListened/1000} s")
#print(f"{timeListened/1000/60} min")
print(f"for {HOURSLISTENEDTO} hours")
#print(f"{timeListened/1000/60/60/24} d")

AVGLISTENINGTIMEPDAY = math.floor(HOURSLISTENEDTO / TIMESPAN * 10) / 10

print(f"on average, {AVGLISTENINGTIMEPDAY} h per day")

open("/home/dion/Desktop/MyData/ArtistsData.json", "w").write(json.dumps(str(artistsByListeningTime)))

fig, axs = plt.subplots(2,2,facecolor=MAINCOLOR)

topArtistsByListeningTime   = {k: artistsByListeningTime[k]   for k in list(artistsByListeningTime  )[:10]}
topArtistsByTimesListenedTo = {k: artistsByTimesListenedTo[k] for k in list(artistsByTimesListenedTo)[:10]}


artistsListeningTimeX = topArtistsByListeningTime.keys()
artistsListeningTimeY = [i["msListenedTo"]/1000/60/60 for i in topArtistsByListeningTime.values()]

axs[0, 0].yaxis.set_major_locator(loc)
axs[0, 0].set_facecolor(MAINCOLOR)
axs[0, 0].set_title("Top 10 Artists By Listening Time")

axs[0, 0].bar(artistsListeningTimeX, artistsListeningTimeY, color=PALLETTE)



artistsTimesListenedToX = topArtistsByTimesListenedTo.keys()
artistsTimesListenedToY = [i["timesListenedTo"] for i in topArtistsByTimesListenedTo.values()]

#axs[1, 0].yaxis.set_major_locator(loc)
axs[1, 0].set_facecolor(MAINCOLOR)
axs[1, 0].set_title("Top 10 Artists By Times Listened To")

axs[1, 0].bar(artistsTimesListenedToX, artistsTimesListenedToY, color=PALLETTE)



monthsListeningTimeX = months.keys()
monthsListeningTimeY = [i["msListenedTo"]/1000/60/60 for i in months.values()]

axs[0, 1].yaxis.set_major_locator(loc)
axs[0, 1].set_facecolor(MAINCOLOR)
axs[0, 1].set_title("Hours Listened To Each Month")


axs[0, 1].bar(monthsListeningTimeX, monthsListeningTimeY, color=PALLETTE)



monthsTimesListenedToX = list(months.keys())
monthsTimesListenedToY = [i["timesListenedTo"] for i in months.values()]

#axs[1, 1].yaxis.set_major_locator(loc)
axs[1, 1].set_facecolor(MAINCOLOR)
axs[1, 1].set_title("Tracks Listened To Each Month")

axs[1, 1].bar(monthsTimesListenedToX, monthsTimesListenedToY, color=PALLETTE)




plt.show()

print()
#'''