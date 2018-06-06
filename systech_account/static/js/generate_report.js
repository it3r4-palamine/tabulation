var app = angular.module("generate_report",['common_module']);

app.controller('generate_reportCtrl', function($scope, $http, $timeout, $element, $controller,CommonFunc,Notification,CommonRead) {
	angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
	var me = this;
	$scope.record = {}
	$scope.generate_report = {}
	$scope.generated_recommendations = {}

	$scope.filter = {}
	// $scope.filter.date_from = new Date()
	// $scope.filter.date_to = new Date()

	$scope.recommendation = []
	$scope.create_dialog = function(record){
		$scope.download_link = record
		me.open_dialog("/generate_report/download_dialog/","","main")
	}

	$scope.minimum_date = function(){
        $scope.filter.option_to = {
            minDate : new Date($scope.filter.date_from)
        }
	}

	$scope.close_dialog = function(){$uibModalStack.dismissAll();}

	$scope.read = function(print,searchFilter){
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

		if($scope.filter.date_from && $scope.filter.date_to){
			data['date_from'] = moment($scope.filter.date_from).format("YYYY-MM-DD")
			data['date_to'] = moment($scope.filter.date_to).format("YYYY-MM-DD")
		}

		$scope.date_from = $scope.getQueryVariable('date_from');
		$scope.date_to = $scope.getQueryVariable('date_to');

		if($scope.date_from != ""){
			$scope.d_from = moment(JSON.parse($scope.date_from)).format("YYYY-MM-DD")
			data['date_from'] = $scope.d_from
		}
		if($scope.date_to != ""){
			$scope.d_to = moment(JSON.parse($scope.date_to)).format("YYYY-MM-DD")
			data['date_to'] = $scope.d_to
		}

		me.post_generic(url,data,'main')
		.success(function(response){
			$scope.records = response.data;
			$scope.scores = response.scores;
			$scope.company_assessment = response.company_assessment
			$scope.time_in = convertSecondstoHours($scope.company_assessment.session_credits)
			$scope.time_out = convertSecondstoHours($scope.company_assessment.credits_left)
			$scope.time_consumed = convertSecondstoHours($scope.company_assessment.session_credits - $scope.company_assessment.credits_left)

			if(searchFilter){
				$scope.transaction_types = response.transaction_types
			}

    		for(var x in $scope.records){
    			for(var y in $scope.scores){
    				if($scope.scores[y].question == $scope.records[x].id){
    					var percnt = 0
    					$scope.records[x].has_findings = false
    					if($scope.records[x].answers){
    						percnt = $scope.records[x].answers.length
    						if($scope.scores[y].score == $scope.records[x].answers.length){
    							$scope.records[x].has_findings = true
    						}
    					}
    					var z = ($scope.scores[y].score / percnt)
    					$scope.records[x].percentage = z
    					$scope.records[x].score = $scope.scores[y].score
    				}
    			}
    			if ($scope.records[x].uploaded_question){
	    			for(var ans in $scope.records[x].answers){
	    				$scope.records[x].answers[ans]['correct_answer'] = false
	    				$scope.records[x].answers[ans]['is_correct'] = false
	    				for(var answer in $scope.records[x].answers[ans].answer){
		    				for(var images in $scope.records[x].image_answers){
		    					if($scope.records[x].image_answers[images].item_no == $scope.records[x].answers[ans].item_no){
		    						var string1 = $scope.records[x].answers[ans].answer[answer].name.toLowerCase()
		    						var string2 = $scope.records[x].image_answers[images].answer.toLowerCase()

		    						var perc = Math.round($scope.similarity(string1,string2)*10000)/100;
			    					if($scope.records[x].answers[ans].answer[answer].name.toLowerCase().score($scope.records[x].image_answers[images].answer.toLowerCase()) >= 0.88){
					    				$scope.records[x].answers[ans]['correct_answer'] = true
					    				$scope.records[x].answers[ans]['is_correct'] = true
			    					}else if(perc >= 80.00){
			    						$scope.records[x].answers[ans]['correct_answer'] = true
			    						$scope.records[x].answers[ans]['is_correct'] = true
			    					}
		    					}
		    				}
	    				}
	    			}
    			}
    		}

    		// if(print && ($scope.date_from != "" && $scope.date_to != "")){
    		if(data['date_from'] != "" && data['date_to'] != ""){
    			for(var t_type in $scope.records){
    				var total_seconds = 0
    				var total_time =0
	    			for(var session in $scope.company_assessment.sessions){
	    				if($scope.company_assessment.sessions[session].date >= data['date_from'] && $scope.company_assessment.sessions[session].date <= data['date_to']){
		    				if($scope.records[t_type].id == $scope.company_assessment.sessions[session].question){
		    					var start_hms = $scope.company_assessment.sessions[session].time_start
		    					var end_hms = $scope.company_assessment.sessions[session].time_end

		    					var a = start_hms.split(':')
		    					var b = end_hms.split(':')

		    					var start_seconds = (+a[0])*60*60+(+a[1])*60+(+a[2])
		    					var end_seconds = (+b[0])*60*60+(+b[1])*60+(+b[2])

		    					total_seconds += (end_seconds - start_seconds)
		    				}	
		    			}else{
		    				if($scope.records[t_type].id == $scope.company_assessment.sessions[session].question){
		    					var start_hms = $scope.company_assessment.sessions[session].time_start
		    					var end_hms = $scope.company_assessment.sessions[session].time_end

		    					var a = start_hms.split(':')
		    					var b = end_hms.split(':')

		    					var start_seconds = (+a[0])*60*60+(+a[1])*60+(+a[2])
		    					var end_seconds = (+b[0])*60*60+(+b[1])*60+(+b[2])

		    					total_seconds += (end_seconds - start_seconds)
		    				}	
		    			}
	    			}

	    			total_time += total_seconds
	    			$scope.records[t_type]['time_consumed'] = convertSecondstoHours(total_time)
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

	$scope.new_score = function(data, id, id2) {
		$scope.albumNameArray = [];
	    angular.forEach(data, function(album){
	      if (album.is_correct) $scope.albumNameArray.push(album);
	    });

	    var data2 = {
	    	'company_assessment' : $scope.generate_report.id,
	    	'transaction_type' : id,
	    	'question' : id2,
	    	'score' : $scope.albumNameArray.length
	    }

	    me.post_generic("/generate_report/new_score/",data2,"main")
	    .success(function(response) {
	    	
	    })

	}

	$scope.selectScore = function(datus) {
	}

	$scope.similarity = function(s1, s2) {
		var longer = s1;
		var shorter = s2;
		if (s1.length < s2.length) {
			longer = s2;
			shorter = s1;
		}
		var longerLength = longer.length;
		if (longerLength === 0) {
			return 1.0;
		}
		return (longerLength - $scope.editDistance(longer, shorter)) / parseFloat(longerLength);
	}

	$scope.editDistance = function(s1, s2) {
		s1 = s1.toLowerCase();
		s2 = s2.toLowerCase();

		var costs = new Array();
		for (var i = 0; i <= s1.length; i++) {
			var lastValue = i;
			for (var j = 0; j <= s2.length; j++) {
				if (i == 0)
					costs[j] = j;
				else {
					if (j > 0) {
						var newValue = costs[j - 1];
						if (s1.charAt(i - 1) != s2.charAt(j - 1))
							newValue = Math.min(Math.min(newValue, lastValue),
								costs[j]) + 1;
						costs[j - 1] = lastValue;
						lastValue = newValue;
					}
				}
			}
			if (i > 0)
				costs[s2.length] = lastValue;
		}
		return costs[s2.length];
	}

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

	$scope.getQueryVariable = function(variable)
	{
	   var query = window.location.search.substring(1);
	   var vars = query.split("&");
	   for (var i=0;i<vars.length;i++) {
	           var pair = vars[i].split("=");
	           if(pair[0] == variable){return decodeURIComponent(pair[1]);}
	   }
	   return(false);
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