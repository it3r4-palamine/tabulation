angular.module("app")

.controller("QuestionnaireCtrl", function ($scope, $controller, $stateParams, SweeterAlert) {

    angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
    var self = this;

    self.questions     = [];
    self.session_id    = $stateParams.uuid;
    self.session_name  = $stateParams.name;
    self.enrollment_id = $stateParams.enrollment_id;
    self.program_id    = $stateParams.program_id;

    self.read_session_exercises = function()
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

        let exercise = {
            "session" : self.session_id,
            "exercise" : record.exercise.id,
            "session_exercise" : record.uuid
        };

        let response = self.post_api("question/read_exercise_questions/", exercise);

        response.then(function(response){
            let data = response.data;
            self.questions = data.records;

        }, function (response){

        });
    };

    self.submit_answers = function()
    {
        let data = {
            "session" : self.session_id,
            "session_exercise" : self.current_exercise.uuid,
            "questions" : self.questions,
            "enrollment" : self.enrollment_id,
            "program" : self.program_id,
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
            SweeterAlert.error(response.data)
        });
    };

})

.directive('icheck', function($timeout)
{
    return {
        restrict: 'A',
        require: 'ngModel',
        link: function($scope, element, $attrs, ngModel)
        {
            return $timeout(function()
            {
                var value;
                value = $attrs['value'];

                $scope.$watch($attrs['ngModel'], function(newValue){
                    $(element).iCheck('update');
                })

                return $(element).iCheck({
                    checkboxClass: 'icheckbox_square-green',
                    radioClass: 'iradio_square-green'

                }).on('ifChanged', function(event) {
                        if ($(element).attr('type') === 'checkbox' && $attrs['ngModel']) {
                            $scope.$apply(function() {
                                return ngModel.$setViewValue(event.target.checked);
                            });
                        }
                        if ($(element).attr('type') === 'radio' && $attrs['ngModel']) {
                            return $scope.$apply(function() {
                                return ngModel.$setViewValue(value);
                            });
                        }
                    });
            });
        }
    };
})