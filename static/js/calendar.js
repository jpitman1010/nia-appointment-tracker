let nav = 0;
let clicked = null;
let events = localStorage.getItem('events') ? JSON.parse(localStorage.getItem('events')) : [];

const calendar = document.getElementById('calendar');
const newEventModal = document.getElementById('newEventModal');
const deleteEventModal = document.getElementById('deleteEventModal');
const backDrop = document.getElementById('modalBackDrop');
const eventTitleInput = document.getElementById('eventTitleInput');
const weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];



//smaller calendar functions

// (function (root, factory) {
//   root.myCalendar = factory(root);
// })(this, (root) => {
//   let monthList = new Array(
//     "january",
//     "february",
//     "march",
//     "april",
//     "may",
//     "june",
//     "july",
//     "august",
//     "september",
//     "october",
//     "november",
//     "december"
//   );
//   let dayList = new Array(
//     "sunday",
//     "monday",
//     "tuesday",
//     "wednesday",
//     "thursday",
//     "friday",
//     "saturday"
//   );
//   let today = new Date();
//   today.setHours(0, 0, 0, 0);
//   let privateVar = "No, No, No...";

//   let init = () => {
//     let element = document.getElementById("calendar");

//     let currentMonth = new Date(today.getFullYear(), today.getMonth(), 1);

//     // Creating the div for our calendar's header
//     let header = document.createElement("div");
//     header.classList.add("header");
//     element.appendChild(header);

//     // Creating the div that will contain the days of our calendar
//     let content = document.createElement("div");
//     element.appendChild(content);

//     // Our "previous" button
//     let previousButton = document.createElement("button");
//     previousButton.setAttribute("data-action", "-1");
//     previousButton.textContent = "\u003c";
//     header.appendChild(previousButton);

//     // Creating the div that will contain the actual month/year
//     let monthDiv = document.createElement("div");
//     monthDiv.classList.add("month");
//     header.appendChild(monthDiv);

//     // Our "next" button
//     let nextButton = document.createElement("button");
//     nextButton.setAttribute("data-action", "1");
//     nextButton.textContent = "\u003e";
//     header.appendChild(nextButton);

//     // Next/previous button functionality
//     element.querySelectorAll("button").forEach((element) => {
//       element.addEventListener("click", () => {
//         console.log(element.getAttribute("data-action"));
//         currentMonth.setMonth(
//           currentMonth.getMonth() * 1 +
//             parseInt(element.getAttribute("data-action")) * 1
//         );
//         loadMonth(currentMonth, content, monthDiv);
//       });
//     });

//     // Load current month
//     loadMonth(currentMonth, content, monthDiv);
//   };

//   let createDaysNamesCells = (content) => {
//     for (let i = 0; i < dayList.length; i++) {
//       let cell = document.createElement("span");
//       cell.classList.add("cell");
//       cell.classList.add("day");
//       cell.textContent = dayList[i].substring(0, 3).toUpperCase();
//       content.appendChild(cell);
//     }
//   };

//   let createEmptyCellsIfNecessary = (content, date) => {
//     for (let i = 0; i < date.getDay(); i++) {
//       let cell = document.createElement("span");
//       cell.classList.add("cell");
//       cell.classList.add("empty");
//       content.appendChild(cell);
//     }
//   };

//   let loadMonth = (date, content, monthDiv) => {
//     // Empty the calendar
//     content.textContent = "";

//     // Adding the month/year displayed
//     monthDiv.textContent =
//       monthList[date.getMonth()].toUpperCase() + " " + date.getFullYear();

//     // Creating the cells containing the days of the week
//     createDaysNamesCells(content);

//     // Creating empty cells if necessary
//     createEmptyCellsIfNecessary(content, date);

//     // Number of days in the current month
//     let monthLength = new Date(
//       date.getFullYear(),
//       date.getMonth() + 1,
//       0
//     ).getDate();

//     // Creating the cells containing current's month's days
//     for (let i = 1; i <= monthLength; i++) {
//       let cell = document.createElement("span");
//       cell.classList.add("cell");
//       cell.textContent = `${i}`;
//       content.appendChild(cell);

//       // Cell's timestamp
//       let timestamp = new Date(
//         date.getFullYear(),
//         date.getMonth(),
//         i
//       ).getTime();
//       cell.addEventListener("click", () => {
//         console.log(timestamp);
//         console.log(new Date(timestamp));

//         document.querySelector(".cell.today")?.classList.remove("today");
//         cell.classList.add("today");
//       });

//       // Add a special class for today
//       if (timestamp === today.getTime()) {
//         cell.classList.add("today");
//       }
//     }
//   };
//   return {
//     init,
//   };
// });









// larger calendar functions

function openModal(date) {
  clicked = date;

  const eventForDay = events.find(e => e.date === clicked);

  if (eventForDay) {
    document.getElementById('eventText').innerText = eventForDay.title;
    deleteEventModal.style.display = 'block';
  } else {
    newEventModal.style.display = 'block';
  }

  backDrop.style.display = 'block';
}

function load() {
  const dt = new Date();

  if (nav !== 0) {
    dt.setMonth(new Date().getMonth() + nav);
  }

  const day = dt.getDate();
  const month = dt.getMonth();
  const year = dt.getFullYear();

  const firstDayOfMonth = new Date(year, month, 1);
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  
  const dateString = firstDayOfMonth.toLocaleDateString('en-us', {
    weekday: 'long',
    year: 'numeric',
    month: 'numeric',
    day: 'numeric',
  });
  const paddingDays = weekdays.indexOf(dateString.split(', ')[0]);

  document.getElementById('monthDisplay').innerText = 
    `${dt.toLocaleDateString('en-us', { month: 'long' })} ${year}`;

  calendar.innerHTML = '';

  for(let i = 1; i <= paddingDays + daysInMonth; i++) {
    const daySquare = document.createElement('div');
    daySquare.classList.add('day');

    const dayString = `${month + 1}/${i - paddingDays}/${year}`;

    if (i > paddingDays) {
      daySquare.innerText = i - paddingDays;
      const eventForDay = events.find(e => e.date === dayString);

      if (i - paddingDays === day && nav === 0) {
        daySquare.id = 'currentDay';
      }

      if (eventForDay) {
        const eventDiv = document.createElement('div');
        eventDiv.classList.add('event');
        eventDiv.innerText = eventForDay.title;
        daySquare.appendChild(eventDiv);
      }

      daySquare.addEventListener('click', () => openModal(dayString));
    } else {
      daySquare.classList.add('padding');
    }

    calendar.appendChild(daySquare);    
  }
}

function closeModal() {
  eventTitleInput.classList.remove('error');
  newEventModal.style.display = 'none';
  deleteEventModal.style.display = 'none';
  backDrop.style.display = 'none';
  eventTitleInput.value = '';
  clicked = null;
  load();
}

function saveEvent() {
  if (eventTitleInput.value) {
    eventTitleInput.classList.remove('error');

    events.push({
      date: clicked,
      title: eventTitleInput.value,
    });

    localStorage.setItem('events', JSON.stringify(events));
    closeModal();
  } else {
    eventTitleInput.classList.add('error');
  }
}

function deleteEvent() {
  events = events.filter(e => e.date !== clicked);
  localStorage.setItem('events', JSON.stringify(events));
  closeModal();
}

function initButtons() {
  document.getElementById('nextButton').addEventListener('click', () => {
    nav++;
    load();
  });

  document.getElementById('backButton').addEventListener('click', () => {
    nav--;
    load();
  });

  document.getElementById('saveButton').addEventListener('click', saveEvent);
  document.getElementById('cancelButton').addEventListener('click', closeModal);
  document.getElementById('deleteButton').addEventListener('click', deleteEvent);
  document.getElementById('closeButton').addEventListener('click', closeModal);
}

initButtons();
load();