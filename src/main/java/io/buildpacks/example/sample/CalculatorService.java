package io.buildpacks.example.sample;

import org.springframework.stereotype.Service;

/**
 * Service class providing basic calculator operations.
 */
@Service
public class CalculatorService {

    /**
     * Performs addition of two integers.
     *
     * @param a The first integer.
     * @param b The second integer.
     * @return The sum of a and b.
     */
    public int performAddition(int a, int b) {
        // TODO: Add input parameter validation here if necessary
        return a + b;
    }

    /**
     * Performs subtraction of two integers.
     *
     * @param a The first integer (minuend).
     * @param b The second integer (subtrahend).
     * @return The result of subtracting b from a.
     */
    public int performSubtraction(int a, int b) {
        // TODO: Add input parameter validation here if necessary
        return a - b;
    }

    /**
     * Performs multiplication of two integers.
     *
     * @param a The first integer.
     * @param b The second integer.
     * @return The product of a and b.
     */
    public int performMultiplication(int a, int b) {
        // TODO: Add input parameter validation here if necessary
        return a * b;
    }

    /**
     * Performs division of two integers.
     *
     * @param a The numerator.
     * @param b The denominator.
     * @return The result of dividing a by b.
     * @throws IllegalArgumentException If b is zero.
     */
    public int performDivision(int a, int b) throws IllegalArgumentException {
        if (b == 0) {
            throw new IllegalArgumentException("Division by zero is not allowed.");
        }
        return a / b;
    }

    // Other methods can be similarly refactored and documented as needed

}
