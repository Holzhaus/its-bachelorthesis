#!/usr/bin/env node
var num1 = '9007199254740993'; // $= 2^{53}+1$
var num2 = parseInt(num1).toString();
if(num1 == num2) {
    console.log(num1 + " == " + num2);
} else {
    console.log(num1 + " != " + num2);
}
// Output: 9007199254740993 != 9007199254740992
