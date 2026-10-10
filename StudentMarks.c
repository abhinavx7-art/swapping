#include<stdio.h>


int main(){
   char ts ;
   printf("enter ts: ");
   scanf("%c",&ts);

    if(ts=='r'){
        printf("stop");
    } else if (ts == 'g'){
        printf("move forward!!");
    }else if(ts=='y'){
        printf("slow down");
    }else{
        printf("wrong input");
    }
    
    return 0;
}