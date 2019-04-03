var app = angular.module("questions", ['common_module', 'file-model', 'angular-sortable-view','ui.bootstrap.contextMenu']);

app.controller('QuestionCtrl', function($scope, $http, $timeout, $element, $controller, CommonFunc, RightClick, Notification, CommonRead)
{
	angular.extend(this, $controller('CommonCtrl', {$scope: $scope }));
	var self = this;
	self.current_module = "questions";

	// Controller Variables
	self.filters 		  = { name : '' };
	self.record 		  = {};
	self.choice           = {};
	self.question_choices = [];


	self.create_edit_record = function(record)
	{
		self.record = {};

		if (record)
		{
			self.record = angular.copy(record);
			self.get_record(record);


		} else {

			self.initiate();

		}

		self.open_dialog("/get_dialog/questions/dialog_create/", 'dialog_width_80 dialog_width_50', 'main')
	};

	self.add_question_choices = function(data)
	{
		self.question_choices.push({ name: '' , is_correct : false });
	};

	self.delete_question_choices = function(record){
		self.question_choices.splice(self.question_choices.indexOf(record), 1);
	};

	self.initiate = function()
	{
		self.record = {};
		self.question_choices = [];
		self.question_choices.push( { name: '', is_correct : false, options: false})

	};

	self.delete_record = function(record)
	{
		let confirmation = CommonFunc.confirmation("Delete Question " + record.name + "?");
		confirmation.then(function(){

			self.delete_api("question/delete/" + record.uuid, null, "main")
				.success(function(response){
					Notification.success(response);
					self.main_loader();
				})
				.error(function(response){
					Notification.warning(response);
				})
		})
	};

	self.save_record = function(record)
	{
		self.record.question_choices = self.question_choices;

		self.post_api('question/create/', record, null, true, null, false)
			.success(function(response){
				self.close_dialog();
				self.main_loader();
			}).error(function(response){
			})
	};

	self.validate_record = function(data)
	{



		return true;
	};

	self.get_record = function(record)
	{
		let response = self.get_api("question/get/" + record.uuid + "/");

		response.success(function(response){
			self.record = response;
			self.question_choices = response.question_choices;
		})
	};

    self.read_pagination = function(reset)
	{
		if (reset) self.reset_filter();

		self.filters["sort"] = self.sort;
		var filters = angular.copy(self.filters);
		filters = self.format_date(filters);
		filters = self.format_time(filters);

		self.pagination["limit"] = 20;
		filters["pagination"] = self.pagination;

		var post = self.post_api("question/read/", filters, "main");
		post.success(function(response){
			self.records = response.records;
			self.generate_pagination(self,response,"records");
		});

		post.error(function(response){
			Notification.warning(response);
		});
	};

    self.menu_options = function (record) {
	    return RightClick.get_menu(self, record);
	};

	self.main_loader = function(){ self.read_pagination(); };

	CommonRead.get_question_types(self);
	CommonRead.get_subjects(self);

	self.main_loader();
})

.directive('icheck', function($timeout)
{
    return {
        restrict: 'A',
        require: 'ngModel',
        link: function($scope, element, $attrs, ngModel)
        {
            return $timeout(function()
            {
                var value;
                value = $attrs['value'];

                $scope.$watch($attrs['ngModel'], function(newValue){
                    $(element).iCheck('update');
                })

                return $(element).iCheck({
                    checkboxClass: 'icheckbox_square-green',
                    radioClass: 'iradio_square-green'

                }).on('ifChanged', function(event) {
                        if ($(element).attr('type') === 'checkbox' && $attrs['ngModel']) {
                            $scope.$apply(function() {
                                return ngModel.$setViewValue(event.target.checked);
                            });
                        }
                        if ($(element).attr('type') === 'radio' && $attrs['ngModel']) {
                            return $scope.$apply(function() {
                                return ngModel.$setViewValue(value);
                            });
                        }
                    });
            });
        }
    };
})
