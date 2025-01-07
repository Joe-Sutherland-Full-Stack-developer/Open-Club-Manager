document.addEventListener('DOMContentLoaded', function() {

    
    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('event-cell')) {
            var slotTime = event.target.dataset.slot; // Retrieve time from clicked cell
            var day = event.target.dataset.day;

            if (typeof slotTime === 'undefined') {
                console.error("slotTime is not defined");
                return; // Exit if slotTime is not valid
            }

            // Format the slotTime if necessary (ensure it's in HH:mm)
            slotTime = formatTime(slotTime);

            document.getElementById('id_day').value = day; // Assuming your day field has this ID
            document.getElementById('id_start_time').value = slotTime; // Set start time
            document.getElementById('id_finish_time').value = slotTime; // Set finish time

            setFlatpickrValue('id_start_time', slotTime);
            setFlatpickrValue('id_finish_time', slotTime);

            
            // Update timepicker values if necessary
            // Note: You'll need to replace this with the appropriate method calls for your non-jQuery timepicker
            //setTimepickerTime('id_start_time', slotTime);
            //setTimepickerTime('id_finish_time', slotTime);
        }
    });

    // // Initialize timepickers
    // initializeTimepicker('id_start_time');
    // initializeTimepicker('id_finish_time');
});

function formatTime(time) {
    var parts = time.split(':');
    var hours = parts[0].padStart(2, '0'); // Ensure hours are two digits
    var minutes = parts[1].padStart(2, '0'); // Ensure minutes are two digits
    return `${hours}:${minutes}`;
}

// function initializeTimepicker(id) {
    // You'll need to replace this with the appropriate method for your non-jQuery timepicker
    // For example:
    // var element = document.getElementById(id);
    // new Timepicker(element, {
    //     showMeridian: false,
    //     minuteStep: 15,
    //     defaultTime: false
    // });
// }

// function setTimepickerTime(id, time) {
//     // Implement this function to set the time for your non-jQuery timepicker
// }


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
    classLinks.forEach(link => {
      link.addEventListener('click', function(e) {
        e.preventDefault();
        const eventId = this.dataset.eventId;
        if (eventId) {
          fetch(`/load-booking-form/${eventId}/`)
            .then(response => response.text())
            .then(html => {
              document.querySelector('#bookingModal .modal-body').innerHTML = html;
              new bootstrap.Modal(document.getElementById('bookingModal')).show();
            })
            .catch(error => console.error('Error:', error));
        } else {
          console.error('Event ID not found');
        }
      });
    });
  });
  
