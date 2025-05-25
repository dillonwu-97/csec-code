
undefined8 main(void)

{
  byte bVar1;
  byte bVar2;
  size_t sVar3;
  long in_FS_OFFSET;
  uint local_134;
  int local_130;
  undefined8 local_128;
  undefined8 local_120;
  undefined4 local_118;
  char local_108 [32];
  undefined8 local_e8;
  undefined8 local_e0;
  undefined4 local_d8;
  undefined2 local_d4;
  undefined8 local_c8;
  undefined8 local_c0;
  undefined8 local_b8;
  undefined8 local_b0;
  undefined8 local_a8;
  undefined8 local_a0;
  undefined4 local_98;
  undefined2 local_94;
  char acStack137 [105];
  long local_20;
  
  local_20 = *(long *)(in_FS_OFFSET + 0x28);
  fflush(stdout);
  puts("\x1b[36m===================================\x1b[0m");
  puts("\x1b[31mROT IN sHELL\x1b[0m :: \x1b[33mROT13\'s your input!\x1b[0m");
  puts("\x1b[36m===================================\x1b[0m");
  printf("> ");
  fgets(acStack137 + 1,100,stdin);
  sVar3 = strlen(acStack137 + 1);
  acStack137[sVar3] = '\0';
  sVar3 = strlen(acStack137 + 1);
  if (sVar3 < 0x21) {
    printf("\n\x1b[32mROT13 output:\x1b[0m\n> ");
    local_130 = 0;
    while( true ) {
      sVar3 = strlen(acStack137 + 1);
      if (sVar3 <= (ulong)(long)local_130) break;
      putchar((-1 / (((int)~(~(int)acStack137[(long)local_130 + 1] | 0x20U) / 0xd) * 2 + -0xb)) *
              0xd + (int)acStack137[(long)local_130 + 1]);
      local_130 = local_130 + 1;
    }
    putchar(10);
  }
  else {
    local_128 = 0x61746e656d676553;
    local_120 = 0x756166206e6f6974;
    local_118 = 0x2e746c;
    local_c8 = 0x63617473202a2a2a;
    local_c0 = 0x696873616d73206b;
    local_b8 = 0x636574656420676e;
    local_b0 = 0x3a2a2a2a20646574;
    local_a8 = 0x776f6e6b6e753c20;
    local_a0 = 0x696d726574203e6e;
    local_98 = 0x6574616e;
    local_94 = 100;
    local_e8 = 0x20646574726f6241;
    local_e0 = 0x75642065726f6328;
    local_d8 = 0x6465706d;
    local_d4 = 0x29;
    local_108[0] = 'w';
    local_108[1] = 0xf3;
    local_108[2] = 0xdb;
    local_108[3] = 0xff;
    local_108[4] = 0x38;
    local_108[5] = 0xd2;
    local_108[6] = 0xef;
    local_108[7] = 0xf;
    local_108[8] = 0xeb;
    local_108[9] = 199;
    local_108[10] = 0x1b;
    local_108[11] = 0xb3;
    local_108[12] = 0x33;
    local_108[13] = 0xd7;
    local_108[14] = 0xf7;
    local_108[15] = 0xdf;
    local_108[16] = 0x47;
    local_108[17] = 0x5e;
    local_108[18] = 0x30;
    local_108[19] = 0xf5;
    local_134 = 0;
    while (local_134 < 0x14) {
      bVar2 = (byte)local_134;
      bVar1 = -~-(~((~-local_108[local_134] + 0xb5U ^ bVar2) - 0x1b) - bVar2) ^ 0x13;
      local_108[local_134] = ((bVar1 << 6 | bVar1 >> 2) + 0x38 ^ bVar2) - 0x32;
      local_134 = local_134 + 1;
    }
    printf("\n\x1b[31m%s\n",&local_128);
    puts((char *)&local_c8);
    printf("%s\x1b[0m\n",&local_e8);
    printf("\n\x1b[32m%s\x1b[0m\n",local_108);
  }
  if (local_20 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
