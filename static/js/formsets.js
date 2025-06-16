// formsets.js

// Add this function to validate formsets before submission
function validateFormsets() {
    const prefixes = ["equipment", "ingredient", "instruction"];
    let isValid = true;
    
    for (let prefix of prefixes) {
        const formset = document.getElementById(`${prefix}-formset`);
        const visibleForms = formset.querySelectorAll('.formset-form:not([style*="display: none"])');
        
        if (visibleForms.length === 0) {
            // Show error message
            const errorDiv = document.getElementById(`${prefix}-error`);
            if (errorDiv) {
                errorDiv.innerHTML = `<div class="alert alert-danger">Please provide at least one ${prefix}.</div>`;
                errorDiv.scrollIntoView({ behavior: "smooth", block: "center" });
            }
            isValid = false;
        } else {
            // Clear any existing error
            const errorDiv = document.getElementById(`${prefix}-error`);
            if (errorDiv) {
                errorDiv.innerHTML = '';
            }
        }
    }
    
    return isValid;
}

// Add form submission handler
document.getElementById('recipe-form').addEventListener('submit', function(e) {
    if (!validateFormsets()) {
        e.preventDefault();
    }
});


function addForm(prefix) {
    const totalForms = document.getElementById(`id_${prefix}-TOTAL_FORMS`);
    const formNum = parseInt(totalForms.value);
    const emptyForm = document.getElementById(`empty-form-${prefix}`).innerHTML;
    const newForm = emptyForm.replace(/__prefix__/g, formNum);
    
    const formset = document.getElementById(`${prefix}-formset`);
    formset.insertAdjacentHTML('beforeend', newForm);
    totalForms.value = formNum + 1;
    
    // Scroll to new form
    const newFormElement = formset.lastElementChild;
    newFormElement.scrollIntoView({
        behavior: 'smooth',
        block: 'nearest'
    });
    
    // Focus first input in new form
    const firstInput = newFormElement.querySelector('input, textarea');
    if (firstInput) {
        firstInput.focus();
    }
    
    // Clear any existing errors for this formset
    const section = document.getElementById(`${prefix}-section`);
    if (section) {
        const errorDiv = section.querySelector('.formset-error');
        if (errorDiv) {
            errorDiv.remove();
        }
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const prefixes = ["equipment", "ingredient", "instruction"];
    for (let prefix of prefixes) {
        const errorDiv = document.getElementById(`${prefix}-error`);
        if (errorDiv && errorDiv.innerText.trim() !== "") {
            console.log("Scrolling to error in:", prefix);
            errorDiv.scrollIntoView({ behavior: "smooth", block: "center" });
            errorDiv.classList.add("border", "border-danger", "rounded", "p-3", "bg-light");
            break;  // only scroll to first formset with error
        }
    }
});

// Remove form handler
document.addEventListener('click', function(e) {
    if (e.target && e.target.classList.contains('remove-form')) {
        e.preventDefault();
        const form = e.target.closest('.formset-form');
        if (form) {
            // If this is not an empty form, mark it for deletion
            const deleteInput = form.querySelector('input[name$="-DELETE"]');
            if (deleteInput) {
                deleteInput.value = 'on';
                form.style.display = 'none';
            } else {
                form.remove();
                // Update the TOTAL_FORMS count
                const prefix = form.closest('[id$="-formset"]').id.replace('-formset', '');
                const totalForms = document.getElementById(`id_${prefix}-TOTAL_FORMS`);
                if (totalForms) {
                    totalForms.value = parseInt(totalForms.value) - 1;
                }
            }
        }
    }
});