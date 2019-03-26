angular.module("app")

.controller("LearningCenterCtrl", function ($scope, $controller, $state, $stateParams, CommonFunc, SweeterAlert)
{
    angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
    let self = this;

    self.center_id       = $stateParams.id;
    self.learning_center = {};

    self.read_learning_center_info = function()
    {
        if ($state.current.name === "learning_centers")
        {
            let response = self.get_api("learning_center/read/" + self.center_id);

            response.then(function(response){
                let data = response.data;
                self.learning_center = data.record;
            });
        }
    };

    self.read_course_details = function()
    {
        if ($state.current.name === "course_details")
        {
            console.log($stateParams.uuid)
            let course_uuid = $stateParams.uuid;
            let response = self.get_api("course/get/" + course_uuid);

            response.then(function(response){
                self.course = response.data;
            });
        }
    };

    self.read_courses = function()
    {
        let filters = { center_id : self.center_id };

        let response = self.post_api("course/read/", filters, "main");

		response.then(function(response){
		    let data = response.data;
			self.courses = data.records;
		});
    };

    self.enroll_course = function(record)
    {
        CommonFunc.confirmation("Confirm Enrollment", "pag sure, mahal baya ni", null, null, function(){

            let response = self.post_api("enroll_course/", self.course, "main").then(function(response){

                SweeterAlert.simple("Enrolled naka bes")

            }, function(response){
                let data = response.data;
                SweeterAlert.error(data);

            });
        })
    };



});

