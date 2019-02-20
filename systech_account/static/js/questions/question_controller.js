var app = angular.module("questions", ['common_module', 'file-model', 'angular-sortable-view','ui.bootstrap.contextMenu']);

app.controller('QuestionCtrl', function($scope, $http, $timeout, $element, $controller, CommonFunc, RightClick, Notification, CommonRead)
{
	angular.extend(this, $controller('CommonCtrl', {$scope: $scope }));
	var self = this;
	var me = this;
	self.current_module = "evaluation_list"

	self.filters = { name : ''};
	self.pagination;
	self.session_exercises = [];
	self.draft_session;
	self.records = [];
	self.today = new Date();
	self.sessionEvalPage = true;
	// self.session = {};
	self.exercise_arr = [];
	self.record = {}
	self.filter = { name : "" }
	$scope.filter = { name : "" }


	self.create_edit_session = function(student_session, fromDraft, record){
		$scope.record = {}
		$scope.record['is_active'] = true

		if (student_session && !fromDraft ) {
			$scope.read_transaction_types(record)
			var response = self.post_generic('/student_sessions/read_student_session/'+student_session.id);
			response.success(function(response){
				self.session = response;
				self.session.session_date = new Date(response.session_date);
				self.session.session_timein = new Date(response.session_timein);
				self.session.session_timeout = new Date(response.session_timeout);

				self.read_programs(self.session, true);
			})

			response.error(function(response){
				self.session.exercise = [];
			})

		} else {
			localStorage.clear();

			self.session = {
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

			self.session.session_exercises = [];

			self.session_exercise = {
				exercise : {},
				score : null,
				trainer_note : {},
				facilitated_by : {},
			}

			self.add_session_exercise(false);
			self.set_date_and_time();
			self.post_generic("/student_sessions/check_reference_no/","","main")
			.success(function(response){
				self.session.code = response;
			})
		}

		self.open_dialog("/get_dialog/questions/dialog_create/", 'dialog_whole', 'main')
	};

	self.add_session_exercise = function(is_save)
	{
		self.session_exercise = {
			score : null,
			trainer_note : {},
		};

		if (self.session.session_exercises.length > 0) {
			self.session_exercise.facilitated_by = self.session.session_exercises[self.session.session_exercises.length-1].facilitated_by
			// self.session_exercise.trainer_note = self.session.session_exercises[self.session.session_exercises.length-1].trainer_note
		} else {
			self.session_exercise.facilitated_by = {};
			// self.session_exercise.trainer_note = {};
		}

		self.session.session_exercises.push(angular.copy(self.session_exercise));

		if (self.session.session_exercises.length == 3) {
			$("#top-ibox-collapse").trigger("click");
		}
	};
	
	self.read_exercises = function()
	{
		$http.post("/transaction_types/read/").success(function(response){
			self.exercise_arr = response;
		}).error(function(err){
			Notification.error(err);
		});
	};

	self.load_exercises_by_program = function(program_id)
	{
		$http.post("/transaction_types/read/"+program_id).success(function(response){
			self.exercise_arr = response;
		}).error(function(err){
			Notification.error(err);
		});
	};

	self.get_selected_exercise = function(exercise)
	{
		var filter = {
			exercise_code : exercise.exercise_code,
			set_no : exercise.exercise_set_no.set_no,
		}

		$http.post('/exercise/read_exercise/', filter)
			.success(function(response){
				exercise.exercise = response;

				if(response < exercise.score)
				{
					exercise.score = 0;
				}

			})
	}

	self.set_date_and_time = function()
	{
		var today = new Date();
		var hour = today.getHours()
		var minute = today.getMinutes()
		var second_minute = minute + 60;
		self.session.session_date = today;
		self.session.session_timein = new Date(1970, 0, 1, hour, minute, 0);
		self.session.session_timeout = new Date(1970, 0, 1, hour, second_minute, 0);
	};

	self.confirm_close_dialog = function(){
		if (self.session.session_exercises.length>1) {
			var confirmation = CommonFunc.confirmation("Are you sure?", null, null, "Yes");
			confirmation.then(function(){
				clear_session();
			});
		} else clear_session();

	};

	clear_session = function(){
		init_student_session();
		localStorage.clear();
		read_drafted_sessions();
		self.programs = [];
		self.close_dialog();
	}

	self.read_programs = function(session, silent_notification)
	{
		self.programs = [];
		// self.session.program = {};

		var response = self.post_generic("/program/read_enrolled_programs/", session.student, null, false, null, null)

		response.success(function(response){
			self.programs = response.records;
		});

		response.error(function(response){
			if (!silent_notification)
			{
				Notification.error(response)
			}
		});
	};

	self.initiate = function(){
		CommonRead.load_enrolled_students(self);
		CommonRead.get_trainers(self);
		CommonRead.get_trainer_notes(self);
		self.read_exercises();
		self.read_pagination();
	};

	self.delete_session_excercise = function(session_exercise){
		self.session.session_exercises.splice(self.session.session_exercises.indexOf(session_exercise), 1);
	};
	
	self.print_student_session = function(student_session){

		$http.post('/student_sessions/read_student_session/' + student_session.id)
			.success(function(response){
				console.log(response)
				sessionStorage.form_data = angular.toJson(response);
				window.open('/print_forms/get_document/')
			})
	};

	self.delete_student_session = function(student_session)
	{
		var confirmation = CommonFunc.confirmation("Delete Session of " + student_session.student_full_name + "?");
		confirmation.then(function(){

			self.post_generic("/student_sessions/delete/" + student_session.id, null, true)
				.success(function(response){
					self.main_loader();
				})
		})
	};

	self.display_existing_sessions = function()
	{
		self.open_dialog("/get_dialog/session_evaluation/session_list_dialog", "second_dialog dialog_height_100 dialog_weight_50")
	}

	self.check_for_existing_session = function()
	{

		if(self.session.id)
		{
			return;
		}

		var filters = {
			"enrollment_id" : self.session.program.enrollment_id,
			"session_date": self.session.session_date
		}

		$http.post('/student_sessions/read_student_session/' + self.session.student.id, filters)
			.success(function(response){
				self.existing_sessions = response;
				if (response.length > 0){
					self.display_existing_sessions();
				}
			})
	}

	self.save_session = function(datus, save_opt)
	{

		if (datus) var post_data = angular.copy(datus);
		else var post_data = angular.copy(self.session);

		post_data.session_timein = moment(post_data.session_timein).format("HH:mm:ss");
		post_data.session_timeout = moment(post_data.session_timeout).format("HH:mm:ss");

		// Save to Local Storage In case unable to connect to server, able to refresh
		save_to_localstorage();

		// if (self.validate_session(post_data)) {

		self.post_generic('/student_sessions/create/', post_data, null, false, null, false)
			.success(function(response){
				self.session.id = response.session_pk;
				check_save_options(save_opt, self.session, response.message);
				self.main_loader();
			}).error(function(response){
				Notification.error(response)
			})


	};

	check_save_options = function(save_opt, session, message){
		switch (save_opt) {
			case "close":
				self.close_dialog();
				init_student_session();
				self.set_date_and_time();
				self.main_loader();
				success_notif_link(message, session, false);
				break;
			case "new":
				self.close_dialog();
				init_student_session();
				self.set_date_and_time();
				self.create_edit_session();
				success_notif_link(message, session, true);
				break;
			case "print":
				self.print_student_session(session);
				Notification.success(message);
				break;
			default:
				Notification.success(message);
				break;
		}
	}

	self.validate_session = function(data)
	{
		var title;
		var message;
		var continue_save = false;
		var confirmButton = null;

		if(!data.hasOwnProperty("student"))
		{
			title = "Check the Student";
			message = "No Student Selected";
		}
		else if(angular.equals(data.program, {}))
		{
			title = "Check the Program";
			message = "No Program Selected";
		}
		// else if(!data.hasOwnProperty("evaluated_by"))
		// {
		// 	title = "Check the Evaluated By";
		// 	message = "No Evaluator Selected";
		// }
		else if(data.session_timein > data.session_timeout)
		{
			title = "Check the Time";
			message = "Time in is Greater than Time Out";
		}

		

		if(title)
		{
			confirmation = CommonFunc.attention(title, message);
			return false;
		}

		return true;

	};

	function init_student_session()
	{
		self.session = { session_exercises: []};
	}

	function save_to_localstorage()
	{
		localStorage.session = angular.toJson(self.session);
	}

	function read_drafted_sessions()
	{
		self.draft_session = angular.fromJson(localStorage.session);
	}

	$scope.read_transaction_types = function(record){
	    	self.post_generic("/transaction_types/read/",{"company_rename":record.company_rename.id, "with_questions":true},"dialog")
	    	.success(function(response){
	    		$scope.transaction_types = response.data;
	    	})
	    }

	$scope.read_companies = function(record){
		$scope.record.company = {}
		var data = {
			exclude : true
		}
    	me.post_generic("/company/read/",data,"main")
    	.success(function(response){
    		$scope.companies = response.data;
    	})
    }

   $scope.read_transaction_types = function(){
    	var post = CommonRead.get_transaction_types2($scope,{"bypass_code_exists": true});
    	post.success(function(response){
    		var records = response.data;
    		$scope.transaction_types2 = angular.copy(records);
    		$scope.transaction_types = angular.copy(records);
    		$scope.transaction_types.unshift({'name' : 'ALL'});
    	})
    	/*me.post_generic("/transaction_types/read/","","main")
    	.success(function(response){
    		$scope.transaction_types = response.data;
    	})*/
    }

  $scope.select_transaction_type = function(record){
    	$scope.record.transaction_types = {}
		$scope.read_transaction_types(record);
		$scope.read_user_credits(record);
    }

    $scope.select_user = function(record){
    	$scope.read_user_credits(record);
    }

   	$scope.read_user_credits = function(record){
    	// record.date_from = moment(new Date(record.date_from)).format('YYYY-MM-DD');
    	// record.date_to = moment(new Date(record.date_to)).format('YYYY-MM-DD');
    	self.post_generic("/users/read_user_credits/",record,"dialog")
    	.success(function(response){
    		if(response.data.length > 0) {
	    		$scope.record.session_credits = response.data[0].session_credits
	    		$scope.record.date_from = new Date(response.data[0].session_start_date)
	    		$scope.record.date_to = new Date(response.data[0].session_end_date)
    		}else{
    			$scope.record.session_credits = null
    			$scope.record.date_from = null
    			$scope.record.date_to = null
    			Notification.error("No session credits left. Please advised!")
    		}
    	})
    }

	$scope.read_users = function(){
    	self.post_generic("/users/read_students/","","main")
    	.success(function(response){
    		self.students = response.records;
    	})
    };

    self.read_facilitators = function()
    {
    	self.post_generic("/users/read_facilitators/","","main")
    	.success(function(response){
    		self.facilitators = response.records;
    	})
    }

    $scope.read_companies = function(record){
		self.record.company = {}
		var data = {
			exclude : true
		}
    	self.post_generic("/company/read/",data,"main")
    	.success(function(response){
    		$scope.companies = response.data;
    	})
    }

    self.read_trainer_notes = function(record)
    {
    	var response = self.post_generic("/settings/read_trainer_notes/")

    	response.success(function(response){
    		self.trainers_notes = response.data
    	});
    }
	
    $scope.read_student_session = function(){
		self.post_generic("/questions/read_questions/",null,"main")
		.success(function(response){
			console.log(response);
			self.records = response.records;
			for(var record in $scope.records){
				var credits_left = $scope.records[record].credits_left ? $scope.records[record].credits_left : 0 
				var session_credits = $scope.records[record].session_credits
				$scope.records[record]['credits_left_seconds'] = convertSecondstoHours(credits_left);
				$scope.records[record]['session_credits_seconds'] = convertSecondstoHours(session_credits);
			}
			self.starting = response.starting;
			self.ending = response.records.length;
			self.pagination.limit_options = angular.copy(self.pagination.read_user_credits);
			// self.pagination.limit_options.push(response.total_records);
			self.pagination["total_records"] = response.total_records;
			self.pagination["total_pages"] = response.total_pages;
		})		
    }

    self.read_pagination = function(reset){
		if(reset) self.reset_filter();

		self.filters["sort"] = self.sort;
		var filters = angular.copy(self.filters);
		filters = self.format_date(filters);
		filters = self.format_time(filters);

		self.pagination["limit"] = 20;

		filters["pagination"] = self.pagination;

		var post = self.post_generic("/questions/read_questions/", filters, "main");
		post.success(function(response){
			self.records = response.records;
			self.generate_pagination(self,response,"records");
		});
	};

	self.set_date_filter = function()
	{
		self.filters.date_to = angular.copy(self.filters.date_from)
	}

	me.menu_options = function (record) {
	    me.context_id = record.id;
	    return RightClick.get_menu(me,record)
	};

	convertSecondstoHours = function(d){
			d = Number(d);
		    var h = Math.floor(d / 3600);
		    var m = Math.floor(d % 3600 / 60);
		    var s = Math.floor(d % 3600 % 60);

		    var hDisplay = h > 0 ? h + (h == 1 ? " hour" : " hours, ") : "";
		    var mDisplay = m > 0 ? m + (m == 1 ? " minute" : " minutes, ") : "";
		    var sDisplay = s > 0 ? s + (s == 1 ? " second" : " seconds") : "";
		    return hDisplay + mDisplay + sDisplay; 
	}
   	
	self.main_loader = function(){ self.read_pagination(); }

	$scope.read_companies();
	$scope.read_users();

	self.read_facilitators();
	self.read_trainer_notes();

	CommonRead.get_display_terms($scope)
	CommonRead.get_transaction_types($scope);
	CommonRead.get_company($scope);
	CommonRead.get_users($scope);
	$scope.read_transaction_types();

	self.main_loader();
});
