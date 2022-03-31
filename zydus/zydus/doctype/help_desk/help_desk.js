// Copyright (c) 2022, Atrina Technologies Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Help Desk', {
	 validate : function(frm) {
		var email_pattern = "^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$";
        var email = frm.doc.email
		if(email.length > 0  && !email.match(email_pattern))
				{
					frappe.throw('Enter Valid Email ID')
				}
		var mobile_pattern = "^\\d{10}$";
		var mobile = frm.doc.mobile_number
		if(mobile.length > 0  && !mobile.match(mobile_pattern))
				{
					frappe.throw('Enter Valid Mobile No')
				}	

	 }
});
