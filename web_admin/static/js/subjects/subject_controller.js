var app = angular.module("subject", ['common_module', 'file-model', 'angular-sortable-view','ui.bootstrap.contextMenu']);

app.controller('SubjectCtrl', function($scope, $http, $timeout, $element, $controller, CommonFunc, RightClick, Notification, CommonRead)
{
	angular.extend(this, $controller('CommonCtrl', {$scope: $scope }));

	let self = this;
	let me = this;

	self.current_module 	= "subjects";
	self.pagination			= {};
	self.session_exercises 	= [];
	self.records 			= [];
	self.record 			= {};
	self.sessionEvalPage 	= true;
	self.today 				= new Date();
	self.filters 			= { name : ''};
	self.filter 			= { name : "" };
	$scope.filter 			= { name : "" };


	self.create_edit_session = function(record)
	{
		$scope.record = {};

		if ( record ) {
			self.record = record;
		}

		self.open_dialog("/get_dialog/subjects/dialog_create/", 'dialog_width_60 dialog_height_60', 'main')
	};

	self.confirm_close_dialog = function(){
		self.close_dialog();
	};

	self.read_records = function(session, silent_notification)
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
	};

	self.check_for_existing_session = function()
	{

		if(self.session.id)
		{
			return;
		}

		var filters = {
			"enrollment_id" : self.session.program.enrollment_id,
			"session_date": self.session.session_date
		};

		$http.post('/student_sessions/read_student_session/' + self.session.student.id, filters)
			.success(function(response){
				self.existing_sessions = response;
				if (response.length > 0){
					self.display_existing_sessions();
				}
			})
	};

	self.save_record = function(datus, save_opt)
	{

		if (datus) var post_data = angular.copy(datus);
		else var post_data = angular.copy(self.session);

		self.post_api('subject/create/', post_data, null, false, null, false)
			.success(function(response){
				self.close_dialog();
				self.main_loader();
			}).error(function(response){
				Notification.error(response)
			})


	};




    self.read_pagination = function(reset){
		if(reset) self.reset_filter();

		self.filters["sort"] = self.sort;
		var filters = angular.copy(self.filters);
		filters = self.format_date(filters);
		filters = self.format_time(filters);

		self.pagination["limit"] = 20;

		filters["pagination"] = self.pagination;

		var post = self.post_api("subject/read/", filters, "main");
		post.success(function(response){
			self.records = response.records;
			self.generate_pagination(self,response,"records");
		});
	};

	self.menu_options = function (record) {
	    me.context_id = record.id;
	    return RightClick.get_menu(me,record)
	};

	self.main_loader = function(){ self.read_pagination(); };
	self.main_loader();
});
