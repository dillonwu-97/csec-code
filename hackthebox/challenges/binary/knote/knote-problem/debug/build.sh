cd ./exploit-fs/
musl-gcc exploit.c -static -pie -O0 -fPIE -o exploit
find . -print0 | cpio --null --format=newc -o | gzip -9 > ../new-rootfs.cpio.gz
cd ..
./qemu-cmd


