# -*- coding: utf-8 -*-

"""Modular exponentiation

Provides a pure python implementation of modular exponentiation
modexp(b, e, m) computes b^e mod m using python's pow(b, e, m)
by range reducing b, e and m to natural numbers

For negative exponents, modexp uses the identity b^-e == (b^-1)^e mod m
The multiplicative inverse b^-1 mod m is computed using the Extended GCD

modexp always returns natural numbers. negative numbers are converted
to the additive inverses of their magnitudes using the identity -a mod m = m-a mod m

"""
__license__ = "poetic"

from egcd import ExtendedGCD

def natural_mod(a, m):
	"mod returning natural number"

	assert isinstance(a, int) and isinstance(m, int)

	invert = False

	if m < 0:
		invert = True
		m = -m

	am = a % m
	if am < 0:
		am += m

	assert am >= 0 and m >= 0

	if invert:
		assert am <= m
		am = m - am

	return am

def congruent(a, b, m):
	"test for a = b mod m"

	return natural_mod(a, m) == natural_mod(b, m)

def natural_multiplicative_inverse(b, m):
	"modular multiplicative inverse returning natural number"

	assert isinstance(b, int) and isinstance(m, int)

	egcd = ExtendedGCD(b, m)
	mi = egcd.multiplicative_inverse
	mi_m = natural_mod(mi, m)

	return mi_m

def natural_additive_inverse(a, m):
	"modular additive inverse returning natural number"

	assert isinstance(a, int) and isinstance(m, int)

	ai = natural_mod(-a, m)

	return ai


def natural_pow(b, e, m, sign):
	"modular power for natural numbers returning natural number"

	assert isinstance(b, int) and isinstance(e, int)
	assert isinstance(m, int)
	assert sign == 1 or sign == -1
	assert b >= 0 and e >= 0 and m >= 0

	np = natural_mod(sign * pow(b, e, m), m)
	return np

def natural_modexp(b, e, m):
	"modular exponentiation returning natural number"

	assert isinstance(b, int) and isinstance(e, int) and isinstance(m, int)

	sign = 1

	if m < 0:
		sign = -sign
		m = -m

	if b < 0:
		b = natural_mod(b, m)

	if e < 0:
		e =- e
		b = natural_multiplicative_inverse(b, m)

	return natural_pow(b, e, m, sign)

def test_natural_modexp(n):
	from random import choice

	big_number = 1000 * 1000 * 1000 * 10000
	big_range = range(1, big_number)

	n_coprime = 0

	for i in range(n):
		while True:
			b = choice(big_range)
			e = choice(big_range)
			m = choice(big_range)

			# the base probability of b and m being coprime approaches 6/pi^2 (~61%)

			# force b and m odd to make the probability even higher (~80%)

			b += 1 - (b % 2)
			m += 1 - (m % 2)

			# make sure at most one of the ints is divisible by 3
			# (raises the probalitity of comprimality to 90+%)

			if b % 3 or m % 3:
				break

		egcd = ExtendedGCD(b, m)
		if egcd.gcd == 1:
			n_coprime += 1

			# verify that b^e == (b^-1)^-e mod m

			c = natural_modexp(b, e, m)
			B = egcd.multiplicative_inverse
			C = natural_modexp(B, -e, m)

			try:
				assert congruent(c, C, m)
			except AssertionError:
				print('incongruence; b^e != (b^-1)^-e mod m')
				print('  b={}, e={}, m={}'.format(b, e, m))
				print('  c={}, B={}, C={}'.format(c, B, C))
				raise

			# verify that b^e * b^-e == 1 mod m

			d = natural_modexp(b, -e, m)

			try:
				assert congruent(c * d, 1, m)
			except AssertionError:
				print('incongruence; b^e * b^-e != 1 mod m')
				print('  b={}, e={}, m={}'.format(b, e, m))
				print('  c={}, d={}'.format(c, d))
				raise

	print('# coprimes tested = {}'.format(n_coprime))

if __name__ == '__main__':
	import sys

	try:
		if sys.argv[1] == 'test':
			n = 100
			try:
				n = int(sys.argv[2])
			except IndexError:
				pass

			test_natural_modexp(n)

		else:
			b = int(sys.argv[1])
			e = int(sys.argv[2])
			m = int(sys.argv[3])

			c = natural_modexp(b, e, m)
			print('natural_modexp({}, {}, {}) = {}'.format(b, e, m, c))

	except IndexError:
		raise
		print('usage:')
		print('  (python) natural_modexp b e m')
		print('    compute b^e mod m')
		print('  (python) natural_modexp test n')
		print('    tests implementation n times')
	except ValueError:
		print('integer expected')
