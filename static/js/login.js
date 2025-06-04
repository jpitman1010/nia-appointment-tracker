class Appform {
    constructor() {
        this.form = [];
        this.step = 0;
        this.currentGroup = null;

        this.setListeners();
        this.getForm();
        document.getElementById("next-button").disabled = true;
        this.refresh();
        this.check();
        this.pageType = window.location.href.includes('login') ? 'login' : 'staff_registration'
    } 

    submit = () => {

        console.log('submitted')
        // const submitButton = document.getElementById('next-button')
        // console.log(this.form['input'])
        // submitButton.addEventListener('click', () => {

        // let formdata = new FormData();
        // url = this.form.attr('action');


        // const user_email = document.getElementById('email-input').value;
        // const user_password = document.getElementById('password-input').value;
        // formdata.append(user_email)
        // formdata.append(user_password)
        // if(this.pageType != 'login'){ 
        //     const user_fname = document.getElementById('fname-input').value;
        //     const user_lname = document.getElementById('lname-input').value;
        //     const user_role = document.getElementById('role-input').value;
        //     formdata.append(user_fname)
        //     formdata.append(user_lname)
        //     formdata.append(user_role)
        // }
        // console.log(this.getForm())
        // console.log(formdata)

        //     $.ajax({
        //         url: url,
        //         type:'POST',
        //         data: this.inputValues,
        //         success: function(){
        //           alert("Form Data Submitted :)")
        //         },
        //         error: function(e){
        //           alert("There was an error :(")
        //         }
        //     });
        // })


       
    }

    currentInput = () => this.form[this.step -1].input;

    previousInput = () => this.form[this.step-2].input;

    
   

    check = () => {
        this.currentInput().addEventListener('keyup', this.enableDisable) 
    }

    enableDisable = () => {
        if(this.valid(this.currentInput())) {
            this.currentInput().classList.remove('invalid');
            this.setListeners();
            document.getElementById("next-button").disabled = false;
        } 
        else {
            this.currentInput().classList.add('invalid');
            this.removeListeners();
            document.getElementById("next-button").disabled = true;
        }
    }

    valid = (input) => {
        const formType = input.id;
        const value = input.value;
        const empty = (str) =>  !str.split('').every(_char => _char !== ' ');
    

        if(!value || empty(value)) return false;

        if(this.pageType === 'login') return value && !empty(value);

        switch(formType) {

            // use reg expression to check that there are letters, an @ symbol, a '.' and some more letters;
            case 'email-input': return /\S+@\S+\.\S+/.test(value);

            case 'email-verification-input':return this.previousInput().value === value;
            console.log(this.previousInput().value);
            console.log(value);
            // use reg expression to check to ensure there is at least 1 digit, 1 upper-case, 1 lower-case and length >=8  AND allowed symbols;
            case 'password-input': return /(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[a-zA-Z0-9@$&!]{8,}/.test(value);

            case 'password-verification-input': return this.previousInput().value === value;            

            case 'fname-input': return (/^[A-Za-z]+$/).test(value);

            case 'lname-input': return (/^[A-Za-z]+$/).test(value);
            
            case 'role-input':  return true


            default: return false;
        }

    }

    goback = () => {
        if(this.step > 1) {
            this.step--;
            this.displayStep();
            this.enableDisable();
        }
    }
    
    refresh = () => {
        console.log(this.step)
        console.log(this)
        console.log(this.form)
        this.step++;
        if(this.step <= this.form.length) {
            this.displayStep();
            this.removeListeners();
            document.getElementById('next-button').disabled = true;
            this.check();
        }
        else
            document.getElementById('next-button').type = 'submit'
            this.submit();
    }

    displayStep = () => {
        if(this.currentGroup)
            this.currentGroup.style.display = "none";
        this.currentGroup = this.form.find(_group => _group.step === this.step).element;
        this.currentGroup.style.display = "block";
    }


    getForm = () => {
        const groups = Array.from(document.getElementsByClassName('form-group'));
        groups.forEach(_group => {
            const children = Array.from(_group.children);
            this.form.push({
                'step': Number.parseInt(_group.dataset.step),
                'element': _group,
                'input': children.find(_el => _el.nodeName === "INPUT")
             });
        });
    }

    setListeners = () => {
        document.getElementById("next-button").addEventListener('click', this.refresh);
        document.getElementById("back-button").addEventListener('click', this.goback);

    }

    removeListeners = () => {
        document.getElementById("next-button").removeEventListener('click', this.refresh);
    }
        
    
}

new Appform();