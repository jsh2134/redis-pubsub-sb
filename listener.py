import redis
from channels import NEW
from channels import UPDATES

def listen(channels):
    r = redis.Redis("localhost")
    ps = r.pubsub()
    ps.subscribe(channels)
    # Print messages
    for item in ps.listen():
        alert(item['channel'], item['data'])

def alert(channel, message):
    # TODO get users subscribed to this channel
    #   subscribers = get_subscribers(channel)
    # TODO send webhook/email/push to each of them
    #   for subscriber in subscribers:
    #       subscriber.notify()
    print "[%s] %s" % (channel, message)

if __name__ == "__main__":
    # Listen for channel updates
    listen([UPDATES, NEW])
