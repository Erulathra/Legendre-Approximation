def legendre_polynomial(x: float, degree: int):
    previous_result = 1
    result = x

    if degree == 0:
        return previous_result
    elif degree == 1:
        return result

    for n in range(1, degree):
        new_result = (2 * n + 1) * x * result - n * previous_result
        new_result /= (n + 1)

        previous_result = result
        result = new_result

    return result
