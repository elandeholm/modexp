from egcd import ExtendedGCD
from modexp import natural_modexp, natural_mod, congruent

"""Pure Python Toy RSA implementation

Warning: no padding, no checking public exponent for bad values
beyond guaranteeing coprimality of e and phi
If e does not have a multiplicative inverse mod phi, an exception is generated

References:

RSA -
https://en.wikipedia.org/wiki/RSA_(cryptosystem)

"""
__license__ = "poetic"

class ToyRSA():
	def __init__(self, p=None, q=None, e=None):
		if p is None:
			p = 123471147116473837
		if q is None:
			q = 157049038824611

		phi = self._compute_phi(p, q)
		self._n = p * q

		if e is None:
			e = 65537
		self._e = self._reduce(e)

		egcd = ExtendedGCD(self._e, phi)

		if egcd.gcd != 1:
			raise ValueError('Bad e, e and phi not coprime (gcd is {})'.format(egcd.gcd))

		self._d = natural_mod(egcd.multiplicative_inverse, phi)

		assert congruent(self._d * self._e, 1, phi)

	def _compute_phi(self, p, q):
		egcd = ExtendedGCD(p, q)
		if egcd.gcd != 1:
			raise ValueError('Bad p/q, p and q not coprime (gcd is {})'.format(egcd.gcd))

		s, t = p - 1, q - 1

		small_primes = ( 2, 3, 5, 7, 11, 13 )

		g = ExtendedGCD(s, t).gcd

		for sp in small_primes:
			while not g % sp:
				g //= sp

		if g > 1:
			raise ValueError('Bad p/q, (p-1) and (q-1) share large factors (g is {})'.format(g))

		return s * t

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

	trsa = ToyRSA(p=123456719, q=101820033136434259, e=65537)

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
