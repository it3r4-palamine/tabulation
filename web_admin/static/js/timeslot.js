var app = angular.module("timeslot", ['common_module', 'file-model', 'angular-sortable-view','ui.bootstrap.contextMenu']);

app.controller('TimeSlotCtrl', function($scope, $http, $timeout, $element, $controller, CommonFunc, RightClick, Notification, CommonRead)
{
	angular.extend(this, $controller('CommonCtrl', {$scope: $scope }));

	var self = this;

	self.current_module = "timeslot"
	self.records = [];
	self.timeslot = {};

	self.open_create_dialog = function(data)
	{
		console.log(data);

		if (data)
		{
			self.timeslot = angular.copy(data);

			self.timeslot.time_start = new Date(data.time_start);
			self.timeslot.time_end = new Date(data.time_end);

		} else {

			self.timeslot = {};

		}

		self.open_dialog("/get_dialog/timeslot/create_dialog/", 'dialog_width_50', 'main');
	}

	self.save_timeslot = function(data)
	{
		if (data) var post_data = angular.copy(data);
		else var post_data = angular.copy(self.timeslot);

		post_data.time_start = moment(post_data.time_start).format("HH:mm:ss");
		post_data.time_end = moment(post_data.time_end).format("HH:mm:ss");

		self.post_generic('/timeslots/save_timeslot/', post_data, null, false, null, false)
			.success(function(response){
				Notification.success(response)
				self.close_dialog()
			}).error(function(response){
				Notification.error(response)
			})
	}

	self.delete = function(data)
	{
		var confirmation = CommonFunc.confirmation("Delete Timeslot of " + data.student.fullname + "?");
		confirmation.then(function(){

			self.post_generic("/timeslots/delete_timeslot/" + data.id, null, true)
				.success(function(response){
					self.main_loader();
				})
		})
	}

	self.read = function(reset)
	{
		if(reset) self.reset_filter();

		self.filters["sort"] = self.sort;
		var filters = angular.copy(self.filters);
		filters = self.format_date(filters);
		filters = self.format_time(filters);

		self.pagination["limit"] = 20;

		filters["pagination"] = self.pagination;

		var post = self.post_generic("/timeslots/read_timeslots/", filters, "main");
		post.success(function(response){
			self.records = response.records;
			self.generate_pagination(self,response,"records");
		});
	}

	self.main_loader = function()
	{
		self.read();
	}

	self.read();

	CommonRead.get_students(self);

});