$(document).ready(function() {

      // first we hide opions 2-5 and button
      $('#wname').hide();
      $('#main_p').hide();
      $('#major_p').hide();
      $('#minor_p').hide();
      $('#submitbtn').hide();

      // when 1st available option is changed, we get JSON from "/options"
      $('#wtype').change(function(){

        $.getJSON('/options', {
          wtype: $('#wtype').val()
        
        // if request successful process data
        }).done(function(data) {
              
              // remeber selected options for later use
              mainp=$('#main_p').val();
              majorp=$('#major_p').val();
              minorp=$('#minor_p').val();
              
              // empty options for now...
              $('#wname').empty();
              $('#main_p').empty();
              $('#major_p').empty();
              $('#minor_p').empty();
              
              // appending placeholder options
              $('#wname').append($('<option disabled selected>Weapon Name</option>'));
              $('#main_p').append($('<option disabled selected>Main Prefix &#9734</option>'));
              $('#major_p').append($('<option disabled selected>Major Prefix &#9734&#9734</option>'));
              $('#minor_p').append($('<option disabled selected>Minor Prefix &#9734&#9734&#9734</option>'));              
              
              // appending real options available for chosen type trough itteration
              $.each(data.weapons, function(key, val) {
                $('#wname').append($('<option>').text(val.name).attr('value', val.id));
              });
              $.each(data.mains, function(key, val) {
                $('#main_p').append($('<option>').text(val.name).attr('value', val.id));
              });
              $.each(data.majors, function(key, val) {
                $('#major_p').append($('<option>').text(val.description).attr('value', val.id));
              });
              $.each(data.minors, function(key, val) {
                $('#minor_p').append($('<option>').text(val.description).attr('value', val.id));
              });
              
              // after all new options were added to selection, this "if" condition checks if previously saved option is in new options list
              if ($("#main_p option[value="+mainp+"]").length > 0){
                // if true, select this option
                $('#main_p').val(mainp).change();
              }
              
              if ($("#major_p option[value="+majorp+"]").length > 0){
                $('#major_p').val(majorp).change();
              }
              
              if ($("#minor_p option[value="+minorp+"]").length > 0){
                $('#minor_p').val(minorp).change();
              }
              
              // make select options and button fadeIn from "hide", with delay
              $('#wname').fadeIn();
              $('#main_p').delay(100).fadeIn();
              $('#major_p').delay(200).fadeIn();
              $('#minor_p').delay(300).fadeIn();
              $('#submitbtn').delay(400).fadeIn();
         })
      });
    });