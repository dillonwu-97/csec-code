
void mission(undefined8 param_1,void *param_2,undefined8 param_3,char *param_4,int param_5,
            int param_6)

{
  ulonglong *puVar1;
  ulonglong uVar2;
  int extraout_EDX;
  int extraout_EDX_00;
  void *pvVar3;
  long in_FS_OFFSET;
  char first_buffer [10];
  char second_buffer [10];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  printf("Insert type of mine: ");
  r(first_buffer,param_2,extraout_EDX,param_4,param_5,param_6);
  pvVar3 = (void *)0x0;
  puVar1 = (ulonglong *)strtoull(first_buffer,(char **)0x0,0); // convert string to unsigned int
  printf("Insert location to plant: ");
  r(second_buffer,pvVar3,extraout_EDX_00,param_4,param_5,param_6);
  puts("We need to get out of here as soon as possible. Run!");
  uVar2 = strtoull(second_buffer,(char **)0x0,0);
  *puVar1 = uVar2; // taking two inputs, a/puVar1 and b/uVar2; a should be an address, b should be a value
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}


void r(void *param_1,void *param_2,int param_3,char *param_4,int param_5,int param_6)

{
  long lVar1;
  long in_FS_OFFSET;
  
  lVar1 = *(long *)(in_FS_OFFSET + 0x28);
  read(0,param_1,9);
  if (lVar1 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}



// need to call this?
void _(void)

{
  long lVar1;
  size_t __n;
  long in_FS_OFFSET;
  
  lVar1 = *(long *)(in_FS_OFFSET + 0x28);
  __n = strlen(&DAT_00400ccc);
  write(1,&DAT_00400ccc,__n);
  system("cat flag*");
  if (lVar1 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}