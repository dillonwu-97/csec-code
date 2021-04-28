
void fill(void)

{
  undefined8 local_28;
  undefined8 local_20;
  undefined8 local_18;
  undefined8 local_10;
  
  local_28 = 0;
  local_20 = 0;
  local_18 = 0;
  local_10 = 0;
  color("\nYou can add these ingredients to your dish:","green",&DAT_00401144);
  puts(&DAT_004011a5);
  color("You can also order something else.\n> ","green",&DAT_00401144);
  read(0,&local_28,0x400);
  printf("\nEnjoy your %s",&local_28);
  return;
}

