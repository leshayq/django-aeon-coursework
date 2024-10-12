$('#sort_option').change(function(event){
    var selectedcategory = $(this).children("option:selected").val();
    sessionStorage.setItem("itemName",selectedcategory);
    $('#sort-form').submit()
});

$('select').find('option[value='+sessionStorage.getItem('itemName')+']').attr('selected','selected');