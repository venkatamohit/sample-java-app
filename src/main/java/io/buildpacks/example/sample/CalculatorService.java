package io.buildpacks.example.sample;

import org.springframework.stereotype.Service;

@Service
public class CalculatorService {

    public int add(int a, int b) {
        return a + b;
    }

    public int subtract(int a, int b) {
        return a - b;
    }

    public int multiply(int a, int b) {
        return a * b;
    }

    public int divide(int a, int b) throws IllegalArgumentException {
        if (b == 0) {
            throw new IllegalArgumentException("Division by zero is not allowed.");
        }
        return a / b;
    }

    // Intentional errors added below

    // Error 1: Uncommented method with syntax error
    /*
    public int modulo(int a, int b) {
        return a % b;
    */

    // Error 2: Method with unreachable code
    public int subtractWithUnusedParameter(int a, int b, int c) {
        int result = a - b;
        if (c > 0) {
            return result;
        } else {
            return result; // Unreachable code here
        }
    }

    // Error 3: Incorrect exception type in method signature
    public int divide(int a, int b) throws ArithmeticException { // Should be IllegalArgumentException
        if (b == 0) {
            throw new ArithmeticException("Division by zero is not allowed.");
        }
        return a / b;
    }

    // Error 4: Unhandled exception in method signature
    public int safeDivide(int a, int b) { // Should declare throws IllegalArgumentException
        if (b == 0) {
            throw new IllegalArgumentException("Division by zero is not allowed.");
        }
        return a / b;
    }

    // Error 5: Incorrect logic in method
    public int divideByZero(int a, int b) throws IllegalArgumentException {
        if (b != 0) { // Should be if (b == 0)
            throw new IllegalArgumentException("Division by zero is not allowed.");
        }
        return a / b;
    }
}
