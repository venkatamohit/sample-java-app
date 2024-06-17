package io.buildpacks.example.sample;

/**
 * The MathOperations class provides a method to perform basic mathematical operations.
 * This class currently contains a method to sum two integers.
 */
public class MathOperations {

    /**
     * Sums two integers.
     * <p>
     * This method takes two integers as input parameters and returns their sum.
     * It is a straightforward implementation of addition.
     * 
     * @param a the first integer
     * @param b the second integer
     * @return the sum of a and b
     */
    public int sum(int a, int b) {
        return a + b;
    }

    /**
     * Main method to test the sum method.
     * <p>
     * This method creates an instance of the MathOperations class and tests the sum method
     * by printing the results of summing different pairs of integers.
     * 
     * @param args command-line arguments (not used)
     */
    public static void main(String[] args) {
        MathOperations mathOperations = new MathOperations();

        // Test the sum method and print the results
        System.out.println("Sum of 1 and 2: " + mathOperations.sum(1, 2)); // Expected output: 3
        System.out.println("Sum of 3 and 4: " + mathOperations.sum(3, 4)); // Expected output: 7
        System.out.println("Sum of 5 and 6: " + mathOperations.sum(5, 6)); // Expected output: 11
    }
}
