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
    const editAllButtons = document.querySelectorAll('.edit-all');

    editAllButtons.forEach(button => {
          button.addEventListener('click', function () {
              const form = button.closest('.participant-form');
              const editFields = form.querySelectorAll('.edit-form-input');
              const saveButtons = form.querySelectorAll('.save-field');
              const plainTexts = form.querySelectorAll('.form-control-plaintext');
              const individualEditButtons = form.querySelectorAll('.edit-field');
              const saveAllButton = form.querySelector('.save-all');

              // Show all input fields and save buttons, hide plain text and individual edit buttons
              editFields.forEach(field => field.classList.remove('d-none'));
              plainTexts.forEach(text => text.classList.add('d-none'));
              // saveButtons.forEach(saveButton => saveButton.classList.remove('d-none'));
              individualEditButtons.forEach(editButton => editButton.classList.add('d-none'));

              // Show the "Save All" button and hide the "Edit All" button
              saveAllButton.classList.remove('d-none');
              button.classList.add('d-none');
          });
      });


      const saveAllButtons = document.querySelectorAll('.save-all');

      saveAllButtons.forEach(button => {
          button.addEventListener('click', function () {
              const form = button.closest('.participant-form');
              const editFields = form.querySelectorAll('.edit-form-input');
              const plainTexts = form.querySelectorAll('.form-control-plaintext');
              const individualEditButtons = form.querySelectorAll('.edit-field');
              const editAllButton = form.querySelector('.edit-all');
  
              // Hide all input fields and save buttons, show plain text and individual edit buttons
              editFields.forEach(field => field.classList.add('d-none'));
              plainTexts.forEach(text => text.classList.remove('d-none'));
              individualEditButtons.forEach(editButton => editButton.classList.remove('d-none'));
  
              // Show the "Edit All" button and hide the "Save All" button
              editAllButton.classList.remove('d-none');
              button.classList.add('d-none');
  
              // Optionally, submit the form here if needed
              form.submit();
          });
      });

      document.addEventListener('DOMContentLoaded', function () {
        const deleteButtons = document.querySelectorAll('.delete-participant-btn');
        const participantIdInput = document.getElementById('participantIdInput');
    
        // Attach event listeners to all delete buttons
        deleteButtons.forEach(button => {
            button.addEventListener('click', function () {
                const participantId = button.getAttribute('data-participant-id'); // Get the participant ID
                participantIdInput.value = participantId; // Set the hidden input value
            });
        });
    });


function formatTime(time) {
    const parts = time.split(':');
    const hours = parts[0].padStart(2, '0');
    const minutes = parts[1].padStart(2, '0');
    return `${hours}:${minutes}`;
}



// Script to dynamically adjust the text-color to remain high-contrast with the background color of its element.
// document.addEventListener('DOMContentLoaded', function(){
// function hexToRGBA(hex) {
//     hex = hex.replace(/^#/, '');
//     const r = parseInt(hex.slice(0, 2), 16);
//     const g = parseInt(hex.slice(2, 4), 16);
//     const b = parseInt(hex.slice(4, 6), 16);
//     let a = 1;
//     if (hex.length === 8) {
//       a = parseInt(hex.slice(6, 8), 16) / 255;
//     }
//     return `rgba(${r}, ${g}, ${b}, ${a.toFixed(2)})`;
//   }
  
//   function getLuminance(clr) {
//     if (clr.startsWith('#')) {
//       clr = hexToRGBA(clr);
//     }
    
//     let rgb = clr.match(/\d+/g).map(Number);
//     let alpha = rgb.length === 4 ? rgb[3] / 255 : 1;
    
//     // Apply alpha blending with white background
//     rgb = rgb.slice(0, 3).map(c => {
//       c = c / 255;
//       return alpha * c + (1 - alpha);
//     });
    
//     // Apply gamma correction
//     rgb = rgb.map(c => c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
    
//     return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2];
//   }
  
//   function chooseForeground(bkg) {
//     let relativeLuminance = getLuminance(bkg);
//     let contrastRatioBlack = (relativeLuminance + 0.05) / 0.05;
//     let contrastRatioWhite = 1.05 / (relativeLuminance + 0.05);
//     return (contrastRatioBlack > contrastRatioWhite) ? 'rgba(0, 0, 0, 1)' : 'rgba(255, 255, 255, 1)';
//   }
// //   // Use
// //   let btnElements = document.getElementsByClassName('btn');
// //   let autoColorElements = document.getElementsByClassName('auto-color-text');
  
// //   let combinedElements = [...btnElements, ...autoColorElements];
  
// //   combinedElements.forEach(element => {

// //     let computedStyle = window.getComputedStyle(element);
// //     let bkgColour = computedStyle.backgroundColor;
// //     element.style.color = chooseForeground(bkgColour);
// //   });
// // });

// function updateElementColor(element) {
//     let computedStyle = window.getComputedStyle(element);
//     let bkgColor = computedStyle.backgroundColor;
//     let textColor = chooseForeground(bkgColor);
    
//     const customStylesheet = document.getElementById('custom-css').sheet;
//     if (!customStylesheet) {
//         console.error('Stylesheet with ID "custom-css" not found!');
//         return;
//     }
//     const rules = customStylesheet.cssRules || customStylesheet.rules;
    
//     // Get the element's ID
//     let elementId = element.id;
//     // exception catcher to help development 
//     if (!elementId) {
//         console.error('Element does not have an ID:', {
//             tagName: element.tagName,
//             classes: Array.from(element.classList),
//             textContent: element.textContent.slice(0, 50) + (element.textContent.length > 50 ? '...' : ''),
//             parentId: element.parentElement ? element.parentElement.id : 'No parent ID',
//             nthChild: Array.from(element.parentElement.children).indexOf(element) + 1
//         });
        
//         // Generate a temporary ID
//         elementId = 'auto-color-' + Math.random().toString(36).substr(2, 9);
//         element.id = elementId;
//         console.warn(`Temporary ID "${elementId}" assigned to element.`);
//     }
    
//     // Look for an existing rule for this element
//     let existingRule = Array.from(rules).find(rule => rule.selectorText === `#${elementId}`);
    
//     if (existingRule) {
//         // Update existing rule
//         existingRule.style.setProperty('color', textColor);
//     } else {
//         // Add new rule
//         customStylesheet.insertRule(`#${elementId} { color: ${textColor}; }`, rules.length);
//     }
    
//     // Update hover state
//     let hoverBkgColor = applyBrightnessFilter(bkgColor, 90);
//     let hoverTextColor = chooseForeground(hoverBkgColor);
    
//     let existingHoverRule = Array.from(rules).find(rule => rule.selectorText === `#${elementId}:hover`);
    
//     if (existingHoverRule) {
//         existingHoverRule.style.setProperty('color', hoverTextColor);
//     } else {
//         customStylesheet.insertRule(`#${elementId}:hover { color: ${hoverTextColor}; filter: brightness(90%); }`, rules.length);
//     }
// }

// let autoColorElements = document.getElementsByClassName('auto-color-text');

// Array.from(autoColorElements).forEach(updateElementColor);
// });

// // Set up MutationObserver for each element
// const observer = new MutationObserver((mutations) => {
//     mutations.forEach((mutation) => {
//         if (mutation.type === 'attributes' && mutation.attributeName === 'style') {
//             updateElementColor(mutation.target);
//         }
//     });
// });

// Array.from(autoColorElements).forEach(element => {
//     observer.observe(element, {
//         attributes: true,
//         attributeFilter: ['style']
//     });
// });

document.addEventListener('DOMContentLoaded', function(){
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
      let alpha = rgb.length === 4 ? rgb[3] / 255 : 1;
      
      // Apply alpha blending with white background
      rgb = rgb.slice(0, 3).map(c => {
        c = c / 255;
        return alpha * c + (1 - alpha);
      });
      
      // Apply gamma correction
      rgb = rgb.map(c => c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
      
      return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2];
    }
    
    function chooseForeground(bkg) {
      let relativeLuminance = getLuminance(bkg);
      let contrastRatioBlack = (relativeLuminance + 0.05) / 0.05;
      let contrastRatioWhite = 1.05 / (relativeLuminance + 0.05);
      return (contrastRatioBlack > contrastRatioWhite) ? 'rgba(0, 0, 0, 1)' : 'rgba(255, 255, 255, 1)';
    }
  
    function applyBrightnessFilter(color, brightness) {
      let rgb = color.match(/\d+/g).map(Number);
      return `rgb(${rgb.map(c => Math.max(0, Math.min(255, Math.round(c * brightness / 100)))).join(', ')})`;
    }
  
    function updateElementColor(element) {
      let computedStyle = window.getComputedStyle(element);
      let bkgColor = computedStyle.backgroundColor;
      let textColor = chooseForeground(bkgColor);
      
      const customStylesheet = document.getElementById('custom-css').sheet;
      if (!customStylesheet) {
        console.error('Stylesheet with ID "custom-css" not found!');
        return;
      }
      const rules = customStylesheet.cssRules || customStylesheet.rules;
      
      // Get the element's ID
      let elementId = element.id;
      // exception catcher to help development 
      if (!elementId) {
        console.error('Element does not have an ID:', {
          tagName: element.tagName,
          classes: Array.from(element.classList),
          textContent: element.textContent.slice(0, 50) + (element.textContent.length > 50 ? '...' : ''),
          parentId: element.parentElement ? element.parentElement.id : 'No parent ID',
          nthChild: Array.from(element.parentElement.children).indexOf(element) + 1
        });
        
        // Generate a temporary ID
        elementId = 'auto-color-' + Math.random().toString(36).substr(2, 9);
        element.id = elementId;
        console.warn(`Temporary ID "${elementId}" assigned to element.`);
      }
      
      // Look for an existing rule for this element
      let existingRule = Array.from(rules).find(rule => rule.selectorText === `#${elementId}`);
      
      if (existingRule) {
        // Update existing rule
        existingRule.style.setProperty('color', textColor);
      } else {
        // Add new rule
        customStylesheet.insertRule(`#${elementId} { color: ${textColor}; }`, rules.length);
      }
      
      // Update hover state
      let hoverBkgColor = applyBrightnessFilter(bkgColor, 90);
      let hoverTextColor = chooseForeground(hoverBkgColor);
      
      let existingHoverRule = Array.from(rules).find(rule => rule.selectorText === `#${elementId}:hover`);
      
      if (existingHoverRule) {
        existingHoverRule.style.setProperty('color', hoverTextColor);
      } else {
        customStylesheet.insertRule(`#${elementId}:hover { color: ${hoverTextColor}; filter: brightness(90%); }`, rules.length);
      }
    }
  
    let autoColorElements = document.getElementsByClassName('auto-color-text');
  
    Array.from(autoColorElements).forEach(updateElementColor);
  
    // Set up MutationObserver for each element
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (mutation.type === 'attributes' && mutation.attributeName === 'style') {
          updateElementColor(mutation.target);
        }
      });
    });
  
    Array.from(autoColorElements).forEach(element => {
      observer.observe(element, {
        attributes: true,
        attributeFilter: ['style']
      });
    });
  });
  
  


    