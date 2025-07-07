import { GridStack } from 'gridstack';
import 'gridstack/dist/gridstack.min.css';

document.addEventListener('DOMContentLoaded', () => {
  const grid = GridStack.init({
    cellHeight: 250,
    draggable: {
      handle: '.grid-stack-item-content'
    },
    resizable: {
      handles: 'e, se, s, sw, w'
    },
    float: true
  });
});


document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('patient-search-form');
  const resultsTable = document.getElementById('patient-results-table');
  const resultsBody = document.getElementById('patient-results-body');
  const noResultsMsg = document.getElementById('no-results-msg');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const params = new URLSearchParams({
      mrn: document.getElementById('search-mrn').value.trim(),
      greek_fname: document.getElementById('search-greek-fname').value.trim(),
      greek_lname: document.getElementById('search-greek-lname').value.trim(),
      fname: document.getElementById('search-fname').value.trim(),
      lname: document.getElementById('search-lname').value.trim(),
      dob: document.getElementById('search-dob').value,
      phone: document.getElementById('search-phone').value.trim(),
      email: document.getElementById('search-email').value.trim(),
      amka: document.getElementById('search-amka').value.trim(),
    });

    try {
      const response = await fetch(`/api/patients?${params.toString()}`);
      if (!response.ok) throw new Error('Network response was not ok');

      const patients = await response.json();

      resultsBody.innerHTML = '';

      if (patients.length === 0) {
        resultsTable.style.display = 'none';
        noResultsMsg.style.display = 'block';
      } else {
        noResultsMsg.style.display = 'none';
        resultsTable.style.display = 'table';

        patients.forEach(p => {
          const row = document.createElement('tr');
          row.innerHTML = `
            <td>${p.mrn}</td>
            <td>${p.greek_fname || ''}</td>
            <td>${p.greek_lname || ''}</td>
            <td>${p.fname}</td>
            <td>${p.lname}</td>
            <td>${p.dob || ''}</td>
            <td>${p.phone || ''}</td>
            <td>${p.email || ''}</td>
            <td>${p.amka || ''}</td>
          `;
          resultsBody.appendChild(row);
        });
      }
    } catch (error) {
      console.error('Error fetching patient data:', error);
      resultsTable.style.display = 'none';
      noResultsMsg.textContent = 'Error loading results.';
      noResultsMsg.style.display = 'block';
    }
  });
});


