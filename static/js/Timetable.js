// document.addEventListener('DOMContentLoaded', function() {
//     const table = document.querySelector('.timetable-grid');
//     const tooltip = document.createElement('div');
//     tooltip.classList.add('tooltip');
//     document.body.appendChild(tooltip);
  
//     table.addEventListener('mouseover', function(e) {
//       if (e.target.tagName === 'TD') {
//         const day = e.target.dataset.day;
//         const slot = e.target.dataset.slot;
//         if (day && slot) {
//           tooltip.textContent = `${day} - ${slot}`;
//           tooltip.style.display = 'block';
//         }
//       }
//     });
  
//     table.addEventListener('mousemove', function(e) {
//       tooltip.style.left = e.pageX + 10 + 'px';
//       tooltip.style.top = e.pageY + 10 + 'px';
//     });
  
//     table.addEventListener('mouseout', function() {
//       tooltip.style.display = 'none';
//     });
//   });
