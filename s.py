class EncryptionContext(object):
    """ Holds state of encryption.  Use AffinePoint.encrypt_to """

    def __init__(self, f, p, mac_bytes=10):
        self.f = f
        self.mac_bytes = mac_bytes
        key, R = p._ECIES_encryption()
        self.h = hmac.new(key[32:], digestmod=hashlib.sha256)
        f.write(R.to_bytes(SER_BINARY))
        ctr = Crypto.Util.Counter.new(128, initial_value=0)
        self.cipher = Crypto.Cipher.AES.new(
            key[:32], Crypto.Cipher.AES.MODE_CTR, counter=ctr)

    def finish(self):
        if not self.f:
            raise IOError("closed")
        self.f.write(self.h.digest()[:self.mac_bytes])
        self.f = None

class DecryptionContext(object):
    """ Holds state of decryption.  Use Curve.decrypt_from """

    def __init__(self, curve, f, privkey, mac_bytes=10):
        self.f = f
        self.mac_bytes = mac_bytes
        R = curve.point_from_string(f.read(curve.pk_len_bin), SER_BINARY)
        key = R._ECIES_decryption(privkey)
        self.h = hmac.new(key[32:], digestmod=hashlib.sha256)
        ctr = Crypto.Util.Counter.new(128, initial_value=0)
        self.cipher = Crypto.Cipher.AES.new(
            key[:32], Crypto.Cipher.AES.MODE_CTR, counter=ctr)
        self.ahead = f.read(mac_bytes)

    
def encrypt_to(self, f, mac_bytes=10):
        """ Returns a file like object `ef'.  Anything written to `ef'
            will be encrypted for this pubkey and written to `f'. """
        ctx = EncryptionContext(f, self.p, mac_bytes)
        yield ctx
        ctx.finish()
    
def encrypt(self, s, mac_bytes=10):
        """ Encrypt `s' for this pubkey. """
        if isinstance(s, six.text_type):
            raise ValueError(
                "Encode `s` to a bytestring yourself to" +
                " prevent problems with different default encodings")
        out = BytesIO()
        with self.encrypt_to(out, mac_bytes) as f:
            f.write(s)
        return out.getvalue()
    
    
def decrypt_from(self, f, mac_bytes=10):
    """ Decrypts a message from f. """
    ctx = DecryptionContext(self.curve, f, self, mac_bytes)
    yield ctx
    ctx.read()

def decrypt(self, s, mac_bytes=10):
    if isinstance(s, six.text_type):
        raise ValueError("s should be bytes")
    instream = BytesIO(s)
    with self.decrypt_from(instream, mac_bytes) as f:
        return f.read()
    
    
    
class ECIES:
    
    def _ECIES_KDF(self, R):
        h = hashlib.sha512()
        h.update(serialize_number(self.x, SER_BINARY, self.curve.elem_len_bin))
        h.update(serialize_number(R.x, SER_BINARY, self.curve.elem_len_bin))
        h.update(serialize_number(R.y, SER_BINARY, self.curve.elem_len_bin))
        return h.digest()
    
    def _ECIES_encryption(self):
        while True:
            k = gmpy2.mpz(
                Crypto.Random.random.randrange(
                    0, int(self.curve.order - 1)))
            R = self.curve.base * k
            k = k * self.curve.cofactor
            Z = self * k
            if Z:
                break
        return (Z._ECIES_KDF(R), R)
    
    def _ECIES_decryption(self, d):
        if isinstance(d, PrivKey):
            d = d.e
        e = d * self.curve.cofactor
        if not self.valid_embedded_key:
            raise ValueError
        Z = self * e
        if not Z:
            raise ValueError
        return Z._ECIES_KDF(self)
    
    def passphrase_to_pubkey(self, passphrase):
            return PubKey(self.base * self.passphrase_to_privkey(passphrase).e)