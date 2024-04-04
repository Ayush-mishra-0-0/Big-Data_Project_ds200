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

// JavaScript code for rotating text effect (optional)
$(document).ready(function() {
  var words = $(".cd-words-wrapper b");
  var wordIndex = 0;

  setInterval(function() {
    words.removeClass("is-visible");
    words.eq(wordIndex).addClass("is-visible");
    wordIndex = (wordIndex + 1) % words.length;
  }, 3000); // Change the interval (in milliseconds) as needed
});

document.addEventListener('DOMContentLoaded', function() {
  const content = document.querySelector('.content');

  function checkScroll() {
    const contentTop = content.getBoundingClientRect().top;
    const windowHeight = window.innerHeight;

    if (contentTop < windowHeight * 0.75) { // Adjust as needed for when to trigger animation
      content.classList.add('content-visible');
    }
  }

  window.addEventListener('scroll', checkScroll);
  checkScroll(); // Check initial scroll position
});

// JavaScript for hover effect on steps
document.querySelectorAll('.step').forEach(step => {
  step.addEventListener('mouseover', () => {
    step.style.transform = 'translateY(-5px)';
    step.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.2)';
  });

  step.addEventListener('mouseleave', () => {
    step.style.transform = 'none';
    step.style.boxShadow = '0 2px 4px rgba(0, 0, 0, 0.1)';
  });
});

// document.addEventListener('DOMContentLoaded', function() {
//   // Get all step titles
//   const stepTitles = document.querySelectorAll('.step-title');

//   // Add click event listener to each step title
//   stepTitles.forEach(title => {
//     title.addEventListener('click', function() {
//       // Toggle the 'hidden' class on the step content when clicked
//       const content = this.nextElementSibling;
//       content.classList.toggle('hidden');
//     });
//   });
// });
