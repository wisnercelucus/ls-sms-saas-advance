$(document).ready(

	function()
	{
    	$("#list_pupil").dataTable();
    	$("#list_teacher").dataTable();
    	$("#list_responsible").dataTable();
    	$("#list_course").dataTable();
    	$("#list_mark").dataTable();
    	$("#list_attendance").dataTable();
      $("#list_grade").dataTable();
      $("#list_term").dataTable();
      $("#list_fy").dataTable();


      $("#select_amount").change(function()
        {
          if ($(this).val() != "custom")
          {
            console.log("Herre disabled")
            $("#custom_amount").attr("disabled", "disabled");
          } else {
            console.log("Herre enabled")
            $("#custom_amount").removeAttr("disabled");
          }
        }).trigger("change");

    }

);



