#include<stdio.h>


int main(){
    int a,b;
    printf("enter the value of a = ");
    scanf("%d",&a);
    printf("enter the value of b = ");
    scanf("%d",&b);

    int c = a;
    a=b;
    b=c;
    printf("a=%d\nb=%d\n",a,b);
    return 0;
}