var app = angular.module("index",['ngAnimate','ngSanitize','ui.bootstrap','ui.select','toastr','oitozero.ngSweetAlert','jutaz.ngSweetAlertAsPromised','ui.router']);

app.config(['$httpProvider', '$interpolateProvider', function($httpProvider, $interpolateProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $interpolateProvider.startSymbol('{$').endSymbol('$}');
}]);

app.controller('indexCtrl', function($scope,$http,$uibModal,$uibModalStack,SweetAlert,toastr){
	$scope.record = {}
	$scope.credentials = {};
	$scope.reg_form = {};
	
	$scope.login = function(credentials){

		$http.post('/login/',credentials)
		.success(function(response){
			toastr.success("Loggin In...")
			$scope.credentials = {};
			console.log(response)
			var redirect = "/company_assessment"
			if(response == 'Technical'){
				redirect = "/assessments"
			}
			setTimeout(function(){
			    window.location.href = redirect;
			}, 500);
		}).error(function(err){
			toastr.error(err)
		})
	}

	$scope.reg_company = function(data){
		$http.post('/register/',data)
		.success(function(response){
			toastr.success(response)
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
