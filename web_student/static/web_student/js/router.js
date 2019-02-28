var app = angular.module("app");

app.config(function($stateProvider) {

    var dashboardState = {
        name: 'dashboard',
        url: 'dashboard',
        templateUrl: '/student_portal/dashboard/',
        controller : 'DashboardCtrl as ctrl',
    };

    var sessionsState = {
        name: 'sessions',
        url: '/sessions',
        templateUrl: '/student_portal/session_page/',
        controller: 'SessionCtrl'
    };

    var centerState = {
        name: 'learning_centers',
        url: '/learning_centers',
        templateUrl: '/student_portal/learning_centers/programs/'
    };

    var questionnaireState = {
        name: 'questionnaire',
        url: '/questionnaire',
        templateUrl: '/student_portal/questionnaire/',
        controller : 'QuestionnaireCtrl as ctrl'
    };

    $stateProvider.state(questionnaireState);
    $stateProvider.state(sessionsState);
    $stateProvider.state(dashboardState);
    $stateProvider.state(centerState);

});