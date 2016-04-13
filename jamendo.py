import requests

class Jamendo:

    def __init__(self,client_id):
        self.client_id = client_id

    def do_query(self, segment, params):
        params["client_id"] = self.client_id
        params["format"] = "json"

        host = "https://api.jamendo.com/v3.0"
        url = host + segment

        r = requests.get(url, params=params)
        r.raise_for_status()
        return r.json()

    def get_playlist(self, playlistid):
        limit = 200
        offset = 0
        params = {"id": playlistid,
                  "limit": limit,
                  "audiodlformat": "flac"}

        url = "/playlists/tracks/"

        finished = False
        all_tracks = []
        while not finished:
            print("offset %s" % offset)
            params["offset"] = offset
            d = self.do_query(url, params)
            results = d["results"]
            if results:
                tracks = results[0]["tracks"]
                if tracks:
                    all_tracks.extend(tracks)
                    offset += limit
            else:
                print("results is empty")
                finished = True

        return all_tracks

    def download_track(self, trackid, audioformat="flac"):
        url = "/tracks/file/"
        params = {"id": trackid, "audioformat": audioformat}
        d = self.do_query(url, params)
