angular.module("app")

.controller("QuestionnaireCtrl", function ($scope, $controller, $stateParams, SweeterAlert) {

    angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
    var self = this;

    self.questions          = [];
    self.session_id         = $stateParams.uuid;
    self.session_name       = $stateParams.name;
    self.enrollment_id      = $stateParams.enrollment_id;
    self.program_id         = $stateParams.program_id;
    self.is_assessment_test = $stateParams.is_assessment_test;
    self.course_id          = $stateParams.course_id;

    self.read_session_exercises = function()
    {
        let filters = {
            "uuid" : self.session_id,
            "enrollment_id" : self.enrollment_id,
            "program_id" : self.program_id,
            "is_assessment_test" : self.is_assessment_test,
            "course_id" : self.course_id,
        };

        let response = self.post_api("session/read_session_exercises/", filters);

        response.then(function(response){

            let data = response.data;
            self.session_exercises = data.records;
            self.session_videos    = data.session_videos

        }, function (response){

        });
    };

    self.read_questions = function(record)
    {
        self.current_exercise = angular.copy(record);

        let exercise = {
            "session" : self.session_id,
            "exercise" : record.exercise.id,
            "session_exercise" : record.uuid,
            "enrollment_id" : self.enrollment_id,
            "program_id" : self.program_id,
            "is_assessment_test" : self.is_assessment_test,
        };

        let response = self.post_api("question/read_exercise_questions/", exercise);

        response.then(function(response){
            let data = response.data;
            self.questions = data.records;

        }, function (response){
            SweeterAlert.error({title : "Oops!", message : response.data});
        });
    };

    self.select_question = function(question) {
        self.selected_question = angular.copy(question);
    };

    self.submit_answers = function()
    {
        let data = {
            "session" : self.session_id,
            "session_exercise" : self.current_exercise.uuid,
            "questions" : self.questions,
            "enrollment" : self.enrollment_id,
            "program" : self.program_id,
            "is_assessment_test" : self.is_assessment_test,
        };

        let response = self.post_api("student_answers/save/", data);

        response.then(function(response){

            let data = {
                title : response.data,
                message : "Exercise Completed"
            };

            SweeterAlert.simple(data);

            self.read_session_exercises();
            self.questions = [];

        }, function (response){
            SweeterAlert.error({title : "Oops!", message : response.data});
        });
    };

    self.checkUnicode = function(idx)
    {
        for (var i = 0; i < self.questions[idx].question_choices.length; i++)
        {
            self.questions[idx].question_choices[i].isUnicode = false;

            for (var j = 0; j < self.questions[idx].question_choices[i].name.length; j++)
            {
                if (self.questions[idx].question_choices[i].name.charCodeAt(j) > 128)
                {
                    self.questions[idx].question_choices[i].isUnicode = true
                }
            }
        }
    }

});

app.filter('trusted', ['$sce', function ($sce) {
    return function(url) {
            var video_id = url.split('v=')[1].split('&')[0];
        return $sce.trustAsResourceUrl("https://www.youtube.com/embed/" + video_id);
    };
}]);

