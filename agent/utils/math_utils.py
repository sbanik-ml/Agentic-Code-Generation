import math

def is_prime(n):
    """
    Checks if a number is prime.
    
    Parameters:
    n (int): The number to check.
    
    Returns:
    bool: True if the number is prime, False otherwise.
    """
    
    # Check if input is an integer
    if not isinstance(n, int):
        raise TypeError("Input must be an integer.")
    
    # Handle edge cases
    if n < 2:
        return False
    
    # Check for divisibility up to the square root of n
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    
    return True

# Test the function
print(is_prime(25))  # Should return False
print(is_prime(23))  # Should return True
print(is_prime(37))  # Should return True
print(is_prime(48))  # Should return False

def test_is_prime():
    # Test cases
    test_cases = [
        (25, False),
        (23, True),
        (37, True),
        (48, False),
        (2, True),
        (1, False),
        (0, False),
        (-1, False)
    ]
    
    for n, expected in test_cases:
        try:
            result = is_prime(n)
            assert result == expected, f"Expected is_prime({n}) to return {expected}, but got {result}"
        except TypeError as e:
            if n != int(n):
                continue
            else:
                raise e

    print("All test cases pass")

test_is_prime()
