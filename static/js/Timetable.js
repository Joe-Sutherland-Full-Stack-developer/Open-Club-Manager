document.addEventListener('DOMContentLoaded', function() {
    const emptyCells = document.querySelectorAll('.empty-cell');
    const modal = document.getElementById('classModal');
    const form = document.getElementById('classInstanceForm');
    const bootstrapModal = new bootstrap.Modal(modal);
    let isModalOpen = false;

    function updateDuration() {
        const startTime = form.elements['start_time'].value;
        const finishTime = form.elements['finish_time'].value;
        
        if (startTime && finishTime) {
            const start = new Date(`2000-01-01T${startTime}`);
            const finish = new Date(`2000-01-01T${finishTime}`);
            const durationMs = finish - start;
            const durationMinutes = Math.round(durationMs / 60000);
            document.getElementById('duration').value = `${durationMinutes} minutes`;
        }
    }

    emptyCells.forEach(cell => {
        cell.addEventListener('click', function(event) {
            if (!isModalOpen) {
                const day = this.dataset.day;
                const slot = this.dataset.slot;

                form.elements['day'].value = day;
                form.elements['start_time'].value = slot;

                const startTimeInput = document.querySelector('[data-name="start_time"]');
                if (startTimeInput) {
                    startTimeInput.value = slot;
                }

                isModalOpen = true;
                bootstrapModal.show();
            }
        });
    });

    modal.addEventListener('shown.bs.modal', function() {
        isModalOpen = true;
    });

    modal.addEventListener('hidden.bs.modal', function() {
        isModalOpen = false;
    });

    // Allow changing start time
    const startTimeInput = document.querySelector('[data-name="start_time"]');
    if (startTimeInput) {
        startTimeInput.addEventListener('change', function() {
            form.elements['start_time'].value = this.value;
            updateDuration();
        });
    }

    // Update duration when finish time changes
    const finishTimeInput = document.querySelector('[data-name="finish_time"]');
    if (finishTimeInput) {
        finishTimeInput.addEventListener('change', updateDuration);
    }

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(form);

        fetch(form.action, {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Class instance added successfully!');
                bootstrapModal.hide();
                // Optionally, update the timetable here
            } else {
                alert('Error: ' + data.error);
            }
        })
        .catch(error => console.error('Error:', error));
    });
});
