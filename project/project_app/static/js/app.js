function validatePostCode(postCode){
  const postCodeList = postCode.split('-');
  if (postCodeList.length === 2){
    if (postCodeList[0].length !== 2 || postCodeList[1].length !== 3){
      return false;
    } else {
      for (let i=0; i<postCodeList[0].length; i++){
        if (isNaN(postCodeList[0][i])){
          return false;
        }
      }
      for (let i=0; i<postCodeList[1].length; i++){
        if (isNaN(postCodeList[1][i])){
          return false;
        }
      }
      return true;
    }
  } else {
    return false;
  }
}
function validatePhone(phone){
  if (phone.length === 9){
      for (let i=0; i<phone.length; i++){
        if (isNaN(phone[i])){
          return false;
        }
      }
      return true;
  } else {
    return false;
  }
}

function validateDate(myDate, myDateMin){
  const myDateList = myDate.split('-');
  const myDateMinList = myDateMin.split('-');
  if (myDateList.length < 3){
    return false;
  }
  if (myDateList[0].length > 4){
    return false;
  }
  for (let i=0; i<3; i++){
    if(myDateList[i] < myDateMinList[i]){
      return false;
    }
  }
  return true;
}


document.addEventListener("DOMContentLoaded", function() {
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
      const myPaginator = e.target.parentElement.parentElement;
      const myList = myPaginator.children;
      for (let i=0; i<myList.length; i++){
        myList[i].firstElementChild.classList.remove('active');
      };
      const page = e.target.dataset.page;
      const institution= e.target.dataset.institution;

      fetch('' + `?institution=${institution}&page=${page}`, {
                    method: 'GET',
                })
                .then(async (response) => {
                    return await response.json();
                })
                .then(data => {
                    e.target.classList.add('active');
                    const myInstitutionList = e.target.parentElement.parentElement.previousElementSibling;
                    const myInstitution = myInstitutionList.children[0].cloneNode(true);
                    for (let i=myInstitutionList.children.length; i>0; i--){
                      myInstitutionList.removeChild(myInstitutionList.children[i-1]);
                    };
                    data.forEach(function (element){
                      const myNewInstitution = myInstitution.cloneNode(true);
                      myNewInstitution.firstElementChild.firstElementChild.innerText = element.name;
                      myNewInstitution.firstElementChild.lastElementChild.innerText = element.description;
                      myNewInstitution.lastElementChild.firstElementChild.innerText = element.categories;
                      e.target.parentElement.parentElement.previousElementSibling.appendChild(myNewInstitution);
                    })
                })
                .catch(e => console.error('Błąd' + e));
    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.$formSteps = this.$form.children[1].children[1];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep++;
          this.updateForm();
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          if (this.currentStep > 1){
            this.currentStep--;
          };
          this.updateForm();
        });
      });

      // Form submit
      this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;

      if (this.currentStep == 1){

        const myStep = this.$formSteps.children[0];
        const myPrevButton = myStep.lastElementChild.firstElementChild;
        myPrevButton.addEventListener('click', function (){
          window.location = '/';
        })
        const myNextButton = myStep.lastElementChild.lastElementChild;
        let myCategoriesCounter = 0;
        const myCategories = document.querySelectorAll('input[name=categories]');
        myCategories.forEach(function (element){
          if (element.checked){
            myCategoriesCounter += 1;
          }
        });
        if (myCategoriesCounter < 1){
          myNextButton.style.display = 'None';
        }
        myCategories.forEach(function (element){
          element.addEventListener('change', function (event){
            if (element.checked){
              myCategoriesCounter += 1;
            } else {
              myCategoriesCounter -= 1;
            }
            if (myCategoriesCounter > 0){
              myNextButton.style.display = 'block';
            } else {
              myNextButton.style.display = 'None';
            }
          });
        })
      }

      if (this.currentStep == 2){

        const myStep = this.$formSteps.children[1];
        const myNextButton = myStep.lastElementChild.lastElementChild;
        const myBags = document.querySelector('input[name=bags]');
        if (myBags.value === ''){
          myNextButton.style.display = 'None';
        }
        myBags.addEventListener('input', function (event){
          if (myBags.value !== ''){
            myNextButton.style.display = 'block';
          } else {
            myNextButton.style.display = 'None';
          }
        });
      }

      if (this.currentStep == 3){

        const myStep = this.$formSteps.children[2];
        const myNextButton = myStep.lastElementChild.lastElementChild;
        myNextButton.style.display = 'None';
        const myCategoriesList = [];
        const myInstitutionsActive = [];
        const myCategories = document.querySelectorAll('input[name=categories]');
        myCategories.forEach(function (element){
          if (element.checked){
            myCategoriesList.push(element.value);
          }
        });
        const myInstitutions = document.querySelectorAll('input[name=organization]');
        myInstitutions.forEach(function (institution){
          institution.parentElement.parentElement.style.display = 'block';
          const myInstitutionsCategories = institution.dataset.categories;
          const myInstitutionsCategoriesList = myInstitutionsCategories.split(',');
          let i = 0;
          myCategoriesList.forEach(function (category){
            myInstitutionsCategoriesList.forEach(function (category2){
              if (category === category2){
                i += 1;
              }
            })
          })
          if (i === myCategoriesList.length){
            myInstitutionsActive.push(institution);
            institution.parentElement.parentElement.style.display = 'block';
            if (institution.checked){
              myNextButton.style.display = 'block';
            }
          } else {
            institution.parentElement.parentElement.style.display = 'None';
          }
        });
        if (myInstitutionsActive.length === 0){
          myStep.children[1].style.display = 'block';
        } else {
          myStep.children[1].style.display = 'None';
        }
        myInstitutionsActive.forEach(function (element){
          element.addEventListener('change', function (event){
            if (element.checked){
              myNextButton.style.display = 'block';
            }
          });
        })
      }

      if (this.currentStep == 4){

        const myList = [];
        const myStep = this.$formSteps.children[3];
        const myNextButton = myStep.lastElementChild.lastElementChild;
        const myInputs = myStep.querySelectorAll('input');
        for (let i=0; i<myInputs.length; i++){
          if (myInputs[i].value === ''){
            myList.push(false);
            myNextButton.style.display = 'None';
          } else {
            myList.push(true);
          }
        }
        for (let i=0; i<myInputs.length; i++){
          myInputs[i].addEventListener('input', function (e){
            if (this.name === 'postcode'){
              if (validatePostCode(this.value)){
                myList[i] = true;
                this.parentElement.classList.remove('danger');
              } else {
                myList[i] = false;
                this.parentElement.classList.add('danger');
              }
            }
            else if (this.name === 'phone'){
              if (validatePhone(this.value)){
                myList[i] = true;
                this.parentElement.classList.remove('danger');
              } else {
                myList[i] = false;
                this.parentElement.classList.add('danger');
              }
            }
            else if (this.name === 'data'){
              if (validateDate(this.value, this.min)){
                myList[i] = true;
                this.parentElement.classList.remove('danger');
              } else {
                myList[i] = false;
                this.parentElement.classList.add('danger');
              }
            }
            else {
              if (this.value !== ''){
                myList[i] = true;
              } else {
                myList[i] = false;
              }
            }
            const myFlag = myList.every(function (element){
              return element === true;
            })
            if (myFlag){
              myNextButton.style.display = 'block';
            } else {
              myNextButton.style.display = 'None';
            }
          })
        }
      }

      if (this.currentStep == 5){

        const mySummaryElement = document.querySelector('.summary');
        const myCategoriesList = [];
        const myCategories = document.querySelectorAll('input[name=categories]');
        myCategories.forEach(function (element){
          if (element.checked){
            myCategoriesList.push(element.parentElement.lastElementChild.innerHTML)
          }
        });
        mySummaryElement.firstElementChild.lastElementChild.firstElementChild.children[3].innerHTML = myCategoriesList.join(', ');

        const myBags = document.querySelector('input[name=bags]').value;
        mySummaryElement.firstElementChild.lastElementChild.firstElementChild.children[1].innerHTML = `Liczba worków: ${myBags}`;

        let myInstitution = '';
        const myInstitutions = document.querySelectorAll('input[name=organization]');
        myInstitutions.forEach(function (element){
          if (element.checked){
            myInstitution = element.parentElement.lastElementChild.firstElementChild.innerHTML;
          }
        });
        mySummaryElement.firstElementChild.lastElementChild.lastElementChild.lastElementChild.innerHTML = `Dla - ${myInstitution}`;

        const myAddress = document.querySelector('input[name=address]').value;
        mySummaryElement.lastElementChild.firstElementChild.lastElementChild.children[0].innerHTML = myAddress;

        const myCity = document.querySelector('input[name=city]').value;
        mySummaryElement.lastElementChild.firstElementChild.lastElementChild.children[1].innerHTML = myCity;

        const myPostCode = document.querySelector('input[name=postcode]').value;
        mySummaryElement.lastElementChild.firstElementChild.lastElementChild.children[2].innerHTML = myPostCode;

        const myPhone = document.querySelector('input[name=phone]').value;
        mySummaryElement.lastElementChild.firstElementChild.lastElementChild.children[3].innerHTML = myPhone;

        const myDate = document.querySelector('input[name=data]').value;
        mySummaryElement.lastElementChild.lastElementChild.lastElementChild.children[0].innerHTML = myDate;

        const myTime = document.querySelector('input[name=time]').value;
        mySummaryElement.lastElementChild.lastElementChild.lastElementChild.children[1].innerHTML = myTime;

        const myMoreInfo = document.querySelector('textarea[name=more_info]').value;
        if (myMoreInfo !== ''){
          mySummaryElement.lastElementChild.lastElementChild.lastElementChild.children[2].innerHTML = myMoreInfo;
        } else {
          mySummaryElement.lastElementChild.lastElementChild.lastElementChild.children[2].innerHTML = 'Brak uwag';
        }
      }
      // TODO: Validation

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

      // TODO: get data from inputs and show them in summary
    }


    /**
     * Submit form
     *
     * TODO: validation, send data to server
     */
    submit(e) {
      e.preventDefault();
      this.currentStep++;
      this.updateForm();
      const myCategoriesList = [];
      const myCategories = document.querySelectorAll('input[name=categories]');
      myCategories.forEach(function (element){
        if (element.checked){
          myCategoriesList.push(element.value);
        }
      });
      const myBags = document.querySelector('input[name=bags]').value;
      let myInstitution = '';
      const myInstitutions = document.querySelectorAll('input[name=organization]');
      myInstitutions.forEach(function (element){
        if (element.checked){
          myInstitution = element.value;
        }
      });
      const myAddress = document.querySelector('input[name=address]').value;
      const myCity = document.querySelector('input[name=city]').value;
      const myPostCode = document.querySelector('input[name=postcode]').value;
      const myPhone = document.querySelector('input[name=phone]').value;
      const myDate = document.querySelector('input[name=data]').value;
      const myTime = document.querySelector('input[name=time]').value;
      const myMoreInfo = document.querySelector('textarea[name=more_info]').value;

      const obj = {
        quantity: myBags,
        categories: myCategoriesList,
        institution: myInstitution,
        address: myAddress,
        phone_number: myPhone,
        city: myCity,
        zip_code: myPostCode,
        pick_up_date: myDate,
        pick_up_time: myTime,
        pick_up_comment: myMoreInfo
      };

      fetch(window.location.href, {
        method: 'POST',
        body: JSON.stringify(obj),
      })
          .then(async (response) => {
            return await response.text();
          })
          .then(data => {
            if (data === 'True'){
              window.location = '/thanks_donation';
            }
          })
          .catch(e => console.error('Błąd' + e));
    }
  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }
});
