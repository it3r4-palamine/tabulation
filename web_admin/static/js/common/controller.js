var app = angular.module("common_controller",[]).controller('CommonCtrl', function($scope,$http,$uibModal,$uibModalStack,$templateCache,CommonFunc,SweetAlert,toastr,Notification,configSettings){
	var me = this;
	me.current_dialogs = []
	me.page_loader = {"main" : false,"dialog" : false};
	me.resizeMode = "BasicResizer";
	me.controls = {"dynamic_columns": true,"advance_filters": true}
	me.no_dynamic_columns = []
	me.uibdates = {}


	let baseUrl = configSettings.baseUrl;

	me.update_default_columns = function(scope){
		$http.post("/common/update_default_columns/"+scope.current_module,scope.columns);
	};

	me.open_date = function(key){
		if(!key){key='date';}
		me.uibdates[key] = true;
	};

	me.sort_default = function(){
		default_sort_key = {
			"accounts" : "code",
			"customers" : "code",
			"inventory" : "code",
			"inventory_cost_history_details" : "receive_inventory__date",
		};

		key = "id";
		if(default_sort_key[$scope.module_code] !== undefined){
			key = default_sort_key[$scope.module_code];
		}
		return key;
	};

	me.export = function(url,filters,fields,current_module){
		if(!fields){
			fields = {}
		}

		date_fields = ["date_from","date_to","date","pdccheckdate_from","pdccheckdate_to"]

		filters = angular.copy(filters)
		if('supplier' in filters && 'id' in filters["supplier"]){
			filters["supplier"] = filters["supplier"]["id"]
		}

		if('customer' in filters && 'id' in filters["customer"]){
			filters["customer"] = filters["customer"]["id"]
		}

		if(filters["paymenttype"] && filters["paymenttype"].constructor === Array){
			paymenttype = []
			ids = me.values_list(filters["paymenttype"])
			for(var i in ids){
				paymenttype.push({"id": ids[i]})
			}
			filters["paymenttype"] = paymenttype;
		}

		if('charts' in filters){
			charts = angular.copy(filters["charts"]);
			raw_charts = [];
			for(i in charts){
				raw_charts.push({
					"id": charts[i]["id"],
					"accounttype": {
						"code": charts[i]["accounttype"]["code"]
					}
				})
			}
			filters["charts"] = raw_charts;
		}

		if('account_types' in filters){
			account_types = angular.copy(filters["account_types"]);
			raw_account_types = [];
			for(i in account_types){
				raw_account_types.push({
					"id": account_types[i]["id"],
					"code2": account_types[i]["code2"],
				})
			}
			filters["account_types"] = raw_account_types;
		}

		if($scope.module_code && me.key_in_list($scope.module_code,["sales_journal","collection_journal",])){
			if(filters["customer"]){
				filters["customer"] = me.values_list(filters["customer"]);
			}
		}

		if($scope.module_code == "vendor_item_purchased"){
			reference_nos = filters["reference_nos"]
			if(reference_nos){
				filters["reference_nos"] = me.values_list(reference_nos);
			}
		}

		var fields = angular.copy(fields)
		if(current_module == "payment_journal"){
			fields = {}
		}

		fields = JSON.stringify(fields);
		var filters = JSON.stringify(me.format_date(filters,date_fields));

		filters = encodeURIComponent(filters)

		url += ("?fields="+fields)
		url += ("&filters="+filters)
		window.open(url,"_blank")
	};
	
	me.clean_url = function(url){
		url = url.replace(/\s+/g, '-').toLowerCase();

		if(url[url.length - 1] != "/"){
			url += "/";	
		}
		return url;
	};

	me.post_generic = function(url,params,loader_key,notify,assign_response,closedialog)
	{
		me.loader2(loader_key,true);
		if(!params){ params = {}; }

		return $http.post(url, params)
		.success(function(response){
			me.loader2(loader_key,false);
			if(notify){
				if(response){
					if(typeof(response) == "object"){
						Notification.success(response.message);
					}else{
						Notification.success(response);
					}
				}
			}
			if(assign_response){me[assign_response] = response;} //not working
			if(closedialog){
				me.close_dialog();
			}
		})
		.error(function(response,status){
			me.loader2(loader_key,false)

			if(status == 404 || status == 500){
				if(notify){Notification.error("Connection error. Please contact administrator.")}
				return;
			}
			if(notify){Notification.error(response)}
		})
	};

	me.post_api = function(url, params, loader_key, notify, dialog_notify, assign_response, close_dialog){

		if (loader_key) me.page_loader[loader_key] = true;
		if (dialog_notify )me.page_loader["dialog"] = true
		if (!params) params = {};

		let absoluteUrl = baseUrl + url;
		let api_token = me.apiToken = document.querySelector('input[name="token"]').getAttribute('value');

		options = {
			headers : {
				"Authorization" : "Token " + api_token
			}
		};

		return $http.post(absoluteUrl, params, options).success(function(response){
			if (dialog_notify) me.page_loader["dialog"] = false;
			if (loader_key) me.page_loader[loader_key] = false;
			if (notify) Notification.success(response);
			if (assign_response) me[assign_response] = response; //not working
			if (close_dialog) me.close_dialog();
		}).error(function(response, status){
			if (loader_key) me.page_loader[loader_key] = false;
			if (dialog_notify) me.page_loader["dialog"] = false;
			if (status == 404 || status == 500){
				if(notify) Notification.error("Connection error. Please contact administrator.");
				return;
			}

			if (notify) Notification.error(response);
		})
	};

	me.get_api = function(url, params, loader_key, notify, assign_response, close_dialog){
		if (loader_key) me.page_loader[loader_key] = true;
		if (!params) params = {};

		let absoluteUrl = baseUrl + url;
		let api_token = me.apiToken = document.querySelector('input[name="token"]').getAttribute('value');

		options = {
			headers : {
				"Authorization" : "Token " + api_token
			},
			params : params

		};

		return $http.get(absoluteUrl, options).success(function(response){
			if (loader_key) me.page_loader[loader_key] = false;
			if (assign_response) me[assign_response] = response; //not working
			if (close_dialog) me.close_dialog();
		}).error(function(response, status){
			if (loader_key) me.page_loader[loader_key] = false;
			if (status == -1)
			{
				if(notify) Notification.error("Can't Connect to Server.");
				return;
			}
			if (status == 404 || status == 500){
				if(notify) Notification.error("Connection error. Please contact administrator.");
				return;
			}
		})
	};

	me.loader2 = function(loader_key,status){
		// console.log(loader_key)
		if(loader_key){
			if(loader_key == "all"){
				me.page_loader["dialog"] = status
				me.page_loader["main"] = status
			}else{
				me.page_loader[loader_key] = status
			}
		}
	}

	me.common_filter_dialog = function(){
		me.open_dialog("/common/filter_dialog2/","dialog_height_100 dialog_width_50");
	}

	me.open_dialog = function(url,dialog_class,key){
		if(!key){key = "main";}
		me.page_loader[key] = true;
		$templateCache.remove(url);
		var dialog = $uibModal.open({
	        templateUrl: url,
	        windowClass : dialog_class,
	        backdrop : 'static',
	        keyboard : false,
	        scope : $scope,
	    })

	    dialog.opened.then(function(){
			me.page_loader[key] = false;
	    	me.current_dialogs.push(dialog)
	    })

	    return dialog
	}

	me.columns_dialog = function(scope){
		if(!scope.current_module){return;}
		me.open_dialog("/common/columns_dialog/"+scope.current_module,"dialog_height_60 dialog_width_30 second_dialog");
	}
 
	me.close_dialog = function(dialog_instance,last){
		if(dialog_instance){
			me.current_dialogs[dialog_instance].close()
		}else if(last){
			var modal_len = me.current_dialogs.length;
			last_instance = me.current_dialogs[modal_len - 1];
			last_instance.close();
			me.current_dialogs.splice(-1,1)
		}else{
			$uibModalStack.dismissAll();
		}
	}

	me.select_all = function(value,lists,key){
		if(!key){key = "value"}

		for(var i in lists){
			if(lists[i]["uneditable"] !== undefined){continue;}
			lists[i][key] = value;
		}
	}

	/*Mostly called from directives that's unable to load the Notification service*/
	me.notify = function(msg,type){
		if(type == "success"){
			Notification.success(msg)
		}else if(type == "error"){
			Notification.error(msg)
		}
	}

	me.loader = function(remove,key){		
		if(!key){
			key = "main";
		}
		me.page_loader[key] = !remove;
	}

	me.read_module_columns = function(scope,exclude_not_import,force, hide_unit_cost = false){
		if(me.no_dynamic_columns.indexOf(scope.current_module) != -1){
			me.controls.dynamic_columns = false;
		}

		if(me.no_advance_filters.indexOf(scope.current_module) != -1){
			me.controls.advance_filters = false;
		}

		if((!scope.current_module || scope.columns) && !force){return;}
		var post = me.post_generic("/common/read_module_columns/"+scope.current_module)
		post.success(function(response){
			if(scope.current_module == "accounts"){
				response["sub_account_name"] = {"sort":2.5, "display" : "Sub account", "selected" : false,'size': 40,"uneditable" : true,"notshow": true}
			}
			if(hide_unit_cost){
				if (scope.current_module == "receive_inventory"){
					unit_cost_keys = ["vat","total","net"] 
				}else{
					unit_cost_keys = ["unit_cost","last_unit_cost","purchase_cost","purchase_cost_unit","cost_of_sale"] 
					if (scope.current_module == "assembly"){
						unit_cost_keys.push("cost")
						unit_cost_keys.push("total")
					}
				}
				for (x in unit_cost_keys){
					if (response[unit_cost_keys[x]]){
						response[unit_cost_keys[x]]["selected"] = false
						response[unit_cost_keys[x]]["notshow"] = true
					}
				}
				// if (response["unit_cost"]){
				// 	response["unit_cost"]["selected"] = false
				// 	response["unit_cost"]["notshow"] = true
				// }
				// if (response["last_unit_cost"]){
				// 	response["last_unit_cost"]["selected"] = false
				// 	response["last_unit_cost"]["notshow"] = true
				// }
			}
			var arr = []
			for(i in response){
				row = response[i]
				row["value"] = i
				arr.push(row)
			}
			var sorted = sortByAttribute(angular.copy(arr),"sort");
			scope.columns = {}
			for(i in sorted){
				if(exclude_not_import && sorted[i].not_import){
					continue
				}
				scope.columns[sorted[i].value] = sorted[i];
			}
		})
	}

	

	me.convert_seconds_duration = function(time)
    {
		var hrs = ~~(time / 3600);
    	var mins = ~~((time % 3600) / 60);
    	var secs = time % 60;

    	return { hours : hrs, minutes : mins, seconds : secs };
    }

	me.related_transactions = function(scope,record,trans_id){
		if(!trans_id){
			trans_id = record.id;
		}

		var template_url = "/common/show_history/"+scope.current_module+"/"+trans_id;
		me.open_dialog(template_url,"width50 second_dialog");
	}

	me.columns_dialog = function(scope){
		if(!scope.current_module){return;}
		me.open_dialog("/common/columns_dialog/"+scope.current_module,"dialog_height_60 dialog_width_30 second_dialog");
	}

	me.list_format_date = function(lists,fields,from_backend){
		for(i = 0;i < lists.length; i++){
			lists[i] = me.format_date(lists[i],fields,from_backend)
		}
        return lists
    }

    me.parse_float = function(num,precision = 2){
    	if(!num){
    		num = 0;
    	}
    	return parseFloat(num).toFixed(precision)
    }

	me.format_date = function(obj,fields,from_backend){
		if(!fields){fields = ["date_from","date_to","date","pdccheckdate_from","pdccheckdate_to","other_date_from","other_date_to","date_of_birth"]}
        for(var i in fields){
            var field = fields[i];
            if(obj[field]){
            	if(from_backend){
                	obj[field] = new Date(obj[field]);
            	}else{
                	obj[field] = moment(obj[field]).format('YYYY-MM-DD');
            	}
            }
        }
        return obj
    }

    me.format_time = function(arr,fields,from_backend){

    	if(!fields){fields = ["session_timein","session_timeout"]}
        for(var i in fields){
            var field = fields[i];
            if(arr[field]){
            	if(from_backend){
        			arr[field] = Date.parse(arr[field]);
            	}else{
                	arr[field] = me.format_single_time(arr[field]);
            	}
            }
        }

        return arr
    }

    me.pad = function(num, size,rightpad) {
        var s = num+"";
        while (s.length < size){
        	if(rightpad){
        		s = s + "0";
        	}else{
        		s = "0" + s;	
        	}
        }
        return s;
    }

    me.go = function(url,newtab){
    	if(newtab){
			var win = window.open(url, '_blank');
			win.focus();
    	}else{
    		window.location.href = url;
    	}
    }

    me.round_off = function(temp_num){
    	var num = angular.copy(temp_num);
    	if(!num || !CommonFunc.isNumeric(num)){
    		num = 0;
    	}

    	precision = 2;
    	num = num.toFixed(precision);
    	num = parseFloat(num);
    	return num;
    }

    me.date_now = function(){
    	return new Date(moment())
    }

    me.reset_date = function(obj,include_from,current_month,date_from_key,date_to_key){
    	if(!date_from_key){
    		date_from_key = "date_from";
    	}
    	
    	if(!date_to_key){
    		date_to_key = "date_to";
    	}

    	var current_year = moment().year()
    	// current_year = 2016;

    	if(current_month == undefined){
    		current_month = moment().month()
    	}
    	var date_from = moment([current_year, current_month]);
    	var date_to = moment(date_from).endOf('month');
    	if(include_from){
    		obj[date_from_key] = new Date(date_from);
    	}
    	obj[date_to_key] = new Date(moment());
    }

    me.read_employees = function(employee_type){
        filter = {"employee_type" : [employee_type]}
        $http.post("/employee/read_employee_selection/",filter)
        .success(function(response){
        	if(!me.employees){me.employees={}}
            me.employees[employee_type] = response;
        })
    }

    me.read_employees = function(scope,employee_type){
        filter = {"employee_type" : [employee_type]}
        $http.post("/employee/read_employee_selection/",filter)
        .success(function(response){
        	if(!scope.employees){scope.employees={}}
            scope.employees[employee_type] = response;
        })
    }

    me.key_in_list = function(item_to_search,arr){
    	var status = false;	
    	for(index in arr){
    		item = arr[index]
    		if(item_to_search == item){
    			status = true;
    		}
    	}
    	return status
    }

    me.generate_pagination = function(scope, response, key){

    	console.log(response);

		scope.starting = response.starting;
		scope.ending = response[key].length;
		scope.pagination.limit_options = angular.copy(scope.pagination.limit_options_orig);
		scope.pagination.limit_options.push(response.total_records);
		scope.pagination["total_records"] = response.total_records;
		scope.pagination["total_pages"] = response.total_pages;
	}

    me.values_list = function(arr,key){
    	if(!key){
    		key = "id";
    	}
    	arr = angular.copy(arr);
    	values = [];
    	for(var i in arr){
    		if(arr[i] !== undefined){
    			values.push(arr[i][key]);
    		}
    	}
    	return values;
    }

    function sortByAttribute(array, ...attrs) {
      // generate an array of predicate-objects contains
      // property getter, and descending indicator
      let predicates = attrs.map(pred => {
        let descending = pred.charAt(0) === '-' ? -1 : 1;
        pred = pred.replace(/^-/, '');
        return {
          getter: o => o[pred],
          descend: descending
        };
      });
      // schwartzian transform idiom implementation. aka: "decorate-sort-undecorate"
      return array.map(item => {
        return {
          src: item,
          compareValues: predicates.map(predicate => predicate.getter(item))
        };
      })
      .sort((o1, o2) => {
        let i = -1, result = 0;
        while (++i < predicates.length) {
          if (o1.compareValues[i] < o2.compareValues[i]) result = -1;
          if (o1.compareValues[i] > o2.compareValues[i]) result = 1;
          if (result *= predicates[i].descend) break;
        }
        return result;
      })
      .map(item => item.src);
    }

    /*Place some of the defaults if can be change or depends on some functions.*/
    me.pagination = {"limit" : 10,"current_page" : 1,"total_records" : 0,"total_pages" : 0,"limit_options_orig" : [20,50,100,150],"limit_options" : []}
    me.filters = {}
    me.sort = {"sort_by": me.sort_default(),"reverse": false};
});