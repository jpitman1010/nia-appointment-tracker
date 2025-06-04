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
    }

    submit = () => {

        console.log('submitted')

    }

    currentInput = () => this.form[this.step - 1].input;

    previousInput = () => this.form[this.step - 2].input;




    check = () => {
        const selection = document.getElementById('protocol_type')
        console.log('check() checking selection ===', this.selection)
        if(this.currentInput().id === 'yes_no'){
            console.log('made it into the first if statement of the check() fcn')
            if (selection.value[0] === "Yes" || selection.value[0] ==="No") {
                selection.addEventListener('change', () => {
                this.currentInput().classListremove('invalid');
                this.setListeners();
                document.getElementById("next-button").disabled = false;
                })
            }
        } else {
            this.currentInput().addEventListener('keyup', this.enableDisable)
        }
    }

    enableDisable = () => {
        if (this.valid(this.currentInput())) {
            this.currentInput().classList.remove('invalid');
            this.setListeners();
            document.getElementById("next-button").disabled = false;
        } else {
            this.currentInput().classList.add('invalid');
            this.removeListeners();
            document.getElementById("next-button").disabled = true;
        }
    }

    valid = (input) => {
        const formType = input.id;
        console.log('formType = id =', formType);
        const inputValue = input.value;
        const empty = (str) => !str.split('').every(_char => _char !== ' ');
        let yes_no = document.getElementById('yes_no').value;

        if (!inputValue || empty(inputValue)) return false;

        switch (formType) {
            // use reg expression to check that there are letters, an @ symbol, a '.' and some more letters;
            case formType:
                return (/^[A-Za-z]+$/).test(inputValue);
            case yes_no:
                return "yes" || "no".test(yes_no)
            case "protocol_name_input":
                return (/^[A-Za-z]+[#\$\^]?$/).test(inputValue)

            default:
                return false;
        }


    }

    goback = () => {
        if (this.step > 1) {
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
        if (this.step <= this.form.length) {
            this.displayStep();
            this.removeListeners();
            document.getElementById('next-button').disabled = true;
            this.check();
        } else
            document.getElementById('next-button').type = 'submit'
        this.submit();
    }

    displayStep = () => {
        if (this.currentGroup)
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