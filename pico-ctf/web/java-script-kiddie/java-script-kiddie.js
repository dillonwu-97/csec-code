var bytes = [];
$.get("bytes", function(resp) {
    bytes = Array.from(resp.split(" "), x => Number(x));
});

// what is u_in? user_in
// What does user_in do and what is its point?
function assemble_png(u_in){
    var LEN = 16;
    var key = "0000000000000000";
    var shifter;
    if(u_in.length == LEN){
        key = u_in; 
    }
    var result = [];
    for(var i = 0; i < LEN; i++){
        shifter = key.charCodeAt(i) - 48;
        for(var j = 0; j < (bytes.length / LEN); j ++){
            result[(j * LEN) + i] = bytes[(((j + shifter) * LEN) % bytes.length) + i]
        }
    }
    // get rid of all the trailing 0's
    while(result[result.length-1] == 0){
        result = result.slice(0,result.length-1);
    }

    // base 64 encode the value of the result
    document.getElementById("Area").src = "data:image/png;base64," + btoa(String.fromCharCode.apply(null, new Uint8Array(result)));
    return false;
}