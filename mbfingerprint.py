import os
import argparse
import acoustid
import config
import time
import json

RETRIES = 5

def fingerprint(thefile):
    attempt = 0
    success = False
    while not success and attempt < RETRIES:
        try:
            matches = acoustid.match(config.ACOUSTID_KEY, thefile)
            success = True
        except acoustid.WebServiceError as e:
            time.sleep(1)
            attempt += 1

    if success:
        return list(matches)
    return []

def save_cache(data):
    json.dump(data, open("lookupcache.json", "w"))

def main(thedir):
    if os.path.exists("lookupcache.json"):
        data = json.load(open("lookupcache.json"))
    else:
        data = {}
    total = 0
    matches = 0
    for root, dirs, files in os.walk(thedir):
        for f in files:
            fname = os.path.join(root, f)
            print(fname)
            if fname not in data:
                matchdata = fingerprint(fname)
                data[fname] = matchdata
            else:
                matchdata = data[fname]
            if matchdata:
                matches += 1
            total += 1
            if total % 10 == 0:
                print("{}: matched {}/{} fingerprints".format(total, matches, total))
                save_cache(data)
    save_cache(data)
    print("matched {}/{} files with fingerprint".format(matches, total))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("audiodir", type=str)
    args = parser.parse_args()
    main(args.audiodir)
