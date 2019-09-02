function clickSelect(id) {
  var rate = $('#' + id);
  rate.click();

  $('.rating').each(function() {
     if ((parseInt($( this ).attr('id').split('-')[2]) < parseInt(id.split('-')[2])) && ($( this ).attr('id').split('-')[0] == id.split('-')[0])) {
       $( this ).addClass('previous')
     } else if ($( this ).attr('id').split('-')[0] == id.split('-')[0]){
       $( this ).removeClass('previous')
     }
   }
 )
}
