#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

// Enable ECB, CTR and CBC mode. Note this can be done before including aes.h or at compile-time.
// E.g. with GCC by using the -D flag: gcc -c aes.c -DCBC=0 -DCTR=1 -DECB=1
#define CBC 1
#define CTR 1
#define ECB 1

#include "aes.h"
#include "aes.c"


static void phex(char* display, uint8_t* str);

void disable_buffering() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void menu(){
    puts("Welcome to our encryption and decryption service.....");
    puts("1. Encrypt");
    puts("2. Decrypt");
    puts("3. Exit");
    printf("> ");
}

int validate_input(char* input, int len){
    int i;
    char c;
    for ( i = 0 ; i < len ; i++ ){
        c = input[i];
        if ( c < 65 || c > 65+25 ) return 0;
    }
    return 1;
}

unsigned int toInt(char c) {
    if (c >= '0' && c <= '9') return      c - '0';
    if (c >= 'A' && c <= 'F') return 10 + c - 'A';
    if (c >= 'a' && c <= 'f') return 10 + c - 'a';
    return -1;
}

int validate_encrypted(char* input, int len){
    int i;
    char c;
    if (len <= 32) return 0;
    if (( len % 32 ) != 0) {
        return 0;
    }
    for ( i = 0 ; i < len ; i++ ){
        c = input[i];
        if ( (c >= 0x30 && c <= 0x39) || (c >= 97 && c <= 97+5) ) {} else return 0;
    }

    size_t numdigits = strlen(input) / 2;

    uint8_t * const output = malloc(numdigits);

    for (size_t i = 0; i != numdigits; ++i) {
      input[i] = 16 * toInt(input[2*i]) + toInt(input[2*i+1]);
    }
    for ( size_t i = numdigits; i < len; ++i) {
        input[i] = 0;
    }
    return 1;
    
}

int main(void)
{
    uint8_t str[] = { 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 };
    uint8_t key[] = { 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 };
    uint8_t iv[] = { 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 };
    int option;
    int i;
    int len;
    struct AES_ctx ctx;

    disable_buffering();
    FILE* fr = fopen("/dev/urandom", "r");
    if (!fr) perror("urandom"), exit(EXIT_FAILURE);
    fread(key, sizeof(char), 16, fr);

    while(1){
        menu();
        scanf("%d\n", &option);

        if (option == 1) {

            fread(iv, sizeof(char), 16, fr);
            AES_init_ctx_iv(&ctx, key, iv);
            fgets(str, 16, stdin);
            len = strlen(str);
            str[len-1] = 0;
            if (!validate_input(str, strlen(str))) { printf("wrong stuff..."); break;}
            AES_CBC_encrypt_buffer(&ctx, str, 16);
            phex("iv", iv);
            phex("result", str);
            printf("\n");
            for (i = 0 ; i < 17 ; i++) str[i] = 0;

        } else if (option == 2) {
            gets(str);
            len = strlen(str);
            if (!validate_encrypted(str, len)) break;
            AES_init_ctx_iv(&ctx, key, str);
            AES_CBC_decrypt_buffer(&ctx, str+16, (len-32)/2);
            printf(str+16);
            printf("\n");
        } else break;
    }
    fclose(fr), fr = NULL;
    return 0;
}


// prints string as hex
static void phex(char *display, uint8_t* str)
{

#if defined(AES256)
    uint8_t len = 32;
#elif defined(AES192)
    uint8_t len = 24;
#elif defined(AES128)
    uint8_t len = 16;
#endif

    unsigned char i;
    printf("%s: ", display);
    for (i = 0; i < len; ++i)
        printf("%.2x", str[i]);
    printf("\n");
}

