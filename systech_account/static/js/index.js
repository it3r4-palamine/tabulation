var app = angular.module("index",['ngAnimate','ngSanitize','ui.bootstrap','ui.select','toastr','oitozero.ngSweetAlert','jutaz.ngSweetAlertAsPromised',]);

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
			toastr.success(response)
			$scope.credentials = {};
			setTimeout(function(){
			    window.location.href = "/assessments";
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
