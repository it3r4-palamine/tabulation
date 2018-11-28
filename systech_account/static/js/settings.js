var routerApp = angular.module('settings',['common_module','ui.router']);

routerApp.config(function($stateProvider, $urlRouterProvider){
	var current_url = window.location.href;
	if(current_url.indexOf("#") >= 0){
	    var splitted_url = current_url.split("#");
	    var tab_header = splitted_url[1];
	    if(tab_header == "/display_settings"){
	        $urlRouterProvider.otherwise('/display_settings');
	    }
	    else if(tab_header == "/user_types"){
	        $urlRouterProvider.otherwise('/user_types');
	    }
	    else if(tab_header == "/math_symbols"){
	        $urlRouterProvider.otherwise('/math_symbols');
	    }
	    else if(tab_header == "/to_dos"){
	        $urlRouterProvider.otherwise('/to_dos');
	    }
	    else if(tab_header == "/schools"){
	        $urlRouterProvider.otherwise('/schools');
	    }
	}else{
	    $urlRouterProvider.otherwise('/display_settings');
	}

	$stateProvider
		.state('display_settings', {
			url: '/display_settings',
			templateUrl: '/settings/display_settings',
			controller: 'displaysettingsCtrl',
		})

		.state('user_types', {
			url: '/user_types',
			templateUrl: '/settings/user_types',
			// controller: 'usertypesCtrl',
		})

		.state('math_symbols', {
			url: '/math_symbols',
			templateUrl: '/settings/math_symbols',
			// controller: 'mathsymbolsCtrl',
		})

		.state('to_dos', {
			url: '/to_dos',
			templateUrl: '/settings/to_dos',
			// controller: 'mathsymbolsCtrl',
		})

		.state('schools', {
			url: '/schools',
			templateUrl: '/settings/schools',
			// controller: 'mathsymbolsCtrl',
		})
});

routerApp.controller('settingsCtrl', function($scope, $controller, CommonRead) {
	angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));

	CommonRead.get_display_terms($scope)
})

routerApp.controller('displaysettingsCtrl', function($scope, $http, $timeout, $controller,CommonFunc,Notification,CommonRead) {
	angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
	var me = this;

	$scope.record = {}
	$scope.create_dialog = function(record){
		$scope.record = {}
		$scope.record['is_active'] = true
		if(record){
			$scope.record = angular.copy(record);
		}
		
		me.open_dialog("/user_types/create_dialog/","","main")
	}

	$scope.create = function(){
		me.post_generic("/user_types/create/",$scope.record,"dialog")
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
		me.post_generic("/settings/display_settings_read/","","main")
		.success(function(response){
			$scope.records = response.data;
		})
	};

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
			$http.post("/user_types/delete/"+record.id)
			.success(function(response){
				Notification.success(response);
				$scope.read();
			}).error(function(err){
				Notification.error(err)
			})
		})
	}

	$scope.save_terms = function(){
		me.post_generic("/settings/save_display_terms/",$scope.records[0],"main")
		.success(function(response){
			Notification.success(response)
			$scope.read()
		})
	}

	$scope.read();
	me.main_loader = function(){$scope.read();}
	// CommonRead.get_display_terms($scope)
})

routerApp.controller('usertypesCtrl', function($scope, $http, $timeout, $controller,CommonFunc,Notification,CommonRead) {
	angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
	var me = this;

	$scope.record = {}
	$scope.create_dialog = function(record){
		$scope.record = {}
		$scope.record['is_active'] = true
		if(record){
			$scope.record = angular.copy(record);
		}
		
		me.open_dialog("/settings/user_types_create_dialog/","","main")
	}

	$scope.create = function(){
		me.post_generic("/settings/user_types_create/",$scope.record,"dialog")
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
		me.post_generic("/settings/read_user_types/",{'pagination':me.pagination},"main")
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
		    text: "Remove "+record.name+"?",
		    type: "warning",
		    showCancelButton: true,
		    confirmButtonColor: "#DD6B55",
		    confirmButtonText: "Delete",
		    cancelButtonText: "Cancel",
		    closeOnConfirm: true
		},function(){
			$http.post("/settings/user_types_delete/"+record.id)
			.success(function(response){
				Notification.success(response);
				$scope.read();
			}).error(function(err){
				Notification.error(err)
			})
		})
	}

	$scope.close_dialog = function(){
		me.close_dialog();
	}

	$scope.read();
	me.main_loader = function(){$scope.read();}
	// CommonRead.get_display_terms($scope);
})

routerApp.controller('mathsymbolsCtrl', function($scope, $http, $timeout, $controller,CommonFunc,Notification,CommonRead) {
	angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
	var me = this;

	$scope.record = {}
	$scope.create_dialog = function(record){
		$scope.record = {}
		$scope.record['is_active'] = true
		if(record){
			$scope.record = angular.copy(record);
		}
		
		me.open_dialog("/settings/math_symbols_create_dialog/","","main")
	}

	$scope.create = function(){
		// if(!$scope.record.above_text) $scope.record.syntax = null
		me.post_generic("/settings/math_symbols_create/",$scope.record,"dialog")
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
		me.post_generic("/settings/read_math_symbols/",{'pagination':me.pagination},"main")
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
		    text: "Remove "+record.name+"?",
		    type: "warning",
		    showCancelButton: true,
		    confirmButtonColor: "#DD6B55",
		    confirmButtonText: "Delete",
		    cancelButtonText: "Cancel",
		    closeOnConfirm: true
		},function(){
			$http.post("/settings/math_symbols_delete/"+record.id)
			.success(function(response){
				Notification.success(response);
				$scope.read();
			}).error(function(err){
				Notification.error(err)
			})
		})
	}

	$scope.close_dialog = function(){
		me.close_dialog();
	}

	$scope.read();
	me.main_loader = function(){$scope.read();}
	// CommonRead.get_display_terms($scope);
})

routerApp.controller('todosCtrl', function($scope, $http, $timeout, $controller,CommonFunc,Notification,CommonRead) {
	angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
	var me = this;

	$scope.record = {}
	$scope.create_dialog = function(record){
		$scope.record = {}
		$scope.record['is_active'] = true
		if(record){
			$scope.record = angular.copy(record);
		}
		
		me.open_dialog("/settings/to_dos_create_dialog/","","main")
	}

	$scope.create = function(){
		me.post_generic("/settings/to_dos_create/",$scope.record,"dialog")
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
		me.post_generic("/settings/read_to_dos/",{'pagination':me.pagination},"main")
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
		    text: "Remove "+record.name+"?",
		    type: "warning",
		    showCancelButton: true,
		    confirmButtonColor: "#DD6B55",
		    confirmButtonText: "Delete",
		    cancelButtonText: "Cancel",
		    closeOnConfirm: true
		},function(){
			$http.post("/settings/to_dos_delete/"+record.id)
			.success(function(response){
				Notification.success(response);
				$scope.read();
			}).error(function(err){
				Notification.error(err)
			})
		})
	}

	$scope.close_dialog = function(){
		me.close_dialog();
	}

	$scope.read();
	me.main_loader = function(){$scope.read();}
	// CommonRead.get_display_terms($scope);
})

routerApp.controller('schoolsCtrl', function($scope, $http, $timeout, $controller,CommonFunc,Notification,CommonRead) {
	angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
	var me = this;

	$scope.record = {}
	$scope.create_dialog = function(record){
		$scope.record = {}
		$scope.record['is_active'] = true
		if(record){
			$scope.record = angular.copy(record);
		}
		
		me.open_dialog("/settings/schools_create_dialog/","","main")
	}

	$scope.create = function(){
		me.post_generic("/settings/schools_create/",$scope.record,"dialog")
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
		me.post_generic("/settings/read_schools/",{'pagination':me.pagination},"main")
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
		    text: "Remove "+record.name+"?",
		    type: "warning",
		    showCancelButton: true,
		    confirmButtonColor: "#DD6B55",
		    confirmButtonText: "Delete",
		    cancelButtonText: "Cancel",
		    closeOnConfirm: true
		},function(){
			$http.post("/settings/schools_delete/"+record.id)
			.success(function(response){
				Notification.success(response);
				$scope.read();
			}).error(function(err){
				Notification.error(err)
			})
		})
	}

	$scope.close_dialog = function(){
		me.close_dialog();
	}

	$scope.read();
	me.main_loader = function(){$scope.read();}
	// CommonRead.get_display_terms($scope);
})