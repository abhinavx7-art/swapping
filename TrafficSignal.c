#include<stdio.h>


int main(){
    char ts;
    printf("enter ts: ");
    scanf("%c",&ts);
    if (ts=='r'){
        printf("stopppp!!");
    }else if (ts=='y'){
        printf("sloww downnnn!!");
    } else if (ts=='g'){
        printf("move forward!!");
    }else{
        printf("input is wrong");
    }
    return 0;
}