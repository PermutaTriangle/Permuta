
def factorial(n):
    res = 1
    for i in range(2, n+1):
        res *= i
    return res


def binomial(n, k):
    if k > n:
        return 0
    if n-k < k:
        k = n-k
    res = 1
    for i in range(1, k+1):
        res = res * (n - (k - i)) // i
    return res


def catalan(n):
    return binomial(2*n, n)//(n+1)
