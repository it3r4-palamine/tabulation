var app = angular.module("related_questions",['common_module']);

app.controller('relatedquestionsCtrl', function($scope, $http, $timeout, $element, $controller,CommonFunc,Notification,CommonRead) {
	angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
	var me = this;
	$scope.record = {}
	$scope.questions = []
	$scope.create_dialog = function(record){
		$scope.record = {}
		$scope.record['is_active'] = true
		if(record){
			$scope.record = angular.copy(record);
		}
		
		me.open_dialog("/assessments/related_questions_create_dialog/","","main")
	}

	$scope.create = function(){
		me.post_generic("/assessments/related_questions_create/",$scope.record,"dialog")
		.success(function(response){
			$scope.questions = []
			me.close_dialog();
			Notification.success(response);
			$scope.read();
			$scope.read_questions();
		}).error(function(err){
			Notification.error(err)
		})
	}

	$scope.load_to_edit = function(record){
		$scope.create_dialog(record);
	}

	$scope.read = function(){
		me.post_generic("/assessments/read_related_questions/",{'pagination':me.pagination},"main")
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

	$scope.read_questions = function(){
		me.post_generic("/assessments/read/",{'type':'related_questions'},"main")
		.success(function(response){
			$scope.questions = response.data;
		})
	};

	$scope.minimum_date = function(){
		$scope.minimum_date_to = moment(new Date($scope.record.date_from)).format('YYYY-MM-DD');
	}

	$scope.delete = function(record){
		swal({
		    title: "Continue",
		    text: "Remove related questions?",
		    type: "warning",
		    showCancelButton: true,
		    confirmButtonColor: "#DD6B55",
		    confirmButtonText: "Delete",
		    cancelButtonText: "Cancel",
		    closeOnConfirm: true
		},
		function(){
			me.post_generic("/assessments/delete_related_questions/"+record.id,"","main")
			.success(function(response){
				Notification.success(response);
				$scope.read();
			}).error(function(err){
				Notification.error(err)
			})
		})
	}

	$scope.read_transaction_types = function(record){
    	me.post_generic("/transaction_types/read/",{"company":record.company.id},"main")
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
	$scope.read_questions();
	me.main_loader = function(){$scope.read();}
	// $scope.read_companies();
	// $scope.read_users();
});
