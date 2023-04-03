function trigger(iter){
    obj = [1.0, 1.0]

    if (iter == 999999) {
        for (var i = 0; i < 2; i++) {
        }
        obj[1] = {}
        console.log(obj[1])
        return obj[1]
    }
    return obj[1]
}



for (var i = 0; i < 1000000; i++) {
    ret = trigger(i)
    if (i === 999999) {
        console.log(ret)
    }
}


