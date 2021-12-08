function startLoader() {
	var loader = document.getElementById('preloader');
	loader.style.display = "block";
}
function stopLoader() {
	var loader = document.getElementById('preloader');
	loader.style.display = "none";
}

function getCookie(name) {
     var cookieValue = null;
     if (document.cookie && document.cookie != '') {
         var cookies = document.cookie.split(';');
         for (var i = 0; i < cookies.length; i++) {
             var cookie = jQuery.trim(cookies[i]);
             // Does this cookie string begin with the name we want?
             if (cookie.substring(0, name.length + 1) == (name + '=')) {
                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                 break;
             }
         }
     }
     return cookieValue;
 }
function raiseNotification(message_type, message) {
	var toast_div = document.getElementById('toastDiv');
	if (message_type.toLowerCase() == "error") {
		toast_div.classList.add("bg-danger");
	} else if (message_type.toLowerCase == "success") {
		toast_div.classList.add("bg-success");
	}

	var toastMessage = document.getElementById('toastMessage');
	toastMessage.innerHTML = message;
	$('.toast').toast({
		delay : 4000
	});
	$('.toast').toast('show');
}


function wait(ms){
   var start = new Date().getTime();
   var end = start;
   while(end < start + ms) {
     end = new Date().getTime();
  }
}

function print_receipt(order_id){
    let print_window=window.open('/order/print_order/'+order_id,'','width=200,height=100');
    
    print_window.focus();
    
    print_window.print();
    //wait(3000);
    setTimeout(function () { print_window.close();}, 5000);
     
  }
if (window.location.href.includes('/dashboard')) {
	
	let path_split = window.location.pathname.split('/');
	var pie_chart_data = {};
	var bar_chart_data = {};
	var top_selling_item_category_data = {};
	var order_types_http;
	order_types_http = new XMLHttpRequest();
	startLoader();
	order_types_http.onreadystatechange = function() {
		if (order_types_http.readyState == 4 && order_types_http.status == 200) {
			try {
				var order_types_json_data = JSON.parse(order_types_http.responseText)
				if ("error" == order_types_json_data.status) {
					raiseNotification(order_types_json_data.status,
							order_types_json_data.error.error_message);
				} else {
					raiseNotification(order_types_json_data.status,
							order_types_json_data.success_message);
				     pie_chart_data = {
				        "data": order_types_json_data.data,
				        "title": "Top Selling Item Category",
				        "element": "dashboard1"
				    }

				}
			} catch (err) {
				raiseNotification("error", "Some error occured");
			} finally {
				stopLoader();
			}
		} else if (order_types_http.readyState == 4 && order_types_http.status != 200) {
			raiseNotification("error", "Some error occured");
			stopLoader();
		}
	}
	if (path_split.length > 3){
		order_types_http.open("GET", "/order/get_order_types/"+path_split[2]+"/"+path_split[3], true);
	}
	else{
		order_types_http.open("GET", "/order/get_order_types", true);
	}
	
	order_types_http.withCredentials = true;
	order_types_http.send();
	
	///////////////////////////////////////////////
	
	var http;
	http = new XMLHttpRequest();
	startLoader();
	http.onreadystatechange = function() {
		if (http.readyState == 4 && http.status == 200) {
			try {
				var json_data = JSON.parse(http.responseText)
				if ("error" == json_data.status) {
					raiseNotification(json_data.status,
							json_data.error.error_message);
				} else {
					raiseNotification(json_data.status,
							json_data.success_message);
							
				        	bar_chart_data = {
						        "data": json_data.data,
						        "title": "Top Selling Items",
						        "element": "dashboard3"
						    };
				}
			} catch (err) {
				raiseNotification("error", "Some error occured");
			} finally {
				stopLoader();
			}
		} else if (http.readyState == 4 && http.status != 200) {
			raiseNotification("error", "Some error occured");
			stopLoader();
		}
	}
	if (path_split.length > 3){
		http.open("GET", "/order/get_top_selling_items/"+path_split[2]+"/"+path_split[3], true);
	}
	else{
	http.open("GET", "/order/get_top_selling_items", true);
	}
	http.withCredentials = true;
	http.send();
	
	
	///////////////////////////////////////////////
	
	var top_item_category_http;
	top_item_category_http = new XMLHttpRequest();
	startLoader();
	top_item_category_http.onreadystatechange = function() {
		if (top_item_category_http.readyState == 4 && top_item_category_http.status == 200) {
			try {
				var top_item_category_json_data = JSON.parse(top_item_category_http.responseText)
				if ("error" == top_item_category_json_data.status) {
					raiseNotification(top_item_category_json_data.status,
							top_item_category_json_data.error.error_message);
				} else {
					raiseNotification(top_item_category_json_data.status,
							top_item_category_json_data.success_message);
							
				        	top_selling_item_category_data = {
						        "data": top_item_category_json_data.data,
						        "title": "Top Selling Item Category",
						        "element": "dashboard4"
						    };
				}
			} catch (err) {
				raiseNotification("error", "Some error occured");
			} finally {
				stopLoader();
			}
		} else if (top_item_category_http.readyState == 4 && top_item_category_http.status != 200) {
			raiseNotification("error", "Some error occured");
			stopLoader();
		}
	}
	if (path_split.length > 3){
		top_item_category_http.open("GET", "/order/get_top_selling_item_category/"+path_split[2]+"/"+path_split[3], true);
	}
	else{
	top_item_category_http.open("GET", "/order/get_top_selling_item_category", true);
	}
	top_item_category_http.withCredentials = true;
	top_item_category_http.send();
	
	
	

    var line_chart_data = {
        "data": [['Jan', 7.0], ['Feb', 6.9], ['Mar', 9.5],
        ['Apr', 14.5], ['May', 18.2], ['Jun', 21.5],
        ],
        "title": "Last 30 Days Sale",
        "y_axis_title": "Charger Count",
        "x_axis_title": "Month",
        "element": "dashboard2"
    }

    var area_chart_data = {
        "data": [['Month', 'Usage'],
        ['JAN', 900], ['FEB', 1000], ['MAR', 1170],
        ['APR', 1250], ['MAY', 1530]],
        "title": "Last 30 Days Order Count",
        "x_axis_title": "Month",
        "element": "dashboard4"
    }
    
    wait(3000);
    google.charts.setOnLoadCallback(function () {
    drawPieChart(pie_chart_data);
    });
    
    google.charts.setOnLoadCallback(function () {
		drawBarChart(bar_chart_data)
	});
    google.charts.setOnLoadCallback(function () {
        drawLineChart(line_chart_data);
    });
    google.charts.setOnLoadCallback(function () {
        drawBarChart(top_selling_item_category_data)
    });



}

function accept_order(order_id) {
	var http;
	http = new XMLHttpRequest();
	startLoader();
	http.onreadystatechange = function() {
		if (http.readyState == 4 && http.status == 200) {
			try {
				var json_data = JSON.parse(http.responseText)
				if ("error" == json_data.status) {
					raiseNotification(json_data.status,
							json_data.error.error_message);
				} else {
					raiseNotification(json_data.status,
							json_data.success_message);
							location.href = "pending-orders";
				}
			} catch (err) {
				raiseNotification("error", "Some error occured");
			} finally {
				stopLoader();
			}
		} else if (http.readyState == 4 && http.status != 200) {
			raiseNotification("error", "Some error occured");
			stopLoader();
		}
	}
	http.open("POST", "/order/accept_order", true);
	
	http.setRequestHeader("Content-type",
				"application/x-www-form-urlencoded");
    http.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));

	http.withCredentials = true;
	http.send("order_id=" + order_id);
}

function complete_order_item(order_item_id) {
	var http;
	http = new XMLHttpRequest();
	startLoader();
	http.onreadystatechange = function() {
		if (http.readyState == 4 && http.status == 200) {
			try {
				var json_data = JSON.parse(http.responseText)
				if ("error" == json_data.status) {
					raiseNotification(json_data.status,
							json_data.error.error_message);
				} else {
					raiseNotification(json_data.status,
							json_data.success_message);
							$("#O"+order_item_id).removeClass("bg-primary").addClass("bg-success");
							//location.href = "pending-orders";
				}
			} catch (err) {
				raiseNotification("error", "Some error occured");
			} finally {
				stopLoader();
			}
		} else if (http.readyState == 4 && http.status != 200) {
			raiseNotification("error", "Some error occured");
			stopLoader();
		}
	}
	http.open("POST", "/order/complete_order_item", true);
	
	http.setRequestHeader("Content-type",
				"application/x-www-form-urlencoded");
    http.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));

	http.withCredentials = true;
	http.send("order_item_id=" + order_item_id);
}


function on_dashboard_date_filter_change() {
  let x = document.getElementById("dashboard_date_range").value;
  let from_date ="";
  let from_month = ""; 
  let from_year = "";
  let from_day = "";
  
  let to_date = "";
  let to_month = ""; 
  let to_year = "";
  let to_day = "";
  let d = new Date();
  
  switch (x) {
  case "today":
    from_date = d.getFullYear()+"-"+ (Number(d.getMonth())+1)+"-"+d.getDate();
    to_date = d.getFullYear()+"-"+ (Number(d.getMonth())+1)+"-"+d.getDate();
    break;
  case "yesterday":
  	d.setDate( d.getDate() - 1 );
  	from_month = Number(d.getMonth())+1;
  	from_year = d.getFullYear();
  	
  	to_month = from_month;
  	to_year = from_year; 
    from_date = from_year+"-"+from_month+"-"+(d.getDate());
    to_date = to_year+"-"+to_month+"-"+(d.getDate());
    break;
  case "last 7 days":
  	d.setDate( d.getDate() - 1 );
  	to_month = Number(d.getMonth())+1;
  	to_year = d.getFullYear() 
  	to_day = d.getDate();
  	
  	d.setDate( d.getDate() - 7 );
  	from_month = Number(d.getMonth())+1;
  	from_year = d.getFullYear();
  	from_day = d.getDate();
  	
    from_date = from_year+"-"+from_month+"-"+from_day;
    to_date = to_year+"-"+to_month+"-"+to_day;
    break;
  case "last 15 days":
  	d.setDate( d.getDate() - 1 );
  	to_month = Number(d.getMonth())+1;;
  	to_year = d.getFullYear(); 
  	to_day = d.getDate();
  	
  	d.setDate( d.getDate() - 15 );
  	from_month = Number(d.getMonth())+1;
  	from_year = d.getFullYear();
  	from_day = d.getDate();
  	
    from_date = from_year+"-"+from_month+"-"+from_day;
    to_date = to_year+"-"+to_month+"-"+to_day;
    break;
  case "last 30 days":
  	d.setDate( d.getDate() - 1 );
  	to_month = Number(d.getMonth())+1;;
  	to_year = d.getFullYear(); 
  	to_day = d.getDate();
  	
  	d.setDate( d.getDate() - 30 );
  	from_month = Number(d.getMonth())+1;
  	from_year = d.getFullYear();
  	from_day = d.getDate();
  	
    from_date = from_year+"-"+from_month+"-"+from_day;
    to_date = to_year+"-"+to_month+"-"+to_day;
    break;
  case "this month":
  	d.setDate( d.getDate());
  	to_month = Number(d.getMonth())+1;;
  	to_year = d.getFullYear(); 
  	to_date = d.getDate();
  	
  	d.setDate( 1 );
  	from_month = Number(d.getMonth())+1;
  	from_year = d.getFullYear();
  	from_date = d.getDate();
  	
    from_date = from_year+"-"+from_month+"-"+from_date;
    to_date = to_year+"-"+to_month+"-"+to_date; 
    break;
}
  window.location.href = "/dashboard/"+from_date+"/"+to_date;
}
