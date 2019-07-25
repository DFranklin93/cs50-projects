#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height = get_int("Height: ");
    if (height >= 1 && height <= 10){
        for (int i=1; i<=height; i++){
            for(int j=height; j>i; j--){
                printf(" ");
            }
            for(int k=0; k<i; k++){
                printf("#");
            }
            for(int l=2; l<i; l++){
                printf(" ");
            }
            printf("\n");
        }
    } else {
        printf("Height only accepts intergers from 1 to 10. Try again\n");
        main();
    }
}
