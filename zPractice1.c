#include<stdio.h>
int main(){

    char alpha;

    printf("enter an alphabet: ");
    scanf("%c",&alpha);

    switch(alpha){
        case'a':
        printf("vowel\n");
        break;

        case'e':
        printf("vowel\n");
        break;

        case'i':
        printf("vowel\n");
        break;

        case 'o':
        printf("vowel\n");
        break;

        case'u':
        printf("vowel\n");
        break;

        default:
        printf("consonant\n");
        break;
        
    }

    return 0;
}