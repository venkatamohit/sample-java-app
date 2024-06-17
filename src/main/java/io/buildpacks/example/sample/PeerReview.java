package com.example;

/**
 * This class demonstrates a simple example of a Java program.
 */
public class Main {

    /**
     * Calculates the factorial of a given number.
     * @param n The number for which factorial needs to be calculated.
     * @return The factorial of n.
     */
    public static int factorial(int n) {
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
     * Main method that demonstrates the usage of the factorial method.
     * @param args Command-line arguments (not used in this example).
     */
    public static void main(String[] args) {
        int number = 5;
        int fact = factorial(number);
        System.out.println("Factorial of " + number + " is: " + fact);
        
        // Incorrect method call, should be factorial(5)
        int incorrectFact = factorial(6); // This will calculate 6! instead of 5!
        System.out.println("Factorial of 6 is: " + incorrectFact);
    }

    // Missing Javadoc for this method
    public static int multiply(int a, int b) {
        return a * b;
    }

    // Inconsistent naming convention for methods, should be camelCase
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

}
