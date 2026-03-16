document.addEventListener("DOMContentLoaded", function () {

    const selectAll = document.getElementById("select-all");
    const checkboxes = document.querySelectorAll(".expense-checkbox");
    const deleteButton = document.getElementById("delete-button");

    function updateDeleteButton() {
        let checked = document.querySelectorAll(".expense-checkbox:checked").length;
        deleteButton.disabled = checked === 0;
    }

    selectAll.addEventListener("change", function () {

        checkboxes.forEach(function (checkbox) {
            checkbox.checked = selectAll.checked;

            if (selectAll.checked) {
                checkbox.closest("tr").classList.add("selected-row");
            } else {
                checkbox.closest("tr").classList.remove("selected-row");
            }
        });

        updateDeleteButton();
    });

    checkboxes.forEach(function (checkbox) {

        checkbox.addEventListener("change", function () {

            if (checkbox.checked) {
                checkbox.closest("tr").classList.add("selected-row");
            } else {
                checkbox.closest("tr").classList.remove("selected-row");
            }

            updateDeleteButton();
        });

    });

    updateDeleteButton();

});