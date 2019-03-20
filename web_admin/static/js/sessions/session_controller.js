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
	self.session_exercises  = [];
	$scope.filter 			= { name : "" };


	self.create_edit_record = function(record)
	{
		self.record = {};

		if ( record ) {
			self.record = angular.copy(record);
		} else {
			self.session_exercises.push({})
		}

		self.open_dialog("/get_dialog/sessions/create_dialog/", 'dialog_width_80', 'main')
	};

	self.read_exercise_questions = function(record)
	{
		let response = self.post_api("exercise/read_exercise_questions/", record, null, false, null, null)

		response.success(function(response){
			self.exercise_questions = response.records;

			if(response.records.length === 0)
			{
				self.add_session_exercise();
			}
		});

		response.error(function(response){
		    self.exercise_questions = [{}]

		});
	};

	self.add_session_exercise = function()
    {
        self.session_exercises.push({});
    };

	self.remove_session_exercise = function(record)
	{
		self.session_exercises.splice(self.session_exercises.indexOf(record), 1);
	};

	self.save_record = function(record)
	{
	    let post_data = angular.copy(record);

	    post_data["session_exercises"] = self.session_exercises;

		self.post_api('session/create/', post_data, null, false, null, false)
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

		var post = self.post_api("session/read/", filters, "main");
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
