// C program to demonstrate use of fork() and pipe()
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <signal.h>
#include <openssl/sha.h>
#include <openssl/md5.h>

#define MAX 80

void md5(char *string, char outputBuffer[33])
{
    unsigned char hash[16];
    MD5_CTX MD5;
    // fprintf(stderr, "char is: %c --- ", *string);
    MD5_Init(&MD5);
    MD5_Update(&MD5, string, 1);//strlen(string));
    MD5_Final(hash, &MD5);
    int i = 0;
    for(i = 0; i < 16; i++)
    {
        sprintf(outputBuffer + (i * 2), "%02x", hash[i]);
    }
    outputBuffer[32] = 0;
}

int main()
{
    int fd_0_1[2]; // Used to store two ends of first pipe
    int fd_0_2[2]; // Used to store two ends of second pipe
    int fd_1_1[2]; // Used to store two ends of first pipe
    int fd_1_2[2]; // Used to store two ends of second pipe
    int fd_2_1[2]; // Used to store two ends of first pipe
    int fd_2_2[2]; // Used to store two ends of second pipe
    int fd_3_1[2]; // Used to store two ends of first pipe
    int fd_3_2[2]; // Used to store two ends of second pipe
    int fd_4_1[2]; // Used to store two ends of first pipe
    int fd_4_2[2]; // Used to store two ends of second pipe
    int fd_5_1[2]; // Used to store two ends of first pipe
    int fd_5_2[2]; // Used to store two ends of second pipe
    int fd_6_1[2]; // Used to store two ends of first pipe
    int fd_6_2[2]; // Used to store two ends of second pipe
    int fd_7_1[2]; // Used to store two ends of first pipe
    int fd_7_2[2]; // Used to store two ends of second pipe
 
    pid_t p;
    pid_t multiverse[5];
    if (pipe(fd_0_1) == -1) {
        fprintf(stderr, "something's wrong i can feel it"); //pipe error
        return 1;
    }
    if (pipe(fd_0_2) == -1) {
        fprintf(stderr, "something's wrong i can feel it"); //pipe error
        return 1;
    }
    if (pipe(fd_1_1) == -1) {
        fprintf(stderr, "something's wrong i can feel it"); //pipe error
        return 1;
    }
    if (pipe(fd_1_2) == -1) {
        fprintf(stderr, "something's wrong i can feel it"); //pipe error
        return 1;
    }
    if (pipe(fd_2_1) == -1) {
        fprintf(stderr, "something's wrong i can feel it"); //pipe error
        return 1;
    }
    if (pipe(fd_2_2) == -1) {
        fprintf(stderr, "something's wrong i can feel it"); //pipe error
        return 1;
    }
    if (pipe(fd_3_1) == -1) {
        fprintf(stderr, "something's wrong i can feel it"); //pipe error
        return 1;
    }
    if (pipe(fd_3_2) == -1) {
        fprintf(stderr, "something's wrong i can feel it"); //pipe error
        return 1;
    }
    if (pipe(fd_4_1) == -1) {
        fprintf(stderr, "something's wrong i can feel it"); //pipe error
        return 1;
    }
    if (pipe(fd_4_2) == -1) {
        fprintf(stderr, "something's wrong i can feel it"); //pipe error
        return 1;
    }
    if (pipe(fd_5_1) == -1) {
        fprintf(stderr, "something's wrong i can feel it"); //pipe error
        return 1;
    }
    if (pipe(fd_5_2) == -1) {
        fprintf(stderr, "something's wrong i can feel it"); //pipe error
        return 1;
    }
    if (pipe(fd_6_1) == -1) {
        fprintf(stderr, "something's wrong i can feel it"); //pipe error
        return 1;
    }
    if (pipe(fd_6_2) == -1) {
        fprintf(stderr, "something's wrong i can feel it"); //pipe error
        return 1;
    }
    if (pipe(fd_7_1) == -1) {
        fprintf(stderr, "something's wrong i can feel it"); //pipe error
        return 1;
    }
    if (pipe(fd_7_2) == -1) {
        fprintf(stderr, "something's wrong i can feel it"); //pipe error
        return 1;
    }
 
    char input_str[MAX];
    fgets(input_str, MAX, stdin);
    
    // exit(0);
    if ((strlen(input_str) - 1) % 8 != 0) {
        fprintf(stderr, "Something's wrong i can feel it"); // length test error
        return 1;
    }
    for (int i = 0; i < 5; i++) {
        // creating forks
        int k;
        p = fork();
        // fprintf(stderr, "%d \n", getpid());
        // fprintf(stderr, "%d \n", i);
        k = -1;
        if (p < 0) {
            fprintf(stderr, "Something's wrong i can feel it"); // fork error
            return 1;
        } else {
            // fprintf(stderr, "%d: %d\n", getpid(), k);
            multiverse[0] = p;
            if (p == 0) {
                k = 0;
            }
        }


        for (int j=1; j < 8; j++) {
            if (p != 0) {
                p = fork();
            
                if (p < 0) {
                    fprintf(stderr, "Something's wrong i can feel it"); // fork error
                    return 1;
                } else {
                    if (p == 0) {
                        k = j;
                    }
                    multiverse[j] = p;
                }
            }
            // fprintf(stderr, "%d: %d ->>> %d\n", getpid(), j, k);
        }

        char result[65];
        char my_pipe[1];
        int status = 0;
        // fprintf(stderr, "%d: %d", getpid(), k);
        switch (k) {
            case 0:
                //close(fd_0_1[1]);
                //open(fd_0_1[0]);
                
                read(fd_0_1[0], my_pipe, 1);
                md5(&my_pipe[0],result);
                //sleep(0.5);
                fprintf(stderr, "%s\n", result);
                //close(fd_0_1[0]);
                exit(0);
                break;
            case 1:
                //close(fd_1_1[1]);
                read(fd_1_1[0], my_pipe, 1);
                md5(&my_pipe[0],result);
                //sleep(0.5);
                fprintf(stderr, "%s\n", result);
                //close(fd_1_1[0]);
                exit(0);
                break;
            case 2:
                //close(fd_2_1[1]);
                read(fd_2_1[0], my_pipe, 1);
                md5(&my_pipe[0],result);
                //sleep(0.5);
                fprintf(stderr, "%s\n", result);
                //close(fd_2_1[0]);
                exit(0);
                break;
            case 3:
                //close(fd_3_1[1]);
                read(fd_3_1[0], my_pipe, 1);
                md5(&my_pipe[0],result);
                //sleep(0.5);
                fprintf(stderr, "%s\n", result);
                //close(fd_3_1[0]);
                exit(0);
                break;
            case 4:
                //close(fd_4_1[1]);
                read(fd_4_1[0], my_pipe, 1);
                md5(&my_pipe[0],result);
                //sleep(0.5);
                fprintf(stderr, "%s\n", result);
                //close(fd_4_1[0]);
                exit(0);
                break;
            case 5:
                //close(fd_5_1[1]);
                read(fd_5_1[0], my_pipe, 1);
                md5(&my_pipe[0],result);
                //sleep(0.5);
                fprintf(stderr, "%s\n", result);
                //close(fd_5_1[0]);
                exit(0);
                break;
            case 6:
                //close(fd_6_1[1]);
                read(fd_6_1[0], my_pipe, 1);
                md5(&my_pipe[0],result);
                //sleep(0.5);
                fprintf(stderr, "%s\n", result);
                //close(fd_6_1[0]);
                exit(0);
                break;
            case 7:
                //close(fd_7_1[1]);
                read(fd_7_1[0], my_pipe, 1);
                md5(&my_pipe[0],result);
                //sleep(0.5);
                fprintf(stderr, "%s\n", result);
                //close(fd_7_1[0]);
                exit(0);
                break;
            default:
                // fprintf(stderr, "Wave %d is comming\n", i);
                pid_t wpid;
                //close(fd_0_1[0]);
                //open(fd_0_1[1]);
                write(fd_0_1[1], &input_str[i*8+7], 1);
                //close(fd_0_1[1]);
                waitpid(multiverse[0], &status, 0);

                //close(fd_1_1[0]);
                write(fd_1_1[1], &input_str[i*8+5], 1);
                //close(fd_1_1[1]);
                waitpid(multiverse[1], &status, 0);

                //close(fd_2_1[0]);
                write(fd_2_1[1], &input_str[i*8+2], 1);
                //close(fd_2_1[1]);
                waitpid(multiverse[2], &status, 0);

                //close(fd_3_1[0]);
                write(fd_3_1[1], &input_str[i*8+0], 1);
                //close(fd_3_1[1]);
                waitpid(multiverse[3], &status, 0);

                //close(fd_4_1[0]);
                write(fd_4_1[1], &input_str[i*8+1], 1);
                //close(fd_4_1[1]);
                waitpid(multiverse[4], &status, 0);

                //close(fd_5_1[0]);
                write(fd_5_1[1], &input_str[i*8+3], 1);
                //close(fd_5_1[1]);
                waitpid(multiverse[5], &status, 0);

                //close(fd_6_1[0]);
                write(fd_6_1[1], &input_str[i*8+4], 1);
                //close(fd_6_1[1]);
                waitpid(multiverse[6], &status, 0);

                //close(fd_7_1[0]);
                write(fd_7_1[1], &input_str[i*8+6], 1);
                //close(fd_7_1[1]);
                waitpid(multiverse[7], &status, 0);
                while ((wpid = wait(&status)) > 0);
                // int returnStatus;    
                // waitpid(childPid, &returnStatus, 0); 
        
                // //close(fd_0_2[1]);
                // read(fd_0_2[0], concat_str, 100);
                // fprintf(stderr, "Concatenated string %s\n", concat_str);
                // //close(fd_0_2[0]);

                break;
    }
    }
    /* 
    // Parent process
    if (p > 0) {
        char concat_str[100];
 
        //close(fd1[0]); // Close reading end of first pipe
 
        // Write input string and close writing end of first
        // pipe.
        write(fd1[1], &input_str[i*8+0], 1);
        //close(fd1[1]);

        // Wait for child to send a string
        wait(NULL);
 
        //close(fd2[1]); // Close writing end of second pipe
 
        // Read string from child, print it and close
        // reading end.
        read(fd2[0], concat_str, 100);
        fprintf(stderr, "Concatenated string %s\n", concat_str);
        //close(fd2[0]);
    }
 
    // child process
    else {
        //close(fd1[1]); // Close writing end of first pipe
 
        // Read a string using first pipe
        char concat_str[100];
        read(fd1[0], concat_str, 100);
 
        // Concatenate a fixed string with it
        int k = strlen(concat_str);
        int i;
        for (i = 0; i < strlen(fixed_str); i++)
            concat_str[k++] = fixed_str[i];
 
        concat_str[k] = '\0'; // string ends with '\0'
 
        // Close both reading ends
        //close(fd1[0]);
        //close(fd2[0]);
 
        // Write concatenated string and close writing end
        write(fd2[1], concat_str, strlen(concat_str) + 1);
        //close(fd2[1]);
 
    } */
    exit(0);
}