$(function() {
  'use strict';

  if($('#datePickerExample').length) {
    var date = new Date();
    var today = new Date(date.getFullYear(), date.getMonth(), date.getDate());
    $('#datePickerExample').datepicker({
      format: "mm/dd/yyyy",
      todayHighlight: true,
      autoclose: true
    });
    $('#datePickerExample').datepicker('setDate', today);
  }
});

$(function() {
  'use strict';

  var date = new Date();
  var today = new Date(date.getFullYear(), date.getMonth(), date.getDate());

  // Initialize 'From Date' picker
  if($('#datePickerFrom').length) {
    $('#datePickerFrom').datepicker({
      format: "mm/dd/yyyy",
      todayHighlight: true,
      autoclose: true
    });
    $('#datePickerFrom').datepicker('setDate', today); // Set current date
  }

  // Initialize 'To Date' picker
  if($('#datePickerTo').length) {
    $('#datePickerTo').datepicker({
      format: "mm/dd/yyyy",
      todayHighlight: true,
      autoclose: true
    });
    $('#datePickerTo').datepicker('setDate', today); // Set current date
  }
});