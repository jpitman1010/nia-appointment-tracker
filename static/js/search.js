const patient_card_template = document.querySelector("[data-user-template]");
const patient_card_container = document.querySelector("[data-user-cards-container]");
const searchInput = document.querySelector("[data-search]");
const searchForm = document.getElementById("search_form");
const submit_button = document.getElementById("submit-form");
const header = document.getElementById('card-header');


function submitForm(id) {
    console.log('id ==' , id)
    const mrn = id[0].id;
    console.log('mrn = ', mrn);
    const formData = {'mrn': mrn};
    
    const search_form = document.getElementById('form-'+mrn)

    $.ajax({
                type: 'POST',
                url: '/search',
                data: JSON.stringify(formData),
                contentType: "application/json"
            }).done(function (response) {
                window.rel; 
            });



//     search_form.submit(function(e){
//         e.preventDefault();
//         let form = $(this);
//         let actionUrl = form.attr('action');
  
//     $.ajax({
//         type: 'POST',
//         url: actionUrl,
//         data: formData,
//     }).done(function (data) {
//         alert(formData);
//     });
// });
    // document.getElementById('form-'+mrn).submit( );
}





let patients = []

searchInput.addEventListener("input", (e) => {
    const value = e.target.value.toLowerCase();
    patients.forEach(patient => {
        patient.MRN = String(patient.MRN);
        const isVisible =
            patient.fname.toLowerCase().includes(value) || patient.lname.toLowerCase().includes(value) ||
            patient.MRN.includes(value) || patient.dob.includes(value);
        patient.element.classList.toggle("hide", !isVisible);
    })
})

let fake_patient_list = []
let fname_list = ['Melissa', 'Veronica', 'Audrey', 'Sophie', 'Zenaida', 'Beverly', 'Kenneth', 'Clark', 'Dawn', 'Starla', 'Cory', 'Sally', 'Richard', 'Deborah', 'Alice', 'Mary', 'Manuel', 'Kimberly', 'Charlene', 'Phillip', 'Maria', 'Elizabeth', 'Norman', 'James', 'Rita', 'Harold', 'Cindy', 'Jaqueline', 'Lu', 'James', 'Glen', 'Laurie', 'Billy', 'Kelly', 'Efrain', 'Catherine', 'Sylvia', 'John', 'David', 'Yan', 'Andrew', 'Ashley', 'Aaron', 'Maryann', 'Angela', 'Freddie', 'David', 'Shanna', 'Peter', 'Robert', 'Lula', 'Alice', 'Elizabeth', 'Thomas', 'Mike', 'Kathy', 'Christopher', 'Etta', 'Billy', 'Royce', 'Linda', 'Yolanda', 'Jeanette', 'Anna', 'Leonard', 'Ryan', 'Audrey', 'Nancy', 'Luther', 'Joan', 'John', 'Mary', 'Robbie', 'Gilbert', 'Jim', 'Alan', 'Richard', 'Joyce', 'Robert', 'Billy', 'Ella', 'Jeanette', 'Gregorio', 'Elizabeth', 'Jaime', 'Tom', 'William', 'Jane', 'Lorena', 'Rebecca', 'Dawn', 'Denise', 'Wilma', 'Andrew', 'Miguel', 'Santiago', 'Nicole', 'Richard', 'Angela', 'Melba']
let lname_list = ['Paul', 'Melvin', 'Rosie', 'Howard', 'Angela', 'David', 'Gordon', 'Kimberly', 'Joan', 'Jacqueline', 'Emma', 'Henry', 'Dorothy', 'Van', 'Ryan', 'Griselda', 'Edwin', 'Meghan', 'Larry', 'Norma', 'Cheryl', 'William', 'Dedra', 'Eva', 'James', 'Barbara', 'Carlton', 'Brenda', 'Marco', 'Manuel', 'Susan', 'Roger', 'Dale', 'Gregory', 'James', 'Dale', 'Rhonda', 'Herbert', 'Holly', 'Paul', 'Cierra', 'Elizabeth', 'Joseph', 'Lisa', 'Melissa', 'Ron', 'Leonard', 'Jade', 'Lyle', 'Carl', 'Anthony', 'Jennifer', 'Bobby', 'Karen', 'Henry', 'Mark', 'Robert', 'Dorothy', 'Judith', 'Michele', 'Terry', 'Ivan', 'James', 'Mary', 'Brenda', 'Adriana', 'Leonard', 'Alice', 'John', 'Dorothy', 'Lindsey', 'Sharon', 'Kimberly', 'Patrick', 'Karen', 'Marsha', 'Amanda', 'Stormy', 'Craig', 'Daniel', 'Taylor', 'Kenneth', 'Lindsey', 'Claudia', 'Jeffrey', 'Ivan', 'Amanda', 'James', 'Jeffrey', 'Lynne', 'Charles', 'Gary', 'Daniel', 'Winifred', 'Jessica', 'Kenneth', 'Kristen', 'Edward', 'William', 'Charles']
let mrn_list = [20215489946, 20219242776, 20214231315, 20220729000, 20214441622, 20221792979, 20215810864, 20203005341, 20213765783, 20223534843, 20222620062, 20225989713, 20226895725, 20217639661, 20202690635, 20217284214, 20216141364, 20206423809, 20229921466, 20210153614, 20217095954, 20201406120, 20202658157, 20224442290, 20217004993, 20219661069, 20208671509, 20215142327, 20211592027, 20223591236, 20220621788, 20213650131, 20219772135, 20201535794, 20208690900, 20228681344, 20206984140, 20209668487, 20223046812, 20211994180, 20220423979, 20205113970, 20221338699, 20213642273, 20219104514, 20223540277, 20220215519, 20211331543, 20220999124, 20203391804, 20207136851, 20200690069, 20221107085, 20226227465, 20207587366, 20214924313, 20213464207, 20228731189, 20210301697, 20223542015, 20227845546, 20207364060, 20201474099, 20200585997, 20226922625, 20220691623, 20220923860, 20219071014, 20227787175, 20219891532, 20201439290, 20217648195, 20210080377, 20200163162, 20207169740, 20209584574, 20208361028, 20201358594, 20206835834, 20221657327, 20214668649, 20221594570, 20200847180, 20210485018, 20225770956, 20225083856, 20224175771, 20216835090, 20221969355, 20209476309, 20202215459, 20204301624, 20221249449, 20200628424, 20227697952, 20211898174, 20213068068, 20202710931, 20227167620, 20214716221];
let dob_list = ['1989/3/21', '1982/8/25', '1994/9/19', '1990/6/23', '1957/5/13', '1956/9/12', '1977/2/16', '1952/7/13', '2003/7/29', '1941/3/26', '1945/2/28', '2020/7/3', '1940/7/20', '1946/11/17', '1993/6/6', '1984/3/21', '1997/5/25', '2020/10/10', '2006/1/17', '1988/8/2', '1992/1/8', '1942/2/19', '1988/6/27', '1955/3/10', '1946/10/23', '1956/1/5', '2008/9/19', '1988/5/16', '1950/3/18', '2012/4/4', '1946/11/17', '2007/3/20', '1995/2/4', '1982/5/13', '1952/6/4', '1976/10/27', '1957/10/1', '2006/9/8', '2000/4/3', '2010/1/3', '1964/2/8', '1976/7/29', '1956/7/17', '1987/2/27', '2020/3/8', '2018/6/10', '1945/11/20', '1985/12/20', '1964/5/14', '2010/4/8', '2015/8/13', '1988/10/20', '1981/7/1', '1994/5/12', '2012/10/23', '2011/3/16', '1993/8/5', '1988/7/23', '2016/1/30', '2007/11/16', '1951/12/15', '1989/7/10', '1967/3/12', '2018/11/25', '1963/2/18', '1970/4/30', '2019/10/5', '1976/1/30', '2019/7/3', '1957/5/16', '1979/10/22', '1982/12/12', '1964/3/2', '1968/5/11', '2014/8/11', '2010/8/18', '1963/10/10', '1951/6/25', '1947/12/17', '1986/7/19', '2013/8/21', '1954/4/23', '1981/6/20', '1952/7/16', '1982/10/12', '2000/1/17', '2015/9/20', '1987/9/13', '1972/7/3', '1940/10/9', '1983/3/24', '2022/1/28', '1985/8/26', '2019/7/3', '1964/9/11', '2005/1/30', '2020/6/26', '2022/3/11', '1974/5/23', '1945/12/15']

function fname_generator() {
    let fname = fname_list[Math.floor(Math.random() * fname_list.length)];
    return fname
}

function lname_generator() {
    let lname = lname_list[Math.floor(Math.random() * lname_list.length)];
    return lname
}

function mrn_generator() {
    let mrn = mrn_list[Math.floor(Math.random() * mrn_list.length)];
    return mrn
}

function dob_generator() {
    let dob = dob_list[Math.floor(Math.random() * dob_list.length)];
    return dob
}

function generate_patient_list() {
    let i = 0
    while (i < 100) {
        let patient_card = {
            "MRN": mrn_generator(),
            "dob": dob_generator(),
            "fname": fname_generator(),
            "lname": lname_generator()
        }
        fake_patient_list.push(patient_card)
        i++
    }
}

generate_patient_list();

patients = fake_patient_list.map(patient => {
    const card = patient_card_template.content.cloneNode(true).children[0];
    const header = card.querySelector('[data-header]');
    const dob = card.querySelector('[data-dob]');
    const fname = card.querySelector('[data-fname]');
    const lname = card.querySelector('[data-lname]');
    const form = card.querySelector('[data-form');
    const mrn = patient.MRN
    // const button = document.getElementsByClassName('submit-button')
    
    
    header.textContent = String(patient.MRN);
    card.id = mrn;
    dob.id = 'dob-' + mrn;
    form.id = 'form-' + mrn;
    fname.id = 'fname-' + mrn;
    lname.id = 'lname-' + mrn;
    // button.id = 'button-' + mrn;



    dob.textContent = patient.dob;
    fname.textContent = patient.fname;
    lname.textContent = patient.lname;

    
    patient_card_container.append(card);

    return {
        MRN: patient.MRN,
        fname: patient.fname,
        lname: patient.lname,
        dob: patient.dob,
        element: card
    }

});

