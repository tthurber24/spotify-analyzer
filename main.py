from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import spotipy
from spotipy import SpotifyPKCE
import sys

class Liked_song:
    def __init__(self, date_added, track_data): # date_added is a datetime object, track_data comes from the liked songs API request
        self.date_added = date_added
        self.track_data = track_data
    def get_id(self):
        return self.track_data['id']
    def get_name(self):
        return self.track_data['name']
    def get_artist(self):
        return self.track_data['artists'][0]['name']
    def printable(self):
        return (self.get_name() + " - " + self.get_artist() + " (Added on " + self.date_added.strftime("%m-%d-%Y") + ")" )

def liked_songs_last_six(sp: spotipy.Spotify): # returns a master list of liked_song objects
    today = datetime.today()
    last_year = today - relativedelta(months=6)

    results = sp.current_user_saved_tracks(limit=50, offset=0)

    tracks = []
    checking = True
    while checking:
        for track_data in results['items']:
            added_date_str_list = (track_data['added_at'][:10]).split("-") # get just the added date
            added_date = [int(i) for i in added_date_str_list]
            convert_date = datetime(added_date[0], added_date[1], added_date[2])

            if convert_date < last_year: # if the track was liked more than a year ago, stop
                checking = False
                break
            new_song = Liked_song(convert_date, track_data['track'])
            tracks.append(new_song) # otherwise, add it to the list

        if not results['next']:
            checking = False
        results = sp.next(results)

    return tracks

def get_track_features(track_list, sp: spotipy.Spotify): # returns a dictionary of track feature dictionaries (ids are keys)
    id_list = [song.get_id() for song in track_list]
    feature_list = {}
    while (id_list):
        if len(id_list) > 100:
            selected_ids = id_list[:100]
            selected_features = sp.audio_features(selected_ids)
            for i, id in enumerate(selected_ids):
                feature_list[id] = selected_features[i]
            id_list = id_list[100:]
        else:
            selected_features = sp.audio_features(id_list)
            for i, id in enumerate(id_list):
                feature_list[id] = selected_features[i]
            id_list = []
    return feature_list

def get_data_set(feature_str, liked_songs: list, features: dict): # returns data points for given feature
    dates = [song.date_added for song in liked_songs]
    values = []
    for song in liked_songs:
        song_id = song.get_id()
        song_features = features[song_id]
        values.append(song_features[feature_str])
    return dates, values

def build_graph(x_values, y_values, feature_str: str):
    fig, ax = plt.subplots()
    ax.plot_date(x_values, y_values, 'o')
    plt.xticks(rotation=30)
    plt.title("{} of the last 6 months of your liked songs".format(feature_str.capitalize()))
    new_y_ticks = [min(y_values), max(y_values)]
    new_y_labels = [plt.text(0, new_y_ticks[0], "Lowest"), plt.text(0, new_y_ticks[1], "Highest")]
    plt.yticks(ticks=new_y_ticks, labels=new_y_labels)
    plt.show()

def print_feedback(sp: spotipy.Spotify):
    pitch_class = ["C", "C-sharp", "D", "D-sharp", "E", "F", "F-sharp", "G", "G-sharp", "A", "A-sharp", "B"]

    print("Loading your data from Spotify...")
    last_six = liked_songs_last_six(sp)
    print("Getting the musical attributes for each song...")
    features = get_track_features(last_six, sp)
    selected_feature = sys.argv[1].lower()

    dates, feature_vals = get_data_set(selected_feature, last_six, features)
    build_graph(dates, feature_vals, selected_feature)

def main():
    client_id = '0e74cbd0f44c483ebaa65da4d27df74e'
    redirect_uri = 'http://localhost:3000'
    scope = 'user-library-read, user-top-read'

    pkce = SpotifyPKCE(client_id=client_id, redirect_uri=redirect_uri, scope=scope)
    sp = spotipy.Spotify(auth_manager=pkce)

    print_feedback(sp)

    # last_six = liked_songs_last_six(sp)
    # features = get_track_features(last_six, sp)

    # dates, speechiness_vals = get_data_set('speechiness', last_six, features)

    # build_graph(dates, speechiness_vals, 'speechiness')

    # fig, ax = plt.subplots()
    # ax.plot_date(dates, speechiness_vals, 'o')
    # plt.xticks(rotation=40)
    # plt.title("Speechiness of the last 6 months of your liked songs")
    # new_y_ticks = [min(speechiness_vals), max(speechiness_vals)]
    # new_y_labels = [plt.text(0, new_y_ticks[0], "Lowest\nspeechiness"), plt.text(0, new_y_ticks[1], "Highest\nspeechiness")]
    # plt.yticks(ticks=new_y_ticks, labels=new_y_labels, rotation=40)
    # plt.tight_layout
    
    # new_y_ticks = []
    # new_y_ticks.append(0.0)
    # new_y_ticks.extend(y_ticks)
    # new_y_labels = [plt.text(0, 0, "Lowest\nvalence")]
    # new_y_labels.extend(y_labels[:(len(y_labels) - 1)])
    # new_y_labels.append(plt.text(0, 1, "Highest\nvalence"))

    # plt.yticks(ticks=new_y_ticks, labels=new_y_labels)

    # plt.yticks([0, 0.2, 0.4, 0.6, 0.8, 1], ["Lowest\ndanceability", "0.2", "0.4", "0.6", "0.8", "Highest\ndanceability"])

    # dates, energy_vals = get_data_set('energy', last_six, features)
    # plt.plot_date(dates, energy_vals, 'o')
    # plt.xticks(rotation=30)
    # plt.title("Energy of the last 6 months of your liked songs")
    # plt.show()

    # dates, tempo_vals = get_data_set('tempo', last_six, features)
    # plt.plot_date(dates, tempo_vals, 'o')
    # plt.xticks(rotation=30)
    # plt.title("Tempo of the last 6 months of your liked songs")
    # plt.show()

    # for idx, item in enumerate(results['items']):
    #     # print(item['name'], item['popularity'])
    #     time = item['added_at'][:10]
    #     print(time.split('-'))
    #     # track = item['track']
    #     # print(idx, track['artists'][0]['name'], " – ", track['name'])

    # Matplotlib test
    # x = np.linspace(0, 2 * np.pi, 200)
    # y = np.sin(x)
    # fig, ax = plt.subplots()
    # ax.plot(x, y)
    # plt.show()
    # 0fX4oNGBWO3dSGUZcVdVV2

    # n95 = sp.track("0fX4oNGBWO3dSGUZcVdVV2")
    # print(n95['name'], " - ", n95['artists'][0]['name'])
    # print(get_track_features("0fX4oNGBWO3dSGUZcVdVV2", sp))

if __name__ == "__main__":
    main()