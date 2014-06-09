from behave import *
from test_util import settings
# import tornado.ioloop
from zmq.eventloop import ioloop
ioloop.install()
from node.crypto2crypto import *
import gevent
from gevent import socket
from tornado.testing import *

import logging

port = 12345

def create_layers(context, num_layers):
    layers = []
    for i in range(num_layers):
        layers.append(CryptoTransportLayer('127.0.0.%s' % str(i+1), port, i))
    context.layers = layers
    # Thread(target=ioloop.IOLoop.current().start).start()
    gevent.spawn(ioloop.IOLoop.current().start)


@given('there are {num_layers} layers')
def step_impl(context, num_layers):
    create_layers(context, int(num_layers))

class MyTestCase(AsyncTestCase):
    @tornado.testing.gen_test
    def test_join_network(node, uri):
        yield node.join_network(uri)
        # client = AsyncHTTPClient(self.io_loop)
        # response = yield client.fetch("http://www.tornadoweb.org")
        # Test contents of response
        # self.assertIn("FriendFeed", response.body)


@when('layer {i} connects to layer {j}')
def step_impl(context, i, j):
    i = context.layers[int(i)]
    j = context.layers[int(j)]
    # MyTestCase.test_join_network(j, None)
    j.join_network(None)
    # ioloop.IOLoop.instance().run_sync(lambda : j.join_network(None))
    # MyTestCase.test_join_network(i, j._uri)
    i.join_network(j._uri)
    ioloop.IOLoop.add_timeout(10000, ioloop.IOLoop.stop())
    ioloop.IOLoop.instance().start()
    # ioloop.IOLoop.instance().run_sync(i.join_network, j._uri)

@then('layer {i} is aware of layer {j}')
def step_impl(context, i, j):
    i = int(i)
    j = int(j)
    iLayer = context.layers[i]
    jLayer = context.layers[j]

    print jLayer._knownNodes
    logging.getLogger('').info(iLayer._knownNodes)
    logging.getLogger('').info(jLayer._knownNodes)
    logging.getLogger('').info(jLayer._activePeers[0]._guid)

    assert(('127.0.0.%s'% (j+1), port, jLayer.guid) in iLayer._knownNodes)
    assert(jLayer._guid in map(lambda x: x._guid, iLayer._activePeers))
    # i is not in jLayer._knownNodes
    assert(iLayer._guid in map(lambda x: x._guid, jLayer._activePeers))


# @when('there are {num_layers} connected layers')
# def step_impl(context, num_layers):
#     create_layers(context, numLayers):
#     for l in range(len(context.layers)-1):
#         layers.



