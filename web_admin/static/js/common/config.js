var app =angular.module('common_config', [
	'ngAnimate',
	'ngSanitize',
    'ui.bootstrap',
	'ui.select',
	'oitozero.ngSweetAlert',
	'jutaz.ngSweetAlertAsPromised',
	'toastr',
])

app.config(['$httpProvider', '$interpolateProvider', function($httpProvider, $interpolateProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $interpolateProvider.startSymbol('{$').endSymbol('$}');
}]);

app.config(function(toastrConfig) {
  angular.extend(toastrConfig, {
    progressBar : true,
    newestOnTop: true,
    maxOpened : 5,
    timeOut: 7000,
  });
});

app.config(['$uibTooltipProvider', function ($uibTooltipProvider) {
    $uibTooltipProvider.options({
        'placement': 'bottom'
    });
}]);

app.config(function(uiSelectConfig) {
    angular.extend(uiSelectConfig,{
        theme : "bootstrap",
        placeholder : "Select...",
    })
});