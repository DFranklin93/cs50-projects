#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

int stringEncyrpt(string plainText, int key);

int main(int argc, string argv[])
{
    //Checks to see how many arguments have been provided
    if(argc == 1){
       printf("Caesar has to have at least one argument\n");
        return 2;
    // only one other arugement besides file can progress the program
    }else if(argc == 2){
        printf("Correct amount of arguments have been provided\n");
        // wait 1 second before printing more
        sleep(1);
        // starts a for loop that breaks apart the input and
        // checks to makes sure input is only digits
        for(int i=0, n=strlen(argv[1]); i < n; i++){
          // isdigit returns a zero value if arg has letters
          int c = isdigit(argv[1][i]);
          // check if arg gives zero
          if(c == 0){
              printf("There are letters in this input\n");
              return 1;
          }  
        }
        //after making sure input has no letters, place it into a var of key
        int key = atoi(argv[1]);
        //prompts user to input a message
        string plainText = get_string("plaintext: ");
        stringEncyrpt(plainText, key);
    }else{
        printf("Caesar can't have more than one argument\n");
        return 2;
    }
}

//Creats function that takes plainText and key to convert plainText
int stringEncyrpt(string plainText, int key){
    //loops through each char of plainText
    for(int i=0, n = strlen(plainText); i<n; i++){
        if(isupper(plainText[i])){
            plainText[i] = (plainText[i] - 'A' + key) % 26 + 'A';
        }else if(islower(plainText[i])){
            plainText[i] = (plainText[i] - 'a' + key) % 26 + 'a';
        }else{
            plainText[i] = plainText[i];
        }
    }
    sleep(1);
    printf("ciphertext: %s \n", plainText);
    return 0;
}
