document.querySelector('#patientForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const formData = new FormData(this);
    const patientData = Object.fromEntries(formData.entries());

    // Call duplicate check endpoint
    const response = await fetch('/check_patient_duplicate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(patientData)
    });

    const data = await response.json();

    if (data.duplicates && data.duplicates.length > 0) {
        // Show modal and list duplicates
        const modal = document.getElementById('duplicateModal');
        const list = document.getElementById('duplicateList');
        list.innerHTML = ''; // clear old

        data.duplicates.forEach(p => {
            const li = document.createElement('li');
            li.textContent = `MRN: ${p.mrn}, Name: ${p.fname} ${p.lname}, DOB: ${p.dob}`;
            list.appendChild(li);
        });

        modal.style.display = 'block';

        // Handle buttons
        document.getElementById('btnYes').onclick = () => {
            modal.style.display = 'none';
            // Redirect or open update form for existing patient (using first duplicate ID)
            window.location.href = `/edit_patient/${data.duplicates[0].id}`;
        };

        document.getElementById('btnNo').onclick = () => {
            modal.style.display = 'none';
            // Proceed to submit form normally now for new patient creation
            this.submit();
        };

    } else {
        // No duplicates, proceed with form submit
        this.submit();
    }
});
