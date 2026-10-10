#include<stdio.h>


int main(){
    float a;
    printf("enter the amount: ");
    scanf("%f",&a);

    if(a>=0 && a<=5000){
        printf("amount after discount = %.2f\n",a);
    }else if(a>=5001  &&  a<=7000){
        
        printf("amount after discount = %.2f\n",(a = a - a*5/100));
    }  
    else if(a>=7001  &&  a<=9000){
        printf("amount after discount = %.2f\n",(a - a*10/100));
    } 
    else {
        printf("amount after discount = %.2f\n",(a-a*20/100));
    }

    return 0;
}