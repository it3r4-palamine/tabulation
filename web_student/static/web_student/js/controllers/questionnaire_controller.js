angular.module("app")

.controller("QuestionnaireCtrl", function ($scope, $controller, $stateParams, SweeterAlert) {

    angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
    var self = this;

    self.questions    = [];
    self.session_id   = $stateParams.uuid;
    self.session_name = $stateParams.name;


    self.session_exercises = function()
    {
        let response = self.post_api("session/read_session_exercises/", { "uuid" : self.session_id });

        response.then(function(response){

            let data = response.data;
            self.session_exercises = data.records;

        }, function (response){

        });
    };

    self.read_questions = function(record)
    {
        self.current_exercise = angular.copy(record);

        if (!record.has_answered)
        {
            console.log(record);

            let exercise = { "exercise" : record.exercise.id };
            let response = self.post_api("question/read_exercise_questions/", exercise);

            response.then(function(response){
                let data = response.data;
                self.questions = data.records;

            }, function (response){

            });
        } else {
            SweeterAlert.error({title: "Exercise already answered", message: ""})
        }
    };

    self.test = function()
    {
        let data = {
            "session_exercise" : self.current_exercise.uuid,
            "questions" : self.questions
        };

        let response = self.post_api("student_answers/save/", data);

        response.then(function(response){

            let data = {
                title : response.data,
                message : "Exercise Completed"
            };

            SweeterAlert.simple(data);

            self.session_exercises();

        }, function (response){
            SweeterAlert.error(response.data)
        });
    };

});