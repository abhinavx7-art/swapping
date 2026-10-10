#include<stdio.h>
#include<math.h>


int main(){
    int principle; 
    float R; //annual rate
    int t; //no. of year

    printf("enter the principle amount: ");
    scanf("%d",&principle);
    printf("enter rate: ");
    scanf("%f",&R);
    printf("enter the time period: ");
    scanf("%d",&t);

    printf("compound interest = %.2f",(principle* pow(1+(R/100),t) - principle));

    return 0;
}