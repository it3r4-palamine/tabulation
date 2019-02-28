angular.module("app")

.controller("DashboardCtrl", function ($scope) {

    var self = this;

    self.test = function()
    {
        alert("Working")
    };

    self.test();
});