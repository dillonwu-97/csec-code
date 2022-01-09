undefined8 main(void)

{
  char *__s;
  long in_FS_OFFSET;
  int local_44;
  undefined8 local_38;
  undefined8 local_30;
  undefined8 local_28;
  undefined2 local_20;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  printf("Give me the key and I\'ll give you the flag: ");
  __s = (char *)malloc(4);
  fgets(__s,4,stdin);

  // stack bottom

  // local_38
  // local_30
  // local_28
  // local_20
  // local_44?

  // stack top


  local_38 = 0x6f0547480c35643f;
  local_30 = 0x28130304026f0446;
  local_28 = 0x5000f4358280e52;
  local_20 = 0x4d56;
  local_44 = 0;
  // 0x1a = 16 + 10 = 26
  while (local_44 < 0x1a) {
    *(byte *)((long)&local_38 + (long)local_44) =
         *(byte *)((long)&local_38 + (long)local_44) ^ __s[(long)(local_44 % 3)];
    local_44 = local_44 + 1;
  }


  // https://stackoverflow.com/questions/23776824/what-is-the-meaning-of-s-in-a-printf-format-string/23777065
  // print up to 26 decimal precision?
  printf("%.26s\n",&local_38);
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}

