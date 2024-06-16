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

    // Corrected method - modulo with correct syntax
    public int modulo(int a, int b) {
        return a % b;
    }

    // Corrected method - removed unreachable code
    public int subtractWithUnusedParameter(int a, int b, int c) {
        int result = a - b;
        return result;
    }

    // Corrected method - using correct exception type
    public int divide(int a, int b) throws IllegalArgumentException {
        if (b == 0) {
            throw new IllegalArgumentException("Division by zero is not allowed.");
        }
        return a / b;
    }

    // Corrected method - added throws IllegalArgumentException
    public int safeDivide(int a, int b) throws IllegalArgumentException {
        if (b == 0) {
            throw new IllegalArgumentException("Division by zero is not allowed.");
        }
        return a / b;
    }

    // Corrected method - fixed logic to throw exception when dividing by zero
    public int divideByZero(int a, int b) throws IllegalArgumentException {
        if (b == 0) {
            throw new IllegalArgumentException("Division by zero is not allowed.");
        }
        return a / b;
    }
}
