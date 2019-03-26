angular.module("app")

.controller("QuestionnaireCtrl", function ($scope, $controller, $stateParams, SweeterAlert) {

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
        if (!record.has_answered)
        {
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
        let response = self.post_api("student_answers/save/", self.questions);

        response.then(function(response){

            let data = {
                title : response.data,
                message : "Exercise Completed"
            };

            SweeterAlert.simple(data)

        }, function (response){
            SweeterAlert.error(response)
        });
    };

    self.session_exercises();
});