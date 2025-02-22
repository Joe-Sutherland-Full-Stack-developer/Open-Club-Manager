document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('event-cell')) {
            const slotTime = event.target.dataset.slot;
            const day = event.target.dataset.day;

            if (typeof slotTime === 'undefined') {
                console.error("slotTime is not defined");
                return;
            }

            const formattedTime = formatTime(slotTime);
            document.getElementById('id_day').value = day;
            document.getElementById('id_start_time').value = formattedTime;
            document.getElementById('id_finish_time').value = formattedTime;

            setFlatpickrValue('id_start_time', formattedTime);
            setFlatpickrValue('id_finish_time', formattedTime);
        }
    });

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

    const editButtons = document.querySelectorAll('.edit-field');

    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            const row = button.closest('.row.mb-3');
            const formInput = row.querySelector('.edit-form-input');
            const saveButton = row.querySelector('.save-field');
            const plainText = row.querySelector('.form-control-plaintext');
            
            if (formInput) {
                formInput.classList.toggle('d-none');
                plainText.classList.toggle('d-none');
                saveButton.classList.toggle('d-none');
            }
        });
    });

    const tabs = document.querySelectorAll('#myTab .nav-link');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            tabs.forEach(function(t) {
                t.classList.remove('active-tab');
                t.setAttribute('aria-selected', 'false');
            });
            this.classList.add('active-tab');
            this.setAttribute('aria-selected', 'true');
            
            const tabName = this.id.replace('-tab', '');
            const url = new URL(window.location.href);
            url.searchParams.set('tab', tabName);
            history.replaceState(null, null, url.toString());
        });
    });
});

function formatTime(time) {
    const parts = time.split(':');
    const hours = parts[0].padStart(2, '0');
    const minutes = parts[1].padStart(2, '0');
    return `${hours}:${minutes}`;
}

function setFlatpickrValue(inputId, value) {
    const inputElement = document.getElementById(inputId);
    if (inputElement) {
        inputElement.value = value;

        if (inputElement._flatpickr) {
            inputElement._flatpickr.setDate(value, true);
        } else {
            console.error(`Flatpickr instance not found for #${inputId}`);
        }
    } else {
        console.error(`Element with ID "${inputId}" not found.`);
    }
}
