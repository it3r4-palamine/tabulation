var app = angular.module("app");

app.config(function($stateProvider,$urlRouterProvider) {

    let dashboardState = {
        name: 'dashboard',
        url: '/dashboard',
        templateUrl: '/student_portal/dashboard/',
        controller : 'DashboardCtrl as ctrl',
    };

    let sessionsState = {
        name: 'sessions',
        url: '/sessions',
        templateUrl: '/student_portal/session_page/',
        controller: 'SessionCtrl as ctrl'
    };

    let centerState = {
        name: 'learning_centers',
        url: '/learning_centers?id',
        templateUrl: '/student_portal/learning_centers/programs/',
        controller : "LearningCenterCtrl",
        params : {
            id : null,
        }
    };

    let courseState = {
        name: 'course_details',
        url: '/course_details?uuid',
        templateUrl: '/student_portal/learning_centers/course_details/',
        controller : "LearningCenterCtrl as ctrl",
        params : {
            uuid : null,
        }
    };

    let questionnaireState = {
        name: 'questionnaire',
        url: '/questionnaire?uuid?name',
        templateUrl: '/student_portal/questionnaire/',
        controller : 'QuestionnaireCtrl as ctrl',
        params : {
            uuid : null,
            name : null,
            enrollment_id : null,
            program_id : null,
        }
    };

    let coursesState = {
        name : 'courses',
        url : '/courses',
        templateUrl: '/student_portal/courses/'
    };

    $stateProvider.state(questionnaireState);
    $stateProvider.state(courseState);
    $stateProvider.state(sessionsState);
    $stateProvider.state(dashboardState);
    $stateProvider.state(centerState);
    $stateProvider.state(coursesState);

    $urlRouterProvider.otherwise('/dashboard');

});