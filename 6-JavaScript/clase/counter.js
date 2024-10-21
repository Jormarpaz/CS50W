/**
 * @file counter.js
 * @description This script manages a counter using the browser's local storage. 
 * It initializes the counter if it doesn't exist, increments the counter on button click, 
 * and updates the displayed counter value in an HTML element.
 * 
 * @function increment
 * @description Increments the counter value stored in local storage, updates the displayed counter value in an HTML element, and saves the new counter value back to local storage.
 * 
 * @event DOMContentLoaded
 * @description Sets the initial displayed counter value from local storage and assigns the increment function to the button's onclick event.
 */
/**
 * Local Storage
 * localStorage.getItem('key') obtener un valor
 * localStorage.setItem('key', 'value') guardar un valor
 */

if(!localStorage.getItem('counter')) {
    localStorage.setItem('counter', 0);   
}

function increment() {
    let counter = localStorage.getItem('counter');
    counter++;
    document.querySelector("h1").innerHTML = counter;
    localStorage.setItem('counter', counter);
}

document.addEventListener("DOMContentLoaded", function () {
    document.querySelector('h1').innerHTML = localStorage.getItem('counter');
    document.querySelector("button").onclick = increment;
});





