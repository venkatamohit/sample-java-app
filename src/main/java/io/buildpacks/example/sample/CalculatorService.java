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

    // Removed intentional errors

    // Unused private method removed
    // private void unusedPrivateMethod() {
    //     System.out.println("This method is never used.");
    // }

    // Unused parameter removed from subtract method
    // public int subtract(int a, int b, int c) {
    //     return a - b;
    // }

    // Removed misleading sum method
    // public int sum(int a, int b) {
    //     return a + b;
    // }

    // Corrected divide method to throw IllegalArgumentException
    // public int divide(int a, int b) {
    //     try {
    //         return a / b;
    //     } catch (ArithmeticException e) {
    //         return 0;
    //     }
    // }

    // Renamed Subtract method to follow naming convention
    // public int Subtract(int a, int b) {
    //     return a - b;
    // }
}
