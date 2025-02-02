













const evaluate = require('static-eval');
const parse = require('esprima').parse;

module.exports = {
    isDumb(name){
        return (name.includes('Baker') || name.includes('Purvis'));
    },

    hasPassed({ exam, paper, assignment }, formula) {

        print(exam, paper, assignment)
        let ast = parse(formula).body[0].expression;
        let weight = evaluate(ast, { exam, paper, assignment });
        return parseFloat(weight) >= parseFloat(10.5);
    }
};

// Attack vector is hasPassed(parse(formula)) where formula is user specified code
// 