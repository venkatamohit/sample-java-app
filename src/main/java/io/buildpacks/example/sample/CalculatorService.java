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

    // Error 1: Uncommented method with misleading name
    public int sum(int a, int b) { // Misleading method name
        return a + b;
    }

    // Error 2: Unused private method
    private void unusedPrivateMethod() {
        System.out.println("This method is never used.");
    }

    // Error 3: Incorrect handling of exception
    public int divide(int a, int b) { // No throws clause
        try {
            return a / b;
        } catch (ArithmeticException e) {
            return 0; // Incorrect handling
        }
    }

    // Error 4: Unused parameter in method
    public int subtract(int a, int b, int c) { // Unused parameter 'c'
        return a - b;
    }

    // Error 5: Inconsistent naming convention
    public int Subtract(int a, int b) { // Method name starts with uppercase
        return a - b;
    }
}
