import os
import argparse
import acoustid
import config

def fingerprint(thefile):
    for score, recording_id, title, artist in acoustid.match(config.ACOUSTID_KEY, thefile):
        #print("{} - {} - {}".format(artist, title, recording_id))
        return 1
    return 0

def main(thedir):
    total = 0
    matches = 0
    for root, dirs, files in os.walk(thedir):
        for f in files:
            fname = os.path.join(root, f)
            print(fname)
            fp = fingerprint(fname)
            matches += fp
            total += 1
    print("matched {}/{} files with fingerprint".format(matches, total))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("audiodir", type=str)
    args = parser.parse_args()
    main(args.audiodir)
