let isEditClassModalInitialized = false;
document.addEventListener('DOMContentLoaded', function () {
    // Handle the "Add Class" modal
    initializeAddClassModal();

    // Handle the "Edit Class" modal
    initializeEditClassModal();
    
    initializeGlobalModalCloseButtons();
});

// Function to initialize the "Add Class" modal
function initializeAddClassModal() {
    const emptyCells = document.querySelectorAll('.empty-cell');
    const addClassModalElement = document.getElementById('classModal');
    const addClassForm = document.getElementById('classInstanceForm');
    const addClassModal = new bootstrap.Modal(addClassModalElement);
    console.log(bootstrap)
    emptyCells.forEach(cell => {
        cell.addEventListener('click', function () {
            const day = this.dataset.day;
            const slot = this.dataset.slot;
            console.log("Day:", day, "Slot:", slot);
            // Clear previous content to avoid conflicts
            addClassForm.reset();
            // Populate form fields
            addClassForm.elements['day'].value = day;
            addClassForm.elements['start_time'].value = slot;
            
            const startTimeInput = document.querySelector('[data-name="start_time"]');
                if (startTimeInput) {
                    startTimeInput.value = slot;
                }

            addClassModal.show();
        });
    });
            
        };
    




function initializeEditClassModal() {
    if (isEditClassModalInitialized) return; // Prevent re-initialization
    isEditClassModalInitialized = true;

    const editCells = document.querySelectorAll('td[data-instance-id]');
    const editModalElement = document.getElementById('edit-modal');
    const editModalContent = document.getElementById('edit-modal-content');
    const editModal = new bootstrap.Modal(editModalElement);

    editCells.forEach(cell => {
        cell.addEventListener('click', function () {
            const instanceId = this.dataset.instanceId;

            // Clear previous content to avoid conflicts
            editModalContent.innerHTML = '';

            // Load edit form
            fetch(`/class-instance/${instanceId}/edit/`)
                .then(response => response.text())
                .then(html => {
                    editModalContent.innerHTML = html;

                    // Add event listeners for dynamically loaded content
                    initializeEditModalEventListeners(editModalContent);

                    editModal.show();
                });
        });
    });
}

// Function to initialize event listeners for the "Edit Class" modal
function initializeEditModalEventListeners(modalContent) {
    // Handle individual edit button clicks
    modalContent.addEventListener('click', function (e) {
        const editTrigger = e.target.closest('.edit-trigger');
        if (editTrigger) {
            const field = editTrigger.dataset.field;
            // Toggle edit mode for the specific field
            toggleEditMode(modalContent, field, editTrigger);
        }
    });

    // Handle "Edit All" button
    const editAllButton = modalContent.querySelector('.edit-all-btn');
    if (editAllButton) {
        editAllButton.addEventListener('click', function () {
            const isInEditMode = modalContent.querySelector('.edit-mode:not(.d-none)');
            if (isInEditMode) {
                modalContent.querySelectorAll('.view-mode').forEach(el => el.classList.remove('d-none'));
                modalContent.querySelectorAll('.edit-mode').forEach(el => el.classList.add('d-none'));
            } else {
                modalContent.querySelectorAll('.view-mode').forEach(el => el.classList.add('d-none'));
                modalContent.querySelectorAll('.edit-mode').forEach(el => el.classList.remove('d-none'));
            }
        });
    }

    // Handle delete button with confirmation
    modalContent.addEventListener('click', function (e) {
        const deleteButton = e.target.closest('[hx-delete]');
        if (deleteButton) {
            const confirmMessage = deleteButton.getAttribute('hx-confirm');
            if (confirmMessage && !confirm(confirmMessage)) {
                e.preventDefault(); // Prevent the delete action if the user cancels
            }
        }
    });
}

// Function to toggle edit mode for a specific field
function toggleEditMode(modalContent, field, editTrigger) {
    const viewMode = modalContent.querySelector(`.view-mode[data-field="${field}"]`);
    const editMode = modalContent.querySelector(`.edit-mode[data-field="${field}"]`);
    const parentRow = editTrigger.closest('.row');
    if (viewMode && editMode && parentRow) {
        // Toggle the edit-mode class on the parent row
        if (parentRow.classList.contains('edit-mode')) {
            parentRow.classList.remove('edit-mode');
            viewMode.classList.remove('d-none');
            editMode.classList.add('d-none');
            const icon = editTrigger.querySelector('i');
            if (icon) {
                icon.classList.remove('fa-xmark', 'fa-solid');
                icon.classList.add('fa-edit', 'fas');
            }
        } else {
            parentRow.classList.add('edit-mode');
            viewMode.classList.add('d-none');
            editMode.classList.remove('d-none');
            const icon = editTrigger.querySelector('i');
            if (icon) {
                icon.classList.remove('fa-edit', 'fas');
                icon.classList.add('fa-xmark', 'fa-solid');
            }
        }
    }
}
// // // Function to initialize global modal close buttons
// function initializeGlobalModalCloseButtons() {
//     document.addEventListener('click', function (e) {
//         const closeButton = e.target.closest('[data-bs-dismiss="modal"]');
//         if (closeButton) {
//             alert('No changes were made.');
            
            
//         }
//     });
// }
// Function to handle confirmation dialogs for Save and Delete class instance actions
// This function is called when the user clicks the Save or Delete button
document.addEventListener('DOMContentLoaded', function () {
    // Function to handle the confirmation dialog
    function handleConfirmation(e, message) {
        if (!confirm(message)) {
            e.preventDefault(); // Prevent form submission if the user cancels
        }
    }

    // Event listener for the Save button
    document.addEventListener('click', function (e) {
        if (e.target && e.target.classList.contains('save-btn')) {
            const applyToRepeats = document.querySelector('#applyToRepeats');
            let message;

            if (applyToRepeats && applyToRepeats.checked) {
                message = "These changes will be applied to all future repeats of this session. Would you like to proceed?";
            } else {
                const classType = document.querySelector('[name="class_type"]').value;
                const instanceDate = document.querySelector('[name="instance_date"]').value;
                message = `These changes will be applied exclusively to the ${classType} on ${instanceDate}. Would you like to proceed?`;
            }

            handleConfirmation(e, message);
        }
    });

    // Event listener for the Delete button
    document.addEventListener('click', function (e) {
        if (e.target && e.target.classList.contains('delete-btn')) {
            const applyToRepeats = document.querySelector('#applyToRepeats');
            let message;

            if (applyToRepeats && applyToRepeats.checked) {
                message = "This action will delete all future repeats of this session. Are you sure you want to proceed?";
            } else {
                message = "This action will delete only this class instance. Are you sure you want to proceed?";
            }

            handleConfirmation(e, message);
        }
    });
});