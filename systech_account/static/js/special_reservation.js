var app = angular.module("special_reservation", ['common_module', 'file-model', 'angular-sortable-view','ui.bootstrap.contextMenu']);

app.controller('SpecialReservationCtrl', function($scope, $http, $timeout, $element, $controller, CommonFunc, RightClick, Notification, CommonRead)
{
	angular.extend(this, $controller('CommonCtrl', {$scope: $scope }));

	var self = this;

	self.special_reservation = {};

	self.open_create_dialog = function(data)
	{
		if (data)
		{
			self.special_reservation = angular.copy(data);
		} else {

			self.timeslot = {};

		}

		self.open_dialog("/get_dialog/timeslot/create_dialog_special_reservation/", 'dialog_width_50', 'main');
	}

	self.read_programs = function(session, silent_notification)
	{
		self.programs = [];

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

	self.read_student_timeslot = function()
	{
		let data = self.special_reservation.program;

		var response = self.post_generic("/timeslots/read_student_timeslot/", data, null, false, null, null)

		response.success(function(response){
			self.timeslot = response.timeslot;
		});

		response.error(function(response){
			Notification.error(response)
		});
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

		var post = self.post_generic("/timeslots/read_special_reservations/", filters, "main");
		post.success(function(response){
			self.records = response.records;
			self.generate_pagination(self,response,"records");
		});
	}

	self.main_loader = function()
	{
		self.read();
	}

	self.main_loader();

	CommonRead.get_students(self);

});
