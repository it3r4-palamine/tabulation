var app = angular.module("generate_report",['common_module']);

app.controller('generate_reportCtrl', function($scope, $http, $timeout, $element, $controller,CommonFunc,Notification,CommonRead) {
	angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
	var me = this;
	$scope.record = {}
	$scope.generate_report = {}
	$scope.generated_recommendations = {}

	$scope.recommendation = []
	$scope.create_dialog = function(record){
		$scope.download_link = record
		me.open_dialog("/generate_report/download_dialog/","","main")
	}

	$scope.close_dialog = function(){$uibModalStack.dismissAll();}

	$scope.read = function(print){
		// var url = "/assessments/read/" 
		// var data = {
		// 	"type" : "generate_report"
		// }
			var url = "/generate_report/read_assessments/"
			var data = $scope.generate_report
		data['type'] = 'ppt'
		if(print){
			data['type'] = 'pdf'
		}
		me.post_generic(url,data,'main')
		.success(function(response){
			$scope.records = response.data;
			$scope.scores = response.scores;
		}).error(function(err){
			if(err == "Assessment_answer matching query does not exist."){
				Notification.error("Some answers are not yet sycned.")
			}
		})
	};

	$scope.generate = function(){
		var data = {
			'recommendations' : $scope.recommendation,
			'datus' : $scope.generate_report
		}
		me.post_generic("/generate_report/generate/",data,"main")
		.success(function(response){
			$scope.create_dialog(response)
			// $scope.records = response.data;
		})
	}

	$scope.close_download_dialog = function(){
		var data = $scope.download_link
		me.post_generic("/generate_report/delete_report/",data,"dialog")
		.success(function(response){
			me.close_dialog()
		})
	}

	$scope.check_recommendation = function(record){
		if(record.is_recommended){
			$scope.recommendation.push(record)
		}else{
			$scope.recommendation.splice($scope.recommendation.indexOf(record),1)
		}
	}

	$scope.read_transaction_types = function(record){
    	me.post_generic("/transaction_types/read/",{"ids":$scope.generate_report.transaction_type},"main")
    	.success(function(response){
    		$scope.transaction_types = response.data;
    	})
    }

	$scope.read_recommendations = function(print){
		me.post_generic("/recommendations/read/","","main")
		.success(function(response){
			$scope.recommendations = response.data;
			$scope.read_chosen_recommendations(print);
		})
	}

	$scope.read_chosen_recommendations = function(print){
		me.post_generic("/generate_report/read_chosen_recommendations/",{'id':$scope.generate_report.id},"main")
		.success(function(response){
			$scope.generated_recommendations = response.data
			for(x in $scope.recommendations){
				for(y in $scope.generated_recommendations){
					if($scope.recommendations[x].id == $scope.generated_recommendations[y].id){
						$scope.recommendations[x]['is_recommended'] = true
						$scope.check_recommendation($scope.recommendations[x])
					}
				}
			}
			if(print){
				setTimeout(function(){
                	window.print();
                },1000)
			}
		})
	}

	$scope.instantiate = function(print){
		$scope.read(print);
		$scope.read_transaction_types();
		$scope.read_recommendations(print);
	}
});
