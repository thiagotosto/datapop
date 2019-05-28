function clickSelect(id) {
  var rate = $('#' + id);
  rate.click();

  $('.rating').each(function() {
     if (parseInt($( this ).attr('id').split('-')[2]) < parseInt(id.split('-')[2])) {
       $( this ).addClass('previous')
     } else {
       $( this ).removeClass('previous')
     }
   }
 )
}
