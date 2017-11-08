#include<stdlib.h>
#include<stdio.h>
int main(int args, char **argc) {
  int x = atoi(argc[1]);
  int y = atoi(argc[2]);
  int z = atoi(argc[3]);
  printf("%d %d\n", x, y);
  for(int w = 0; w < y; w++) {
    for(int v = 0; v < x; v++) {
      printf("1");
    }
    printf("\n");
  }
}
