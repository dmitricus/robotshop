window.onload = function () {
$('.products_list').on('click', 'input[type="number"]', function () {
var t_href = event.target;
$.ajax({
url: "/admin/products/edit/" + t_href.id + "/" + t_href.name + "/" + t_href.value + "/",
success: function (data) {
$('.products_list').html(data.result);
},
});
event.preventDefault();
});
}