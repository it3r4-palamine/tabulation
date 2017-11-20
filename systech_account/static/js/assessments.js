var app = angular.module("assessments",['common_module']);

app.controller('assessmentsCtrl', function($scope, $http, $timeout, $element, $controller,CommonFunc,Notification,CommonRead) {
	angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
	var me = this;
	$scope.record = {}
	$scope.filter = {}

	$scope.choices = []
	$scope.effects = []
	$scope.findings = []

	$scope.create_dialog = function(record){
		$scope.choices = []
		$scope.effects = []
		$scope.findings = []
		$scope.choice_list = {}
		$scope.effect_list = {}
		$scope.finding_list = {}
		$scope.record = {}
		$scope.record['is_active'] = true
		if(record){
			$scope.record = angular.copy(record);
			$scope.choices = $scope.record.choices
			$scope.effects = $scope.record.effects
			$scope.findings = $scope.record.findings
		}
		
		me.open_dialog("/assessments/create_dialog/","","main")
	}

	$scope.close_dialog = function(){$uibModalStack.dismissAll();}

	$scope.create = function(){
		if(Object.keys($scope.choice_list).length > 0) $scope.choices.push(angular.copy($scope.choice_list))
		if(Object.keys($scope.effect_list).length > 0) $scope.effects.push(angular.copy($scope.effect_list))
		if(Object.keys($scope.finding_list).length > 0) $scope.findings.push(angular.copy($scope.finding_list))
		var has_true = 0
		for(x in $scope.choices){
			if($scope.choices[x].is_answer == true){
				has_true++
			}
		}
		$scope.choice_list = {}
		$scope.effect_list = {}
		$scope.finding_list = {}
		if($scope.record.is_multiple){
			if(has_true > 1){
				$scope.record['has_multiple_answer'] = true
			}else if(has_true == 0){
				$scope.record['has_multiple_answer'] = false
				return Notification.error("The question has no correct answer. Please select one.")
			}else if(has_true == 1){
				$scope.record['has_multiple_answer'] = false
			}
		}

		if($scope.record.is_general == false) $scope.record.transaction_types = []

		$scope.record['choices'] = $scope.choices
		$scope.record['effects'] = $scope.effects
		$scope.record['findings'] = $scope.findings

		me.post_generic("/assessments/create/",$scope.record,"dialog")
		.success(function(response){
			me.close_dialog();
			Notification.success(response);
			$scope.read();
		}).error(function(err){
			if(err=='code'){
				Notification.error("Code already exists.")
			}else{
				Notification.error(err)
			}
		})
	}

	$scope.load_to_edit = function(record){
		$scope.create_dialog(record);
	}

	$scope.filter.transaction_type = {'name':'ALL'}
	$scope.filter.is_general = true
	$scope.read = function(){
		var data = {
			pagination:me.pagination,
			transaction_type:$scope.filter.transaction_type['id'] ? $scope.filter.transaction_type['id'] : null,
			// show_general:$scope.filter.is_general
		}
		me.post_generic("/assessments/read/",data,"main")
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

	$scope.delete = function(record){
		swal({
		    title: "Continue",
		    text: "Remove "+record.value+"?",
		    type: "warning",
		    showCancelButton: true,
		    confirmButtonColor: "#DD6B55",
		    confirmButtonText: "Delete",
		    cancelButtonText: "Cancel",
		    closeOnConfirm: true
		},
			function(){
				me.post_generic("/assessments/delete/"+record.id,"","main")
				.success(function(response){
					Notification.success(response);
					$scope.read();
				})
			}
		);

	}

	$scope.isMultiple = function(){
		console.log($scope.record.is_multiple)
	}

	$scope.add_choice = function(list){
		$scope.choices.push(angular.copy(list))
	    $scope.choice_list = {}
	}

	$scope.add_effect = function(list){
		$scope.effects.push(angular.copy(list))
	    $scope.effect_list = {}
	}

	$scope.add_finding = function(list){
		$scope.findings.push(angular.copy(list))
	    $scope.finding_list = {}
	}

	$scope.remove_choice = function(list,index){
		if(list.id){
			me.post_generic("/assessments/delete_choice/"+list.id,{},"dialog")
			.success(function(response){
	    		$scope.choices.splice($scope.choices.indexOf(list), 1);
			})
		}else{
	    	$scope.choices.splice($scope.choices.indexOf(list), 1);
		}
    }

	$scope.remove_effect = function(list,index){
		if(list.id){
			me.post_generic("/assessments/delete_effect/"+list.id,{},"dialog")
			.success(function(response){
	    		$scope.effects.splice($scope.effects.indexOf(list), 1);
			})
		}else{
	    	$scope.effects.splice($scope.effects.indexOf(list), 1);
		}
    }

	$scope.remove_finding = function(list,index){
		if(list.id){
			me.post_generic("/assessments/delete_finding/"+list.id,{},"dialog")
			.success(function(response){
	    		$scope.findings.splice($scope.findings.indexOf(list), 1);
			})
		}else{
	    	$scope.findings.splice($scope.findings.indexOf(list), 1);
		}
    }

    $scope.read_transaction_types = function(){
    	me.post_generic("/transaction_types/read/","","main")
    	.success(function(response){
    		$scope.transaction_types = response.data;
    	})
    }

	$scope.read();
    me.main_loader = function(){$scope.read();}
    CommonRead.get_transaction_types($scope);
    CommonRead.get_transaction_types2($scope);
	// $scope.read_transaction_types();
});
