// calc.c

double add(double a, double b) { return a + b; }
double sub(double a, double b) { return a - b; }
double mul(double a, double b) { return a * b; }

double divide(double a, double b) {
    return (b == 0) ? 0 : a / b;
}
