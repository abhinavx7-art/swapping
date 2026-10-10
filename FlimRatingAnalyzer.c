#include<stdio.h>


int main(){
    float movierating;
    printf("enter movie ration between the scale of 0-5: ");
    scanf("%f",&movierating);

    if(movierating >= 0  &&  movierating <= 2){
        printf("flop\n");
    } 
    else if(movierating >= 2.1   &&  movierating <=3.4){
        printf("semi hit\n");
    }
    else if ( movierating >= 3.5    &&   movierating <= 4.5){
        printf("hit\n");
    }
     else {
        printf("super hit");
    }
    return 0;
}