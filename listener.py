import redis
from channels import NEW
from channels import UPDATES

class Listener(object):

    def __init__(self, channels):
        self.channels = channels
        self.client = redis.Redis("localhost")
        self.ps = self.client.pubsub()

    def listen(self):
        self.ps.subscribe(self.channels)
        for item in self.ps.listen():
            self.alert(item['channel'], item['data'])

    def alert(self, channel, message):
        # TODO get users subscribed to this channel
        #   subscribers = get_subscribers(channel)
        # TODO send webhook/email/push to each of them
        #   for subscriber in subscribers:
        #       subscriber.notify()
        print "[%s] %s" % (channel, message)

if __name__ == "__main__":
    # Listen for channel updates
    Listener([UPDATES, NEW]).listen()
