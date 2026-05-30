#include <stdio.h>
int main(void){
float nums;
printf("How many fibonacci numbers do you want?\n");
if(0==scanf("%f", &nums)) {
nums = 0;
scanf("%*s");
}
printf("\n");
float a;
a = 0;
float b;
b = 1;
while(nums>0){
printf("%.2f\n",(float)(a));
float c;
c = a+b;
a = b;
b = c;
nums = nums-1;
}
return 0;
}
