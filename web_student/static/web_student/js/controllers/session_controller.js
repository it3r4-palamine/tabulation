angular.module("app")

.controller("SessionCtrl", function ($scope) {

    var self = this;

    self.test = function()
    {
        alert("Session")
    };

});