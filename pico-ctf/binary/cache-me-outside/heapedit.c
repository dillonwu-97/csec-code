undefined8 main(void)

{
  long in_FS_OFFSET;
  undefined local_a9;
  int local_a8;
  int local_a4;
  undefined8 *local_a0;
  undefined8 *local_98;
  FILE *local_90;
  undefined8 *local_88;
  void *local_80;
  undefined8 local_78;
  undefined8 local_70;
  undefined8 local_68;
  undefined local_60;
  char local_58 [72];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  setbuf(stdout,(char *)0x0);]

  // Need to somehow read from local_90
  local_90 = fopen("flag.txt","r");
  fgets(local_58,0x40,local_90);
  local_78 = 0x2073692073696874; // attaches itself to local_88 later on
  local_70 = 0x6d6f646e61722061; // what is this used for??
  local_68 = 0x2e676e6972747320; // what is this used for??
  local_60 = 0;
  local_a0 = (undefined8 *)0x0;
  local_a4 = 0;

  // runs for 7 times and mallocs 144 bytes each time
  while (local_a4 < 7) {
    local_98 = (undefined8 *)malloc(0x80);

    // at the first iteration, this is true
    // I think this only runs for one iteration
    //undefined_8 must be an int
    if (local_a0 == (undefined8 *)0x0) {
      local_a0 = local_98;
    }
    *local_98 = 0x73746172676e6f43; // Value at the start of the heap? I'm pretty sure this is a value assignment
    local_98[1] = 0x662072756f592021; // local_98[1] = 8 byte integer
    local_98[2] = 0x203a73692067616c; // local_98[2] = 8 byte integer
    *(undefined *)(local_98 + 3) = 0; // null byte termination?
    strcat((char *)local_98,local_58); // local_98 += local_58
    local_a4 = local_a4 + 1; // increment 1
  }

  // creating a value called local_88 and setting some values to it similar to above but only doing it once
  // where will this be allocated?
  local_88 = (undefined8 *)malloc(0x80);
  *local_88 = 0x5420217972726f53;
  local_88[1] = 0x276e6f7720736968;
  local_88[2] = 0x7920706c65682074;
  *(undefined4 *)(local_88 + 3) = 0x203a756f;
  *(undefined *)((long)local_88 + 0x1c) = 0;
  strcat((char *)local_88,(char *)&local_78); // vulnerability is here i think because it appends the local_78

    // Free everything
    // but a0 is not freed, but where is it after malloc?
  free(local_98);
  free(local_88);
  local_a8 = 0;
  local_a9 = 0;
  puts("You may edit one byte in the program.");
  printf("Address: ");
  __isoc99_scanf(&DAT_00400b48,&local_a8);
  printf("Value: ");
  __isoc99_scanf(&DAT_00400b53,&local_a9);
  *(undefined *)((long)local_a8 + (long)local_a0) = local_a9;

  local_80 = (local_a8 + local_a9) need address to be that??
  local_80 = malloc(0x80); // what address is this going to point to? // this will point back to local_98 since it was just freed I think

  // puts the character at local_80 + 0x10; need this to contain the flag but how?
  // local_80 is a reused address? But which one?
  puts((char *)((long)local_80 + 0x10));
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
