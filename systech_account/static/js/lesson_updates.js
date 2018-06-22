var app = angular.module("lessonUpdateApp", ['common_module']);

app.controller('lessonUpdateCtrl', function($scope, $http, $timeout, $element, $controller, CommonFunc, Notification, CommonRead)
{
	angular.extend(this, $controller('CommonCtrl', { $scope: $scope }));
	var me = this;
	$scope.lessonUpdateArr = [];
	$scope.lessonUpdateActivityArr = [];


	me.main_loader = function()
	{
		$scope.read();
	}

	$scope.loadLessonUpdateActivities = function()
	{
		me.post_generic("/lesson_updates/load_lesson_update_activities/", {}, "main")
		.success(function(response)
		{
			$scope.lessonUpdateActivityArr = response;
		})
	}

	$scope.read = function()
	{
		var data = { pagination: me.pagination }
	
		me.post_generic("/lesson_updates/read/", data, "main")
		.success(function(response)
		{
			$scope.lessonUpdateArr = response.data;
			me.starting = response.starting;
			me.ending = response.data.length;
			me.pagination.limit_options = angular.copy(me.pagination.limit_options_orig);
			me.pagination.limit_options.push(response.total_records)
			me.pagination["total_records"] = response.total_records;
			me.pagination["total_pages"] = response.total_pages;
		})
	};


	$scope.loadLessonUpdateActivities();
	$scope.read();
});
