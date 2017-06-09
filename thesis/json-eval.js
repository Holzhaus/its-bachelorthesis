// Maliciously constructed JSON string
let data = '[ "foo", (function(){alert("pwned!");})() ]';
// This executes the attacker's payload and returns the Array [ "foo", undefined ]
eval('(' + data + ')');
