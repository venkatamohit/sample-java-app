public class IntegerCalculator {
    // Class to perform integer addition
    public static int sum(int a, int b) {
        return a + b;
    }
    public static void main(String[] args) {
        System.out.println(sum(5, 3)); // Expected output: 8
        System.out.println(sum(-1, 1)); // Expected output: 0
        System.out.println(sum(10, -5)); // Expected output: 5
        // Additional test cases
        System.out.println(sum(0, 0)); // Expected output: 0
        System.out.println(sum(100, 200)); // Expected output: 300
    }
}
