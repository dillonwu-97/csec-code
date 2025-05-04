#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <assert.h>
#include <unistd.h>

// int data_buf[104] = {0};
// def bitmix (chr):
//     '''
//     Accept some character
//     generate new permutation based on the bits of the chr
//     0 1 2 3 4 -> 4 3 1 2 0 
//     '''
//     # second half
//     a = 2 * (chr & 4) 
//     b = 2 * (chr & 8)
//     c = (chr & 0x10) >> 2
//     d = (a | b | c)
//     second_half = (d & 0x1c) >> 2
//
//     # first half
//     a = (chr & 2) >> 1
//     b = 2 * (chr & 1)
//     c = (a | b) & 3
//     first_half = 8 * c
//
//     return first_half | second_half
uint8_t bitmix(uint8_t chr) {
    uint8_t a,b,c,d;
    uint8_t first_half, second_half;
    a = 2 * (chr & 4);
    b = 2 * (chr & 8);
    c = (chr & 0x10) >> 2;
    d = (a | b | c);
    second_half = (d & 0x1c) >> 2;

    a = (chr & 2) >> 1;
    b = 2 * (chr & 1);
    c = (a | b) & 3;
    first_half = 8 * c;

    return first_half | second_half;
}

uint8_t checker(int* arr) {
    uint8_t new_val = 0;
    uint8_t a, b, c;
    int dub;
    int idx;
    int result;
    for (int i = 0; i < 5; i++) {
        dub = (int)((double) arr[8] * 5.0);
        a = (uint8_t)(arr[0] + dub + 5 * i); // first part
        b = (uint8_t)(arr[4] + 5 * arr[6] + i + 5 * arr[7]);
        c = a * b + new_val;
        new_val = c % 199;
        // printf("%d %x %c\n", new_val, new_val, new_val);
    }

    idx = 5 * arr[7] + 5 * arr[6] + (int)((double)arr[8] * 5.0);
    printf("idx is %d\n", idx);

    //data_buf[idx] = new_val;
    // dub = (int)((double)arr[8] * 5.0);
    // result = (uint8_t)(arr[2] + (int)bitmix(dub) + 5 * arr[7] + 5 * arr[6]);
    // printf("Result: %d %x %c\n", result, result, result);
        
    return 0;
}

void test() {
    for (uint16_t i = 0; i < 256; i++) {
        printf("%d %d\n", (uint8_t)i, bitmix((uint8_t)i));
    }
}

int sandbox2() {
    // test();
    // i might need to combine the bytes, and then use 
    // 4 * 8 = 32
    // 8 integers int total 
    // int internal_buf[32] = {
    //     0xC2, 0x3F, 0x9C, 0x15, 0x7C, 0x19, 0x81, 0x47,
    //     0x1F, 0xB2, 0xC9, 0xA7, 0x46, 0x97, 0x3F, 0x8D,
    //     0x68, 0x0B, 0x7C, 0x31, 0x2A, 0x79, 0x49, 0x43,
    //     0x2D, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    //     0x08, 0xBA, 0xB6, 0x16, 0xC5, 0x4A, 0x1B, 0x27,
    //     0x0B, 0x95, 0x6A, 0x02, 0x91, 0x30, 0x6F, 0x81,
    //     0x6F, 0x80, 0x2B, 0x5D, 0xB6, 0xA5, 0x21, 0x83,
    //     0x10, 0x89, 0xA1, 0x66, 0x15, 0x93, 0x1A, 0x00
    // };

    int int_buf[17] = {
        0x159C3FC2, // from .data:0000000140009008
        0x4781197C, // from .data:000000014000900C
        0xA7C9B21F, // from .data:0000000140009010
        0x8D3F9746, // from .data:0000000140009014
        0x317C0B68, // from .data:0000000140009018
        0x4349792A, // from .data:000000014000901C
        0x0000002D, // from .data:0000000140009020 (originally dd 2Dh)
        0x00000000, // from .data:0000000140009024 (originally dd 0)
        0x16B6BA08, // from .data:0000000140009028 (more_rand_characters)
        0x271B4AC5, // from .data:000000014000902C
        0x026A950B, // from .data:0000000140009030 (originally dd 26A950Bh)
        0x816F3091, // from .data:0000000140009034
        0x5D2B806F, // from .data:0000000140009038
        0x8321A5B6, // from .data:000000014000903C
        0x66A18910, // from .data:0000000140009040
        0x001A9315  // from .data:0000000140009044 (originally dd 1A9315h)
    };
    // for (int i = 0; i < sizeof(buff_a) / sizeof(int); i++) {
    //     printf("%d\n", (int)(5.0 * (double)buff_a[i]));
    // }
    // printf("%d\n", (int)(5.0 * (double)buff_a[8]));
    int new_val = int_buf[7] * 5 + int_buf[6] * 5 + (int)((double)int_buf[8] * 5.0);
    printf("%d %x\n", int_buf[6] * 5, int_buf[6] * 5);
    printf("new_val %d %x\n", new_val, new_val);

    int arr[9] = {'a','a','a','a',
                    'a','a','a','a',
                    'a'};
    // checker(buff_a);
    unsigned long long val = 0x3fd999999999999a;
    printf("%lld\n:", val);
}

int data_buf[0x1000] = {0};
int flag = 0x0;
int rotated_arr[40] = {0};
int counter = 0;

// so we have to find some way to recvoer new_val 
int solve(uint8_t* c2, uint8_t* ob, uint8_t* inp, int x, int y, double db) {
    int new_val = 0;
    uint8_t temp1,temp2;
    uint8_t e, f;
    uint8_t result;

    for (int i = 0; i < 5; i++) {
        // printf("%d\n", 5 * i + (int)(db * 5.0));
        // return 0;
        temp1 = 5 * i + (int)(db * 5.0);
        e = *(c2 + temp1);
        temp2 = 5 * x + 5 * y + i;
        f = *(inp + temp2);
        printf("c2 idx: %d, inp idx: %d\n", temp1, temp2);
        new_val = (new_val + e * f) % 199;
    } 
    // what is the point of storing this in the data_buf though?
    // this looks like it wraps back around as well interestingly
    // the SAT solver looks like it isn't solving our problem wtf 
    printf("data_buf idx: %d\n", 5 * y + 5 * x + (int)(db * 5.0));
    data_buf[ 5 * y + 5 * x + (int)(db * 5.0) ] = new_val;
    // calculating result 
    temp1 = (int)(db * 5.0) + 5 * (y & 0xf) + 5 * (x & 0xf);
    temp2 = bitmix( temp1 );
    printf("bitmix value: %d\n",temp2);
    result = *(ob + temp2);
    printf("result we need: %d %x\n", result, result);
    char whatever;
    // read(1, &whatever, 1);
    return temp2; // this is more important, i think it gives us more constraints for the sat solver
    data_buf [ 5 * y + 5 * x + (int)(db * 5.0) ] = result;

    assert (result <= 199);
    printf("result we need: %d %x\n", result, result);
    // return temp2;

    // checking that the implementation is correct essentially
    // this also does a result == new_val check 
    temp1 = (int)(db * 5.0) + 5 * (y & 0xf) + 5 * (x & 0xf);
    temp2 = 1 << temp1;
    flag |= temp2;
    result = flag;
    return result;
}

int wrap() {
    uint8_t a_buf[32] = {
        0xC2, 0x3F, 0x9C, 0x15, 0x7C, 0x19, 0x81, 0x47,
        0x1F, 0xB2, 0xC9, 0xA7, 0x46, 0x97, 0x3F, 0x8D,
        0x68, 0x0B, 0x7C, 0x31, 0x2A, 0x79, 0x49, 0x43,
        0x2D, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
    };

    uint8_t b_buf[32] = {
        0x08, 0xBA, 0xB6, 0x16, 0xC5, 0x4A, 0x1B, 0x27,
        0x0B, 0x95, 0x6A, 0x02, 0x91, 0x30, 0x6F, 0x81,
        0x6F, 0x80, 0x2B, 0x5D, 0xB6, 0xA5, 0x21, 0x83,
        0x10, 0x89, 0xA1, 0x66, 0x15, 0x93, 0x1A, 0x00
    };

    uint8_t user_inp[25];
    for (int i = 0; i < 25; i++) {
        user_inp[i] = 'a';
    }
    

    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            for (double k = 0.0; k < 1.0; k += 0.2) {
                int val = solve(a_buf, b_buf, user_inp, i, j, k);
                printf("val: %d\n", val);
                rotated_arr[val] += 1;
            }
        }
    }
    // for (int i = 0; i < 25; i++) {
    //     printf("%d ", data_buf[i]);
    // }
    // printf("\n");
    for (int i = 0; i < 32; i++) {
        printf("%d ", rotated_arr[i]);
    }
    printf("\n");

}

int main() {
    wrap();
    // printf("%lf",0x3fe999999999999a);
    return 0;
}
