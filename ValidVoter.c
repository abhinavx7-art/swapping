#include<stdio.h>


int main(){
    char name[50];
    int age;
    printf("enter name: ");
    scanf("%s",&name);
    printf("enter age: ");
    scanf("%d",&age);

    if (age >= 18){
        printf("hello %s, you are eligible to vote\n",name);
    } else {
        printf("hello %s, you will eligible to vote in %d years\n",name,(18-age));
    }


    return 0;
}