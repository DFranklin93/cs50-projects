#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void){
    float inputTotal;
    int dollarAmount, dollarCount, quarterAmount, quarterCount, dimeAmount, dimeCount, nickelAmount, nickelCount, pennyAmount, pennyCount, outputTotal;
    // set amounts to ints instead of floats since floats are a little harder to work with
    dollarAmount = 100;
    quarterAmount = 25;
    dimeAmount = 10;
    nickelAmount = 5;
    pennyAmount = 1;
    inputTotal = get_float("Total: $");
    // converts inputTotal from a float to an int
    outputTotal = inputTotal*100;
    // just to see if changed from float to int
    printf("%i\n", outputTotal);
    //as long as outputTotal is not zero run
    while(outputTotal > 0){
        dollarCount = outputTotal/dollarAmount;
        outputTotal = outputTotal - (dollarCount*100);
        quarterCount = outputTotal/quarterAmount;
        outputTotal = outputTotal - (quarterCount*25);
        dimeCount = outputTotal/dimeAmount;
        nickelCount = outputTotal/nickelAmount;
        outputTotal = outputTotal - (nickelCount*5);
        pennyCount = outputTotal/pennyAmount;
        outputTotal = outputTotal - (pennyCount);
    }
    printf("dollars: %i\nquarters: %i\ndimes: %i\nnickels: %i\npennies: %i\n", dollarCount, quarterCount, dimeCount, nickelCount, pennyCount);
}
