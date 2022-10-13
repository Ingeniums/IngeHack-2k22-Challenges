#include <stdlib.h>
#include <stdio.h>
#include<sys/types.h>
#include<sys/stat.h>
#include <fcntl.h>
#include <string.h>

#define MAX_ENTRIES 2
#define MAX_FREED_ENTRIES 1 

#define STRING_GUESS 1 
#define LONG_GUESS 2 
#define DOUBLE_GUESS 3

typedef union {
    char *str_guess; 
    long long_guess; 
    double double_guess;
} Guess;

unsigned int freed_entries = 0;
unsigned long seed;
unsigned int computer_score = 1337; 
unsigned int user_score = 0;
Guess *union_guesses[MAX_ENTRIES] = {NULL};
char *str_guesses[MAX_ENTRIES];
unsigned int created_entries = 0;

unsigned long get_seed() {
    unsigned long seed = 0; 
    int fd = 0; 

    fd = open("/dev/random", O_RDONLY);
    read(fd, &seed, sizeof(seed));
    close(fd);
    return seed;
}

void menu() {
    puts("1- Add a guess"); 
    puts("2- View your guess"); 
    puts("3- edit a guess");
    puts("4- delete a guess");
    puts("5- Win the game");
    puts("6- exit");
    puts(">> ");
}

int get_option() {
    int option = 0; 
    printf("Option: "); 
    scanf("%d", &option); 
    return option;
}

void init() {
    seed = get_seed();
    srand(seed);
    setbuf(stdin, NULL);
    setbuf(stdout, NULL); 
    setbuf(stderr, NULL);
}

long read_long() {

    char buff[16];
    printf("Guess: ");
    read(0, buff, 14);
    return atol(buff);
}

double read_double() {

    char buff[16]; 
    printf("Guess: "); 
    read(0, buff, 14);
    return atof(buff);
}

void read_str(char *buff) {

    printf("Guess: ");
    int size = read(0, buff, 127);
    char *nl = strchr(buff, '\n');
    if (nl != NULL)
        *nl = '\x00';
    else
        buff[size] = 0;
}

void view_guess() {

    int index = 0;

    printf("Index: ");
    scanf("%d", &index);

    if (index < 0 || index >= MAX_ENTRIES) {
        printf("Invalid index"); 
        exit(0);
    }

    if (union_guesses[index] == 0) {
        printf("Invalid index");
        exit(0);
    }

    printf("View guess as: \n");
    puts("1- string");
    puts("2- long");
    puts("3- double");

    switch(get_option()) {

        case LONG_GUESS:
            printf("Your guess is: %ld\n", union_guesses[index]->long_guess);
            break; 
        case DOUBLE_GUESS:
            printf("Your guess is: %lf\n", union_guesses[index]->double_guess);
            break; 
        case STRING_GUESS:
            printf("Your guess is: %s\n", union_guesses[index]->str_guess);
            break;
        default:
            printf("Invalid option\n");
            break;
    }
}

void add_guess() {
    char buff[128];
    Guess* union_guess;
    printf("Type of guess: \n");
    puts("1- string");
    puts("2- long");
    puts("3- double");

    if (created_entries >= MAX_ENTRIES) {
        printf("Max entries reached");
        exit(0);
    }

    union_guess = (Guess*)malloc(sizeof(Guess));
    if (union_guess == NULL) {
        printf("Error while allocating memory\n");
        exit(1);
    }
    union_guesses[created_entries] = union_guess;

    switch(get_option()) {
        case LONG_GUESS:
            union_guess->long_guess = read_long();
            created_entries++;
            printf("Guess added successfully\n");
            break;
        case DOUBLE_GUESS:
            union_guess->double_guess = read_double();
            created_entries++;
            printf("Guess added successfully\n");
            break;
        case STRING_GUESS:
            read_str(buff);
            union_guess->str_guess = strdup(buff);
            str_guesses[created_entries] = union_guess->str_guess;
            created_entries++;
            printf("Guess added successfully\n");
            break;
        default:
            printf("Invalid option\n");
            break;
    }
}

void delete_guess() {
    int index = 0;
    if (freed_entries >= MAX_FREED_ENTRIES) {
        printf("Max freed entries reached");
        exit(0);
    }

    printf("Index: ");
    scanf("%d", &index);

    if (index < 0 || index >= MAX_ENTRIES) {
        printf("Invalid index\n");
        exit(0);        
    }
    free(union_guesses[index]);
    freed_entries++;
    created_entries--;
    printf("Done\n");
}

void edit_guess() {
    int index = 0;
    char buff[128];

    printf("Index: ");
    scanf("%d", &index);

    if (index < 0 || index >= MAX_ENTRIES) {

        printf("Invalid index\n");
        exit(0);
    }

    printf("Edit as: \n");
    puts("1- string");
    puts("2- long");
    puts("3- double");

    switch(get_option()) {

        case LONG_GUESS:
            union_guesses[index]->long_guess = read_long();
            printf("Done\n");
            break; 
        case DOUBLE_GUESS:
            union_guesses[index]->double_guess = read_double();
            printf("Done\n");
            break; 
        case STRING_GUESS:
            read_str(buff);
            union_guesses[index]->str_guess = strdup(buff);
            printf("Done\n");
            break; 
        default:
            printf("Invalid option\n");
            break;
    }
}

void print_flag() {
    char buff[64];
    FILE *flag_fd = NULL;

    memset(buff, 0, 64);
    flag_fd = fopen("flag.txt", "r");
    if (flag_fd == NULL) {
        printf("Error: opening flag file failed");
        exit(1);
    }

    fgets(buff, 64, flag_fd);
    fclose(flag_fd);
    write(1, buff, strlen(buff));    
}

void win_game() {
    unsigned int random_num = rand(); 
    unsigned int user_guess = 0; 
    printf("Enter your guess here: \n");
    scanf("%u", &user_guess);

    if (random_num == user_guess) {

        if (user_score == computer_score) {
            printf("Congrats here is your flag\n");
            print_flag();
            exit(0);
        }
        else {
            printf("Nope computer is still better then you \n");
            exit(0);
        }
    }
    else {
        printf("Incorrect guess\n");
        exit(0);
    }

}

int main(int argc, char *argv[]) {

    init();
    
    while (1) {
        menu();
        switch(get_option()) {

            case 1:
                add_guess(); 
                break; 
            case 2:
                view_guess();
                break;
            case 3:
                edit_guess();
                break;
            case 4:
                delete_guess();
                break;
            case 5:
                win_game();
                break;
            case 6:
                exit(0);
            default:
                printf("Invalid option\n");
                break;
        }
    }
    add_guess();
    return 0;
}

