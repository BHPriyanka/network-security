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
    strncpy(buf, argv[1], 512);
    for (i=0; i<strlen(buf); i++)
      buf[i] = toupper(buf[i]);
    printf("%s\n", buf);
  }

  return 0;
}
