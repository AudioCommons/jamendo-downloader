"""

Download all jamendo licensing tracks.

"""

import argparse
import json

import config
import jamendo

def main(updatefile, outputfile):

    most_recent = None
    existing_ids = set()
    if updatefile:
        update = json.load(open(updatefile))
        update = sorted(update, key=lambda i: i["releasedate"], reverse=True)
        most_recent = update[0]["releasedate"]
        existing_ids = set([i["id"] for i in update])
        print("Updating {} with new recordings since {}".format(updatefile, most_recent))


    finished = False
    all_tracks = []
    offset = 0
    limit = 200
    j = jamendo.Jamendo(config.JAMENDO_KEY)
    while not finished:
        print("offset %s" % offset)
        d = j.get_tracks("musicinfo stats licenses", "1", "releasedate_desc", limit, offset)
        results = d["results"]
        if results:
            # Release date is at a day resolution. We check the date
            # including the most recent date, plus checking for the
            # ID in the existing file, because we may have missed
            # some from this day when we last updated.
            if not most_recent:
                all_tracks.extend(results)
            else:
                for r in results:
                    if r["releasedate"] >= most_recent and r["id"] not in existing_ids:
                        all_tracks.append(r)
                    else:
                        print("Caught up with newly added tracks")
                        finished = True
                        break

            offset += limit
        else:
            print("results is empty")
            finished = True

    if most_recent:
        all_tracks.extend(update)
    all_tracks = sorted(all_tracks, key=lambda i: i["releasedate"])
    json.dump(all_tracks, open(outputfile, "w"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", type=str, required=False, help="")
    parser.add_argument("output", type=str, help="Playlist output filename")
    args = parser.parse_args()
    main(args.u, args.output)

