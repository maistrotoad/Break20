def factor(number):
    factors = []

    for whole_number in range(1, number + 1):
        if number % whole_number == 0:
            factors.append(whole_number)

    print(factors)