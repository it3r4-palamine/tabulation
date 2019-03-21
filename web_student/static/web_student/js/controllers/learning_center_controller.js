angular.module("app")

.controller("LearningCenterCtrl", function ($scope, $controller ,$stateParams)
{
    angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
    let self = this;

    self.center_id = $stateParams.id;

    self.read_learning_center_info = function()
    {

    };

    self.read_courses = function()
    {
        let filters = { center_id : self.center_id };

        let post = self.post_api("course/read/", filters, "main");
		post.then(function(response){
		    let data = response.data;
			self.records = data.records;
			console.log(self.records)
		});
    };

    self.read_courses();

});