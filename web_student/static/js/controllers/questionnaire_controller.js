angular.module("app")

.controller("QuestionnaireCtrl", function ($scope) {

    var self = this;

    self.test = function()
    {
        alert("Questionnaire")

        let response = self.post_api("test/");

    };


});