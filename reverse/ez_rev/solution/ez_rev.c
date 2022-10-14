#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define MAX 100
#include <string.h>
int main()
{
    char a[MAX];
    fprintf(stdout, "Let me check your secret: ");
    fgets(a, MAX, stdin);
    fprintf(stdout, "\n");
    int fl4g[] = {18, 58, 50, 57, 17, 11, 22, 29, 28, 25, 45, 48, 60, 12, 49, 33, 30, 61, 36, 39, 56, 44, 53, 16, 55, 51, 59, 27, 41, 62, 23, 42, 47, 43, 21, 14, 24, 67};
    int x0r[] = {91, 84, 85, 92, 89, 106, 117, 118, 103, 122, 29, 94, 5, 126, 5, 85, 43, 98, 76, 19, 91, 71, 6, 98, 90, 7, 85, 68, 94, 13, 123, 70, 112, 79, 37, 96, 43, 62};
    int cpt = 0;
    for (int x = 0; x < 38; x++) {
        char ch = fl4g[x] ^ x0r[x];

        if (ch != a[x]) {
            fprintf(stdout, "Nah\n");
            return 1337;
        }
    } 
    fprintf(stdout, "congrats, now go submit it\n");
    return 0;
}
