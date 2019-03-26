angular.module("app")

.controller("QuestionnaireCtrl", function ($scope, $controller, $stateParams) {

    angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
    var self = this;

    self.session_id = $stateParams.uuid;


    self.session_exercises = function()
    {
        console.log(self.session_id)
        let response = self.post_api("session/read_session_exercises/", { "uuid" : self.session_id });

        response.then(function(response){

            let data = response.data;
            self.session_exercises = data.records;

        }, function (response){

        });
    };

    self.read_questions = function(record)
    {
        let exercise = { "exercise" : record.exercise.id };
        let response = self.post_api("question/read_exercise_questions/", exercise);

        response.then(function(response){
            let data = response.data;
            self.questions = data.records;

        }, function (response){

        });
    };

    self.test = function()
    {
        let response = self.post_api("student_answers/save/", self.questions);

        response.then(function(response){


        }, function (response){

        });
    };

    self.session_exercises();
});