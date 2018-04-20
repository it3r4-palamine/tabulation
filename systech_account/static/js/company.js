var app = angular.module("company",['common_module']);

app.controller('companyCtrl', function($scope, $http, $timeout, $element, $controller,CommonFunc,Notification,CommonRead) {
	angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
	var me = this;
	$scope.record = {}
	$scope.subject_transaction_types = []
	$scope.new_transaction_types = []
	$scope.filter = {}
	$scope.create_dialog = function(record){
		$scope.record = {}
		$scope.record['is_active'] = true
		if(record){
			$scope.record = angular.copy(record);
			$scope.record['transaction_types'] = $scope.record.transaction_type
			$scope.t_types_total_records = $scope.record.transaction_type.length
			$scope.setPagingData($scope.currentPage);
			$scope.read_subject_transaction_types($scope.record)
		}
		
		me.open_dialog("/company/create_dialog/","","main")
	}

	$scope.create = function(){
		$scope.record['updated_transaction_types'] = []
		for(var ids in $scope.record.transaction_types){
			$scope.record.updated_transaction_types.push($scope.record.transaction_types[ids].id)
		}
		if($scope.record.new_transaction_types){
			for(var t_type in $scope.record.new_transaction_types){
				$scope.record.updated_transaction_types.push($scope.record.new_transaction_types[t_type].id)
			}
		}
		$scope.record.transaction_type = []
		$scope.record.transaction_types = []
		me.post_generic("/company/create/",$scope.record,"dialog")
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
		var data = {
			name : $scope.filter.name,
			pagination : me.pagination,
			sort : me.sort,
		}
		me.post_generic("/company/read/",data,"main")
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

	$scope.currentPage = 1;
	$scope.itemsPerPage = 10;
	$scope.$watch("currentPage", function() {
	    $scope.setPagingData($scope.currentPage);
	});

	$scope.changePage = function(page){
		$scope.$watch("currentPage", function() {
		    $scope.setPagingData(page);
		});		
	}

	$scope.setPagingData = function(page) {
		if($scope.record['transaction_types']) {
		    var pagedData = $scope.record['transaction_types'].slice(
		      (page - 1) * $scope.itemsPerPage,
		       page * $scope.itemsPerPage
		    );
		    
		    $scope.subject_transaction_types = pagedData;
		}
	}

	$scope.remove_transaction_type = function(list){
		$scope.record.transaction_types.splice($scope.record.transaction_types.indexOf(list), 1);
		$scope.subject_transaction_types.splice($scope.record.transaction_types.indexOf(list), 1);
	}

	$scope.delete = function(record){
		swal({
		    title: "Continue",
		    text: "Remove "+record.name+"?",
		    type: "warning",
		    showCancelButton: true,
		    confirmButtonColor: "#DD6B55",
		    confirmButtonText: "Delete",
		    cancelButtonText: "Cancel",
		    closeOnConfirm: true
		},
		function(){
			$http.post("/company/delete/"+record.id)
			.success(function(response){
				Notification.success(response);
				$scope.read();
			}).error(function(err){
				Notification.error(err)
			})
		})
	}

	$scope.get_intelex_subjects = function()
	{
		me.post_generic("/company/get_intelex_subjects/","","main")
		.success(function(data)
		{
			Notification.success(data)
			$scope.read()
		})

	}

	$scope.read_transaction_types = function(){
    	me.post_generic("/transaction_types/read/","","")
    	.success(function(response){
    		$scope.transaction_types = response.data;
    	})
    }

    $scope.read_subject_transaction_types = function(data){
    	transaction_typesArr = []
    	for(var t_types in data.transaction_types){
    		transaction_typesArr.push(data.transaction_types[t_types].id)
    	}
    	console.log(transaction_typesArr)
    	var datus = {
    		program_id: transaction_typesArr
    	}
    	me.post_generic("/transaction_types/read/",datus,"")
    	.success(function(response){
    		$scope.old_subject_transaction_types = response.data;
    	})
    }

	$scope.read();
	me.main_loader = function(){$scope.read();}
	$scope.read_transaction_types();
	CommonRead.get_display_terms($scope);
});
