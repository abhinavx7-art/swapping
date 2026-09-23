#include<stdio.h>


int main(){
    int a,b;
    printf("enter a value: ");
    scanf("%d",&a);
    printf("enter b value: ");
    scanf("%d",&b);

    int c = a;
    a = b;
    b = c;
    printf("a = %d\n,b = %d\n", a,b);

    printf("b = %d\n",(b/=a));
    return 0;
}