// This was able to create a segfault

function bug(arr) {
    ret = 0;
    for (var i = 0; i< 100; i++) {
        ret ++;
    }
    return arr[1]
}

function trigger() {
    dbl = [1.0, 1.0] 
    obj = [{}, {}] 
    for (var i = 0; i < 100000; i++) {
        // wil this get optimized out since the value isnt' used?
        bug(dbl);
    }
    console.log(bug(obj));

}

trigger()
