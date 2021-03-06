var app = angular.module("recommendations",['common_module']);

app.controller('recommendationsCtrl', function($scope, $http, $timeout, $element, $controller,CommonFunc,Notification,CommonRead) {
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
		
		me.open_dialog("/recommendations/create_dialog/","","main")
	}

	$scope.create = function(){
		me.post_generic("/recommendations/create/",$scope.record,"dialog")
		.success(function(response){
			me.close_dialog();
			Notification.success(response);
			$scope.read();
		})
	}

	$scope.load_to_edit = function(record){
		$scope.create_dialog(record);
	}

	$scope.read = function(){
		var data = {
			value : $scope.filter.value,
			pagination : me.pagination,
			sort : me.sort,
		}
		me.post_generic("/recommendations/read/",data,"main")
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
		},function(){
			me.post_generic("/recommendations/delete/"+record.id)
			.success(function(response){
				Notification.success(response);
				$scope.read();
			}).error(function(err){
				Notification.error(err)
			})
		})
	}

	$scope.read();
	me.main_loader = function(){$scope.read();}
	CommonRead.get_display_terms($scope)
});
