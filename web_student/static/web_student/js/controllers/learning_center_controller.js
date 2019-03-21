angular.module("app")

.controller("LearningCenterCtrl", function ($scope, $controller ,$stateParams)
{
    angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
    let self = this;

    self.center_id       = $stateParams.id;
    self.learning_center = {};

    self.read_learning_center_info = function()
    {
        let response = self.get_api("learning_center/read/" + self.center_id);

        response.then( function(response){
            let data = response.data;
            self.learning_center = data.record;
        });
    };

    self.read_courses = function()
    {
        let filters = { center_id : self.center_id };

        let post = self.post_api("course/read/", filters, "main");

		post.then(function(response){
		    let data = response.data;
			self.courses = data.records;
		});
    };

    self.read_learning_center_info();
    self.read_courses();

});

