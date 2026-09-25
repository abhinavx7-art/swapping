#include<stdio.h>


int main(){
    float celsius,fahrenheit;
    printf("enter temperature in celsius: ");
    scanf("%f",&celsius);

    printf("temperature in fahrenheit = %.2f",fahrenheit,(fahrenheit = celsius*9/5 +32));
    return 0;
} 