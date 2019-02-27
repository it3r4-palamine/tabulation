angular.module("enrollment")

.controller("student_reportsCtrl", function($scope, $http, $timeout,$controller,$uibModal,$uibModalStack,$templateCache,Notification,CommonRead,CommonFunc){
	angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
	var self = this;
	var me = this;

	CommonRead.get_users2($scope);
	CommonRead.get_company2($scope);
	CommonRead.get_schools($scope);
	CommonRead.get_grade_level($scope);

	$scope.reports = [];

	$scope.read_enrollment_report = function(reset)
	{
		if(reset){me.reset_filter()}
		me.filters["sort"] = me.sort;
		var filters = angular.copy(me.filters);
		filters = me.format_date(filters);
		filters = me.format_time(filters);
		filters["pagination"] = me.pagination;
		var post = me.post_generic("/enrollments/read_enrollment_report/",filters,"main");
		post.success(function(response){
			$scope.reports = response.records;
			me.starting = response.starting;
			me.ending = response.records.length;
			me.pagination.limit_options = angular.copy(me.pagination.limit_options_orig);
			me.pagination.limit_options.push(response.total_records)
			me.pagination["total_records"] = response.total_records;
			me.pagination["total_pages"] = response.total_pages;
			// self.response = response;
			// self.generate_pagination(self,response,"records");
		});
	}

	me.main_loader = function()
	{
		me.read_enrollment_report();
	}

});