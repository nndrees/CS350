#include <stdio.h>
#include <stdlib.h>

int main(int argc, char* argv[])
{
  if (argc < 2)
  {
    fprintf(stderr, "Usage: %s randomseed [maxnumber]\n", argv[0]);
    exit(1);
  }
  srand(atoi(argv[1]));

  int guessed = 0;
  printf("Guess the number: ");
  scanf("%d", &guessed);
  printf("Wrong!\n");
  return 0;
}
