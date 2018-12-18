angular.module("customFilters", []).
	filter('dateInMillis', function(){
		return function(dateString){
			return Date.parse(dateString);
		};
	});