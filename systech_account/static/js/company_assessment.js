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
			me.starting = response.starting;
			me.ending = response.data.length;
			me.pagination.limit_options = angular.copy(me.pagination.limit_options_orig);
			me.pagination.limit_options.push(response.total_records)
			me.pagination["total_records"] = response.total_records;
			me.pagination["total_pages"] = response.total_pages;
		})
	};

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
		console.log(record)
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
    }

	$scope.read();
	me.main_loader = function(){$scope.read();}
	$scope.read_companies();
	$scope.read_users();
	CommonRead.get_display_terms($scope)
});
