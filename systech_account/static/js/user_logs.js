var app = angular.module("user_logs",['common_module']);

app.controller('UserLogsCtrl', function($scope, $http, $timeout, $element, $controller,CommonFunc,Notification,CommonRead) {
	angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
	let me = this;
	$scope.record = {};
	$scope.filter = {};

	$scope.read = function(){

		let data = {
			pagination: me.pagination,
			code: $scope.filter.code,
		};

		me.post_generic("/user_logs/read/",data,"main")
		.success(function(response){
			$scope.records = response.data;
			me.starting = response.starting;
			me.ending = response.data.length;
			me.pagination.limit_options = angular.copy(me.pagination.limit_options_orig);
			me.pagination.limit_options.push(response.total_records);
			me.pagination["total_records"] = response.total_records;
			me.pagination["total_pages"] = response.total_pages;
		})
	};

	$scope.read();


	me.main_loader = function(){ $scope.read(); };
	CommonRead.get_display_terms($scope)
});
