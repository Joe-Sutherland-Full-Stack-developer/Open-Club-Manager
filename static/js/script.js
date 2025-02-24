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

// function setFlatpickrValue(inputId, value) {
//     const inputElement = document.getElementById(inputId);
//     if (inputElement) {
//         inputElement.value = value;

//         if (inputElement._flatpickr) {
//             inputElement._flatpickr.setDate(value, true);
//         } else {
//             console.error(`Flatpickr instance not found for #${inputId}`);
//         }
//     } else {
//         console.error(`Element with ID "${inputId}" not found.`);
//     }
// }


//SCript to dynamically set the text-color to be high-contrast against its background

// function getContrastRatio(color) {
//     const rgb = color.match(/\d+/g);
//     const luminance = (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255;
//     return luminance > 0.5 ? 'dark' : 'light';
// }

// function setTextColor(element) {
//     const bgColor = window.getComputedStyle(element).backgroundColor;
//     const contrastRatio = getContrastRatio(bgColor);
    
//     if (contrastRatio === 'light') {
//         element.classList.remove('text-dark');
//         element.classList.add('text-white');
//     } else {
//         element.classList.remove('text-white');
//         element.classList.add('text-dark');
//     }
// }
// document.querySelectorAll('.dynamic-text').forEach(setTextColor);

// Mutation observer for testing the above
// const observer = new MutationObserver(mutations => {
//     mutations.forEach(mutation => {
//         if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
//             setTextColor(mutation.target);
//         }
//     });
// });

// document.querySelectorAll('.dynamic-text').forEach(element => {
//     observer.observe(element, { attributes: true });
// });

// Script to dynamically adjust the text-color to remain high-contrast with the background color of its element.
function hexToRGBA(hex) {
    hex = hex.replace(/^#/, '');
    const r = parseInt(hex.slice(0, 2), 16);
    const g = parseInt(hex.slice(2, 4), 16);
    const b = parseInt(hex.slice(4, 6), 16);
    let a = 1;
    if (hex.length === 8) {
      a = parseInt(hex.slice(6, 8), 16) / 255;
    }
    return `rgba(${r}, ${g}, ${b}, ${a.toFixed(2)})`;
  }
  
  function getLuminance(clr) {
    if (clr.startsWith('#')) {
      clr = hexToRGBA(clr);
    }
    
    let rgb = clr.match(/\d+/g).map(Number);
    rgb = rgb.map(c => {
      c = c / 255;
      return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
    });
    
    return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2];
  }
  
  function chooseForeground(bkg) {
    let relativeLuminance = getLuminance(bkg);
    let chooseBlack = (relativeLuminance + 0.05) / 0.05;
    let chooseWhite = 1.05 / (relativeLuminance + 0.05);
    return (chooseBlack > chooseWhite) ? 'rgba(0, 0, 0, 1)' : 'rgba(255, 255, 255, 1)';
  }
  
  // Use
  let testAreas = document.getElementsByClassName('btn');
  Array.from(testAreas).forEach(testArea => {
    let computedStyle = window.getComputedStyle(testArea);
    let bkgColour = computedStyle.backgroundColor;
    testArea.style.color = chooseForeground(bkgColour);
  });
  