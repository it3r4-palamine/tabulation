var app = angular.module("users",['common_module']);

app.controller('usersCtrl', function($scope, $http, $timeout, $element, $controller,CommonFunc,Notification,CommonRead) {
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
		
		me.open_dialog("/users/create_dialog/","","main")
	}

	$scope.create = function(){
		if($scope.record.password1 != $scope.record.password2) return Notification.error("Password do not match.")
		me.post_generic("/users/create/",$scope.record,"dialog")
		.success(function(response){
			me.close_dialog();
			Notification.success(response);
			$scope.read();
		}).error(function(err){
			Notification.error(err)
		})
	}

	$scope.get_intelex_students = function()
	{
		me.post_generic("/users/get_intelex_students/","","main")
		.success(function(data)
		{
			Notification.success(data)
			$scope.read()
		})

	}

	$scope.load_to_edit = function(record){
		$scope.create_dialog(record);
	}

	$scope.change_pass_dialog = function(record){
		$scope.pwd_form = record
		me.open_dialog("/users/change_pass_dialog/","","main")
	}

	$scope.change_password = function(){
		if(!$scope.pwd_form.password1 || !$scope.pwd_form.password2) return Notification.error("Please input password.")
		if($scope.pwd_form.password1 != $scope.pwd_form.password2) return Notification.error("Password do not match.")
	    me.post_generic('/users/change_password/', $scope.pwd_form,"dialog").then(function(response){
	        me.close_dialog();
	        Notification.success(response.data)
	        $scope.pwd_form.password1 = "";
	        $scope.pwd_form.password2 = "";
	    }, function(err_res){
	        console.log(err_res); Notification.error(err_res.data);
	    })
	}

	$scope.read = function(){
		var data = {
			pagination: me.pagination,
			code: $scope.filter.code,
		}
		me.post_generic("/users/read/",data,"main")
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

	$scope.checkAdmin = function(){
		if($scope.record.is_admin){
			$scope.record.is_edit = true
		}else{
			$scope.record.is_edit = false
		}
	}

	$scope.delete = function(record){
		swal({
		    title: "Continue",
		    text: "Remove "+record.fullname+"?",
		    type: "warning",
		    showCancelButton: true,
		    confirmButtonColor: "#DD6B55",
		    confirmButtonText: "Delete",
		    cancelButtonText: "Cancel",
		    closeOnConfirm: true
		},
		function(){
			$http.post("/users/delete/"+record.id)
			.success(function(response){
				Notification.success(response);
				$scope.read();
			}).error(function(err){
				Notification.error(err)
			})
		})
	}

	$scope.read_transaction_types = function(){
    	me.post_generic("/transaction_types/read/","","main")
    	.success(function(response){
    		$scope.transaction_types = response.data;
    	})
    }

	$scope.read_user_types = function(){
    	me.post_generic("/users/read_user_types/","","main")
    	.success(function(response){
    		$scope.user_types = response;
    	})
    }

	$scope.read();
	// $scope.read_transaction_types();
	$scope.read_user_types();
	me.main_loader = function(){$scope.read();}
	CommonRead.get_display_terms($scope)
});
