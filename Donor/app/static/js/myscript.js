$(document).ready(function() {
    $('#mytable').DataTable();
} );

let btn = document.querySelector("#btn-sidebar")
let sidebar = document.querySelector(".sidebar")

btn.onclick = function(){
    console.log("click");
    sidebar.classList.toggle("active");
}