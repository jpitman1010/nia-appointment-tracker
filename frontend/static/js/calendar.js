
window.onload = function() {
  const calendarEl = document.getElementById('calendar');
  
  if (!calendarEl) {
    console.error('Calendar container not found!');
    return;
  }

  let appointmentModal;
  function getModal() {
    if (!appointmentModal) {
      appointmentModal = new bootstrap.Modal(document.getElementById('appointmentModal'));
    }
    return appointmentModal;
  }

  
  // const appointmentModal = new bootstrap.Modal(document.getElementById('appointmentModal'));
  const appointmentForm = document.getElementById('appointmentForm');
  const errorMsg = document.getElementById('errorMsg');
  const deleteBtn = document.getElementById('deleteBtn');
  const saveBtn = document.getElementById('saveBtn');

  // Modal inputs
  const appointmentIdInput = document.getElementById('appointmentId');
  const patientIdInput = document.getElementById('patientId');
  const providerIdInput = document.getElementById('providerId');
  const startTimeInput = document.getElementById('startTime');
  const endTimeInput = document.getElementById('endTime');

  // Initialize FullCalendar without plugins array (using global min builds)
  // Assign calendar globally to window so you can call updateSize() from other scripts
  window.calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'timeGridWeek', // default to week view
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,timeGridWeek,timeGridDay,listWeek'
    },
    slotDuration: '00:30:00',
    slotLabelInterval: '00:30:00',
    slotMinTime: '07:00:00',
    slotMaxTime: '19:00:00',
    nowIndicator: true,
    editable: false,
    selectable: true,
    selectMirror: true,
    events: fetchAppointments,

    // On selecting time slot
    select: function (info) {
      console.log('select fired', info);
      clearForm();
      // populate form inputs
      appointmentIdInput.value = '';
      patientIdInput.value = '';
      providerIdInput.value = '';
      startTimeInput.value = info.startStr.slice(0, 16);
      endTimeInput.value = info.endStr.slice(0, 16);
      deleteBtn.style.display = 'none';
      errorMsg.classList.add('d-none');
      // appointmentModal.show();
      getModal().show();

    },

    // On clicking existing event
    eventClick: function (info) {
      console.log('eventClick fired', info.event);
      clearForm();
      const event = info.event;
      appointmentIdInput.value = event.id;
      patientIdInput.value = event.extendedProps.patient_id || '';
      providerIdInput.value = event.extendedProps.provider_id || '';
      startTimeInput.value = event.startStr.slice(0, 16);
      endTimeInput.value = event.endStr.slice(0, 16);
      deleteBtn.style.display = 'inline-block';
      errorMsg.classList.add('d-none');
      getModal().show();
      // appointmentModal.show();
    }
  });
  console.log('FullCalendar initialized:', window.calendar);

  calendar.render();

  // --- New addition for tab resize update ---
  // Listen for Bootstrap tab shown event to trigger calendar resize
  document.querySelectorAll('a[data-bs-toggle="tab"]').forEach(tab => {
    tab.addEventListener('shown.bs.tab', function (event) {
      const targetTab = event.target.getAttribute('href');
      // Replace '#calendar-tab' with your calendar tab pane ID if different
      if (targetTab === '#calendar-tab' || targetTab === '#calendar') {
        if (window.calendar) {
          window.calendar.updateSize();
        }
      }
    });
  });

  // Fetch appointments API
  async function fetchAppointments(fetchInfo, successCallback, failureCallback) {
    try {
      const url = `/api/appointments?start=${fetchInfo.startStr}&end=${fetchInfo.endStr}`;
      const response = await fetch(url);
      if (!response.ok) throw new Error('Network response was not ok');
      const data = await response.json();

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

      successCallback(events);
    } catch (error) {
      console.error('Failed to fetch appointments:', error);
      failureCallback(error);
    }
  }

  // Clear form inputs and errors
  function clearForm() {
    errorMsg.classList.add('d-none');
    errorMsg.textContent = '';
    appointmentForm.reset();
  }

  // Form submit handler: create or update appointment
  appointmentForm.addEventListener('submit', async function (e) {
    e.preventDefault();
    errorMsg.classList.add('d-none');

    const id = appointmentIdInput.value;
    const payload = {
      patient_id: patientIdInput.value.trim(),
      provider_id: providerIdInput.value.trim(),
      start_time: startTimeInput.value,
      end_time: endTimeInput.value
    };

    if (!payload.patient_id || !payload.provider_id || !payload.start_time || !payload.end_time) {
      errorMsg.textContent = 'All fields are required.';
      errorMsg.classList.remove('d-none');
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
        errorMsg.classList.remove('d-none');
        return;
      }

      appointmentModal.hide();
      calendar.refetchEvents();

    } catch (error) {
      errorMsg.textContent = 'Network error. Please try again.';
      errorMsg.classList.remove('d-none');
      console.error(error);
    }
  });

    // Delete button handler
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
          errorMsg.classList.remove('d-none');
        }
      } catch (error) {
        errorMsg.textContent = 'Network error. Please try again.';
        errorMsg.classList.remove('d-none');
        console.error(error);
      };
    });
};