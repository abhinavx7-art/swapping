#include<stdio.h>


int main(){
    int a,b;
    printf("enter the 1st value: ");
    scanf("%d",&a);
    printf("enter the 2nd value: ");
    scanf("%d",&b);

    int c = a;
    a=b;
    b=c;
    printf("a=%d\n,b=%d",a,b);
    return 0;
}