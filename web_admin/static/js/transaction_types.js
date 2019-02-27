var app = angular.module("transaction_types",['common_module']);

app.controller('transaction_typesCtrl', function($scope, $http, $timeout, $element, $controller,CommonFunc,Notification,CommonRead) {
	angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
	var me = this;
	$scope.record = {}
	$scope.filter = {}
	$scope.create_dialog = function(record){
		$scope.record = {}
		$scope.record['is_active'] = true
		if(record){
			$scope.record = angular.copy(record);
		}
		
		me.open_dialog("/transaction_types/create_dialog/","","main")
	}

	$scope.create = function(){
		me.post_generic("/transaction_types/create/",$scope.record,"dialog")
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
		// me.sort.sort_by = "name"
		var data = {
			name : $scope.filter.name,
			pagination : me.pagination,
			sort : me.sort,
		}
		me.post_generic("/transaction_types/read/",data,"main")
		.success(function(response){
			$scope.records = response.data;
			me.starting = response.starting;
			me.ending = response.data.length;
			me.pagination.limit_options = angular.copy(me.pagination.limit_options_orig);
			me.pagination.limit_options.push(response.total_records)
			me.pagination["total_records"] = response.total_records;
			me.pagination["total_pages"] = response.total_pages;
			$scope.selectAll()
		})
	};

	$scope.selectAll = function(){
		$scope.selected = 0
		for(var record in $scope.records){
			$scope.records[record].is_selected = $scope.select_all
			if($scope.records[record].is_selected){
				$scope.selected++
			}
		}
	}

	$scope.selected = 0
	$scope.select = function(){
		$scope.selected = 0
		checkSelected(0)

		function checkSelected(idx){
			if(idx == $scope.records.length){
				if($scope.selected == $scope.records.length){
					$scope.select_all = true
				}else{
					$scope.select_all = false
				}
			}else{
				if($scope.records[idx].is_selected){
					$scope.selected++
				}
				checkSelected(++idx)
			}
		}
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
		},function(){
			me.post_generic("/transaction_types/delete/"+record.id,"","main")
			.success(function(response){
				Notification.success(response);
				$scope.read();
			}).error(function(err){
				Notification.error(err)
			})
		})
	}

	$scope.delete_selected = function(){
		var transactionTypesArr = []
		for(var record in $scope.records){
			if($scope.records[record].is_selected){
				transactionTypesArr.push($scope.records[record].id)
			}
		}
		var term = !$scope.display_terms[0].transaction_types ? 'Transaction Type' : $scope.display_terms[0].transaction_types
		swal({
		    title: "Continue",
		    text: "Remove selected "+ term +"?",
		    type: "warning",
		    showCancelButton: true,
		    confirmButtonColor: "#DD6B55",
		    confirmButtonText: "Delete",
		    cancelButtonText: "Cancel",
		    closeOnConfirm: true
		},function(){
			me.post_generic("/transaction_types/delete_selected/",{ids:transactionTypesArr},"main")
			.success(function(response){
				Notification.success(response);
				$scope.read();
			}).error(function(err){
				Notification.error(err)
			})
		})
	}

	$scope.get_intelex_exercises = function()
	{
		me.post_generic("/transaction_types/get_intelex_exercises/","","main")
		.success(function(data)
		{
			Notification.success(data)
			$scope.read()
		})

	}

	$scope.read();
	me.main_loader = function(){$scope.read();}
	CommonRead.get_display_terms($scope);
});
