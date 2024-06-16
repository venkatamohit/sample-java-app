// MathUtils.java

/**
 * A utility class containing methods for mathematical operations.
 */
public class MathUtils {

    /**
     * Calculates the sum of two integers.
     * 
     * @param a the first integer
     * @param b the second integer
     * @return the sum of a and b
     */
    public static int sum(int a, int b) {
        return a + b;
    }

    public static void main(String[] args) {
        // Test cases
        System.out.println(sum(5, 3));   // Expected output: 8
        System.out.println(sum(-1, 1));  // Expected output: 0
        System.out.println(sum(10, -5)); // Expected output: 5
    }
}
