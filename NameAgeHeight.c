#include<stdio.h>


int main(){
    int age;
    float height;
    char name[50];
    printf("Enter name of the user: ");
    scanf("%s",&name);

    printf("Enter user's age:   ");
    scanf("%d",&age);

    printf("Enter user's height:   ");
    scanf("%f",&height);

    printf("User name = %s\n",name);
    printf("User age = %d\n",age);
    printf("User hieght = %.2f\n", height);


    return 0;
}