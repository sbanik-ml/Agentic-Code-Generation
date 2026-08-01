
import math

class PrimeChecker:
    def __init__(self):
        pass

    def is_prime(self, n):
        """Check if a number is prime."""
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    def check_prime(self):
        """Get user input and display the result."""
        while True:
            try:
                num = input("Enter a number to check if it's prime (or 'q' to quit): ")
                if num.lower() == 'q':
                    break
                num = int(num)
                if num == -1:
                    break
                if self.is_prime(num):
                    print(f"{num} is a prime number.")
                else:
                    print(f"{num} is not a prime number.")
            except ValueError:
                print("Invalid input. Please enter an integer or 'q' to quit.")
            except EOFError:
                print("Input stream closed unexpectedly. Exiting...")
                break
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                break

def main():
    prime_checker = PrimeChecker()
    prime_checker.check_prime()

if __name__ == "__main__":
    main()

