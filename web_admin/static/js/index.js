var app = angular.module("index",['ngAnimate','ngSanitize','ui.bootstrap','ui.select','toastr','oitozero.ngSweetAlert','jutaz.ngSweetAlertAsPromised','ui.router',"common_directives"]);

app.config(['$httpProvider', '$interpolateProvider', function($httpProvider, $interpolateProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $interpolateProvider.startSymbol('{$').endSymbol('$}');
}]);

app.controller('indexCtrl', function($scope,$http,$uibModal,$uibModalStack,SweetAlert,toastr){

	$scope.record 	   			= {};
	$scope.reg_form    			= {};
	$scope.learning_center_form = {};
	$scope.credentials = { "email" : null, password : null };

	function validate_credentials(credentials)
	{
		if (credentials.email == null || credentials.password == null)
		{
			swal("Enter email and password", null, "warning");
			return false;
		}

		return true;
	}
	
	$scope.login = function(credentials)
	{
		if (validate_credentials(credentials))
		{
			$http.post('/login/',credentials)
			.success(function(response){
				toastr.success("Loggin In...");
				$scope.credentials = {};

				var redirect = "/"
				// if(response == 'Technical'){
				// 	redirect = "/assessments"
				// }
				setTimeout(function(){
				    window.location.href = redirect;
				}, 500);
			}).error(function(err){
				swal(err, null, "info")
			})
		}
	};

	$scope.sign_up_learning_center = function(learning_center_form)
	{
		let response = $http.post("/register/", learning_center_form);

		response.success(function (response){
			toastr.success(response);
			setTimeout(function(){
				    window.location.href = "/";
				}, 500);
		});

		response.error(function (response){
			toastr.error(response);
		})
	};

	$scope.reg_company = function(data){
		$http.post('/register/',data)
		.success(function(response){
			toastr.success(response);
			$scope.reg_form = {};
			setTimeout(function(){
			    window.location.href = "/login";
			}, 500);
		}).error(function(err){
			toastr.error(err)
		})
	}


});

app.config(function($stateProvider,$urlRouterProvider) {

    var studentState = {
        name: 'student',
        url: '/student',
        templateUrl: '/sign_in/student/',
    };

    var learningCenterState = {
        name: 'learning_center',
        url: '/learning_center',
        templateUrl: '/sign_in/learning_center/',
    };

    $stateProvider.state(studentState);
    $stateProvider.state(learningCenterState);

    $urlRouterProvider.otherwise('student');

});
