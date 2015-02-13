import urllib2
import redis
import solvebio
import dateutil.parser
from channels import NEW, UPDATES

# Redis Keys
DEPOS = "depos"
DEPO_KEY = "depos_%s"

def iso_to_dt(isotime):
    """ Convert isoformat time to datetime using dateutil
        because python iso converstion with TZ is no bueno
    """
    return dateutil.parser.parse(isotime)

def get_fresh_depos():
    """ return list of all solvebio depos """
    try:
        depos = solvebio.Depository.all()
        return depos
    except urllib2.HTTPError as e:
        print "API Error code: %s" % e.code
        return []

def get_stored_depo_status(r):
    """ return a dict of stored depos {name:updated_timestamp} """
    stored_depos = r.smembers(DEPOS)
    pipe = r.pipeline()
    for depo in stored_depos:
        pipe.get(DEPO_KEY % depo)
    depo_res = pipe.execute()
    depo_tups = zip(stored_depos, depo_res)
    # if key not found dtime will be None, so ignore
    return {d:dtime for d,dtime in depo_tups if dtime}

def alert_updated_depos(r, fresh_depos, stored_depos):
    """ Alert subscribers to a new or updated depository """
    for depo in fresh_depos:
        # New Depo
        if depo.name not in stored_depos:
            r.publish(NEW, "New Dataset %s" % depo.name)
            r.sadd(DEPOS, depo.name)
            r.set(DEPO_KEY % depo.name, depo.updated_at)
        else:
            depo_time = iso_to_dt(stored_depos[depo.name])
            # Updated Depo
            if depo_time != iso_to_dt(depo.updated_at):
                r.publish(UPDATES, "Updated Dataset %s found. Updated at %s" % (depo.name, depo.updated_at))
                r.set(DEPO_KEY % depo.name, depo.updated_at)

#############
#
# Pull latest Depository data from SolveBio
# Grab stored Depository data from redis
# Alert to new/updated depositories on different channels
#
#############
if __name__ == '__main__':
    # login environment or hardcode key
    # solvebio.api_key = 'YOUR KEY'
    r = redis.Redis("localhost")
    fresh_depos = get_fresh_depos()
    stored_depos = get_stored_depo_status(r)
    alert_updated_depos(r, fresh_depos, stored_depos)



