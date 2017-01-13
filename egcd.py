# -*- coding: utf-8 -*-

"""Extended GCD

This library provides a pure python implementation of the extended GCD algorithm
The greatest common divisor of the two ints a and b is computed.
Additionally, it gives the Bézout coefficients and the canonical form of
the quotient a/b (no extra charge)

When the GCD is unary (a and b coprime), the zeroth Bézout coefficient
gives the multiplicative inverse of a mod b

References:

Greatest common divisor -
https://en.wikipedia.org/wiki/Greatest_common_divisor

Euclid's algorithm
https://en.wikipedia.org/wiki/Euclidean_algorithm

Bézouts identity -
https://en.wikipedia.org/wiki/B%C3%A9zout's_identity

Modular multiplicative inverse -
https://en.wikipedia.org/wiki/Modular_multiplicative_inverse

"""
__license__ = "poetic"

# https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm

def computed_method(f):
	def wrapped(self):
		self.compute()
		return f(self)
	return wrapped

class ExtendedGCD():
	def __init__(self, a, b):
		assert isinstance(a, int) and isinstance(b, int)
		self._a = a
		self._b = b
		self.computed = False

	@property
	def a(self):
		return self._a

	@property
	def b(self):
		return self._b

	@property
	@computed_method
	def bézout(self):
		return self._bézout

	@property
	@computed_method
	def gcd(self):
		return self._gcd

	@property
	@computed_method
	def quotient(self):
		return self._quotient

	@property
	def multiplicative_inverse(self):
		if self.gcd != 1:
			raise ValueError('gcd({}, {}) != 1, no multiplicative inverse exists'.format(self.a, self.b))
		return self.bézout[0]

	def compute(self):
		if not self.computed:
			r, prev_r = self.b, self.a
			s, prev_s = 0, 1
			t, prev_t = 1, 0

			while r != 0:
				q = prev_r // r
				prev_r, r = r, prev_r - q * r
				prev_s, s = s, prev_s - q * s
				prev_t, t = t, prev_t - q * t

			self._bézout = prev_s, prev_t
			self._gcd = prev_r
			self._quotient = s, t

			self.computed = True
