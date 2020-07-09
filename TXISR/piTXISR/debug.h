#include<stdio.h>
#ifdef DEBUG
#define PRINT_DEBUG(n) printf("Value of " #n ": %d\n", n);
#define PRINT_DEBUG_f(n) printf("Value of " #n ": %f\n", n);
#define PRINT_DEBUG_c(n) printf("Value of " #n ": %c\n", n);
#define DEBUG_REST(n) printf(#n" Has been rest\n");
#define DEBUG_P(n) printf(#n"\n");
#define PRINT_DEBUG_CHAR(n) putchar(n);
#define PRINT_TIME(n) printf("%jd milliseconds\n", (intmax_t)n);
#define PRINT_LONG(n) printf(#n" %ld\n", n);
#else
#define PRINT_DEBUG(n)
#define PRINT_DEBUG_f(n) 
#define PRINT_DEBUG_c(n) 
#define DEBUG_REST(n) 
#define DEBUG_P(n)
#define PRINT_DEBUG_CHAR(n) 
#define PRINT_TIME(n)
#define PRINT_LONG(n)
#endif