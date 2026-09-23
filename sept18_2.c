#include<stdio.h>


int main(){
    int age;
    float height;
    printf("enter your age: ");
    scanf("%d",&age);
    printf("enter your height: ");
    scanf("%f",&height);
    printf(     "user age = %d and user height = %.2f\n",age,height);
    return 0;
}