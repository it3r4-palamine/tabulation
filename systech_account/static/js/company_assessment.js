var app = angular.module("company_assessment",['common_module']);

app.controller('company_assessmentCtrl', function($scope, $http, $timeout, $element, $controller,CommonFunc,Notification,CommonRead) {
	angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
	var me = this;
	$scope.record = {}
	$scope.create_dialog = function(record){
		$scope.record = {}
		$scope.record['is_active'] = true
		if(record){
			$scope.read_transaction_types(record)
			$scope.record = angular.copy(record);
			$scope.record.date_from = new Date($scope.record.date_from)
			$scope.record.date_to = new Date($scope.record.date_to)
			$scope.record.transaction_types = $scope.record.transaction_type
			$scope.minimum_date()
		}else{
			
			me.post_generic("/company_assessment/check_reference_no/","","main")
			.success(function(response){
				$scope.record.reference_no = response
			})
		}

		
		me.open_dialog("/company_assessment/create_dialog/","","main")
	}

	$scope.create = function(){
		$scope.record.date_from = moment(new Date($scope.record.date_from)).format('YYYY-MM-DD');
		$scope.record.date_to = moment(new Date($scope.record.date_to)).format('YYYY-MM-DD');
		var total_seconds = 0
		var total_time =0
		for(var sessions in $scope.record.sessions){
			var start_hms = $scope.record.sessions[sessions].time_start
			var end_hms = $scope.record.sessions[sessions].time_end

			var a = start_hms.split(':')
			var b = end_hms.split(':')

			var start_seconds = (+a[0])*60*60+(+a[1])*60+(+a[2])
			var end_seconds = (+b[0])*60*60+(+b[1])*60+(+b[2])

			total_seconds += (end_seconds - start_seconds)
		}
		total_time += total_seconds
		credits = angular.copy($scope.record.session_credits)
		if(total_time > 0){
			credits -= total_time
		}

		if(!$scope.record.transaction_types){
			Notification.error("Transaction type is required.")
		}
		// console.log(credits)
		$scope.record.credits_left = credits
		me.post_generic("/company_assessment/create/",$scope.record,"dialog")
		.success(function(response){
			me.close_dialog();
			Notification.success(response);
			$scope.read();
		}).error(function(err){
			Notification.error(err)
		})
	}

	$scope.load_to_edit = function(record){
		$scope.create_dialog(record);
	}

	$scope.read = function(){
		me.post_generic("/company_assessment/read/",{'pagination':me.pagination},"main")
		.success(function(response){
			$scope.records = response.data;
			for(var record in $scope.records){
				var credits_left = $scope.records[record].credits_left ? $scope.records[record].credits_left : 0 
				var session_credits = $scope.records[record].session_credits
				$scope.records[record]['credits_left_seconds'] = convertSecondstoHours(credits_left);
				$scope.records[record]['session_credits_seconds'] = convertSecondstoHours(session_credits);
			}
			console.log($scope.records)
			me.starting = response.starting;
			me.ending = response.data.length;
			me.pagination.limit_options = angular.copy(me.pagination.limit_options_orig);
			me.pagination.limit_options.push(response.total_records)
			me.pagination["total_records"] = response.total_records;
			me.pagination["total_pages"] = response.total_pages;
		})
	};

	convertSecondstoHours = function(d){
			d = Number(d);
		    var h = Math.floor(d / 3600);
		    var m = Math.floor(d % 3600 / 60);
		    var s = Math.floor(d % 3600 % 60);

		    var hDisplay = h > 0 ? h + (h == 1 ? " hour" : " hours, ") : "";
		    var mDisplay = m > 0 ? m + (m == 1 ? " minute" : " minutes, ") : "";
		    var sDisplay = s > 0 ? s + (s == 1 ? " second" : " seconds") : "";
		    return hDisplay + mDisplay + sDisplay; 
	}

	$scope.minimum_date = function(){
		$scope.minimum_date_to = moment(new Date($scope.record.date_from)).format('YYYY-MM-DD');
	}

	$scope.delete = function(record){
		swal({
		    title: "Continue",
		    text: "Remove "+record.company.name+"'s assessment?",
		    type: "warning",
		    showCancelButton: true,
		    confirmButtonColor: "#DD6B55",
		    confirmButtonText: "Delete",
		    cancelButtonText: "Cancel",
		    closeOnConfirm: true
		},
		function(){
			me.post_generic("/company_assessment/delete/"+record.id,"","main")
			.success(function(response){
				Notification.success(response);
				$scope.read();
			}).error(function(err){
				Notification.error(err)
			})
		})
	}

	$scope.read_transaction_types = function(record){
    	me.post_generic("/transaction_types/read/",{"company_rename":record.company_rename.id},"main")
    	.success(function(response){
    		$scope.transaction_types = response.data;
    	})
    }

    $scope.read_users = function(){
    	me.post_generic("/users/read/","","main")
    	.success(function(response){
    		$scope.consultants = response.data;
    	})
    };

	$scope.read_companies = function(record){
		$scope.record.company = {}
    	me.post_generic("/company/read/","","main")
    	.success(function(response){
    		$scope.companies = response.data;
    	})
    }

    $scope.select_transaction_type = function(record){
    	$scope.record.transaction_types = {}
		$scope.read_transaction_types(record);
		$scope.read_user_credits(record);
    }

    $scope.select_user = function(record){
    	$scope.read_user_credits(record);
    }

    $scope.read_user_credits = function(record){
    	// record.date_from = moment(new Date(record.date_from)).format('YYYY-MM-DD');
    	// record.date_to = moment(new Date(record.date_to)).format('YYYY-MM-DD');
    	me.post_generic("/users/read_user_credits/",record,"dialog")
    	.success(function(response){
    		if(response.data.length > 0) {
	    		$scope.record.session_credits = response.data[0].session_credits
	    		$scope.record.date_from = new Date(response.data[0].session_start_date)
	    		$scope.record.date_to = new Date(response.data[0].session_end_date)
    		}else{
    			$scope.record.session_credits = null
    			$scope.record.date_from = null
    			$scope.record.date_to = null
    			Notification.error("No session credits left. Please advised!")
    		}
    	})
    }

	$scope.read();
	me.main_loader = function(){$scope.read();}
	$scope.read_companies();
	$scope.read_users();
	CommonRead.get_display_terms($scope)
});
