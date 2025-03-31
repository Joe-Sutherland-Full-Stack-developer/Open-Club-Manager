// document.addEventListener('DOMContentLoaded', function() {
//     const emptyCells = document.querySelectorAll('.empty-cell');
//     const modal = document.getElementById('classModal');
//     const form = document.getElementById('classInstanceForm');
//     const bootstrapModal = new bootstrap.Modal(modal);
//     let isModalOpen = false;

    // function updateDuration() {
    //     let startTime = form.elements['start_time'].value;
    //     let finishTime = form.elements['finish_time'].value;
        
    //     if (startTime && finishTime) {
    //         const start = new Date(`2000-01-01T${startTime}`);
    //         const finish = new Date(`2000-01-01T${finishTime}`);
    //         const durationMs = finish - start;
    //         const durationMinutes = Math.round(durationMs / 60000);
    //         document.getElementById('duration').value = `${durationMinutes} minutes`;
    //     }
    // }

    // emptyCells.forEach(cell => {
    //     cell.addEventListener('click', function() {
    //         if (!isModalOpen) {
    //             const day = this.dataset.day;
    //             const slot = this.dataset.slot;

    //             form.elements['day'].value = day;
    //             form.elements['start_time'].value = slot;

    //             const startTimeInput = document.querySelector('[data-name="start_time"]');
    //             if (startTimeInput) {
    //                 startTimeInput.value = slot;
    //             }

    //             isModalOpen = true;
    //             bootstrapModal.show();
    //         }
    //     });
    // });

    // modal.addEventListener('shown.bs.modal', function() {
    //     isModalOpen = true;
    // });

    // modal.addEventListener('hidden.bs.modal', function() {
    //     isModalOpen = false;
    // });

    // // Ensure dismissal buttons work properly
    // const closeButtons = modal.querySelectorAll('[data-bs-dismiss="modal"]');
    // closeButtons.forEach(button => {
    //     button.addEventListener('click', function() {
    //         bootstrapModal.hide(); // Explicitly hide the modal
            
    //         form.reset(); // Optional: Reset form fields when closing
            
    //     });
    // });

//     // Allow changing start time
//     const startTimeInput = document.querySelector('[data-name="start_time"]');
//     if (startTimeInput) {
//         startTimeInput.addEventListener('change', function() {
//             form.elements['start_time'].value = this.value;
//             updateDuration();
//         });
//     }

//     // Update duration when finish time changes
//     const finishTimeInput = document.querySelector('[data-name="finish_time"]');
//     if (finishTimeInput) {
//         finishTimeInput.addEventListener('change', updateDuration);
//     }

//     form.addEventListener('submit', function(e) {
//         e.preventDefault();
//         const formData = new FormData(form);

//         fetch(form.action, {
//             method: 'POST',
//             body: formData,
//         })
//         .then(response => response.json())
//         .then(data => {
//             if (data.success) {
//                 alert('Class instance added successfully!');
//                 bootstrapModal.hide();
//                 // Optionally, update the timetable here
//             } else {
//                 alert('Error: ' + data.error);
//             }
//         })
//         .catch(error => console.error('Error:', error));
//     });
// });

// // script to dynamically update the modal form fields depending on selected class type
// document.addEventListener('DOMContentLoaded', function () {
//     const classTypeSelect = document.querySelector('.class-type-select');
//     const durationField = document.querySelector('#id_duration'); // Assuming you have a duration field
//     const startTimeField = document.querySelector('#id_start_time');
//     const finishTimeField = document.querySelector('#id_finish_time');
//     const capacityField = document.querySelector('#id_capacity');

    // function updateFields() {
    //     const selectedOption = classTypeSelect.options[classTypeSelect.selectedIndex];
    //     if (!selectedOption.value) return; // Exit if no option is selected

    //     // Retrieve duration and capacity from data attributes
    //     const duration = parseInt(selectedOption.getAttribute('data-duration'), 10); // Parse as integer
    //     const capacity = selectedOption.getAttribute('data-capacity');

    //     // Update duration field
    //     if (durationField) {
    //         durationField.value = isNaN(duration) ? '' : duration; // Ensure valid value
    //     }

    //     // Update capacity field
    //     if (capacityField) {
    //         capacityField.value = capacity || ''; // Fallback to empty string if no capacity
    //     }

    //     // Update finish time based on start time and duration
    //     if (startTimeField.value && !isNaN(duration)) {
    //         const [hours, minutes] = startTimeField.value.split(':').map(Number); // Split and parse start time
    //         if (!isNaN(hours) && !isNaN(minutes)) {
    //             // Create a Date object for the start time
    //             const startTime = new Date();
    //             startTime.setHours(hours, minutes, 0, 0); // Set hours and minutes

    //             // Add the duration (in minutes)
    //             const finishTime = new Date(startTime.getTime() + duration * 60000); // Add duration in milliseconds

    //             // Format the finish time as HH:MM
    //             const formattedFinishTime = `${String(finishTime.getHours()).padStart(2, '0')}:${String(finishTime.getMinutes()).padStart(2, '0')}`;
    //             finishTimeField.value = formattedFinishTime;
    //             console.log("Finish time:", formattedFinishTime);
    //         } else {
    //             console.error("Invalid start time format.");
    //         }
    //     } else {
    //         finishTimeField.value = ''; // Clear finish time if inputs are invalid
    //     }
    // }

//     classTypeSelect.addEventListener('change', updateFields);
//     startTimeField.addEventListener('change', updateFields);

//     // Initial update if a class type is pre-selected
//     if (classTypeSelect.value) {
//         updateFields();
//     }
// });

document.addEventListener('DOMContentLoaded', function() {
    const emptyCells = document.querySelectorAll('.empty-cell');
    const modal = document.getElementById('classModal');
    const form = document.getElementById('classInstanceForm');
    const bootstrapModal = new bootstrap.Modal(modal);

    emptyCells.forEach(cell => {
        cell.addEventListener('click', function() {
            const day = this.dataset.day;
            const slot = this.dataset.slot;
            
            
            form.elements['day'].value = day;
            form.elements['start_time'].value = slot;
            

             const startTimeInput = document.querySelector('[data-name="start_time"]');
                if (startTimeInput) {
                    startTimeInput.value = slot;
                }
             
            bootstrapModal.show();
        });
    });
    

    const closeButtons = modal.querySelectorAll('[data-bs-dismiss="modal"]');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            bootstrapModal.hide(); // Explicitly hide the modal
        })
    // Reset state on modal hide
    modal.addEventListener('hidden.bs.modal', function() {
        form.reset(); // Optional: Reset form fields when closing
    });
})});
