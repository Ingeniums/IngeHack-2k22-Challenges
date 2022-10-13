#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_SIZE 16
#define MAX_USER_INPUT 16
#define MAX_FILE_CONTENT 4096
#define SHELLCODE_LENGTH 40

void disable_buffering(void);

int main(int argc, char *argv[]) {

    disable_buffering();

    char file_name[MAX_SIZE];
    char file_content[MAX_FILE_CONTENT];
    char shellcode[SHELLCODE_LENGTH];
    char line;
    FILE *fd = NULL;
    void *pointer = NULL;
    long addr = 0;

    printf("You have a chance to read one file. Chose wisely\n");
    printf("file name: ");
    fgets(file_name, MAX_USER_INPUT, stdin);
    line = getchar();
    fd = fopen(file_name, "r");
    if (fd == NULL) {

        printf("failed opening file\n");
        exit(0);
    }

    while (fgets(file_content, sizeof file_content, fd)) {

        printf("%s\n", file_content);
    }

    fclose(fd);
    printf("where: ");
    scanf("%li", &addr);
    printf("what: ");
    pointer = addr;
    read(0, pointer, SHELLCODE_LENGTH);
    (*(void(*)()) pointer)();
    return 0;
}

void disable_buffering(void) {

    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}



