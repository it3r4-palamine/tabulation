var app = angular.module("enrollment", ['common_module','ui.bootstrap.contextMenu'])

app.controller("enrollmentCtrl", function($scope, $http, $timeout, $element, $controller, Notification, CommonRead, CommonFunc, RightClick){
	
	angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
	var self = this;
	var me = this;
	
	me.current_module = "enrollment_list"
	$scope.enrollment_data = {};
	$scope.total_payment = 0;
	me.filters = {};
	$scope.deleted_payment_ids = [];
	$scope.is_renew = false;
	$scope.excess_time = 0;
	$scope.payment = {
		official_receipt_no: null,
		payment_date: new Date(),
		amount_paid : null
	};
	$scope.enrollment_data = { 
		payments: [],
		session_credits:{ hours: 0, minutes: 0}  
	};
	$scope.filter = {}

	CommonRead.get_users2($scope);
	CommonRead.get_company2($scope);
	CommonRead.get_schools2($scope);


	$scope.enrollment_dialog = function(enrollment, is_renew)
	{
		if(enrollment && !is_renew)
		{

			$scope.read_enrollment(enrollment);
			
		} else if (is_renew) {
			$scope.enrollment_data = angular.copy(enrollment);
			delete $scope.enrollment_data.id
			delete $scope.enrollment_data.code
			$scope.enrollment_data.payments = []
			$scope.enrollment_data.payments.push(angular.copy($scope.payment));

			var session_credits = me.convert_seconds_duration(enrollment.session_credits_seconds)
			$scope.enrollment_data.session_credits = {"hours" : session_credits.hours, "minutes" : session_credits.minutes }

			$scope.is_renew = is_renew;
			$scope.set_date_and_time();

		} else {
			$scope.enrollment_data = {
				payments: [],
				session_credits:{ hours: 0, minutes: 0}  
			};
			$scope.enrollment_data.payments.push(angular.copy($scope.payment));
			$scope.set_date_and_time();

			me.post_generic("/enrollments/check_reference_no/","","main")
			.success(function(response){
				$scope.enrollment_data.code = response
			})
		}
		
		me.open_dialog("/enrollments/create_dialog/", 'dialog_width_90','main');
	};

	$scope.get_excess_time = function(){
		$scope.excess_time = 0;
		if (!$scope.enrollment_data.user || !$scope.enrollment_data.company_rename) return;
		var data = {
			student_id: $scope.enrollment_data.user.id,
			program_id: $scope.enrollment_data.company_rename.id,
		}

		me.post_generic("/enrollments/get_excess_time/", data, 'dialog')
		.success(function(response){
			$scope.excess_time = response.excess_time
		}).error(function(error){
			Notification.error(error);
		});
	}

	$scope.read_enrollment = function(enrollment)
	{

		me.post_generic("/enrollments/read_enrollment/" + enrollment.id, "", 'main')
			.success(function(enrollment){
				for(var i in enrollment.payments)
				{
					enrollment.payments[i].payment_date = new Date(enrollment.payments[i].payment_date);
				}

				$scope.enrollment_data = angular.copy(enrollment);
				$scope.enrollment_data.enrollment_date = new Date(enrollment.enrollment_date);
				$scope.enrollment_data.session_end_date = new Date(enrollment.session_end_date);
				$scope.enrollment_data.session_start_date = new Date(enrollment.session_start_date);

				var session_credits = me.convert_seconds_duration(enrollment.session_credits_seconds)
				$scope.enrollment_data.session_credits = {"hours" : session_credits.hours, "minutes" : session_credits.minutes }
			});


	}

	$scope.save_enrollment = function(data, save_opt){
		if ($scope.validate_enrollment()) {
			data["deleted_payments"] = $scope.deleted_payment_ids;

			if(data['school'].name == 'No School') delete(data['school'])

			$http.post("/enrollments/save_enrollment/", data).success(function(response){
				data.id = response.enrollment_pk;
				check_save_options(save_opt, data, response.message);
				self.close_dialog();
				$scope.main_loader();

			}).error(function(err){
				Notification.error(err);
				$scope.enrollment_data.enrollment_date = new Date();
			});
		}
	};

	$scope.change_start_date = function(data,date) {
		if(date == "date_from") {
			$scope.enrollment_data.session_end_date = moment($scope.enrollment_data.session_start_date).add(30,'d').format('YYYY-MM-DD')
			$scope.enrollment_data.session_end_date = new Date($scope.enrollment_data.session_end_date)
		}else if(date == 'date_to'){
            $scope.enrollment_data.session_start_date = moment($scope.enrollment_data.session_end_date).subtract(30,'d').format('YYYY-MM-DD');
            $scope.enrollment_data.session_start_date = new Date($scope.enrollment_data.session_start_date)
        }
	}

	success_notif_link = function(title, data, is_new){
		var config = {
            timeOut: 2000,
            onTap: function(toast){
            	if (is_new) me.close_dialog();
            	$scope.enrollment_dialog(data);
            },
        }

        toastr.success("", title, config);
	}

	check_save_options = function(save_opt, enrollment, message){
		switch(save_opt){
			case "close":
				me.close_dialog();
				success_notif_link(message, enrollment, false);
				break;
			case "new":
				me.close_dialog();
				$scope.enrollment_dialog();
				success_notif_link(message, enrollment, true);
				break;
			case "print":
				enrollment.student = enrollment.student.full_name;
				self.print_enrollment_form(enrollment);
				Notification.success(message);
				break;
			default:
				Notification.success(message);
				break;
		}

		$scope.is_renew = false;
		$scope.excess_time = 0;
	}


	me.delete_enrollment = function(data)
	{
		var confirmation = CommonFunc.confirmation("Delete Enrollment \n" + data.user.fullname + "?");
		confirmation.then(function(){

			me.post_generic("/enrollments/delete_enrollment/", data, null, true)
				.success(function(response){
					$scope.main_loader();
				})
		})
	};

	$scope.compute_program_session_credits = function(seconds)
	{
		var session_credits = me.convert_seconds_duration(seconds)
		$scope.enrollment_data.session_credits = {"hours" : session_credits.hours, "minutes" : session_credits.minutes }
	}

	$scope.validate_enrollment = function()
	{
		if($scope.get_total_payments() <= 0)
		{
			confirmation = CommonFunc.attention("Payment Error", "Must provide reference No.(OR/TR) and Amount");
			return false;
		}


		return true;

	}

	$scope.read_pagination = function(reset){
		if(reset){me.reset_filter()}
		me.filters["sort"] = me.sort;
		var filters = angular.copy(me.filters);
		filters = me.format_date(filters);
		filters = me.format_time(filters);
		filters["pagination"] = me.pagination;
		filters['name_search'] = $scope.filter.name

		var post = me.post_generic("/enrollments/read_enrollees/",filters,"main");
		post.success(function(response){
			self.records = response.records;
			self.generate_pagination(self,response,"records");
		});
	};

	$scope.set_date_and_time = function(){
		const now = new Date();
		$scope.enrollment_data.enrollment_date = new Date();
		$scope.enrollment_data.session_start_date = new Date();
		$scope.enrollment_data.session_end_date = new Date(now.setDate(now.getDate() + 30));
	};


	self.main_loader = function()
	{
		$scope.read_pagination();
	};

	self.main_loader();


	// Session Reconciler Module Functions

	self.add_this_session = function(session)
	{
		self.response.enrolled_sessions.push(angular.copy(session))
		self.response.unenrolled_sessions.splice(self.response.unenrolled_sessions.indexOf(session), 1);
		self.get_total_enrolled_time();
	};

	self.remove_this_session = function(session)
	{
		self.response.unenrolled_sessions.push(angular.copy(session))
		self.response.enrolled_sessions.splice(self.response.enrolled_sessions.indexOf(session), 1);
		self.get_total_enrolled_time();
	};

	$scope.get_total_enrolled_time = function()
	{
		var total_seconds = 0;
		for(var i in $scope.response.enrolled_sessions)
		{
			total_seconds += $scope.response.enrolled_sessions[i].total_session_time_seconds;
		}
		$scope.response.enroll_total_session_time_seconds = total_seconds;

		var total_seconds = 0;
		for(var i in $scope.response.unenrolled_sessions)
		{
			total_seconds += $scope.response.unenrolled_sessions[i].total_session_time_seconds;
		}

		$scope.response.non_enroll_total_session_time_seconds = total_seconds;
		$scope.response.remaining_credits = $scope.selected_enrollment.session_credits_seconds - $scope.response.enroll_total_session_time_seconds;
	};

	me.open_session_handler_dialog = function(enrollment)
	{
		$scope.selected_enrollment = enrollment;

		var response = me.post_generic("/enrollments/read_sessions_reconcile/", $scope.selected_enrollment);

		response.success(function(response){
			$scope.response = response;
			$scope.get_total_enrolled_time();

			for (x in $scope.response.enrolled_sessions) {
				var total_seconds = 0
				var start_hms = $scope.response.enrolled_sessions[x].time_start
				var end_hms = $scope.response.enrolled_sessions[x].time_end

				var a = start_hms.split(":")
				var b = end_hms.split(":")

				var start_seconds = (+a[0])*60*60+(+a[1])*60+(+a[2])
				var end_seconds = (+b[0])*60*60+(+b[1])*60+(+b[2])

				total_seconds += (end_seconds - start_seconds)

				$scope.response.enrolled_sessions[x]['time_consumed'] = convertSecondstoHours(total_seconds)
			}
			me.open_dialog("/enrollments/session_handler_dialog/", 'dialog_width_90');
		})

	};

	convertSecondstoHours = function(d){
		d = Number(d);
	    var h = Math.floor(d / 3600);
	    var m = Math.floor(d % 3600 / 60);
	    var s = Math.floor(d % 3600 % 60);

	    var hDisplay = h > 0 ? h + (h == 1 ? " hour, " : " hours, ") : "";
	    var mDisplay = m > 0 ? m + (m == 1 ? " minute, " : " minutes, ") : "";
	    var sDisplay = s > 0 ? s + (s == 1 ? " second" : " seconds") : "";
	    return hDisplay + mDisplay + sDisplay; 
	}

	$scope.save_enrolled_sessions = function()
	{
		var data = {
			enrollment : $scope.selected_enrollment,
			enrolled_sessions : $scope.response.enrolled_sessions,
			unenrolled_sessions : $scope.response.unenrolled_sessions
		}

		var response = me.post_generic("/enrollment/save_enrolled_sessions/", data, "dialog", true, null, true);

		response.success(function(response)
		{
			$scope.selected_enrollment = {};
			$scope.response = {};
			$scope.main_loader();
		})
	};

	// Assessment Test

	$scope.read_taken_tests = function(enrollee){
		console.log(enrollee)
		$scope.read_assessments();
	};

	$scope.read_assessments = function(){
		$http.post("/assessment/read_assessments/").success(function(response){
			$scope.assessments = response;
		}).error(function(err){
			Notification.error(err);
		});
	};

	$scope.take_test_dialog = function(){
		self.open_dialog("/enrollment/test_dialog/", 'dialog_height_55')
	};

	$scope.data = {};
	$scope.take_assessment = function(data){
		$http.post('', data).success(function(response){
			
		})
	}


	// Add Student
	self.open_create_edit_dialog = function(){
		self.student = {
			date_of_birth: new Date()
		};

		self.load_schools();
		self.load_grade_levels();

		self.open_dialog("/get_dialog/student/create_edit_dialog/", "second_dialog dialog_width_80 dialog_height_20");
	};

	self.load_schools = function(){
		var response = self.post_generic("/school/read_schools/");
		response.success(function(response){
			self.school_list = response.records;
		})
	}

	self.load_grade_levels = function(){
		var response = self.post_generic("/grade-level/load-list");
		response.success(function(response){
			self.grade_level_list = response;
		})
	}

	self.save_student = function(data){
		var response = self.post_generic('/student/save_student/', self.student, null, true, null, false);
		self.close_dialog(self.dialog, true)

		response.success(function(response){
			CommonRead.get_students(self, "students");
		})
	};

	self.print_enrollment_form = function(enrollment){
		sessionStorage.enrollment = angular.toJson(enrollment);
		window.open('/print_forms/get_enrollment_document/')
	};

	// Enrollment Payment Module

	$scope.add_payment = function(payment)
	{
		var payment = {
			official_receipt_no : null,
			payment_date: new Date(),
			amount_paid : null
		}

		$scope.enrollment_data.payments.push(angular.copy(payment));

	}

	$scope.delete_payment = function(payment)
	{
		if(payment.hasOwnProperty("id"))
		{
			$scope.deleted_payment_ids.push(payment.id);
		}

		$scope.enrollment_data.payments.splice($scope.enrollment_data.payments.indexOf(payment), 1);
	}

	$scope.compute_session_credits = function()
	{

		$scope.total_payment = $scope.get_total_payments();

		if($scope.total_payment >= $scope.enrollment_data.company_rename.rate)
		{
			$scope.enrollment_data.session_credits.hours = $scope.total_payment / 125;
		}else{
			$scope.enrollment_data.session_credits.hours = $scope.total_payment / 250;
		}
	}

	$scope.get_total_payments = function()
	{
		var total = 0;
		for(var i in $scope.enrollment_data.payments)
		{
			if (!$scope.enrollment_data.payments[i].official_receipt_no)
				return -1;

			total += $scope.enrollment_data.payments[i].amount_paid;
		}

		return total;
	}

	self.print_enrollment_form = function(enrollment){
		sessionStorage.enrollment = angular.toJson(enrollment);
		window.open('/print_forms/get_enrollment_document/')
	};

	me.menu_options = function (record) {
	    me.context_id = record.id;
	    return RightClick.get_menu(me,record)
	};

	CommonRead.get_display_terms($scope)

})
