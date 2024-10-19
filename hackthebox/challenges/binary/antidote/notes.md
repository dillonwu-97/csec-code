In order to run the binary, we must do this:
https://stackoverflow.com/questions/16158994/how-to-solve-error-while-loading-shared-libraries-when-trying-to-run-an-arm-bi

# Setup:
To run:
qemu-arm -L /usr/arm-linux-gnueabihf/ ./antidote_patched

To debug:
qemu-arm -L /usr/arm-linux-gnueabihf/ -g 1234 ./antidote_patched
gdb-multiarch -q


Inside gdb:
pwndbg> file antidote_patched
Reading symbols from antidote_patched...
(No debugging symbols found in antidote_patched)
pwndbg> target remote localhost:1234

In order to pass in payload, need to write to payload and then redirect in using < payload

https://reverseengineering.stackexchange.com/questions/8829/cross-debugging-for-arm-mips-elf-with-qemu-toolchain

for sending in payloads from multiple reads
(cat payload; cat payload2 ) | qemu-arm -L /usr/arm-linux-gnueabihf/ -g 1234
 ./antidote_patched

# Notes:
Need to 

