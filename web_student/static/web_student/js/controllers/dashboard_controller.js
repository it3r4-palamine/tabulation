angular.module("app")

.controller("DashboardCtrl", function ($scope,$controller,$uibModal, CommonRead) {

    angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
    var self = this;

    self.open_search_sidenav = function()
    {
        // self.open_dialog("", "animated slideInLeft left");

        var dialog = $uibModal.open({
	        templateUrl: "/student_portal/get_dialog/user/dialog_search/",
	        windowClass : "slide-in-left left-side-modal",
	        keyboard : true,
	        scope : $scope,
            animation : true,
	    });

	    dialog.opened.then(function(){
			// self.page_loader[key] = false;
	    	// self.current_dialogs.push(dialog)
	    });

    };

    self.open_account_sidenav = function()
    {
        var dialog = $uibModal.open({
	        templateUrl: "/student_portal/get_dialog/user/sidenav_account/",
	        windowClass : "slide-in-right right-side-modal",
	        keyboard : true,
	        scope : $scope,
            animation : true,
	    });

        dialog.opened.then(function(){
			// self.page_loader[key] = false;
	    	// self.current_dialogs.push(dialog)
	    });
    };

    self.open_notification_sidenav = function()
    {
        var dialog = $uibModal.open({
	        templateUrl: "/student_portal/get_dialog/user/sidenav_notifications/",
	        windowClass : "slide-in-right right-side-modal",
	        keyboard : true,
	        scope : $scope,
            animation : true,
	    });

        dialog.opened.then(function(){
			// self.page_loader[key] = false;
	    	// self.current_dialogs.push(dialog)
	    });
    }

    self.read_enrolled_programs = function()
    {
        let response = self.post_api("enrollment/read/");

        response.then(function (response) {

            let data = response.data;
            self.enrolled_programs = data.records;

        }, function (response) {

        });

    };

    self.read_learning_centers = function()
    {
        let response = self.get_api("learning_center/read/");

        response.then(function (response) {

            let data = response.data;
            self.learning_centers = data.records;

        }, function (response){

        });
    };

    self.read_sessions = function()
    {
        let response = self.post_api("sessions/read/");

        response.then(function (response) {

        }, function (response) {

        });
    };



    // self.read_sessions();
    self.read_enrolled_programs();
    // self.read_learning_centers();

    CommonRead.get_learning_centers(self);

});