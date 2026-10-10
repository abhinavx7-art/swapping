#include<stdio.h>


int main(){
    char ch;
    printf("enter an alphabet: ");
    scanf("%c",&ch);

    if (ch=='a' || ch == 'e' || ch == 'i' || ch== 'o' || ch=='u'){    // { || means OR }
        printf("vowel");
    } else {
        printf("consonant");
    }
    return 0;
}