document.addEventListener('DOMContentLoaded', function () {
    const calendarEl = document.getElementById('calendar');
  
    const appointmentModal = new bootstrap.Modal(document.getElementById('appointmentModal'));
    const appointmentForm = document.getElementById('appointmentForm');
    const errorMsg = document.getElementById('errorMsg');
    const deleteBtn = document.getElementById('deleteBtn');
    const saveBtn = document.getElementById('saveBtn');
  
    // Elements in modal
    const appointmentIdInput = document.getElementById('appointmentId');
    const patientIdInput = document.getElementById('patientId');
    const providerIdInput = document.getElementById('providerId');
    const startTimeInput = document.getElementById('startTime');
    const endTimeInput = document.getElementById('endTime');
  
    // Initialize FullCalendar
    const calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'timeGridWeek',
      nowIndicator: true,
      headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'timeGridWeek,timeGridDay,listWeek'
      },
      slotMinTime: '07:00:00',
      slotMaxTime: '19:00:00',
      editable: false,
      selectable: true,
      selectMirror: true,
  
      events: fetchAppointments,
  
      // When user selects time range to create appointment
      select: function (info) {
        clearForm();
        appointmentIdInput.value = ''; // new appointment
        patientIdInput.value = '';
        providerIdInput.value = '';
        startTimeInput.value = info.startStr.slice(0,16);
        endTimeInput.value = info.endStr.slice(0,16);
        deleteBtn.style.display = 'none';
        errorMsg.style.display = 'none';
        appointmentModal.show();
      },
  
      // When user clicks on an existing event
      eventClick: function (info) {
        clearForm();
        const event = info.event;
  
        appointmentIdInput.value = event.id;
        patientIdInput.value = event.extendedProps.patient_id || '';
        providerIdInput.value = event.extendedProps.provider_id || '';
        startTimeInput.value = event.startStr.slice(0,16);
        endTimeInput.value = event.endStr.slice(0,16);
  
        deleteBtn.style.display = 'inline-block';
        errorMsg.style.display = 'none';
        appointmentModal.show();
      }
    });
  
    calendar.render();
  
    // Fetch appointments from backend API
    async function fetchAppointments(fetchInfo, successCallback, failureCallback) {
        console.log('Fetching appointments from', fetchInfo.startStr, 'to', fetchInfo.endStr);

        try {
        const response = await fetch('/api/appointments?start=' + fetchInfo.startStr + '&end=' + fetchInfo.endStr);
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        console.log('Fetched appointments:', data);
  
        // Convert data to FullCalendar event format
        
        const events = data.map(appt => ({
          id: appt.id.toString(),
          title: `${appt.patient_name} - ${appt.provider_name}`,
          start: appt.start_time,
          end: appt.end_time,
          extendedProps: {
            patient_id: appt.patient_id,
            provider_id: appt.provider_id
          }
        }));

        events: [
            { id: '1', title: 'Test Appt', start: new Date().toISOString(), end: new Date(new Date().getTime() + 3600000).toISOString() }
          ],
  
        successCallback(events);
      } catch (error) {
        console.error('Failed to fetch appointments:', error);
        failureCallback(error);
      }
    }
  
    // Clear modal form fields and error message
    function clearForm() {
      errorMsg.style.display = 'none';
      errorMsg.textContent = '';
      appointmentForm.reset();
    }
  
    // Handle form submit for create/update
    appointmentForm.addEventListener('submit', async function (e) {
      e.preventDefault();
      errorMsg.style.display = 'none';
  
      const id = appointmentIdInput.value;
      const payload = {
        patient_id: patientIdInput.value.trim(),
        provider_id: providerIdInput.value.trim(),
        start_time: startTimeInput.value,
        end_time: endTimeInput.value
      };
  
      if (!payload.patient_id || !payload.provider_id || !payload.start_time || !payload.end_time) {
        errorMsg.textContent = 'All fields are required.';
        errorMsg.style.display = 'block';
        return;
      }
  
      try {
        let url = '/api/appointments';
        let method = 'POST';
        if (id) {
          url += `/${id}`;
          method = 'PUT';
        }
  
        const response = await fetch(url, {
          method,
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
  
        const result = await response.json();
  
        if (!response.ok) {
          errorMsg.textContent = result.error || 'Failed to save appointment.';
          errorMsg.style.display = 'block';
          return;
        }
  
        appointmentModal.hide();
        calendar.refetchEvents();
  
      } catch (error) {
        errorMsg.textContent = 'Network error. Please try again.';
        errorMsg.style.display = 'block';
        console.error(error);
      }
    });
  
    // Handle delete button click
    deleteBtn.addEventListener('click', async function () {
      const id = appointmentIdInput.value;
      if (!id) return;
  
      if (!confirm('Are you sure you want to delete this appointment?')) return;
  
      try {
        const response = await fetch(`/api/appointments/${id}`, { method: 'DELETE' });
        const result = await response.json();
  
        if (result.success) {
          appointmentModal.hide();
          calendar.refetchEvents();
        } else {
          errorMsg.textContent = 'Failed to delete appointment.';
          errorMsg.style.display = 'block';
        }
      } catch (error) {
        errorMsg.textContent = 'Network error. Please try again.';
        errorMsg.style.display = 'block';
        console.error(error);
      }
    });
  });
  