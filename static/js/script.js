document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('fileUploadForm').addEventListener('submit', function(event) {
        event.preventDefault(); 
        console.log('Form submitted');
        let formData = new FormData();
        formData.append('file', document.getElementById('file').files[0]); // Append the file data
        
        console.log('Uploading file');
        fetch('http://localhost:5000/upload', {
            method: 'POST',
            body: formData
        }).then(response => {
            console.log(response);
            if (response.ok) {
                $('#fileUploadModal').modal('hide'); // Hide the modal
                alert('File uploaded successfully!');
            } else {
                response.json().then(data => {
                    alert(data.error || 'Error uploading file');
                });
            }
        }).catch(error => {
            console.error('Error:', error);
            alert('Error uploading file');
        });
    });
});
$(document).ready(function() {
    $('.malware-title').hover(
        function() {
            $(this).siblings('.popover-content').fadeIn('fast');
        },
        function() {
            $(this).siblings('.popover-content').fadeOut('fast');
        }
    );
});


//Get the button
let mybutton = document.getElementById("btn-back-to-top");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function () {
  scrollFunction();
};

function scrollFunction() {
  if (
    document.body.scrollTop > 20 ||
    document.documentElement.scrollTop > 20
  ) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}
// When the user clicks on the button, scroll to the top of the document
mybutton.addEventListener("click", backToTop);

function backToTop() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}