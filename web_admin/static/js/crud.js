// var app = angular.module("crudapp",['ngAnimate','ngSanitize','ui.bootstrap','ui.select','toastr','oitozero.ngSweetAlert','jutaz.ngSweetAlertAsPromised',]);
var app = angular.module("crudapp",[
		'common_module',
	]);

app.config(['$httpProvider', '$interpolateProvider', function($httpProvider, $interpolateProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $interpolateProvider.startSymbol('{$').endSymbol('$}');
}]);

app.controller('crudCtrl', function($scope,$http,$uibModal,$uibModalStack,SweetAlert,toastr){
	$scope.record = {}
	$scope.create_dialog = function(record){
		$scope.record = {}
		if(record){
			$scope.record = angular.copy(record);
		}
		
		var dialog = $uibModal.open({
	        templateUrl: "/crud/create_dialog/",
	        backdrop : 'static',
	        keyboard : false,
	        scope : $scope,
	    })
	}

	$scope.close_dialog = function(){$uibModalStack.dismissAll();}

	$scope.create = function(){
		$http.post("/crud/create/",$scope.record)
		.success(function(response){
			$scope.close_dialog();
			toastr.success(response);
			$scope.read();
		})
	}

	$scope.load_to_edit = function(record){
		$scope.create_dialog(record);
	}


	$scope.read = function(){
		$http.post("crud/read/")
		.success(function(response){
			console.log(response)
			$scope.records = response;
		})
	};

	$scope.delete = function(record){
		var sweetalert = SweetAlert.swal({
		    title: "Continue",
		    text: "Remove "+record.name+"?",
		    type: "warning",
		    showCancelButton: true,
		    confirmButtonColor: "#DD6B55",
		    confirmButtonText: "Delete",
		    cancelButtonText: "Cancel",
		    closeOnConfirm: true
		});

		sweetalert.then(function(){
			$http.post("crud/delete/"+record.id)
			.success(function(response){
				toastr.success(response);
				$scope.read();
			})
		})
	}

	$scope.read();
});
