
void vuln(void)

{
  int iVar1;
  char local_28 [24];
  int local_10;
  char local_9;
  
  printf(" Would you like edit a category (Y/*) >>> ");
  __isoc99_scanf(&DAT_00402053,&local_9);
  iVar1 = strcmp(&local_9,"Y");
  if (iVar1 == 0) {
    printf(" Which category num >>> ");
    __isoc99_scanf(&DAT_00402072,&local_10);
    printf(" Enter the new value >>> ");
    __isoc99_scanf(&DAT_0040208f,local_28);
    iVar1 = strcmp(local_28,"recon");
    if (iVar1 == 0) {
      puts("<<< Sorry, category not accepted.");
      system("echo Goodbye");
      sleep(1);
                    /* WARNING: Subroutine does not return */
      exit(-1);
    }
    strcpy(&categories + (long)local_10 * 0xf,local_28);
    puts("<<< Categories updated.");
    print_cats();
  }
  return;
}