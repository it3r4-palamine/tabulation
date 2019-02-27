angular.module("dashboard", ['common_module', 'common_config', 'angular-flot', 'angles'])

.controller("DashboardCtrl", function($scope, $http, $timeout, $controller, $uibModal, $uibModalStack, $templateCache, Notification, CommonFunc, CommonRead) {
	angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
	var self = this;

	self.lineOptions = {
		scaleLabel: function(label){
			return label.value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
		},
	    scaleShowGridLines : true,
	    scaleGridLineColor : "#ADD8E6",
	    scaleGridLineWidth : 1,
	    bezierCurve : true,
	    bezierCurveTension : 0.4,
	    pointDot : true,
	    pointDotRadius : 4,
	    pointDotStrokeWidth : 1,
	    pointHitDetectionRadius : 20,
	    datasetStroke : true,
	    datasetStrokeWidth : 2,
	    datasetFill : true,
	    multiTooltipTemplate: function(label){
	        return label.datasetLabel + ': ' +    label.value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
       	},
	};

	self.read_timeslot_summary = function()
	{
		var response = self.post_generic("/dashboard/read_timeslot_summary/", null, "main", true)

		response.success(function(response){
			console.log(response)
			self.timeslots = response.records

			for(var i in self.timeslots)
			{
				var data = self.timeslots[i]
				if (data.timeslot)
				{
					self.timeslots[i].timeslot.time_start = new Date(data.timeslot.time_start);
					self.timeslots[i].timeslot.time_end = new Date(data.timeslot.time_end);
				}
			}

		});
	}

	self.read_timeslot_summary();


	self.read_student_status = function()
	{
		var response = self.post_generic("/dashboard/read_student_status/", null, "main2")
		response.success(function(response){
			self.student_data = response;
		});
	}

	self.show_detail = function()
	{
		var response = self.post_generic("/dashboard/read_monthly_students_enrolled/", null, "main3")
		response.success(function(response){

			var labels = []
			var data = []
			var data2 = []
			for(x in response.data){
				labels.push(response.data[x].month)
				data.push(response.data[x].students)
				data2.push(response.data[x].inactive)
			}

			self.lineData = {
				labels:labels,
				datasets: [
					{
						label: 'Students enrolled',
		            	fillColor: "#84d0c1",
		                strokeColor: "#00b893",
		                pointColor: "#00b893",
		                pointStrokeColor: "#fff",
		                pointHighlightFill: "#00b893",
		                pointHighlightStroke: "#00b893",
		            	data: data
					},
					{
		            	label: 'Inactive',
		            	fillColor: "#eeeeee",
		            	strokeColor: "#c9c9c9",
		            	pointColor: "#c9c9c9",
		            	pointStrokeColor: "#fff",
		            	pointHighlightFill: "#c9c9c9",
		            	pointHighlightStroke: "#c9c9c9",
		            	data: data2
		            },
				]
			}
			self.open_dialog("/get_dialog/dashboard/monthly_enrolled_details/", 'dialog_width_50');
			var legend = "<ul style=\"list-style-type:none;\">";
		    self.lineData.datasets.forEach(function(dataset){
		      legend += "<li><div style=\"background-color:" + dataset.strokeColor + ";height:0.5em;width:0.5em;float:left;margin-top:0.5em;margin-right:0.5em;\"></div><span style='font-family:Verdana;font-size: 12px;'>";
		      if (dataset.label) {
		        legend += dataset.label
		      }
		      legend += "</span></li>";
		    })
		    legend += "</ul>";

		    setTimeout(function(){
			    document.getElementById("p1").innerHTML = legend;
		    },500)
		});
	}

	self.show_session_detail = function()
	{
		var response = self.post_generic("/dashboard/read_monthly_session_created/", null, "main4")
		response.success(function(response){

			var labels = []
			var data = []
			var data2 = []
			for(x in response.data){
				labels.push(response.data[x].month)
				data.push(response.data[x].created)
				data2.push(response.data[x].inactive)
			}

			self.lineData2 = {
				labels:labels,
				datasets: [
					{
						label: "Sessions created",
		            	fillColor: "#84d0c1",
		                strokeColor: "#00b893",
		                pointColor: "#00b893",
		                pointStrokeColor: "#fff",
		                pointHighlightFill: "#00b893",
		                pointHighlightStroke: "#00b893",
		            	data: data
					},
					{
		            	label: "Inactive sessions",
		            	fillColor: "#eeeeee",
		            	strokeColor: "#c9c9c9",
		            	pointColor: "#c9c9c9",
		            	pointStrokeColor: "#fff",
		            	pointHighlightFill: "#c9c9c9",
		            	pointHighlightStroke: "#c9c9c9",
		            	data: data2
		            },
				]
			}
			self.open_dialog("/get_dialog/dashboard/monthly_session_created/", 'dialog_width_50');
			var legend = "<ul style=\"list-style-type:none;\">";
		    self.lineData2.datasets.forEach(function(dataset){
		      legend += "<li><div style=\"background-color:" + dataset.strokeColor + ";height:0.5em;width:0.5em;float:left;margin-top:0.5em;margin-right:0.5em;\"></div><span style='font-family:Verdana;font-size: 12px;'>";
		      if (dataset.label) {
		        legend += dataset.label
		      }
		      legend += "</span></li>";
		    })
		    legend += "</ul>";

		    setTimeout(function(){
			    document.getElementById("p2").innerHTML = legend;
		    },500)
		});
	}

	self.showUnenrolledSessionsGraph = function()
	{
		var response = self.post_generic("/dashboard/unenrolled_sessions_graph/", null, "main3")
		response.success(function(response){
			var labels = [], data1 = [], data2 = [];
			$scope.unenrolled_sessions = response.session_list

			for(x in response.graph_data){
				labels.push(response.graph_data[x].month);
				data1.push(response.graph_data[x].session_count);
				data2.push(response.graph_data[x].inactive_session_count);
			}

			self.lineData = {
				labels: labels,
				datasets: [
					{
						label: 'Unenrolled Sessions',
		            	fillColor: "#84d0c1",
		                strokeColor: "#00b893",
		                pointColor: "#00b893",
		                pointStrokeColor: "#fff",
		                pointHighlightFill: "#00b893",
		                pointHighlightStroke: "#00b893",
		            	data: data1,
					},
					{
		            	label: 'Inactive',
		            	fillColor: "#eeeeee",
		            	strokeColor: "#c9c9c9",
		            	pointColor: "#c9c9c9",
		            	pointStrokeColor: "#fff",
		            	pointHighlightFill: "#c9c9c9",
		            	pointHighlightStroke: "#c9c9c9",
		            	data: data2,
		            },
				]
			}

			self.open_dialog("/get_dialog/dashboard/unenrolled_sessions_graph/", 'dialog_width_25');
			
			var legend = "<ul style=\"list-style-type:none;\">";
		    self.lineData.datasets.forEach(function(dataset){
		    	legend += "<li><div style=\"background-color:" + dataset.strokeColor + ";height:0.5em;width:0.5em;float:left;margin-top:0.5em;margin-right:0.5em;\"></div><span style='font-family:Verdana;font-size: 12px;'>";
		      	
		      	if (dataset.label) {
		        	legend += dataset.label
		      	}
		      	
		      	legend += "</span></li>";
		    })

		    legend += "</ul>";

		    setTimeout(function(){
			    document.getElementById("p1").innerHTML = legend;
		    }, 500)
		});
	}

	self.read_session_status = function()
	{
		var response = self.post_generic("/dashboard/read_sessions_status/", null, "main")
		response.success(function(response){

			self.session_data = response;
			calculate_remaining_time();

		});
	}

	self.read_student_birthdate = function()
	{
		var response = self.post_generic("/dashboard/read_student_birthdate/", null, "main3")
		response.success(function(response){
			self.student_birthdates = response.data
		})
	}

	self.init = function()
	{
		self.read_session_status();
		self.read_student_status();
		self.read_student_birthdate();
	}

	function calculate_remaining_time()
	{
		self.today = new Date();

		for(i in self.session_data.expiring_sessions)
		{
			var session_date = new Date(self.session_data.expiring_sessions[i].session_date);

			var session_timeout = new Date(self.session_data.expiring_sessions[i].session_timeout);
			session_timeout.setFullYear(self.today.getFullYear());
			session_timeout.setMonth(self.today.getMonth());
			session_timeout.setDate(self.today.getDate());

			var difference = session_timeout - self.today;

			minutes = Math.floor(difference / 60000);
			seconds = Math.floor(difference / 1000);

			if(seconds >= 0)
			{
				self.session_data.expiring_sessions[i].time_remaining = seconds;
				if(seconds >= 900){
					self.session_data.expiring_sessions[i].class_row = "green_row"
				}else if(seconds >= 301 && seconds <= 899){
					self.session_data.expiring_sessions[i].class_row = "yellow_row"
				}else if(seconds >= 1 && seconds <= 300){
					self.session_data.expiring_sessions[i].class_row = "orange_row"
				}
			}
			else{
				self.session_data.expiring_sessions[i].class_row = "red_row"
			}
		}
	}

	self.init = function()
	{
		self.read_session_status();
		self.read_student_status();
	}


	self.init();

});