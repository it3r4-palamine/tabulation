var app = angular.module("exercise", ['common_module', 'file-model', 'angular-sortable-view','ui.bootstrap.contextMenu']);

app.controller('ExerciseCtrl', function($scope, $http, $timeout, $element, $controller, CommonFunc, RightClick, Notification, CommonRead)
{
	angular.extend(this, $controller('CommonCtrl', {$scope: $scope }));

	var self = this;
	let me = this;

	self.current_module 	= "exercise";
	self.pagination			= {};
	self.session_exercises 	= [];
	self.records 			= [];
	self.record 			= {};
	self.sessionEvalPage 	= true;
	self.today 				= new Date();
	self.filters 			= { name : ''};
	self.filter 			= { name : "" };
	self.exercise_questions = [];
	$scope.filter 			= { name : "" };
	self.exercise_types = [
		"Exercise",
		"Post Test",
		"Assessment Test",
	];

	self.create_edit_session = function(record)
	{
		self.record = {};

		if ( record ) {
			self.record["exercise"] = record;
			self.read_exercise_questions(record);
		} else {
			self.exercise_questions = [{}]
		}

		if (record && record.is_assessment_test)
		{
			self.record = record;
			self.open_dialog("/get_dialog/exercise/dialog_create_assessment/", 'dialog_width_80', 'main')
		} else {
			self.open_dialog("/get_dialog/exercise/dialog_create/", 'dialog_width_80', 'main')
		}
	};

	self.create_edit_dialog_assessment = function()
	{
		self.record = {};
		self.exercise_questions = [];

		self.open_dialog("/get_dialog/exercise/dialog_create_assessment/", 'dialog_width_80', 'main')
	};

	self.read_exercise_questions = function(record)
	{
		let response = self.post_api("exercise/read_exercise_questions/", record, null, false, null, null)

		response.success(function(response){
			self.exercise_questions = response.records;

			if(response.records.length === 0)
			{
				self.add_exercise_question();
			}
		});

		response.error(function(response){
		    self.exercise_questions = [{}]

		});
	};

	self.add_exercise_question = function()
    {
        self.exercise_questions.push({});
    };

	self.remove_session_exercise = function(record)
	{
		self.exercise_questions.splice(self.exercise_questions.indexOf(record), 1);
	};

	self.save_assessment_test = function(record)
	{
		let post_data = record;

		post_data["is_assessment_test"] = true;
	    post_data["exercise_questions"] = self.exercise_questions;

		self.post_api('exercise/create/', post_data, null, false, null, false)
		.success(function(response){

			self.record = {};
			self.session_exercises = [];

			self.close_dialog();
			self.main_loader();
		}).error(function(response){
			Notification.error(response)
		})
	};

	self.delete_record = function(record)
	{
		console.log(record)
		let confirmation = CommonFunc.confirmation("Delete Exercise " + record.name + "?");
		confirmation.then(function(){

			self.delete_api("exercise/delete/" + record.id, null, "main")
				.success(function(response){
					Notification.success(response);
					self.main_loader();
				})
		})
	};

	self.save_record = function(record)
	{
	    let post_data = record;

	    post_data["exercise_questions"] = self.exercise_questions;
        console.log(post_data);

		self.post_api('exercise/create/', post_data, null, false, null, false)
			.success(function(response){

				self.record = {};
				self.session_exercises = [];

				self.close_dialog();
				self.main_loader();
			}).error(function(response){
				Notification.error(response)
			})
	};


    self.read_pagination = function(reset)
    {
		if(reset) self.reset_filter();

		self.filters["sort"] = self.sort;
		var filters = angular.copy(self.filters);
		filters = self.format_date(filters);
		filters = self.format_time(filters);

		self.pagination["limit"] = 20;
		filters["pagination"] = self.pagination;

		var post = self.post_api("exercise/read/", filters, "main");
		post.success(function(response){
			self.records = response.records;
			self.starting = response.starting;
			self.ending = response.records.length;
			self.pagination.limit_options = angular.copy(self.pagination.read_user_credits);
			self.pagination["total_records"] = response.total_records;
			self.pagination["total_pages"] = response.total_pages;
		});
	};

    self.read_exercises = function(search)
    {
		let filters = {
    		"search" : search,
			"exercise_type" : self.filters.exercise_type,
		};

        var post = self.post_api("exercise/read/", filters, null);
		post.success(function(response){
			self.exercises = response.records;
		});
    };

    self.read_courses = function()
	{
		let post = self.post_api("course/read/", { exclude_with_assessment : true }, "main");
		post.success(function(response){
			self.courses = response.records;
		});
	};

	self.menu_options = function (record) {
		console.log(record)
	    me.context_id = record.id;
	    return RightClick.get_menu(me,record)
	};

	self.main_loader = function(){
		self.read_pagination();
		self.read_courses();
	};

	self.main_loader();

	CommonRead.get_questions_new(self);
	self.read_courses();
	self.read_exercises();
});
