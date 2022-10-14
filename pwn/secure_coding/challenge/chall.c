#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define MAX_CHUNKS 3
#define CHUNK_SIZE 280
#define MAX_FREED 1
#define MAX_CODES 5

char *entries[MAX_CHUNKS];
int created_entries = 0;
int freed_entries = 0;

void disable_buffering() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

void menu() {
    puts("1- Add code");
    puts("2- View code");
    puts("3- Remove Code");
    puts("4- Organize Your codes");
    printf(">> ");
}

int get_option() {
    int option = 0; 
    char line;
    printf("Option: ");
    scanf("%d", &option);
    line = getchar();
    return option;
}

void add_code() {
    if (created_entries < MAX_CHUNKS) {
        void *heapChunk = NULL;
        heapChunk = malloc(sizeof(int) * CHUNK_SIZE);
        printf("Code: ");
        read(0, heapChunk, CHUNK_SIZE - 1);
        entries[created_entries] = heapChunk;
        created_entries++;
        printf("Code added\n");
    }
    else {
        printf("Max chunks reached \n");
        exit(0);
    }
}

void view_code() {
    int index = 0; 
    printf("Index: ");
    scanf("%d", &index);
    if (entries[index] != 0) {
        printf("%s", entries[index]);
    }
}

void remove_code() {
    if (freed_entries < MAX_FREED) {
        int index = 0; 
        printf("Index: ");
        scanf("%d", &index);
        if (index < 0 || index > MAX_CHUNKS) {
            printf("Invalid index\n");
            exit(0);
        }
        if (entries[index] == 0) {
            printf("Nope \n");
            exit(0);
        }
        free(entries[index]);
        entries[index] = 0;
        freed_entries++;
        printf("Code removed\n");
    }
    else {
        printf("Max freed entries reached\n");
        exit(0);
    }
}

void organize_code() {
    int *code = NULL, index = 0, size = 0;
    printf("How many codes do you have?: ");
    scanf("%d", &size);
    if (size > MAX_CODES) 
        exit(0);
    code = calloc(size, sizeof(int));
    printf("Index of code to change: ");
    scanf("%d", &index);
    printf("codes[%d]: ", index);
    scanf("%d", &code[index]);
    printf("Done \n");
}

int main(int argc, char *argv[]) {
    disable_buffering();

    while (1) {
        menu();
        switch(get_option()) {
            case 1:
                add_code();
                break; 
            case 2:
                view_code();
                break;
            case 3:
                remove_code();
                break;
            case 4:
                organize_code();
                break;
            default:
                printf("Invalid option\n");
                break;
        }
    }
    return 0;
}