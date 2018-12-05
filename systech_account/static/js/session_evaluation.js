var app = angular.module("session_evaluation", ['common_module', 'file-model', 'angular-sortable-view']);

app.controller('StudentSessionCtrl', function($scope, $http, $timeout, $element, $controller, CommonFunc, Notification, CommonRead)
{
	angular.extend(this, $controller('CommonCtrl', { $scope: $scope }));
	var me = this;
	$scope.current_module = "evaluation_list"

	$scope.filters = { name : ''};
	$scope.pagination;
	$scope.session_exercises = [];
	$scope.draft_session;
	$scope.records = [];
	$scope.today = new Date();
	$scope.sessionEvalPage = true;
	// $scope.session = {};
	$scope.exercise_arr = [];

	$scope.add_session_exercise = function(is_save)
	{
		$scope.session_exercise = {
			score : null,
			trainer_note : {},
		};

		if ($scope.session.session_exercises.length > 0) {
			$scope.session_exercise.facilitated_by = $scope.session.session_exercises[$scope.session.session_exercises.length-1].facilitated_by
			$scope.session_exercise.trainer_note = $scope.session.session_exercises[$scope.session.session_exercises.length-1].trainer_note
		} else {
			$scope.session_exercise.facilitated_by = {};
			$scope.session_exercise.trainer_note = {};
		}

		$scope.session.session_exercises.push(angular.copy($scope.session_exercise));

		if ($scope.session.session_exercises.length == 3) {
			$("#top-ibox-collapse").trigger("click");
		}

		if (is_save) 
		{
			save_to_localstorage();
			$scope.save_session(null, 'open')
		}
	};

	$scope.set_date_and_time = function()
	{
		var today = new Date();
		var hour = today.getHours()
		var minute = today.getMinutes()
		var second_minute = minute + 60;
		$scope.session.session_date = today;
		$scope.session.session_timein = new Date(1970, 0, 1, hour, minute, 0);
		$scope.session.session_timeout = new Date(1970, 0, 1, hour, second_minute, 0);
	};

	$scope.create_edit_session = function(student_session, fromDraft){
		if (student_session && !fromDraft) {

			var response = $scope.post_generic('/student_sessions/read_student_session/'+student_session.id);
			response.success(function(response){
				$scope.session = response;
				$scope.session.session_date = new Date(response.session_date);
				$scope.session.session_timein = new Date(response.session_timein);
				$scope.session.session_timeout = new Date(response.session_timeout);

				if ($scope.session.session_exercises.length > 0) {
					$scope.session_exercise.facilitated_by = $scope.session.session_exercises[$scope.session.session_exercises.length-1].facilitated_by
				}

				$scope.read_programs($scope.session);
			})

		} else if (student_session && fromDraft) {

			$scope.session = $scope.draft_session;
			$scope.session.session_date = new Date($scope.draft_session.session_date);
			$scope.session.session_timein = new Date($scope.draft_session.session_timein);
			$scope.session.session_timeout = new Date($scope.draft_session.session_timeout);

			$scope.read_programs($scope.session);

		} else {
			localStorage.clear();
			
			$scope.session = {
				session_exercises : [],
				evaluated_by: {
					 "first_name":"Leonil",
			         "last_name":"Bagayna",
			         "code":"LDB",
			         "program_handle":{  
			            "name":"Arts",
			            "id":4
			         },
			         "full_name":"Leonil Bagayna",
			         "id":3
				},
			};
			$scope.session_exercise = {
				exercise : {},
				score : null,
				trainer_note : {},
				facilitated_by : {},
			}

			$scope.add_session_exercise(false);
			$scope.set_date_and_time();
		}

		me.open_dialog("/student_sessions/create_dialog", 'dialog_whole', 'main')
	};
});
