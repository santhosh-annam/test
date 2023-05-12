$(function() {
		history.replaceState(null, document.title, location.href);

		if($("#callback_url").val() && $("#session_id").val() && $("#auth_status_code").val() && $("#auth_status_description").val() && $("#rim_no").val()){
			$("#redirect_callbackurl_form").attr("action", $("#callback_url").val());
			$("#callback_url").remove();
			$("#redirect_callbackurl_form").submit();
		}

	 $.mask.definitions['~'] = '[+-]';
        $('#id_expiry').mask('99/99', {
          placeholder: 'MM/YY'
        });
        $('').mask('9999 9999 9999 9999');
        $('#phoneExt').mask('(999) 999-9999? x99999');
        $('#iphone').mask('+33 999 999 999');
        $('#tin').mask('99-9999999');
        $('#ssn').mask('999-99-9999');
        $('#product').mask('a*-999-a999', { placeholder: ' ' });
        $('#eyescript').mask('~9.99 ~9.99 999');
        $('#po').mask('PO: aaa-999-***');
        $('#pct').mask('99%');
        $('#phoneAutoclearFalse').mask('(999) 999-9999', {
          autoclear: false,
          completed: function() {
            alert('completed autoclear!');
          }
        });
        $('#phoneExtAutoclearFalse').mask('(999) 999-9999? x99999', {
          autoclear: false
        });

        $('input')
          .blur(function() {
            $('#info').html('Unmasked value: ' + $(this).mask());
          })
          .dblclick(function() {
            $(this).unmask();
          });
      });
  
	function isNumber(evt) {
		evt = (evt) ? evt : window.event;
		var charCode = (evt.which) ? evt.which : evt.keyCode;
		if (charCode > 31 && (charCode < 48 || charCode > 57)) {
			return false;
		}
		return true;
	}
    function Validate(e) {
        var keyCode = e.keyCode || e.which;
        var lblError = document.getElementById("lblError");
        lblError.innerHTML = "";

        //Regex for Valid Characters i.e. Alphabets and Numbers.
        var regex = /^[0-9]+$/;

        //Validate TextBox value against the Regex.
        var isValid = regex.test(String.fromCharCode(keyCode));
        if (!isValid) {
            lblError.innerHTML = "Only Numbers are allowed.";
        }
        return isValid;
    }
	
for(y = new Date().getFullYear(); y >= 1900; y--) {
        var optn = document.createElement("OPTION");
        optn.text = y;
        optn.value = y;
        document.getElementById('id_dob_year').options.add(optn);
}
 
for(y = 1; y <= 31; y++) {
        var optn = document.createElement("OPTION");
        optn.text = y;
        optn.value = y;
        document.getElementById('id_dob_day').options.add(optn);
}
 
var d = new Date();
var monthArray = new Array();
monthArray[0] = "Jan";
monthArray[1] = "Feb";
monthArray[2] = "Mar";
monthArray[3] = "Apr";
monthArray[4] = "May";
monthArray[5] = "Jun";
monthArray[6] = "Jul";
monthArray[7] = "Aug";
monthArray[8] = "Sep";
monthArray[9] = "Oct";
monthArray[10] = "Nov";
monthArray[11] = "Dec";

for(m = 0; m <= 11; m++) {
    var optn = document.createElement("OPTION");
    optn.text = monthArray[m];
    optn.value = (m+1);
    document.getElementById('id_dob_month').options.add(optn);
}

$(document).ready(function(){
  $("#card").validate({
    rules: {
      cpr: {
        required: true,
        minlength: 1,
        maxlength: 18,
      },
      dob_day: "required",
      dob_month: "required",
      dob_year: "required",
      expiry: "required",
      card_number: {
        required: true,
        minlength: 19,
        maxlength: 19,
      },
    },
    messages: {
      cpr: {
      required: "Enter CPR",
      minlength: "CPR is empty",
      maxlength: "CPR should be upto 18 digits only",
     },
     dob_day: {
      required: "Select Day",
     },
     dob_month: {
      required: "Select Month",
     },
     dob_year: {
      required: "Select Year",
     },
     expiry: {
      required: "Select Expiry",
     },
     card_number: {
      required: "Enter card number",
      minlength: "Enter 16 digit card number",
      maxlength: "Card number should have 16 digits only",
     },
    },
  });
});

  $("#id_card_number").on("keydown", function(e) {
    var cursor = this.selectionStart;
    if (this.selectionEnd != cursor) return;
    if (e.which == 46) {
        if (this.value[cursor] == " ") this.selectionStart++;
    } else if (e.which == 8) {
        if (cursor && this.value[cursor - 1] == " ") this.selectionEnd--;
    }
}).on("input", function() {
    var value = this.value;
    var cursor = this.selectionStart;
    var matches = value.substring(0, cursor).match(/[^0-9]/g);
    if (matches) cursor -= matches.length;
    value = value.replace(/[^0-9]/g, "").substring(0, 16);
    var formatted = "";
    for (var i=0, n=value.length; i<n; i++) {
        if (i && i % 4 == 0) {
            if (formatted.length <= cursor) cursor++;
            formatted += " ";
        }
        formatted += value[i];
    }
    if (formatted == this.value) return;
    this.value = formatted;
    this.selectionEnd = cursor;
});

$("#id_cpr").on("input", function(){
	if($("#id_cpr").val().length == 0)
		$("#id_cpr").removeClass("ui-state-filled");
	else
		$("#id_cpr").addClass("ui-state-filled");
});
 
$("#id_card_number").on("input", function(){
	if($("#id_card_number").val().length == 0)
		$("#id_card_number").removeClass("ui-state-filled");
	else
		$("#id_card_number").addClass("ui-state-filled");
});
	
$("#id_expiry").focus(function(){
	if($("#id_expiry").hasClass("ui-state-filled"))
		$("#id_expiry").removeClass("ui-state-filled");
	else
		$("#id_expiry").addClass("ui-state-filled");
});