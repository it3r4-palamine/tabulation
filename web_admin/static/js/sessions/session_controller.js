var app = angular.module("session", ['common_module', 'file-model', 'angular-sortable-view','ui.bootstrap.contextMenu']);

app.controller('SessionCtrl', function($scope, $http, $timeout, $element, $controller, CommonFunc, RightClick, Notification, CommonRead)
{
	angular.extend(this, $controller('CommonCtrl', {$scope: $scope }));

	var self = this;
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
	self.exercise_questions = [];
	$scope.filter 			= { name : "" };


	self.create_edit_session = function(record)
	{
		self.record = {};

		console.log(record);

		if ( record ) {
			self.record["exercise"] = record;
			self.read_exercise_questions(record);
		}

		self.open_dialog("/get_dialog/exercise/dialog_create/", 'dialog_width_80', 'main')
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

	self.remove_exercise_question = function(record)
	{
		self.exercise_questions.splice(self.exercise_questions.indexOf(record), 1);
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
			// self.generate_pagination(self,response,"records");
		});
	};

    self.read_exercises = function()
    {
        var post = self.post_api("exercise/read/", null, "main");
		post.success(function(response){
			self.exercises = response.records;
		});
    };

	self.menu_options = function (record) {
	    me.context_id = record.id;
	    return RightClick.get_menu(me,record)
	};

	self.main_loader = function(){ self.read_pagination(); };
	self.main_loader();

	CommonRead.get_questions_new(self);
	self.read_exercises();
});
