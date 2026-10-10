#include<stdio.h>


int main(){
    float celsius,fahrenheit;
    printf("enter the temperature in celsius: ");
    scanf("%f",&celsius);

    printf("temperature in fahrenheit = %.2f", (fahrenheit = celsius*9/5 + 32));
    return 0;
}