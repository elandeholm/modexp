from random import randint
from egcd import ExtendedGCD
from modexp import natural_modexp, natural_mod, congruent

"""Pure Python Toy RSA implementation

Warning: no padding, no coprimality testing, no checking public exponent for bad values
beyond guaranteeing coprimality of e and phi
If e does not have a multiplicative inverse mod phi, an exception is generated

Note that even if e does have a multiplicative inverse mod phi, the encryption will be
weak if p and q are not coprime and/or e is small

"""

class ToyRSA():
	def __init__(self, p=None, q=None, e=None):
		if p is None:
			p = 123471147116473837
		if q is None:
			q = 157049038824611

		self._n = p * q
		phi = (p - 1) * (q - 1)	

		if e is None:
			e = 65537
		self._e = self._reduce(e)

		egcd = ExtendedGCD(self._e, phi)

		assert egcd.gcd == 1

		self._d = natural_mod(egcd.multiplicative_inverse, phi)

		assert congruent(self._d * self._e, 1, phi)

	def _reduce(self, a):
		return natural_mod(a, self.modulus)

	@property
	def modulus(self):
		return self._n

	@property
	def private_exponent(self):
		return self._d

	@property
	def public_exponent(self):
		return self._e

	def encrypt(self, m):
		return natural_modexp(m, self.public_exponent, self.modulus)

	def decrypt(self, m):
		return natural_modexp(m, self.private_exponent, self.modulus)

	def roundtrip(self, m):
		assert congruent(self.decrypt(self.encrypt(m)), m, self.modulus)
		assert congruent(self.encrypt(self.decrypt(m)), m, self.modulus)

if __name__ == '__main__':
	import sys

	trsa = ToyRSA()

	try:
		for arg in sys.argv[1:]:
			m = int(arg)
			m_n = natural_mod(m, trsa.modulus)

			trsa.roundtrip(m_n)

			e = trsa.encrypt(m)
			d = trsa.decrypt(e)

			print('m = {} = {} mod {}'.format(m, m_n, trsa.modulus))
			print('e = {}'.format(e))
			print('d = {}'.format(d))

	except ValueError:
		print('integer expected')
