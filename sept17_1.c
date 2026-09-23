#include<stdio.h>


int main(){
    int num1;
    char ch;
    printf("enter an integer value:  ");
    scanf("%d",&num1);
    getchar();
    printf("enter a character value:  ");
    scanf("%c",&ch);

    printf("value of integer = %d\n",num1);
    printf("value of ch = %c\n",ch);
    return 0;
}