// core/calc_functions.c
// Final C library with a full suite of scientific and hyperbolic functions.

#include <math.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

// --- Basic & Advanced Operations ---
double add(double a, double b) { return a + b; }
double sub(double a, double b) { return a - b; }
double mul(double a, double b) { return a * b; }
double divide(double a, double b) { return (b == 0) ? NAN : a / b; }
double power(double base, double exp) { return pow(base, exp); }
double root(double a) { return (a < 0) ? NAN : sqrt(a); }
double modulo(double a, double b) { return fmod(a, b); }
double power_of_two(double a) { return pow(a, 2); }
double inverse(double a) { return (a == 0) ? NAN : 1.0 / a; }

// --- Trigonometric Functions ---
double sine(double a, int is_rad) { return sin(is_rad ? a : a * M_PI / 180.0); }
double cosine(double a, int is_rad) { return cos(is_rad ? a : a * M_PI / 180.0); }
double tangent(double a, int is_rad) { return tan(is_rad ? a : a * M_PI / 180.0); }
double arcsin(double a, int is_rad) { double val = asin(a); return is_rad ? val : val * 180.0 / M_PI; }
double arccos(double a, int is_rad) { double val = acos(a); return is_rad ? val : val * 180.0 / M_PI; }
double arctan(double a, int is_rad) { double val = atan(a); return is_rad ? val : val * 180.0 / M_PI; }

// --- Hyperbolic Functions ---
double sinh_(double a) { return sinh(a); }
double cosh_(double a) { return cosh(a); }
double tanh_(double a) { return tanh(a); }
double asinh_(double a) { return asinh(a); }
double acosh_(double a) { return acosh(a); }
double atanh_(double a) { return atanh(a); }

// --- Logarithmic & Exponential Functions ---
double natural_log(double a) { return (a <= 0) ? NAN : log(a); }
double base10_log(double a) { return (a <= 0) ? NAN : log10(a); }
double exp_func(double a) { return exp(a); }

// --- Factorial ---
double factorial(double n) {
    if (n < 0 || floor(n) != n || n > 170) return NAN;
    if (n == 0) return 1;
    double result = 1;
    for (int i = 1; i <= (int)n; ++i) result *= i;
    return result;
}