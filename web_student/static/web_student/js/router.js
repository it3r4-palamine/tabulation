var app = angular.module("app");

app.config(function($stateProvider,$urlRouterProvider) {

    var dashboardState = {
        name: 'dashboard',
        url: '/dashboard',
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
        url: '/learning_centers?id',
        templateUrl: '/student_portal/learning_centers/programs/',
        controller : "LearningCenterCtrl",
        params : {
            id : null,
        }
    };

    var questionnaireState = {
        name: 'questionnaire',
        url: '/questionnaire',
        templateUrl: '/student_portal/questionnaire/',
        controller : 'QuestionnaireCtrl as ctrl'
    };

    var coursesState = {
        name : 'courses',
        url : '/courses',
        templateUrl: '/student_portal/courses/'
    };

    $stateProvider.state(questionnaireState);
    $stateProvider.state(sessionsState);
    $stateProvider.state(dashboardState);
    $stateProvider.state(centerState);
    $stateProvider.state(coursesState);

    $urlRouterProvider.otherwise('/dashboard');

});