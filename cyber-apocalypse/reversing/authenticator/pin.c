
undefined8 checkpin(char *param_1)

{
  size_t sVar1;
  int local_24;
  
  local_24 = 0;
  while( true ) {
    sVar1 = strlen(param_1);
    if (sVar1 - 1 <= (ulong)(long)local_24) {
      return 0;
    }
    if ((byte)("}a:Vh|}a:g}8j=}89gV<p<}:dV8<Vg9}V<9V<:j|{:"[local_24] ^ 9U) != param_1[local_24])
    break;
    local_24 = local_24 + 1;
  }
  return 1;
}
