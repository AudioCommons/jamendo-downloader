# AudioCommons Jamendo tools

This project contains tools used to get metadata and recordings from Jamendo for use
in the AudioCommons project.

We are currently working with the Jamendo Licensing catalog. This catalog has about 200,000
available tracks, of which we are using a subset of about 80,000.

## Setup

This code uses python 3. Make sure to use a python3 virtual environment
(`virtualenv -p python3 ve`) or use `python3`/`pip3`.

Install dependencies with

    $ pip -r requirements

To configure, copy `config.py.dist` to `config.py` and fill in your
jamendo api key.



## Usage

To get the contents of the licensing catalog

    $ python getlicensing.py <outputname.json>

To update the catalog with entries that have been published since a playlist was downloaded

    $ python getlicensing.py -u <existingplaylist.json> <outputname.json>

To get the contents of a playlist

    $ python getplaylist.py <playlistid> <outputname.json>

To download the flac files listed in a playlist file

    $ python downloadplaylist.py <playlistfile.json>
