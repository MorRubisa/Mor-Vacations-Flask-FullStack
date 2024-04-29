//Show a message that verifies that you really want to Delete a  vacation
function confirmDelete() {
    const ok = confirm("Press OK in order to delete?");
    if (!ok) event.preventDefault();
}

//Show a message that verifies that you really want to cancel
function confirmCancel() {
    const ok = confirm("Are you sure you want to Cancel?");
    if (!ok) event.preventDefault();
}

//Show a message that verifies that you really want to Update a vacation
function confirmUpdate() {
    const isValid = validateDatesUpdate()
    if (!isValid) {
        event.preventDefault();
        return //Stop if not validate
    }
    //if valid continue
    const ok = confirm("Are you sure you want to Update?");
    if (!ok) event.preventDefault();
}

//Show a message that verifies that you really want to Add a new vacation
function confirmInsert() {
    const isValid = validateDatesInsert()
    if (!isValid) {
        event.preventDefault();
        return //Stop if not validate
    }
    //if valid continue
    const ok = confirm("Press OK in order to add this new vacation?");
    if (!ok) event.preventDefault();
}

//Finds element by css & removes the errorSpan element by setTimeout
const errorSpan = document.querySelector(".error");
if (errorSpan) {
    setTimeout(()=> {
        errorSpan.parentNode.removeChild(errorSpan);
    }, 4000);
}

// Validation check for insert a new vacation
function validateDatesInsert() {

    var startDate = new Date(document.getElementById("start_date").value);
    var endDate = new Date(document.getElementById("end_date").value);
    var currentDate = new Date();
    //change the hour for current date to : 00:00:00 
    currentDate.setHours(0)
    currentDate.setMinutes(0)
    currentDate.setSeconds(0)
    // check if start date is earlier than the current date
    if (startDate<currentDate) {
        alert ("Start date can't be earlier than the current date")
        return false
    }
    // check if end date is earlier than the start date
    if (endDate < startDate) {
        alert ("Start date must be before the end date")
        return false
    }
    
    return true    
}

// Validation check for updating an existing vacation
function validateDatesUpdate() {

    var startDate = new Date(document.getElementById("start_date").value);
    var endDate = new Date(document.getElementById("end_date").value);
   // check if end date is earlier than the start date
    if (endDate < startDate) {
        alert ("Start date must be before the end date")
        return false
    }

    return true   
}

//Display the selected image (by the file name)
function previewImage(){
    const fileInput = document.getElementById("fileInput"); 
    const imagePreview  = document.getElementById ("imagePreview");

    const file = fileInput.files[0];
    if (file){
        const reader = new FileReader();

        reader.addEventListener ('load', function() {
            imagePreview.src = this.result;
        });

        reader.readAsDataURL(file);
    }
}


