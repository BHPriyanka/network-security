#include <sys/types.h>
#include <unistd.h>
#include <string.h>
#include <ctype.h>
#include <stdio.h>

int main(int argc, char *argv[]) 
{
  char buf[512];
  int i;
  
  setuid(0);
  
  if (argc > 1) 
  {
    for (i=0; i<strlen(argv[1]); i++)
      argv[1][i] = tolower(argv[1][i]);
    strcpy(buf, argv[1]);
    printf("%s\n", buf);
  }

  return 0;
}
