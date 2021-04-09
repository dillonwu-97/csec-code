
int main() {
  typedef unsigned char byte;
  byte y;
  long in_FS_OFFSET;
  unsigned int i;
  byte a [24];
  long local_10;
  byte x;
  

    a[0] = 0x15;
    a[1] = 0x70;
    a[2] = 0xe5;
    a[3] = 100;
    a[4] = 0x7a;
    a[5] = 0xd4;
    a[6] = 0x6d;
    a[7] = 0x75;
    a[8] = 0xeb;
    a[9] = 0xf4;
    a[10] = 0x6a;
    a[11] = 0xd1;
    a[12] = 0xfa;
    a[13] = 0xd1;
    a[14] = 0xf9;
    a[15] = 0xe8;
    a[16] = 0x9d;
    a[17] = 0x7c;
    a[18] = 0x41;
    i = 0;
    while (i < 0x13) {
      y = (byte)i;
      x = ~-((~a[i] + y ^ 0x48) - y);
      y = ((x << 3 | x >> 5) - y ^ 0x5d) - 0x23 ^ y;
      x = (y * '\x02' | y >> 7) + 0xbf;
      a[i] = (x * ' ' | x >> 3) ^ 0x65;
      i = i + 1;
    }
    printf("%s", a);
}

