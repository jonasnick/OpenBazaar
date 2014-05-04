import json
import sys
import pyelliptic as ec

from p2p import PeerConnection, TransportLayer
from multiprocessing import Process
import traceback

from protocol import hello, proto_response_pubkey
import obelisk

# Check if user specified a crypto file to load for their marketplace
# This is located in the ppl/ folder 
if len(sys.argv) < 2:
    print >> sys.stderr, "[Error] You need to specify a user crypto file in `ppl/` folder"
    sys.exit(-1)

# Return data array with details from the crypto file
# TODO: This needs to be protected better; potentially encrypted file or DB
def load_crypto_details():
    print sys.argv[1]
    with open(sys.argv[1]) as f:
        data = json.loads(f.read())
    assert "nickname" in data
    assert "secret" in data
    assert "pubkey" in data
    assert len(data["secret"]) == 2 * 32
    assert len(data["pubkey"]) == 2 * 33
    return data["nickname"], data["secret"].decode("hex"), data["pubkey"].decode("hex")

# Look in crypto file for market details
NICKNAME, SECRET, PUBKEY = load_crypto_details()

class CryptoPeerConnection(PeerConnection):

    def __init__(self, address, transport, pub):
        self._transport = transport
        self._priv = transport._myself
        self._pub = pub
        PeerConnection.__init__(self, address)

    def encrypt(self, data):
        return self._priv.encrypt(data, self._pub)

    def send(self, data):
        self.send_raw(self.encrypt(json.dumps(data)))

    def on_message(self, msg):
        # this are just acks
        pass

class CryptoTransportLayer(TransportLayer):

    def __init__(self, port=None):
        TransportLayer.__init__(self, port)
        self._myself = ec.ECC(curve='secp256k1')
        self.nick_mapping = {}

    def get_profile(self):
        peers = {}
        for uri, peer in self._peers.iteritems():
            if peer._pub:
                peers[uri] = peer._pub.encode('hex')
        return {'uri': self._uri, 'pub': self._myself.get_pubkey().encode('hex'), 'peers': peers}

    def respond_pubkey_if_mine(self, nickname, ident_pubkey):
        
        if ident_pubkey != PUBKEY:
            print "Public key does not match your identity"
            return
        
        # Return signed pubkey     
        pubkey = self._myself.get_pubkey()
        ec_key = obelisk.EllipticCurveKey()
        ec_key.set_secret(SECRET)
        digest = obelisk.Hash(pubkey)
        signature = ec_key.sign(digest)
        
        # Send array of nickname, pubkey, signature to transport layer
        self.send(proto_response_pubkey(nickname, pubkey, signature))


    def create_peer(self, uri, pub):
        if pub:
            self.log("Creating peer " + uri + " " + pub[0:16] + "...", '*')
            pub = pub.decode('hex')
        else:
            self.log("Creating peer [seed] " + uri, '*')

        # Create the peer
        self._peers[uri] = CryptoPeerConnection(uri, self, pub)

        # Call 'peer' callbacks on listeners
        self.trigger_callbacks('peer', self._peers[uri])

        # Now send a hello message to the peer
        if pub:
            self.log("Sending encrypted profile to %s" % uri)
            self._peers[uri].send(hello(self.get_profile()))
        else:
            # Will send clear profile on initial if no pub
            self.log("Sending unencrypted profile to %s" % uri)
            profile = hello(self.get_profile())
            self._peers[uri].send_raw(json.dumps(profile))

    def init_peer(self, msg):
        print "Initialize Peer: ", msg
        uri = msg['uri']
        pub = msg.get('pub')        
        if not uri in self._peers:
            print 'Create New Peer: ',uri
            self.create_peer(uri, pub)
        elif pub and not self._peers[uri]._pub:
            self.log("Setting public key for seed node")
            self._peers[uri]._pub = pub.decode('hex')

	
    def on_raw_message(self, serialized):
        
        try:
            msg = json.loads(serialized)
            self.log("receive [%s]" % msg.get('type', 'unknown'))
        except ValueError:
            try:
                msg = json.loads(self._myself.decrypt(serialized))
                self.log("Decrypted raw message [%s]" % msg.get('type', 'unknown'))
            except:
                self.log("incorrect msg ! %s..." % self._myself.decrypt(serialized))
                traceback.print_exc()
                return

        msg_type = msg.get('type')              
        
        if msg_type == 'hello' and msg.get('uri') :
            self.init_peer(msg)
            for uri, pub in msg.get('peers', {}).iteritems():
                # Do not add yourself as a peer
                if uri != self._uri:
                    self.init_peer({'uri': uri, 'pub': pub})
            self.log("Update peer table [%s peers]" % len(self._peers))
        else:
            self.on_message(msg)
            
            
