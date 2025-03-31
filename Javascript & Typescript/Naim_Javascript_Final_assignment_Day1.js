// Task 1: Variable Declarations and Basic Arithmetic Operations
let num1 = 8; // Change the numbers as you like
let num2 = 2;

console.log("Addition: " + (num1 + num2));
console.log("Subtraction: " + (num1 - num2));
console.log("Multiplication: " + num1 * num2);
console.log("Division: " + num1 / num2);

// Task 2: Control Structures - Conditional Statements
function checkNumber(num) {
    if (num > 0) {
        console.log(num + " is positive.");
    } else if (num < 0) {
        console.log(num + " is negative.");
    } else {
        console.log(num + " is zero.");
    }
}

// Example calls for Task 2
checkNumber(3);
checkNumber(-1);
checkNumber(0);

// Task 3: Functions and String Manipulation
function reverseString(str) {
    return str.split('').reverse().join('');
}

// Example calls for Task 3
console.log(reverseString("hello"));
console.log(reverseString("javascript"));

// Task 5: Arrays and Loops
let favoriteFruits = ["Apple", "Banana", "Cherry", "Date", "Stawberry"];

for (let i = 0; i < favoriteFruits.length; i++) {
    console.log(favoriteFruits[i]);
}
