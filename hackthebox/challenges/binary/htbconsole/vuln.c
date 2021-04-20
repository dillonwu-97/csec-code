
void FUN_00401201(char *param_1)

{
  int iVar1;
  char local_18 [16];
  
  iVar1 = strcmp(param_1,"id\n");
  if (iVar1 == 0) {
    puts("guest(1337) guest(1337) HTB(31337)");
  }
  else {
    iVar1 = strcmp(param_1,"dir\n");
    if (iVar1 == 0) {
      puts("/home/HTB");
    }
    else {
      iVar1 = strcmp(param_1,"flag\n");
      if (iVar1 == 0) {
        printf("Enter flag: ");
        fgets(local_18,0x30,stdin);
        puts("Whoops, wrong flag!");
      }
      else {
        iVar1 = strcmp(param_1,"hof\n");
        if (iVar1 == 0) {
          puts("Register yourself for HTB Hall of Fame!");
          printf("Enter your name: ");
          fgets(&DAT_004040b0,10,stdin);
          puts("See you on HoF soon! :)");
        }
        else {
          iVar1 = strcmp(param_1,"ls\n");
          if (iVar1 == 0) {
            puts("- Boxes");
            puts("- Challenges");
            puts("- Endgames");
            puts("- Fortress");
            puts("- Battlegrounds");
          }
          else {
            iVar1 = strcmp(param_1,"date\n");
            if (iVar1 == 0) {
              system("date");
            }
            else {
              puts("Unrecognized command.");
            }
          }
        }
      }
    }
  }
  return;
}

