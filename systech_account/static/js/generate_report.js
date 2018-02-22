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
			$('body').loadingModal({text: 'Generating report...'});
			$('body').loadingModal('animation', 'cubeGrid');
			$('body').loadingModal('backgroundColor', 'green');
		me.post_generic(url,data,'main')
		.success(function(response){
			$scope.records = response.data;
			$scope.scores = response.scores;
			$scope.company_assessment = response.company_assessment
			$scope.time_in = convertSecondstoHours($scope.company_assessment.session_credits)
			$scope.time_out = convertSecondstoHours($scope.company_assessment.credits_left)
			$scope.time_consumed = convertSecondstoHours($scope.company_assessment.session_credits - $scope.company_assessment.credits_left)

    		for(var x in $scope.records){
    			for(var y in $scope.scores){
    				if($scope.scores[y].question == $scope.records[x].id){
    					var z = ($scope.scores[y].score / $scope.records[x].answers.length)
    					$scope.records[x].percentage = z
    					$scope.records[x].score = $scope.scores[y].score
    				}
    			}
    			if ($scope.records[x].uploaded_question){
	    			for(var ans in $scope.records[x].answers){
	    				$scope.records[x].answers[ans]['correct_answer'] = false
	    				for(var answer in $scope.records[x].answers[ans].answer){
		    				for(var images in $scope.records[x].image_answers){
		    					if($scope.records[x].image_answers[images].item_no == $scope.records[x].answers[ans].item_no){
			    					if($scope.records[x].answers[ans].answer[answer].name.toLowerCase().score($scope.records[x].image_answers[images].answer.toLowerCase()) >= 0.88){
					    				$scope.records[x].answers[ans]['correct_answer'] = true
			    					}
		    					}
		    				}
	    				}
	    			}
    			}
    		}

    		$('body').loadingModal('hide');
    		$('body').loadingModal('destroy') ;
			if(print){
				setTimeout(function(){
                	if($scope.records){
                		check_table_height()
                		// window.print();
                	}
                },1000)
			}
		}).error(function(err){
			$('body').loadingModal('hide');
			$('body').loadingModal('destroy') ;
			if(err == "Assessment_answer matching query does not exist."){
				Notification.error("Some answers are not yet sycned.")
			}
		})
	};

	convertSecondstoHours = function(d){
			d = Number(d);
		    var h = Math.floor(d / 3600);
		    var m = Math.floor(d % 3600 / 60);
		    var s = Math.floor(d % 3600 % 60);

		    var hDisplay = h > 0 ? h + (h == 1 ? " hour, " : " hours, ") : "";
		    var mDisplay = m > 0 ? m + (m == 1 ? " minute, " : " minutes, ") : "";
		    var sDisplay = s > 0 ? s + (s == 1 ? " second" : " seconds") : "";
		    return hDisplay + mDisplay + sDisplay; 
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
			// if(print){
			// 	setTimeout(function(){
   //              	window.print();
   //              },1000)
			// }
		})
	}

	$scope.instantiate = function(print){
		$scope.read(print);
		$scope.read_transaction_types();
		$scope.read_recommendations(print);
	}
});

app.filter('percentage', ['$filter', function ($filter) {
  return function (input, decimals) {
    return $filter('number')(input * 100, decimals) + '%';
  };
}]);