var app = angular.module("program", ['common_module', 'file-model', 'angular-sortable-view','ui.bootstrap.contextMenu']);

app.controller('ProgramCtrl', function($scope, $http, $timeout, $element, $controller, CommonFunc, RightClick, Notification, CommonRead)
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
	self.program_sessions   = [];
	$scope.filter 			= { name : "" };


	self.create_edit_record = function(record)
	{
		self.record = {};

		if ( record ) {
			self.record = angular.copy(record);
			self.read_program_sessions(record);
		} else {
			self.program_sessions.push({});
		}

		self.open_dialog("/get_dialog/programs/create_dialog/", 'dialog_width_80', 'main');
	};

	self.read_program_sessions = function(record)
	{
		let response = self.post_api("program/read_program_sessions/", record, null, false, null, null);

		response.success(function(response){
			self.program_sessions = response.records;

			if(response.records.length === 0)
			{
				self.add_session_exercise();
			}
		});

		response.error(function(response){
		    self.program_sessions = [{}]

		});
	};

	self.add_session_exercise = function()
    {
        self.program_sessions.push({});
    };

	self.remove_session_exercise = function(record)
	{
		record["is_deleted"] = true;
	};

	self.save_record = function(record)
	{
	    let post_data = angular.copy(record);

	    post_data["program_sessions"] = self.program_sessions;

		self.post_api('program/create/', post_data, null, false, null, false)
			.success(function(response){

				self.record = {};
				self.program_sessions = [];

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

		var post = self.post_api("program/read/", filters, "main");
		post.success(function(response){
			self.records = response.records;
			// self.generate_pagination(self,response,"records");
		});
	};

	self.menu_options = function (record) {
	    me.context_id = record.id;
	    return RightClick.get_menu(me,record)
	};

	self.main_loader = function(){ self.read_pagination(); };
	self.main_loader();

	CommonRead.get_sessions(self);
});
