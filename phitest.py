from egcd import ExtendedGCD

"""Testing RSA p, q for weaknesses

"""
__license__ = "poetic"

SMALL_PRIMES = ( 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59 )

def rsa_phi_test(p, q):
	egcd = ExtendedGCD(p, q)
	if egcd.gcd != 1:
		return False, 'Bad p/q, p and q not coprime (gcd is {})'.format(egcd.gcd)

	s, t = p - 1, q - 1

	g = ExtendedGCD(s, t).gcd

	for sp in SMALL_PRIMES:
		while not g % sp:
			g //= sp

	if g > 1:
		return False, 'Bad p/q, (p-1) and (q-1) share large factors (g is {})'.format(g)

	return True, ''

if __name__ == '__main__':
	from random import getrandbits

	N = 10000
	bits = 1024
	n_failed = 0

	for i in range(N):
		found = False
		while not found:
			p = getrandbits(bits)
			q = getrandbits(bits)

			# force p and q odd

			p += 1 - (p % 2)
			q += 1 - (q % 2)

			# faux primality test

			maybe_prime = True

			for sp in SMALL_PRIMES[1:]:
				if not p % sp or not q % sp:
					maybe_prime = False
					break

			if maybe_prime:
				found = True

		status, msg = rsa_phi_test(p, q)

		if not status:
			print(msg)
			n_failed += 1

	print('number of failed pairs: {} ({:.2%})'.format(n_failed, n_failed / N))
