import argparse
import json

import config
import jamendo

def main(playlistid, outputfile):
    j = jamendo.Jamendo(config.JAMENDO_KEY)
    playlist = j.get_playlist(playlistid)
    with open(outputfile, "w") as fp:
        json.dump(playlist, fp)
    print("Done")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("playlistid", type=str, help="Playlist ID")
    parser.add_argument("output", type=str, help="Playlist output filename")
    args = parser.parse_args()
    main(args.playlistid, args.output)
