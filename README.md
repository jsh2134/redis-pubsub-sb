Simple Redis Pub/Sub implementation for Solvebio depository changes


Setup and Install
------------------
* pip install redis python-dateutil solvebio
* start redis-server locally
* login to solvebio

Run
-----
* start listener
    $ python listener.py

* run publisher in new window
    $ python publish.py

