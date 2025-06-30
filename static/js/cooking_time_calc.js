    /**
     * Calculates total time by adding prep time and cook time
     */
    function calculateTotalTime() {
        const prepTime = parseFloat(document.getElementById('id_prep_time').value) || 0;
        const cookTime = parseFloat(document.getElementById('id_cook_time').value) || 0;
        const totalTime = prepTime + cookTime;
        document.getElementById('id_total_time').value = totalTime;
    }

    // Add event listeners when DOM is loaded
    document.addEventListener('DOMContentLoaded', function() {
        const prepTimeInput = document.getElementById('id_prep_time');
        const cookTimeInput = document.getElementById('id_cook_time');
        
        if (prepTimeInput && cookTimeInput) {
            prepTimeInput.addEventListener('change', calculateTotalTime);
            cookTimeInput.addEventListener('change', calculateTotalTime);
        }
    });