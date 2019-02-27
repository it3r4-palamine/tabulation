angular.module('form', ['customFilters'])

.config(['$httpProvider', '$interpolateProvider', function($httpProvider, $interpolateProvider) {

	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
	$interpolateProvider.startSymbol('{$').endSymbol('$}');

}])

.controller('FormCtrl',function($scope,$http,$timeout) {

	var self = this;
	$scope.hidethis = false;
	self.enrollment = {};

	self.load_data = function()
	{
		self.form_data = angular.fromJson(sessionStorage.form_data);
		self.form_data.session_date = new Date(self.form_data.session_date);
		self.form_data.session_timein = new Date(self.form_data.session_timein);
		self.form_data.session_timeout = new Date(self.form_data.session_timeout);
		check_table_height();
	}

	self.get_enrollment = function(){
		self.enrollment = angular.fromJson(sessionStorage.enrollment);
		self.session_start_date = new Date(self.enrollment.session_start_date);
		self.session_end_date = new Date(self.enrollment.session_end_date);
		$scope.student_age = getAge(self.enrollment.student.date_of_birth);
		window.print();
	}

	function getAge(dateString){
	    var today = new Date();
	    var birthDate = new Date(dateString);
	    var age = today.getFullYear() - birthDate.getFullYear();
	    var m = today.getMonth() - birthDate.getMonth();
	    if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())){
	        age--;
	    }
	    
	    return age;
	}

	function check_table_height()
	{
		$timeout(function(){
			var table = document.getElementById("table-data");
			$scope.table_height = table.offsetHeight;

			if($scope.table_height >= 500)
			{
				$scope.hidethis = true;
			}

			if ($scope.table_height >= 490 || $scope.table_height <= 500) 
			{
				$scope.footer_position_absolute = true;
			} else {
				$scope.footer_position_absolute = false;
			}

			$scope.$apply();
			window.print();
			
		},400)
	}


});