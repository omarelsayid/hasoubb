const { stdin } = require('process');
const readline = require('readline');
const rl= readline.createInterface(
   {
    input:process.stdin,
    output:process.stdout,
   }

)
rl.question('what is your name bro',Answer => {
    console.log('hello',Answer)
rl.close();
});