#include<stdio.h>


int main(){
    int a,b;
    printf("enter 1st number:");
    scanf("%d",&a);

    printf("enter 2nd value:");
    scanf("%d",&b);

    printf("sum of %d and %d = %d\n",a,b,(a+b));
    printf("substraction of %d and %d = %d\n",a,b,(a-b));
    printf("multiplication of %d and %d = %d\n",a,b,(a*b));
    return 0;
}