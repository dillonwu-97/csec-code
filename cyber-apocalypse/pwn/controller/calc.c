
uint calc(void)

{
  // 22 bytes? 
  ushort uVar1; 
  float fVar2;
  uint a;
  uint b;
  int c;
  uint d;
  
  printstr("Insert the amount of 2 different types of recources: ");
  __isoc99_scanf("%d %d",&b,&a);
  c = menu();
  if ((0x45 < (int)b) || (0x45 < (int)a)) {
    printstr("We cannot use these many resources at once!\n");
                    /* WARNING: Subroutine does not return */
    exit(0x69); 
  }
  if (c == 2) {
    d = sub(b,a,a);
    printf("%d - %d = %d\n",(ulong)b,(ulong)a,(ulong)d);
    return d;
  }
  if (c < 3) {
    if (c == 1) {
      d = add(b,a,a);
      printf("%d + %d = %d\n",(ulong)b,(ulong)a,(ulong)d);
      return d;
    }
  }
  else {
    if (c == 3) {
      uVar1 = mult(b,a,a);
      d = (uint)uVar1;
      printf("%d * %d = %d\n",(ulong)b,(ulong)a,(ulong)d);
      return d;
    }
    if (c == 4) {
      fVar2 = (float)divi(b,a,a);
      d = (uint)(long)fVar2;
      printf("%d / %d = %d\n",(ulong)b,(ulong)a,(long)fVar2 & 0xffffffff);
      return d;
    }
  }
  printstr("Invalid operation, exiting..\n");
  return d;
}

