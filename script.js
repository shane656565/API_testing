document.addEventListener('DOMContentLoaded', () => {
    const customerJson = `{
        "customerCompany": "Apollo",
        "customerNumber": "3",
        "customerName": "Alice"
    }`;
    const customer = JSON.parse(customerJson);
    initializeDisplay(customer);
    fetchData(customer);
    setInterval(() => fetchData(customer), 5000);
});

function initializeDisplay(customer) {
    const authMessage = document.getElementById('authMessage');
    if (customer.customerNumber) {
        let unitNumber = customer.customerNumber.replace("Unit", "");
        authMessage.textContent = `Hello ${customer.customerName}, Welcome to ${customer.customerCompany} Apartment Electricity Control Console. Your Unit Number is ${unitNumber}`;
    } else {
        authMessage.textContent = 'Cannot Find ID, Please Use Apollo Account';
    }
}

function fetchData(customer) {
    if (customer.customerCompany === "Apollo") {
            fetch(`http://127.0.0.1:3000/api/combined-data?customerNumber=${customer.customerNumber}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    throw new Error(data.error);
                }
                else {
                    console.log('Data received:', data);
                    updateDisplay(data, customer.customerNumber);
                    displayError()
                }
            })
            .catch(error => {
                displayError('Something went wrong. Please Wait....');
                console.log(error);
            });
    }
}

function updateDisplay(data, unitNumber) {
    if (!unitNumber) return;

    const voltageDiv = document.getElementById('voltage');
    const currentDiv = document.getElementById('current');
    const powerDiv = document.getElementById('power');

    voltageDiv.textContent = `Voltage: ${data[`V${unitNumber}Eu`] || "Error"} V`; // Need to be changed
    currentDiv.textContent = `Current: ${data[`I${unitNumber}Eu`] || "Error"} A`;
    powerDiv.textContent = `Power: ${data[`kW${unitNumber}Eu`] || "Error"} kW`;

    const displayArea = document.getElementById('displayArea');
    displayArea.style.display = 'flex';
}

function displayError(message) {
    const errorMessageDiv = document.getElementById('error-message');
    errorMessageDiv.textContent = message;
    errorMessageDiv.style.display = 'block';
}
