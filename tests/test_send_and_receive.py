from twisted.trial import unittest
from twisted.internet import defer, task, reactor
from task_receiver.message_helper import MessageHelper

class ClientTimeoutError(Exception):
    pass

class test_send_and_receive(unittest.TestCase):
  def setUp(self):
    self.timeout = 10
    self.clock = task.Clock()

  def test_send_and_receive(self):
    d = defer.Deferred()

    token = "test_send_and_receive"
    configuration = {
      "incoming": {
        "auto_delete_exchange": False,
        "auto_delete_queue": False,
        "durable": "true",
        "exchange": token + "x",
        "exchange_type": "fanout",
        "exclusive": False,
        "no_ack": False,
        "prefetch_count": 1,
        "queue": token + "q",
        "routing_key": "#"
      },
      "outgoing": {
        "auto_delete_exchange": False,
        "auto_delete_queue": False,
        "durable": "true",
        "exchange": token + "x",
        "exchange_type": "fanout",
        "exclusive": False,
        "queue": token + "qo",
        "routing_key": "key"
      },
      "password": "guest",
      "username": "guest",
      "vhost": "/",
      "host": "127.0.0.1",
      "port": 5672,
    }

    def sender_ready():
      helper.send("Arbitrary Message")

    def message_callback(thing):
      self.assertEqual(thing, "Arbitrary Message")
      helper.shutdown()
      self.clock.advance(5)
      d.callback("Completed")

    helper = MessageHelper(configuration, sender_ready, message_callback)
    helper.callLater = self.clock.callLater

    return d

if __name__ == '__main__':
  unittest.main()
