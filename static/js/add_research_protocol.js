fetch('/columns')
    .then(response => response.json())
    .then(sessionList => {
        const tableBody = document.querySelector('#session-table tbody');
        sessionList.forEach(session => {
            const row = document.createElement('tr');
            Object.values(session).forEach(value => {
                const cell = document.createElement('td');
                cell.textContent = value;
                row.appendChild(cell);
            });
            tableBody.appendChild(row);
        });
    });


document.getElementById("add-row").addEventListener("click", function() {
    let table = document.querySelector("table");
    let tbody = table.querySelector("tbody");
    let row = document.createElement("tr");
    row.style.height = "2rem"
    
    
    
    
    i = 0
    while(i<12) {
        let cell = document.createElement("td")
        let select = document.createElement('select')
        let numeric_input = document.createElement('input')
        numeric_input.setAttribute('type', 'number')
        if ( i == 0 ) {
            cell.appendChild(numeric_input)  
        } 
        else if ( i == 1 ) {
            cell.appendChild(numeric_input)   
        }
        else if ( i == 2 ) {
            cell.appendChild(numeric_input)  
        }
       else if ( i == 3 ) {
            cell.appendChild(numeric_input)
        }
        else if (i == 4 ) {
            let drop_down = cell.appendChild(select)

            let option3 = document.createElement('option')
            option3.setAttribute('value', 'day(s)')
            option3.innerHTML = 'Day(s)'
            drop_down.appendChild(option3)

            let option4 = document.createElement('option')
            option4.setAttribute('value', 'week(s)')
            option4.innerHTML = 'Week(s)'
            drop_down.appendChild(option4)

            let option5 = document.createElement('option')
            option5.setAttribute('value', 'month(s)')
            option5.innerHTML = 'Month(s)'
            drop_down.appendChild(option5)

            let option6 = document.createElement('option')
            option6.setAttribute('value', 'year(s)')
            option6.innerHTML = 'Year(s)'
            drop_down.appendChild(option5)

            let option7 = document.createElement('option')
            option7.setAttribute('value', 'repeat')
            option7.innerHTML = 'Repeat'
            drop_down.appendChild(option7)

            let option1 = document.createElement('option')
            option1.setAttribute('value', 'minute(s)')
            option1.innerHTML = 'Minute(s)'
            drop_down.appendChild(option1)

            let option2 = document.createElement('option')
            option2.setAttribute('value', 'hour(s)')
            option2.innerHTML = 'Hour(s)'
            drop_down.appendChild(option2)
        }
        else if ( i == 5 ) {
            let encounter_type_dropdown = cell.appendChild(select)
            let encounter_type_option1 = document.createElement('option')
            encounter_type_option1.setAttribute('value', 'encounter 1 type from database')
            encounter_type_option1.innerHTML = 'encounter 1 Type from Database'
            encounter_type_dropdown.appendChild(encounter_type_option1)

            let encounter_type_option2 = document.createElement('option')
            encounter_type_option2.setAttribute('value', 'encounter 2 type from database')
            encounter_type_option2.innerHTML = 'encounter 2 Type from Database'
            encounter_type_dropdown.appendChild(encounter_type_option2)

            let encounter_type_option3 = document.createElement('option')
            encounter_type_option3.setAttribute('value', 'encounter 3 type from database')
            encounter_type_option3.innerHTML = 'encounter 3 Type from Database'
            encounter_type_dropdown.appendChild(encounter_type_option3)


        }
        else if ( i == 6 ) {
            cell.appendChild(numeric_input)  
        }
        else if ( i == 7 ) {
            cell.appendChild(numeric_input)  
        }

        else if ( i == 8) {
            let duration_drop_down = cell.appendChild(select)
            let duration_option1 = document.createElement('option')
            duration_option1.setAttribute('value', 'minute(s)')
            duration_option1.innerHTML = 'Minute(s)'
            duration_drop_down.appendChild(duration_option1)

            let duration_option2 = document.createElement('option')
            duration_option2.setAttribute('value', 'hour(s)')
            duration_option2.innerHTML = 'Hour(s)'
            duration_drop_down.appendChild(duration_option2)

            let duration_option3 = document.createElement('option')
            duration_option3.setAttribute('value', 'day(s)')
            duration_option3.innerHTML = 'Day(s)'
            duration_drop_down.appendChild(duration_option3)

            let duration_option4 = document.createElement('option')
            duration_option4.setAttribute('value', 'week(s)')
            duration_option4.innerHTML = 'Week(s)'
            duration_drop_down.appendChild(duration_option4)

            let duration_option5 = document.createElement('option')
            duration_option5.setAttribute('value', 'month(s)')
            duration_option5.innerHTML = 'Month(s)'
            duration_drop_down.appendChild(duration_option5)

            let duration_option6 = document.createElement('option')
            duration_option6.setAttribute('value', 'year(s)')
            duration_option6.innerHTML = 'Year(s)'
            duration_drop_down.appendChild(duration_option6)

            let duration_option7 = document.createElement('option')
            duration_option7.setAttribute('value', 'repeat')
            duration_option7.innerHTML = 'Repeat'
            duration_drop_down.appendChild(duration_option7)

        }

        else if (i == 9 ) {
            let provider_type_drop_down = cell.appendChild(select)
            let provider_type_option1 = document.createElement('option')
            provider_type_option1.setAttribute('value', 'provider 1 type from database')
            provider_type_option1.innerHTML = 'Provider 1 Type from Database'
            provider_type_drop_down.appendChild(provider_type_option1)

            let provider_type_option2 = document.createElement('option')
            provider_type_option2.setAttribute('value', 'provider 2 type from database')
            provider_type_option2.innerHTML = 'Provider 2 Type from Database'
            provider_type_drop_down.appendChild(provider_type_option2)

            let provider_type_option3 = document.createElement('option')
            provider_type_option3.setAttribute('value', 'provider 3 type from database')
            provider_type_option3.innerHTML = 'Provider 3 Type from Database'
            provider_type_drop_down.appendChild(provider_type_option3)

        }




        else if (i == 10 ) {
            let provider_drop_down = cell.appendChild(select)
            let provider_option1 = document.createElement('option')
            provider_option1.setAttribute('value', 'provider 1 from database')
            provider_option1.innerHTML = 'Provider 1 from database'
            provider_drop_down.appendChild(provider_option1)

            let provider_option2 = document.createElement('option')
            provider_option2.setAttribute('value', 'provider 2 from database')
            provider_option2.innerHTML = 'Provider 2 from database'
            provider_drop_down.appendChild(provider_option2)

            let provider_option3 = document.createElement('option')
            provider_option3.setAttribute('value', 'provider 3 from database')
            provider_option3.innerHTML = 'Provider 3 from database'
            provider_drop_down.appendChild(provider_option3)

        }

        else if (i == 11 ) {
            let questionnaire_drop_down = cell.appendChild(select)
            let questionnaire_option1 = document.createElement('option')
            questionnaire_option1.setAttribute('value', 'questionnaire 1 from database')
            questionnaire_option1.innerHTML = 'questionnaire 1 from database'
            questionnaire_drop_down.appendChild(questionnaire_option1)

            let questionnaire_option2 = document.createElement('option')
            questionnaire_option2.setAttribute('value', 'questionnaire 2 from database')
            questionnaire_option2.innerHTML = 'questionnaire 2 from database'
            questionnaire_drop_down.appendChild(questionnaire_option2)

            let questionnaire_option3 = document.createElement('option')
            questionnaire_option3.setAttribute('value', 'questionnaire 3 from database')
            questionnaire_option3.innerHTML = 'questionnaire 3 from database'
            questionnaire_drop_down.appendChild(questionnaire_option3)
        }



        row.appendChild(cell)
        tbody.appendChild(row)
        i++
    }

    

    });
    
function hide_submit(e) {
    e.preventEventDefault();
    const protocol_parameters = document.getElementById('protocol_parameters');
    protocol_parameters.style.display = "none"
}