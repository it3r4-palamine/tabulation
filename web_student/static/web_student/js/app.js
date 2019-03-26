var app = angular.module('app', [
    'ui.carousel',
    'ui.router',
    'ui.bootstrap',
    'toaster',
    'ui.select',
    'common_controller',
    'common_services',
    'oitozero.ngSweetAlert',
]);

app.config(['$httpProvider', '$interpolateProvider', function($httpProvider, $interpolateProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $interpolateProvider.startSymbol('{$').endSymbol('$}');
}]);
