var app = angular.module("users",['common_module']);

app.controller('usersCtrl', function($scope, $http, $timeout, $element, $controller,CommonFunc,Notification,CommonRead) {
	angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
	var me = this;
	var self = this;
	$scope.record = {}
	$scope.filter = {}

	$scope.create_dialog = function(record){
		$scope.record = {}
		$scope.record['is_active'] = true

		if(record){
			$scope.record = angular.copy(me.format_date(record,null,true));

			// me.post_generic('/settings/read_to_dos/', "", "main")
			// .success(function(response) {
			// 	$scope.headers = response.data
			// 	$scope.view_lesson_update($scope.headers[0],true);
			// }).error(function(err) {
			// 	console.log(err);
			// });
		}
		// else {
			me.open_dialog("/users/create_user_dialog/","dialog_width_80","main")
		// }

	}

	$scope.view_lesson_update = function(topic,first=false) {
		var data = {
			'user_id' : $scope.record.id,
			'topic_id' : topic.id
		}

		me.post_generic('/users/view_lesson_update/',data,'dialog')
		.success(function(response) {
			$scope.lesson_updates = response.data

			if(first) me.open_dialog("/users/create_dialog/","","main")
		})
	}

	self.generate_student_account_info = function(student)
	{
		var first_name_stripped = student.first_name.replace(/\s+/g, '').toLowerCase();
		var last_name_stripped = student.last_name.replace(/\s+/g, '').toLowerCase();
		var full_name = student.first_name + " " + student.last_name
		var username = first_name_stripped + last_name_stripped
		student.fullname = full_name;
		student.is_active = true;

		if (!student.username)
		{
			student.username = username;
		}

		if (!student.email)
		{
			student.email = username + "@intelex.com"
		}

		if (!student.password1 && !student.password2)
		{
			student.password1 = student.password2 = "yahshuagrace"
		}

		return student
	};

	self.validate_user = function(student)
	{
		if (!student.first_name || !student.last_name)
		{
			Notification.warning("Please Provide First Name and Last Name")
			return false;
		}

		return true;
	};

	$scope.create = function()
	{
		if (self.validate_user($scope.record))
		{
			$scope.record = self.generate_student_account_info($scope.record)

			$scope.record = me.format_date($scope.record)
			if($scope.record.password1 != $scope.record.password2) return Notification.error("Password do not match.")
			me.post_generic("/users/create/",$scope.record,"dialog")
			.success(function(response){
				me.close_dialog();
				Notification.success(response.message);
				$scope.read();
			}).error(function(err){
				Notification.error(err)
			})
		}
	};

	$scope.get_intelex_students = function()
	{
		me.post_generic("/users/get_intelex_students/","","main")
		.success(function(data)
		{
			Notification.success(data)
			$scope.read()
		})

	};

	$scope.reconcile_student_credits = function()
	{
		me.post_generic("/users/reconcile_student_credits/","","main")
		.success(function(data)
		{
			Notification.success(data)
			$scope.read()
		})
	};

	$scope.load_to_edit = function(record, type){
		if(type == 'Technical')
			$scope.create_dialog(record);
	};

	$scope.change_pass_dialog = function(record){
		$scope.pwd_form = record
		me.open_dialog("/users/change_pass_dialog/","","main")
	};

	$scope.credits_summary = function(record)
	{
		me.open_dialog("/users/user_credits_summary/","","main")
		$scope.get_user_credits_yias(record)
	}

	$scope.get_user_credits_yias = function(user)
	{
		me.post_generic("/users/read_user_reconciled_credits/", user, "main")
		.success(function(response){

			$scope.record_yias = response.yias

		})
	}

	$scope.change_password = function(){
		if(!$scope.pwd_form.password1 || !$scope.pwd_form.password2) return Notification.error("Please input password.")
		if($scope.pwd_form.password1 != $scope.pwd_form.password2) return Notification.error("Password do not match.")
	    me.post_generic('/users/change_password/', $scope.pwd_form,"dialog").then(function(response){
	        me.close_dialog();
	        Notification.success(response.data)
	        $scope.pwd_form.password1 = "";
	        $scope.pwd_form.password2 = "";
	    }, function(err_res){
	        console.log(err_res); Notification.error(err_res.data);
	    })
	}

	$scope.read = function()
	{
		var pagination = me.pagination;
		pagination.limit = 20;

		var data = {
			pagination: pagination,
			code: $scope.filter.code,
			user_type : $scope.filter.user_type
		}

		me.post_generic("/users/read/",data,"main")
		.success(function(response){
			$scope.records = response.data;
			me.starting = response.starting;
			me.ending = response.data.length;
			me.pagination.limit_options = angular.copy(me.pagination.limit_options_orig);
			me.pagination.limit_options.push(response.total_records)
			me.pagination["total_records"] = response.total_records;
			me.pagination["total_pages"] = response.total_pages;
		})
	};

	$scope.checkAdmin = function(){
		if($scope.record.is_admin){
			$scope.record.is_edit = true
		}else{
			$scope.record.is_edit = false
		}
	}

	$scope.delete = function(record){
		swal({
		    title: "Continue",
		    text: "Remove "+record.fullname+"?",
		    type: "warning",
		    showCancelButton: true,
		    confirmButtonColor: "#DD6B55",
		    confirmButtonText: "Delete",
		    cancelButtonText: "Cancel",
		    closeOnConfirm: true
		},
		function(){
			$http.post("/users/delete/"+record.id)
			.success(function(response){
				Notification.success(response);
				$scope.read();
			}).error(function(err){
				Notification.error(err)
			})
		})
	}

	$scope.read_transaction_types = function(){
    	me.post_generic("/transaction_types/read/","","main")
    	.success(function(response){
    		$scope.transaction_types = response.data;
    	})
    }

	$scope.read_user_types = function(){
    	me.post_generic("/users/read_user_types/","","main")
    	.success(function(response){
    		$scope.user_types = response;
    	})
    }

	$scope.read();
	// $scope.read_transaction_types();
	$scope.read_user_types();
	me.main_loader = function(){$scope.read();}
	CommonRead.get_display_terms($scope)
	CommonRead.get_schools($scope)
	CommonRead.get_grade_level($scope)
});
