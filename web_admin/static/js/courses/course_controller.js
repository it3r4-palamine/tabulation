var app = angular.module("course", ['common_module', 'file-model', 'angular-sortable-view','ui.bootstrap.contextMenu']);

app.controller('CourseCtrl', function($scope, $http, $timeout, $element, $controller, CommonFunc, RightClick, Notification, CommonRead)
{
	angular.extend(this, $controller('CommonCtrl', {$scope: $scope }));

	let self = this;
	let me = this;

	self.current_module 	= "course";
	self.pagination			= {};
	self.session_exercises 	= [];
	self.records 			= [];
	self.record 			= {};
	self.sessionEvalPage 	= true;
	self.today 				= new Date();
	self.filters 			= { name : ''};
	self.filter 			= { name : "" };
	$scope.filter 			= { name : "" };
	self.course_programs    = [];


	self.create_edit_session = function(record)
	{
		$scope.record = {};

		if ( record ) {
			self.record = record;
			self.read_course_programs(record);
		} else {
		    self.course_programs.push({})
        }

		self.open_dialog("/get_dialog/courses/create_dialog/", 'dialog_width_60 dialog_height_60', 'main')
	};

	self.read_course_programs = function(record)
	{
		let response = self.post_api("course/read_course_programs/", record, null, false, null, null)

		response.success(function(response){
			self.course_programs = response.records;

			if(response.records.length === 0)
			{
				self.add_course_program();
			}
		});

		response.error(function(response){
		    self.course_programs = [{}]
		});
	};

	self.add_course_program = function()
    {
        self.course_programs.push({});
    };

	self.remove_course_program = function(record)
	{
		self.course_programs.splice(self.course_programs.indexOf(record), 1);
	};

	self.save_record = function(record)
	{
		let post_data = angular.copy(record);
	    post_data["course_programs"] = self.course_programs;

		self.post_api('course/create/', post_data, null, false, null, false)
			.success(function(response){

				self.record 		 = {};
				self.course_programs = [];

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

		let post = self.post_api("course/read/", filters, "main");
		post.success(function(response){
			self.records = response.records;
		});
	};

	self.menu_options = function (record) {
	    me.context_id = record.id;
	    return RightClick.get_menu(me,record)
	};

	CommonRead.get_programs(self);

	self.main_loader = function(){ self.read_pagination(); };
	self.main_loader();
});
