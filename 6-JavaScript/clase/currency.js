document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('form').onsubmit = function() {

        fetch('https://api.exchangeratesapi.io/latest?base=USD') // Necesito un codigo API
        .then(response => response.json()) // json es una especie de objeto
        .then(data => {
            const currency = document.querySelector('#currency').value.toUpperCase();
            const rate = data.rates[currency];
            if (rate !== undefined) {
            document.querySelector('#result').innerHTML = `1 USD is equal to ${rate.toFixed(3)} ${currency}.`;
            } else {
            document.querySelector('#result').innerHTML = 'Invalid currency.';
            }
        })
        .catch(error => {
            console.log('Error:', error);
        });

        return false;
    }

    




});