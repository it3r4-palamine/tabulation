var app = angular.module('app', [
    'ui.router',
    'ui.bootstrap',
    'toaster',
    'common_controller',
]);

app.config(['$httpProvider', '$interpolateProvider', function($httpProvider, $interpolateProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $interpolateProvider.startSymbol('{$').endSymbol('$}');
}]);

