angular.module("app")

.controller("DashboardCtrl", function ($scope,$controller) {

    angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
    var self = this;

    self.test = function()
    {
        alert("Working")
    };

    self.read_enrolled_programs = function()
    {
        let response = self.post_api("enrollment/read/");

        response.then(function (response) {

            let data = response.data;
            self.enrolled_programs = data.records;

        }, function (response) {

        });

    };

    self.read_sessions = function()
    {
        let response = self.post_api("sessions/read/");

        response.then(function (response) {

        }, function (response) {

        });
    };

    self.read_sessions();
    self.read_enrolled_programs();

});