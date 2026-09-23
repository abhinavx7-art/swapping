#include<stdio.h>


int main(){

    
    char name[50];
    printf("Enter your name: ");
    scanf("%s",&name);
    printf("Enter your age: ");
    int age;
    scanf("%d",&age);
    printf("Enter your height: ");
    float height;
    scanf("%f",&height);

    printf("User name %s\n",name);
    printf("User age %d\n",age);
    printf("User height %.2f\n",height);


    return 0;
}