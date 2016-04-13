import jamendo
import argparse
import json
import requests
import os
import errno

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

FILE_DIR = "audio"

def download(id, url):
    subdir = id % 10
    thedir = os.path.join(FILE_DIR, str(subdir))
    mkdir_p(thedir)
    fname = os.path.join(thedir, "%s.flac" % id)
    if os.path.exists(fname):
        print(" - exists")
    else:
        print(" - downloading")
        with open(fname, "wb") as fp:
            r = requests.get(url)
            fp.write(r.content)
        print (" - done")


def main(playlistfile):
    playlist = json.load(open(playlistfile))
    pllen = len(playlist)
    for i, t in enumerate(playlist, 1):
        print("{}/{} {} - {}".format(i, pllen, t["artist_name"], t["name"]))
        download(int(t["id"]), t["audiodownload"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("playlistfile", type=str, help="Playlist json filename")
    args = parser.parse_args()
    main(args.playlistfile)
