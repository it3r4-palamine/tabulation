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
        let response = self.post_api("test");
    }

});