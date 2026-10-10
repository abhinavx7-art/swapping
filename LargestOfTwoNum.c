#include<stdio.h>


int main(){
    int a,b;
    printf("enter first number: ");
    scanf("%d",&a);
    printf("enter second value: ");
    scanf("%d",&b); 

    if ( a > b ) {
        printf("%d is the largest\n",a);
    } else if ( b > a) {
        printf("%d is the largest\n",b);
    } else { 

        printf("both numbers are equal\n");
    }
        return 0;
}