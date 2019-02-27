angular.module("payment_reports", ['common_module','ui.bootstrap.contextMenu'])

.controller("payment_reportsCtrl", function($scope, $http, $timeout, $controller, $uibModal, $uibModalStack, $templateCache, Notification, CommonRead, CommonFunc){

	angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
	var self = this;
	var me = this;

	$scope.enrollment_arr = [];

	$scope.read_pagination = function(reset, isExport){
		if(reset) me.reset_filter();

		var filters = angular.copy(me.filters);
		filters = me.format_date(filters);
		filters = me.format_time(filters);

		if (!isExport) {
			filters["sort"] = me.sort;
			me.pagination.limit = 50;
			filters["pagination"] = me.pagination;
		}

		var post = me.post_generic("/enrollments/read_enrollees/", filters, "main");
		post.success(function(response){
			if (isExport) {
				exportEnrollmentReports(response.records)
			} else {
				$scope.enrollment_arr = response.records;
				me.starting = response.starting;
				me.ending = response.records.length;
				me.pagination.limit_options = angular.copy(me.pagination.limit_options_orig);
				me.pagination.limit_options.push(response.total_records)
				me.pagination["total_records"] = response.total_records;
				me.pagination["total_pages"] = response.total_pages;
			}

		});
	}

	exportEnrollmentReports = function(enrollment_arr){
		for (var i = 0; i < enrollment_arr.length; i++) {
			delete enrollment_arr[i].total_time_left;
			delete enrollment_arr[i].school;
			delete enrollment_arr[i].code;
			delete enrollment_arr[i].total_session_time;
			delete enrollment_arr[i].enrollment;
			delete enrollment_arr[i].enrollment_date;

			enrollment_arr[i].student = enrollment_arr[i].student.full_name;
			enrollment_arr[i].program = (enrollment_arr[i].program) ? enrollment_arr[i].program.name : ""
			enrollment_arr[i].session_start_date = enrollment_arr[i].session_start_date;
			enrollment_arr[i].session_end_date = enrollment_arr[i].session_end_date;

			var payment = angular.copy(enrollment_arr[i].payments[0]);
			delete enrollment_arr[i].payments;

			enrollment_arr[i].official_receipt_no = (payment) ? payment.official_receipt_no : ""
			enrollment_arr[i].payment_date = (payment) ? payment.payment_date : ""
			enrollment_arr[i].amount_paid = (payment) ? payment.amount_paid : ""
		}

		alasql('Select student as Student, \
						program as Program, \
						session_start_date as [Session Start Date], \
						session_end_date as [Session End Date], \
						official_receipt_no as [OR#], \
						payment_date as [Date Paid], \
						amount_paid as [Amount Paid] \
						INTO XLSX("enrollment-report.xlsx", { headers: true }) FROM ?', [enrollment_arr]);
	}

	me.main_loader = function(){
		$scope.read_pagination();
	}


	me.main_loader();
	CommonRead.get_display_terms($scope)
});