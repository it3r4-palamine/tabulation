angular.module("app")

.controller("SessionCtrl", function ($scope, $controller, CommonRead) {

    angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
    let self = this;

    self.sessions = [];

    self.read_sessions = function()
    {
        let response = self.post_api("read_student_sessions/");

        response.then(function(response){

            let data      = response.data;
            self.sessions = data.records;

        }, function (response) {

        })
    };

    CommonRead.get_learning_centers(self);

});