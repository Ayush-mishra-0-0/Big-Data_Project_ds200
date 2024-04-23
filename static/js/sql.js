// document.addEventListener('DOMContentLoaded', function() {
//     document.getElementById('queryForm').addEventListener('submit', function(event) {
//         event.preventDefault(); // Prevent default form submission

//         let formData = new FormData(); // Create FormData object

//         // Append the textarea value to the FormData object
//         formData.append('queryText', document.getElementById('textArea').value);

//         // Fetch API to send the form data to the server
//         fetch('/run_query', {
//             method: 'POST',
//             body: formData
//         })
//         .then(response => {
//             if (response.ok) {
//                 return response.text(); // Return the response text if successful
//             } else {
//                 throw new Error('Error uploading data'); // Throw an error if response is not OK
//             }
//         })
//         .then(data => {
//             console.log('Server response:', data); // Log the server response
//             // Do something with the response, such as updating the UI
//             // alert('Query submitted successfully');
//         })
//         .catch(error => {
//             console.error('Error:', error); // Log any errors to the console
//             alert('Error submitting query'); // Show an alert to the user
//         });
//     });
// });


// // sql.js
// $(document).ready(function() {
//     $('#queryForm').submit(function(event) {
//         event.preventDefault(); // Prevent the default form submission

//         // Get the query text from the textarea
//         var queryText = $('#textArea').val();

//         // Make an AJAX POST request to the server
//         $.ajax({
//             type: 'POST',
//             url: '/run_query', // Endpoint URL where the query will be processed
//             data: {queryText: queryText}, // Send the query text as data
//             success: function(response) {
//                 // Update the content of the div with ID 'queryResult' with the response
//                 $('#queryResult').html(response.result);
//             },
//             error: function(error) {
//                 console.log('Error:', error);
//             }
//         });
//     });
// });
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('queryForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission

        let formData = new FormData(); // Create FormData object

        // Append the textarea value to the FormData object
        formData.append('queryText', document.getElementById('textArea').value);

        // Append the selected CSV file value to the FormData object
        formData.append('csvFile', document.getElementById('selectedCSV').value);
        console.log(document.getElementById('selectedCSV').value);
        // Fetch API to send the form data to the server
        fetch('/run_query', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                return response.text(); // Return the response text if successful
            } else {
                throw new Error('Error uploading data'); // Throw an error if response is not OK
            }
        })
        .then(data => {
            document.getElementById('queryResult').innerHTML = data;
            console.log('Server response:', data); // Log the server response
            // Do something with the response, such as updating the UI
            // alert('Query submitted successfully');
        })
        .catch(error => {
            console.error('Error:', error); // Log any errors to the console
            alert('Error submitting query'); // Show an alert to the user
        });
    });
});

// $(document).ready(function() {
//     $('#queryForm').submit(function(event) {
//         event.preventDefault(); // Prevent the default form submission

//         // Get the query text from the textarea
//         var queryText = $('#textArea').val();

//         // Make an AJAX POST request to the server
//         $.ajax({
//             type: 'POST',
//             url: '/run_query', // Endpoint URL where the query will be processed
//             data: {queryText: queryText}, // Send the query text as data
//             success: function(response) {
//                 // Update the content of the div with ID 'queryResult' with the HTML content
//                 $('#queryResult').html(response);
//             },
//             error: function(error) {
//                 console.log('Error:', error);
//             }
//         });
//     });
// });
// $(document).ready(function() {
//     $('#queryForm').submit(function(event) {
//         event.preventDefault(); // Prevent the default form submission

//         // Get the query text from the textarea
//         var queryText = $('#textArea').val();

//         // Create a FormData object
//         var formData = new FormData();

//         // Append the query text to the FormData object
//         formData.append('queryText', queryText);

//         // Append the selected CSV file to the FormData object
//         var selectedCSV = $('#selectedCSV')[0].files[0]; // Get the selected file
//         formData.append('csvFile', selectedCSV);

//         // Make an AJAX POST request to the server
//         $.ajax({
//             type: 'POST',
//             url: '/run_query', // Endpoint URL where the query will be processed
//             data: formData, // Send the FormData object
//             processData: false, // Prevent jQuery from processing the data
//             contentType: false, // Set content type to false
//             success: function(response) {
//                 // Update the content of the div with ID 'queryResult' with the HTML content
//                 $('#queryResult').html(response);
//             },
//             error: function(error) {
//                 console.log('Error:', error);
//             }
//         });
//     });
// });

