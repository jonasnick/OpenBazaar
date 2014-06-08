from behave import *
from node.crypto2crypto import *
from test_util import settings
import logging

port = 12345

def create_layers(context, num_layers):
    layers = []
    for i in range(num_layers):
        layers.append(CryptoTransportLayer('127.0.0.%s' % str(i+1), port, i))
    context.layers = layers

@given('there are {num_layers} layers')
def step_impl(context, num_layers):
    create_layers(context, int(num_layers))

@when('layer {i} connects to layer {j}')
def step_impl(context, i, j):
    i = context.layers[int(i)]
    j = context.layers[int(j)]
    j.join_network(None)
    i.join_network(j._uri)

@then('layer {i} knows layer {j}')
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


