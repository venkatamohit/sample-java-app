package com.example;

/**
 * This class demonstrates intentional issues to fail code review.
 */
public class Main {

    /**
     * Incorrect method name and missing Javadoc.
     */
    public static int Factorial(int n) {
        if (n == 0) {
            return 1;
        }
        int result = 1;
        for (int i = 1; i <= n; i++) {
            result *= i;
        }
        return result;
    }

    /**
     * Main method with incorrect usage of Factorial method.
     */
    public static void main(String[] args) {
        int number = 5;
        int fact = Factorial(number); // Incorrect method call
        System.out.println("Factorial of " + number + " is: " + fact);
        
        // Division by zero
        int result = 10 / a; // This will throw ArithmeticException
        System.out.println("Result: " + result);
    }
}
