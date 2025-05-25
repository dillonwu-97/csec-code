
// молоток123


undefined8 main(void)

{
  byte bVar1; // 1
  byte bVar2; // 1
  int iVar3; // 4
  long in_FS_OFFSET; // 8
  uint local_74; // 4
  byte local_67 [15]; // 15
  char local_58 [72]; // 72
  long local_10; // 8
  // total = 113 bytes

  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  puts(&DAT_001009e0);
  printf("> ");
  fgets(local_58,0x3c,stdin);
  iVar3 = strcmp(&DAT_001009c8,local_58);
  if (iVar3 == 0) {
    local_67[0] = 0xe4;
    local_67[1] = 100;
    local_67[2] = 0xa6;
    local_67[3] = 0x90;
    local_67[4] = 0x7c;
    local_67[5] = 0xa6;
    local_67[6] = 0x75;
    local_67[7] = 0xb8;
    local_67[8] = 0xa4;
    local_67[9] = 0xd;
    local_67[10] = 0xc;
    local_67[11] = 0x7f;
    local_67[12] = 0x7e;
    local_67[13] = 0xf3;
    local_67[14] = 1;
    local_74 = 0;
    while (local_74 < 0xf3) {
      bVar2 = (byte)local_74;
      bVar1 = ~(~(~-((local_67[local_74] ^ 0xa5) - bVar2 ^ bVar2) ^ 0x8d) - 0xb);
      local_67[local_74] = (((bVar1 << 5 | bVar1 >> 3) + 0x37 ^ 0xe5) - 7 ^ bVar2) - 0x39;
      local_74 = local_74 + 1;
    }
    printf(&DAT_00100a08,local_67);
  }
  else {
    puts(&DAT_00100a37);
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}

