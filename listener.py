import redis
from channels import NEW
from channels import UPDATES

def listen(channels):
    r = redis.Redis("localhost")
    ps = r.pubsub()
    ps.subscribe(channels)
    # Print messages
    for item in ps.listen():
        # TODO send webhook/email/push
        print "[%s] %s" % (item['channel'], item['data'])

if __name__ == "__main__":
    # Listen for channel updates
    listen([UPDATES, NEW])
