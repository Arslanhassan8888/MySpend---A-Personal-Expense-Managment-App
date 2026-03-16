console.log("dashboard.js loaded");

function toggleAll(source) {

    var checkboxes = document.getElementsByClassName("expense-checkbox");

    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = source.checked;
    }

}