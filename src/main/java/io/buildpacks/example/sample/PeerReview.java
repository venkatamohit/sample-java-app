package io.buildpacks.example.sample;

/**
 * The PeerReview class provides a method to sum two integers.
 * This class also contains a main method to test the sum method.
 */
public class PeerReview {

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
     * This method creates an instance of the PeerReview class and tests the sum method
     * by printing the results of summing different pairs of integers.
     * 
     * @param args command-line arguments (not used)
     */
    public static void main(String[] args) {
        PeerReview peerReview = new PeerReview();

        // Test the sum method and print the results
        System.out.println("Sum of 1 and 2: " + peerReview.sum(1, 2)); // Expected output: 3
        System.out.println("Sum of 3 and 4: " + peerReview.sum(3, 4)); // Expected output: 7
        System.out.println("Sum of 5 and 6: " + peerReview.sum(5, 6)); // Expected output: 11
    }
}
