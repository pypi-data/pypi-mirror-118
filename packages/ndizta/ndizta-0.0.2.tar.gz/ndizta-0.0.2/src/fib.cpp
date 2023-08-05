#include "fib.h"

unsigned int fibinacci(const unsigned int n){

    if (n < 2){
        return 1;
    }
    return fibinacci(n - 1) + fibinacci(n - 2);
}