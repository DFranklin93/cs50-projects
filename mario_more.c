#include <cs50.h>
#include <stdio.h>

void diamondTop();
void diamondBottom();

int main(void)
{
    int height = get_int("Height: ");
    if (height >= 1 && height <= 10){
        diamondTop(height);
        diamondBottom(height);
//         //prints top half of diamond
//         for (int i=1; i<=height; i++){
//             for(int j=height; j>i; j--){
//                 printf(" ");
//             }
//             for(int k=0; k<i; k++){
//                 printf("#");
//             }
//             printf("  ");
//             for(int j=1; j<=i; j++){
//                 printf("#");
//             }
//             printf("\n");
//         }
//         //prints bottom half of diamond
//         for (int i=height; i>=1; i--){
//             for (int j=i; j<=height-1; j++){
//                 printf(" ");
//             }
//             for (int k=i; k>=1; k--){
//                 printf("#");
//             }
//             printf("  ");
//             for (int l=0; l<i; l++){
//                 printf("#");
//             }
//             printf("\n");
//         }
    } else {
        printf("Height only accepts intergers from 1 to 10. Try again\n");
        main();
    }
}

void diamondTop(height){
   //prints top half of diamond
        for (int i=1; i<=height; i++){
            for(int j=height; j>i; j--){
                printf(" ");
            }
            for(int k=0; k<i; k++){
                printf("#");
            }
            printf("  ");
            for(int j=1; j<=i; j++){
                printf("#");
            }
            printf("\n");
        } 
}

void diamondBottom(height){
            //prints bottom half of diamond
        for (int i=height; i>=1; i--){
            for (int j=i; j<=height-1; j++){
                printf(" ");
            }
            for (int k=i; k>=1; k--){
                printf("#");
            }
            printf("  ");
            for (int l=0; l<i; l++){
                printf("#");
            }
            printf("\n");
        }
}
