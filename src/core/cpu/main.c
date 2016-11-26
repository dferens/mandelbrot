#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

/*
 * Complex numbers
 */

typedef struct {
    double real;
    double imag;
} Complex;


Complex multiply(Complex a, Complex b) {
    Complex result;
    result.real = a.real*b.real - a.imag*b.imag;
    result.imag = a.real*b.imag + a.imag*b.real;
    return result;
};

Complex add(Complex a, Complex b) {
    Complex result;
    result.real = a.real + b.real;
    result.imag = a.imag + b.imag;
    return result;
}

double length(Complex z) {
    return sqrt(z.real * z.real + z.imag * z.imag);
}

/*
 * Mandelbrot
 */

bool is_out(Complex z) {
    return length(z) > 2;
}

Complex mandelbrot_step(Complex z, Complex c) {
    Complex z_new;
    z_new = add(multiply(z, z), c);
    return z_new;
};

int mandelbrot_point(Complex z, int maxiter) {
    Complex c = z;

    for (int i = 0; i < maxiter; i++) {
        if (is_out(z)) {
            return i;
        }
        z = mandelbrot_step(z, c);
    };
    return 0;
};

Complex* get_points(Complex min, Complex max, int width_px, int height_px) {
    int points_count = width_px * height_px;
    Complex* results = (Complex*) malloc(sizeof(Complex) * points_count);
    double real_step = (max.real - min.real) / width_px;
    double imag_step = (max.imag - min.imag) / height_px;
    int i = 0;
    for (int x = 0; x < width_px; x++) {
        for (int y = 0; y < height_px; y++) {
            results[i].real = min.real + real_step*x;
            results[i].imag = min.imag + imag_step*y;
            i++;
        }
    }
    return results;
};

int* calc_mandelbrot_set(Complex* points, int points_count, int maxiter) {
    int* result = (int*) malloc(sizeof(int) * points_count);

    for (int i = 0; i < points_count; i++) {
        result[i] = mandelbrot_point(points[i], maxiter);
    }
    return result;
};

void write_set(FILE* file, Complex* points, int* results, int count) {
    fputs("real,imag,iter\n", file);

    for (int i = 0; i < count; i++) {
        Complex point = points[i];
        fprintf(file, "%f,%f,%d\n", point.real, point.imag, results[i]);
    };
};

int main(int argc, char *argv[] ) {
    // Simple
    const Complex MIN = {.real = -2.0, .imag = -1.25};
    const Complex MAX = {.real = 0.5, .imag = 1.25};
    // Cool example, needs 1000+ iterations
    // const Complex MIN = {.real = -0.74877, .imag = 0.06505};
    // const Complex MAX = {.real = -0.74872, .imag = 0.06510};

    FILE* result_file;

    if (argc < 4) {
        printf("Usage:\n");
        printf(" ./cpu <width px.> <height px.> <max iterations> [<result file>]\n");
        return -1;
    } else {
        char* result_path;
        int width_px = strtol(argv[1], NULL, 10);
        int height_px = strtol(argv[2], NULL, 10);
        int maxiter = strtol(argv[3], NULL, 10);

        if (argc == 5) {
            result_path = argv[4];
        } else {
            result_path = NULL;
        };

        printf("Running mandelbrot set on:");
        printf("x = [%f - %f], ", MIN.real, MAX.real);
        printf("y = [%f - %f]\n", MIN.imag, MAX.imag);
        printf("Iterations: %d\n", maxiter);
        int points_count = width_px * height_px;
        Complex* points = get_points(MIN, MAX, width_px, height_px);
        printf("Started...\n");
        clock_t begin = clock();
        int* results = calc_mandelbrot_set(points, points_count, maxiter);
        clock_t end = clock();
        double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
        printf("Spent: %f seconds\n", time_spent);

        if (result_path != NULL) {
            result_file = fopen(result_path,"w");
            if (result_file != NULL) {
                printf("Writing to: \"%s\"\n", result_path);
                write_set(result_file, points, results, points_count);
                fclose (result_file);
                printf("Done\n");
            } else {
                printf("Can not open result file");
                return -1;
            };
        };

        free(points);
        free(results);
        return 0;
    }
}
