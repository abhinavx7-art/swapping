#include<stdio.h>


int main(){
    int a,b;
    printf("Enter two values: ");
    scanf("%d%d",&a,&b);
    printf("before swapping a=%d,b=%d\n",a,b);

    int c;
    c=a;
    a=b;
    b=c;
    printf("after swapping a=%d,b=%d\n",a,b);
    return 0;
}