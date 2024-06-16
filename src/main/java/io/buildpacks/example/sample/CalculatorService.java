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
     * @throws IllegalArgumentException If any input is null.
     */
    public int performAddition(Integer a, Integer b) {
        validateInputs(a, b);
        return a + b;
    }

    /**
     * Performs subtraction of two integers.
     *
     * @param a The first integer (minuend).
     * @param b The second integer (subtrahend).
     * @return The result of subtracting b from a.
     * @throws IllegalArgumentException If any input is null.
     */
    public int performSubtraction(Integer a, Integer b) {
        validateInputs(a, b);
        return a - b;
    }

    /**
     * Performs multiplication of two integers.
     *
     * @param a The first integer.
     * @param b The second integer.
     * @return The product of a and b.
     * @throws IllegalArgumentException If any input is null.
     */
    public int performMultiplication(Integer a, Integer b) {
        validateInputs(a, b);
        return a * b;
    }

    /**
     * Performs division of two integers.
     *
     * @param a The numerator.
     * @param b The denominator.
     * @return The result of dividing a by b.
     * @throws ArithmeticException If b is zero.
     * @throws IllegalArgumentException If any input is null.
     */
    public int performDivision(Integer a, Integer b) throws ArithmeticException, IllegalArgumentException {
        validateInputs(a, b);
        if (b == 0) {
            throw new ArithmeticException("Division by zero is not allowed.");
        }
        return a / b;
    }

    /**
     * Helper method to validate input parameters.
     *
     * @param inputs The input parameters to validate.
     * @throws IllegalArgumentException If any input is null.
     */
    private void validateInputs(Integer... inputs) {
        for (Integer input : inputs) {
            if (input == null) {
                throw new IllegalArgumentException("Input parameters cannot be null.");
            }
        }
    }

    // Other methods can be similarly refactored and documented as needed

}
