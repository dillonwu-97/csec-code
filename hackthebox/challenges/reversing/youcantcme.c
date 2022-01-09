
ulong FUN_00401160(void)

{
  int iVar1;
  undefined8 local_48;
  undefined8 local_40;
  undefined4 local_38;
  char *local_30;
  undefined8 local_28;
  undefined8 local_20;
  undefined4 local_18;
  undefined local_14;
  int local_10;
  uint local_c;
  
  local_c = 0;
  local_10 = 0;
  printf("Welcome!\n");
  local_28 = 0x5f73695f73696874;
  local_20 = 0x737361705f656874;
  local_18 = 0x64726f77;
  local_14 = 0;
  local_30 = (char *)malloc(0x15);
  local_48 = 0x5517696626265e6d;
  local_40 = 0x555a275a556b266f;
  local_38 = 0x29635559;
  local_10 = 0;
  // 0x14 = 16 + 4 = 20
  while (local_10 < 0x14) {
    // value assignment
    // local_28 = local_48 + local_10
    *(char *)((long)&local_28 + (long)local_10) = *(char *)((long)&local_48 + (long)local_10) + '\n'
    ;
    local_10 = local_10 + 1;
  }
  fgets(local_30,0x15,stdin);
  iVar1 = strcmp((char *)&local_28,local_30);
  if (iVar1 == 0) {
    printf("HTB{%s}\n",local_30);
  }
  else {
    printf("I said, you can\'t c me!\n");
  }
  return (ulong)local_c;
}

// Flag: HTB{wh00ps!_y0u_d1d_c_m3}
// Found it with gdb
