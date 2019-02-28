var app = angular.module('app', [
    'ui.router',
]);

app.config(['$httpProvider', '$interpolateProvider', function($httpProvider, $interpolateProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $interpolateProvider.startSymbol('{$').endSymbol('$}');
}]);

app.config(function($stateProvider) {

    var dashboardState = {
        name: 'dashboard',
        url: 'dashboard',
        templateUrl: '/student_portal/dashboard/'
    };

    var sessionsState = {
        name: 'sessions',
        url: '/sessions',
        templateUrl: '/student_portal/session_page/'
    };

    var centerState = {
        name: 'learning_centers',
        url: '/learning_centers',
        templateUrl: '/student_portal/learning_centers/programs/'
    };

    var questionnaireState = {
        name: 'questionnaire',
        url: '/questionnaire',
        templateUrl: '/student_portal/questionnaire/'
    };

    $stateProvider.state(questionnaireState);
    $stateProvider.state(sessionsState);
    $stateProvider.state(dashboardState);
    $stateProvider.state(centerState);
});

// app.config(function(toastrConfig) {
//   angular.extend(toastrConfig, {
//     progressBar : true,
//     newestOnTop: true,
//     maxOpened : 5,
//     timeOut: 7000,
//   });
// });
//
// app.config(['$uibTooltipProvider', function ($uibTooltipProvider) {
//     $uibTooltipProvider.options({
//         'placement': 'bottom'
//     });
// }]);
//
// app.config(function(uiSelectConfig) {
//     angular.extend(uiSelectConfig,{
//         theme : "bootstrap",
//         placeholder : "Select...",
//     })
// });