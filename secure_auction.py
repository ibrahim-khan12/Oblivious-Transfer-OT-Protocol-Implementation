from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, load_pem_public_key
import hashlib
import time

from auction_ot import NaorPinkasReceiver
from auction_ot import NaorPinkasSender

class Auctioneer:
    def __init__(self):
        self.ot_sender = NaorPinkasSender()
        self.bids = {}
        self.auction_id = hashlib.sha256(str(time.time()).encode()).hexdigest()
    
    def get_auction_params(self):
        return {
            'public_key': self.ot_sender.public_key,
            'auction_id': self.auction_id
        }
    
    def register_bidder(self, bidder_id, pk0, pk1):
        self.bids[bidder_id] = {
            'pk0': pk0,
            'pk1': pk1,
            'ciphertexts': None,
            'revealed_bid': None
        }
    
    def encrypt_bids(self, bidder_id, real_bid, dummy_bid):
        encrypted = self.ot_sender.encrypt_messages(
            self.bids[bidder_id]['pk0'],
            self.bids[bidder_id]['pk1'],
            str(real_bid),
            str(dummy_bid)
        )
        self.bids[bidder_id]['ciphertexts'] = encrypted['ciphertexts']
        return encrypted

class Bidder:
    def __init__(self, bid_value):
        self.real_bid = bid_value
        self.dummy_bid = 0  # Should be random in production
        self.ec_key = ec.generate_private_key(ec.SECP256R1())
        self.commitment = self._generate_commitment()
        self.ot_receiver = None
    
    def _generate_commitment(self):
        digest = hashes.Hash(hashes.SHA256())
        digest.update(str(self.real_bid).encode())
        digest.update(self.ec_key.public_key().public_bytes(
            Encoding.PEM,
            PublicFormat.SubjectPublicKeyInfo
        ))
        return digest.finalize()
    
    def prepare_ot(self, auctioneer_pk):
        self.ot_receiver = NaorPinkasReceiver(choice=0)
        return self.ot_receiver.generate_public_keys(auctioneer_pk)
    
    def decrypt_bid(self, ciphertexts):
        return self.ot_receiver.decrypt_message(ciphertexts[0])
    
    def generate_bid_proof(self):
        signature = self.ec_key.sign(
            str(self.real_bid).encode(),
            ec.ECDSA(hashes.SHA256())
        )
        return {
            'bid': self.real_bid,
            'commitment': self.commitment.hex(),
            'public_key': self.ec_key.public_key().public_bytes(
                Encoding.PEM,
                PublicFormat.SubjectPublicKeyInfo
            ).decode(),
            'signature': signature.hex()
        }

class SecureAuction:
    def __init__(self, duration=60):
        self.auctioneer = Auctioneer()
        self.bidders = {}
        self.start_time = time.time()
        self.duration = duration
    
    def register_bidder(self, bid_value):
        bidder_id = hashlib.sha256(str(time.time()).encode()).hexdigest()
        self.bidders[bidder_id] = Bidder(bid_value)
        return bidder_id
    
    def submit_bid(self, bidder_id):
        bidder = self.bidders[bidder_id]
        params = self.auctioneer.get_auction_params()
        
        # Generate OT parameters
        pks = bidder.prepare_ot(params['public_key'])
        
        # Register bidder with auctioneer
        self.auctioneer.register_bidder(bidder_id, pks['pk0'], pks['pk1'])
        
        # Encrypt bids
        encrypted = self.auctioneer.encrypt_bids(
            bidder_id,
            bidder.real_bid,
            bidder.dummy_bid
        )
        
        # Decrypt and verify bid
        decrypted_bid = bidder.decrypt_bid(encrypted['ciphertexts'])
        if int(decrypted_bid) != bidder.real_bid:
            raise ValueError("Bid decryption mismatch")
        
        # Store revealed bid
        self.auctioneer.bids[bidder_id]['revealed_bid'] = bidder.generate_bid_proof()
    
    def conclude_auction(self):
        if time.time() - self.start_time < self.duration:
            remaining = self.duration - (time.time() - self.start_time)
            raise Exception(f"Auction ongoing. {int(remaining)}s remaining")
        
        valid_bids = {}
        for bidder_id, data in self.auctioneer.bids.items():
            if data['revealed_bid'] and self._verify_bid(data['revealed_bid']):
                valid_bids[bidder_id] = data['revealed_bid']['bid']
        
        if not valid_bids:
            return {"winner": None, "bids": {}}
        
        winner_id = max(valid_bids, key=valid_bids.get)
        return {
            "winner": winner_id,
            "winning_bid": valid_bids[winner_id],
            "all_bids": valid_bids
        }
    
    def _verify_bid(self, bid_data):
        try:
            public_key = load_pem_public_key(
                bid_data['public_key'].encode()
            )
            public_key.verify(
                bytes.fromhex(bid_data['signature']),
                str(bid_data['bid']).encode(),
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except:
            return False