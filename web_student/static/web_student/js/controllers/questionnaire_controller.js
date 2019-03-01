angular.module("app")

.controller("QuestionnaireCtrl", function ($scope,$controller) {

    angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
    var self = this;


    self.session_exercises = function()
    {
        let response = self.post_api("/session_exercises/read/");

        response.then(function(response){

        }, function (response){

        });
    };

    self.read_questions = function()
    {
        let response = self.post_api("question/read/");

        response.then(function(response){
            let data = response.data;
            self.questions = data.records;

        }, function (response){

        });
    };

    self.read_questions();
});