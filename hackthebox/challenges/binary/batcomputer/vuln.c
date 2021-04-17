undefined8 FUN_001011ec(void)

{
  int iVar1;
  int chase_or_track;
  char password_check [16];
  undefined leaked_address [76];
  
  FUN_001011a9();
  while( true ) {
    while( true ) {
      memset(password_check,0,0x10);
      printf(
            "Welcome to your BatComputer, Batman. What would you like to do?\n1. Track Joker\n2.Chase Joker\n> "
            );
      __isoc99_scanf(&DAT_00102069,&chase_or_track);
      if (chase_or_track != 1) break;
      printf("It was very hard, but Alfred managed to locate him: %p\n",leaked_address);
    }
    if (chase_or_track != 2) break;
    printf("Ok. Let\'s do this. Enter the password: ");
    __isoc99_scanf(&DAT_001020d0,password_check);
    iVar1 = strcmp(password_check,"b4tp@$$w0rd!");
    if (iVar1 != 0) {
      puts("The password is wrong.\nI can\'t give you access to the BatMobile!");
                    /* WARNING: Subroutine does not return */
      exit(0);
    }
    printf("Access Granted. \nEnter the navigation commands: ");
    read(0,leaked_address,0x89);
    puts("Roger that!");
  }
  puts("Too bad, now who\'s gonna save Gotham? Alfred?");
  return 0;
}