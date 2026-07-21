$(function () {
  const table = $("#mytable");
  if (table.length && $.fn.DataTable) {
    table.DataTable({
      responsive: true,
      pageLength: 10,
      order: [],
    });
  }

  const sidebarButton = document.querySelector("#btn-sidebar");
  const sidebar = document.querySelector(".sidebar");
  if (sidebarButton && sidebar) {
    sidebarButton.addEventListener("click", function () {
      sidebar.classList.toggle("active");
    });
  }
});
