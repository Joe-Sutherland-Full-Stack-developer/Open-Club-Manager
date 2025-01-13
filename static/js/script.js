document.addEventListener('DOMContentLoaded', function() {

 // Admin timetable view/edit scripts 

    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('event-cell')) {
            var slotTime = event.target.dataset.slot; // Retrieve time from clicked cell
            var day = event.target.dataset.day; //retrieve day from clicked cell

            if (typeof slotTime === 'undefined') {
                console.error("slotTime is not defined");
                return; // Exit if slotTime is not valid
            }

            // Format the slotTime if necessary (ensure it's in HH:mm)
            slotTime = formatTime(slotTime);
            // Populate the add event modal with details from clicked cell
            document.getElementById('id_day').value = day; // set Day 
            document.getElementById('id_start_time').value = slotTime; // Set start time
            document.getElementById('id_finish_time').value = slotTime; // Set finish time

            setFlatpickrValue('id_start_time', slotTime);
            setFlatpickrValue('id_finish_time', slotTime);
        }
    });
});
   

function formatTime(time) {
    var parts = time.split(':');
    var hours = parts[0].padStart(2, '0'); // Ensure hours are two digits
    var minutes = parts[1].padStart(2, '0'); // Ensure minutes are two digits
    return `${hours}:${minutes}`;
}



function setFlatpickrValue(inputId, value) {
    var inputElement = document.getElementById(inputId);
    if (inputElement) {
        // Update the value of the input
        inputElement.value = value;

        // Trigger the flatpickr instance to reflect the change
        if (inputElement._flatpickr) {
            inputElement._flatpickr.setDate(value, true); // true triggers change events
        } else {
            console.error(`Flatpickr instance not found for #${inputId}`);
        }
    } else {
        console.error(`Element with ID "${inputId}" not found.`);
    }
}



// dashboard scripts


document.addEventListener('DOMContentLoaded', function() {
    const classLinks = document.querySelectorAll('.class-instance-link');
    let bookingModal;

    classLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const eventId = this.dataset.eventId;
            if (eventId) {
                fetch(`/load-booking-form/${eventId}/`)
                    .then(response => response.text())
                    .then(html => {
                        document.querySelector('#bookingModal .modal-body').innerHTML = html;
                        bookingModal = new bootstrap.Modal(document.getElementById('bookingModal'));
                        bookingModal.show();

                        // Add event listener for the close button
                        document.querySelector('#bookingModal .btn-close').addEventListener('click', function() {
                            bookingModal.hide();
                        });
                    })
                    .catch(error => console.error('Error:', error));
            } else {
                console.error('Event ID not found');
            }
        });
    });
});


  
// Account details
document.addEventListener('DOMContentLoaded', function() {
    const editButtons = document.querySelectorAll('.edit-field');

    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Find the closest row to the clicked button
            const row = button.closest('.row.mb-3');
            // Find the input field in the same row
            const formInput = row.querySelector('.edit-form-input');
            const saveButton = row.querySelector('.save-field');
            const plainText = row.querySelector('.form-control-plaintext');
            // Toggle the visibility of the input field and save button
            if (formInput) {
                formInput.classList.toggle('d-none'); // Add or remove 'd-none' class
                plainText.classList.toggle('d-none'); //Toggle plain text visibility
                saveButton.classList.toggle('d-none'); // Toggle save button visibility
            }
        });
    });
});


//Toggle active class on tabs for styling purposes

document.addEventListener('DOMContentLoaded', function() {
    const tabs = document.querySelectorAll('#myTab .nav-link');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', function(event) {          
            // Update active state
            tabs.forEach(function(t) {
                t.classList.remove('active-tab');
                t.setAttribute('aria-selected', 'false');
            });
            this.classList.add('active-tab');
            this.setAttribute('aria-selected', 'true');
            // Update URL
            const tabName = this.id.replace('-tab', '');
            const url = new URL(window.location.href);
            url.searchParams.set('tab', tabName);
            history.replaceState(null, null, url.toString());



        });
    });
            
});
