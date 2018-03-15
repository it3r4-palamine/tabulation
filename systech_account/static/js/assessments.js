var app = angular.module("assessments",['common_module','file-model']);

app.controller('assessmentsCtrl', function($scope, $http, $uibModal, $templateCache, $timeout, $element, $controller,CommonFunc,Notification,CommonRead) {
	angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
	var me = this;
	$scope.record = {}
	$scope.filter = {}

	$scope.choices = []
	$scope.effects = []
	$scope.findings = []
	$scope.answers = []

	$scope.chooseQuestion = function(record){
		swal({
		  title: "",
		  showConfirmButton: false,
		  text: "What would you like to create?<br><button>Back</button><button style='background-color: #DD6B55;' id='ot_not_now'>Upload</button><button style='background-color: #3f51b5;' id='ot_yes_now'>Normal</button>",
		  html: true
		});

		$("#ot_not_now").click(function(){
		    $scope.create_dialog(record, true);
		});

		$("#ot_yes_now").click(function(){
		    $scope.create_dialog(record, false);
		});
	}

	$scope.create_dialog = function(record, upload){
		$scope.edit_is_related = false
		$scope.choices = []
		$scope.effects = []
		$scope.findings = []
		$scope.answers = []
		$scope.ImageSrc = []
		$scope.ImageSrcUpload = []
		$scope.multiple_answer_list = []
		$scope.answer_list_arr = []
		$scope.choice_list = {}
		$scope.effect_list = {}
		$scope.finding_list = {}
		$scope.answer_list = {}
		$scope.record = {}
		$scope.record['is_active'] = true
		if(record){
			$scope.record = angular.copy(record);
			$scope.choices = $scope.record.choices
			$scope.effects = $scope.record.effects
			$scope.findings = $scope.record.findings
			$scope.answers = $scope.record.answers
			if($scope.record.timer){
				$scope.record.has_timer = true
			}

			for(var ans in $scope.answers){
				$scope.multiple_answer_list[ans] = {}
				for(var ans2 in $scope.answers[ans].answer){
					$scope.answers[ans].answer[ans2].answer_display = "\\(" + $scope.answers[ans].answer[ans2].name + "\\)"
				}
			}
			$scope.ImageSrc = $scope.record.images
		}
		
		if(upload) {
			// me.open_dialog("/assessments/upload_dialog/","dialog_whole","main")
			$("#myModal").modal('toggle');
		}
		else {
			me.open_dialog("/assessments/create_dialog/","dialog_whole","main")
		}
	}

	$scope.upload_close_dialog = function(){
		$("#myModal").modal('toggle');
	}

	$scope.close_dialog = function(){$uibModalStack.dismissAll();}

	$scope.old_is_related = null
	$scope.create = function(not_upload){
		if(Object.keys($scope.choice_list).length > 0) {
			if($scope.choice_list.value){
				$scope.choices.push(angular.copy($scope.choice_list))
			}
		}
		if(Object.keys($scope.effect_list).length > 0) {
			if($scope.effect_list.value){
				$scope.effects.push(angular.copy($scope.effect_list))
			}
		}
		if(Object.keys($scope.finding_list).length > 0) {
			if($scope.finding_list.value){
				$scope.findings.push(angular.copy($scope.finding_list))
			}
		}
		if(Object.keys($scope.answer_list).length > 0) {
			if($scope.answer_list.name && $scope.answer_list.item_no){
				var new_data = {
					name : $scope.answer_list.name,
					answer_display : $scope.answer_list.answer_display
				}
				$scope.answer_list_arr.push(new_data)
				// $scope.answers.push(angular.copy($scope.answer_list))
			}
		}
		console.log($scope.answer_list_arr)
		if($scope.answer_list_arr.length > 0){
			var newArr = {
				answer : $scope.answer_list_arr,
				item_no : $scope.answer_list.item_no
			}

			$scope.answers.push(angular.copy(newArr))
		}
		// if(Object.keys($scope.answer_list).length > 0) {
		// 	if($scope.answer_list.answer && $scope.answer_list.item_no){
		// 		$scope.answers.push(angular.copy($scope.answer_list))
		// 	}
		// }
		var has_true = 0
		var has_required_document = 0
		if($scope.record.is_document == undefined) $scope.record.is_document = false;
		if(!not_upload)
			if($scope.record.has_timer == undefined || $scope.record.has_timer == false) $scope.record.timer = 0;
		for(x in $scope.choices){
			if($scope.choices[x].is_answer == true){
				has_true++
			}

			if($scope.record.is_document){
				if($scope.choices[x].required_document_image == true){
					has_required_document++
				}
			}else{
				$scope.choices[x].required_document_image = false
			}
		}
		$scope.choice_list = {}
		$scope.effect_list = {}
		$scope.finding_list = {}
		$scope.answer_list = {}
		if($scope.record.is_multiple == undefined) $scope.record.is_multiple = false;
		if(not_upload){

			if($scope.record.is_multiple){
				if(has_true > 1){
					$scope.record['has_multiple_answer'] = true
				}else if(has_true == 0){
					$scope.record['has_multiple_answer'] = false
					return Notification.error("The question has no correct answer. Please select one.")
				}else if(has_true == 1){
					$scope.record['has_multiple_answer'] = false
				}
			}else{
				if(!$scope.record.answer_type){
					return Notification.error("Please select answer type.")	
				}
				if(has_true > 1){
					$scope.record['has_multiple_answer'] = true
				}else if(has_true == 0){
					$scope.record['has_multiple_answer'] = false
					return Notification.error("The question has no correct answer. Please select one.")
				}else if(has_true == 1){
					$scope.record['has_multiple_answer'] = false
				}
			}

			if($scope.record.is_document){
				if(has_required_document == 0){
					return Notification.error("Please select a choice that requires document image.")
				}
			}
		}

		if($scope.record.is_general == false) $scope.record.transaction_types = []

		$scope.record['choices'] = $scope.choices
		$scope.record['effects'] = $scope.effects
		$scope.record['findings'] = $scope.findings
		$scope.record['answers'] = $scope.answers
		$scope.record['old_is_related'] = $scope.old_is_related
		if($scope.record.parent_question){
			$scope.record.parent_question.has_follow_up = true;
		}

		record_data = $scope.record
		var company_settings = new FormData();
		var questionImg = []
		angular.forEach(record_data, function(value, key){
		    if(record_data[key] === undefined){
		        value = ""
		    }
		    is_continue = true;
		    if(key == 'images'){
		    	for(var y in record_data[key]){
					if(typeof record_data[key][y] === 'object' || typeof record_data[key][y] === 'string'){
						company_settings.append(key,record_data[key][y])
					}
		    	}
		    	is_continue = false;
		    }

		    if(is_continue){
			    if(key == 'transaction_type'){
			    	value = record_data[key].id
			    }
			    company_settings.append(key, value);
		    }
		})

		if(not_upload){
			me.post_generic("/assessments/create/",$scope.record,"dialog")
			.success(function(response){
				me.close_dialog();
				Notification.success(response);
				$scope.read();
			}).error(function(err){
				if(err=='code'){
					Notification.error("Code already exists.")
				}else{
					Notification.error(err)
				}
			})
		}else{
			$('body').loadingModal({text: 'Saving...'});
			$('body').loadingModal('animation', 'cubeGrid');
			$('body').loadingModal('backgroundColor', 'green');
			$http.post('/assessments/upload/', company_settings, { 
			    method: "post", 
			    transformRequest: angular.identity, 
			    headers: {'Content-Type': undefined} 
			}).success(function(response){ 
			    // Notification.success(response)
			    // me.close_dialog();
			    // $scope.read();
			    $scope.saveData($scope.record, response)
			})
			.error(function(err){
				$('body').loadingModal('hide');
				$('body').loadingModal('destroy') ;
			    if(err=='code'){
					Notification.error("Code already exists.")
				}else{
					Notification.error(err)
				}
			})
		}

	}

	$scope.saveData = function(record, id) {
		var datus = {
			answers: $scope.record.answers
			effects: $scope.record.effects
			findings: $scope.record.findings
		}
		var data = {
			datus : datus,
			id : id
		}
		me.post_generic("/assessments/saveData/",data,"dialog")
		.success(function(response){
			$('body').loadingModal('hide');
    		$('body').loadingModal('destroy') ;
			// me.close_dialog();
			$("#myModal").modal('toggle');
			Notification.success(response);
			$scope.read();
		}).error(function(err){
			$('body').loadingModal('hide');
			$('body').loadingModal('destroy') ;
			if(err=='code'){
				Notification.error("Code already exists.")
			}else{
				Notification.error(err)
			}
		})
	}

	$scope.setimage = function() {
	    var file = $scope.record;
	    var fayl = document.getElementById('my-file-selector').files
	    $scope.ImageSrcUpload = []
	    $scope.ImageSrcArr = []
	    for(var y in fayl){
	    	if(typeof fayl[y] === 'object')
	    		$scope.ImageSrcArr.push(fayl[y])
	    }

	    for(var z in $scope.ImageSrcArr){
	    	var reader = new FileReader();
		    reader.readAsDataURL($scope.ImageSrcArr[z]);
		    reader.onload = function(e) {
		        $scope.$apply(function(){
		        	row = {}
		        	row['image'] = e.target.result
		        	row['name'] = $scope.ImageSrcArr[z].name

        			$scope.ImageSrcUpload.push(row)
		        })
		    }
	    }
	}

	$scope.load_to_edit = function(record){
		$scope.create_dialog(record, record.uploaded_question);
	}

	$scope.filter.transaction_type = {'name':'ALL'}
	$scope.filter.is_general = true
	$scope.read = function(){
		var data = {
			pagination:me.pagination,
			transaction_type:$scope.filter.transaction_type['id'] ? $scope.filter.transaction_type['id'] : null,
			code : $scope.filter.code,
			sort: me.sort
			// show_general:$scope.filter.is_general
		}
		me.post_generic("/assessments/read/",data,"main")
		.success(function(response){
			$scope.records = response.data;
			me.starting = response.starting;
			me.ending = response.data.length;
			me.pagination.limit_options = angular.copy(me.pagination.limit_options_orig);
			me.pagination.limit_options.push(response.total_records)
			me.pagination["total_records"] = response.total_records;
			me.pagination["total_pages"] = response.total_pages;
		})
	};

	$scope.delete = function(record){
		swal({
		    title: "Continue",
		    text: "Remove "+record.value+"?",
		    type: "warning",
		    showCancelButton: true,
		    confirmButtonColor: "#DD6B55",
		    confirmButtonText: "Delete",
		    cancelButtonText: "Cancel",
		    closeOnConfirm: true
		},
			function(){
				me.post_generic("/assessments/delete/"+record.id,"","main")
				.success(function(response){
					Notification.success(response);
					$scope.read();
				}).error(function(err){
					Notification.error(err)
				})
			}
		);

	}

	$scope.isMultiple = function(){
		console.log($scope.record.is_multiple)
	}

	$scope.add_choice = function(list){
		$scope.choices.push(angular.copy(list))
	    $scope.choice_list = {}
	}

	$scope.add_effect = function(list){
		$scope.effects.push(angular.copy(list))
	    $scope.effect_list = {}
	}

	$scope.add_finding = function(list){
		$scope.findings.push(angular.copy(list))
	    $scope.finding_list = {}
	}

	$scope.add_answer = function(list){
		$scope.answer_list_arr.push(angular.copy(list))
		var answers = []
		for(var ans in $scope.answer_list_arr){
			var row = {
				name : $scope.answer_list_arr[ans].name,
				answer_display : $scope.answer_list_arr[ans].answer_display
			}
			answers.push(row)
		}
		list['answer'] = answers
		$scope.answers.push(angular.copy(list))
	    $scope.answer_list = {}
	    $scope.answer_list['item_no'] = $scope.answers.length + 1
	    $scope.answer_list_arr = []
	}

	$scope.add_multiple_answer = function(record,index,list){
		record.push(angular.copy(list))
		$scope.multiple_answer_list[index] = {}
	}

	$scope.add_multiple_list_answer = function(list){
		copy_list = angular.copy(list)
		$scope.answer_list_arr.push(copy_list)
		$scope.answer_list = {}
		$scope.answer_list['item_no'] = copy_list.item_no
	}

	$scope.remove_choice = function(list,index){
		if(list.id){
			me.post_generic("/assessments/delete_choice/"+list.id,{},"dialog")
			.success(function(response){
	    		$scope.choices.splice($scope.choices.indexOf(list), 1);
			})
		}else{
	    	$scope.choices.splice($scope.choices.indexOf(list), 1);
		}
    }

	$scope.remove_effect = function(list,index){
		if(list.id){
			me.post_generic("/assessments/delete_effect/"+list.id,{},"dialog")
			.success(function(response){
	    		$scope.effects.splice($scope.effects.indexOf(list), 1);
			})
		}else{
	    	$scope.effects.splice($scope.effects.indexOf(list), 1);
		}
    }

	$scope.remove_finding = function(list,index){
		if(list.id){
			me.post_generic("/assessments/delete_finding/"+list.id,{},"dialog")
			.success(function(response){
	    		$scope.findings.splice($scope.findings.indexOf(list), 1);
			})
		}else{
	    	$scope.findings.splice($scope.findings.indexOf(list), 1);
		}
    }

    $scope.remove_answer = function(list,index){
		if(list.id){
			me.post_generic("/assessments/delete_answer/"+list.id,{},"dialog")
			.success(function(response){
	    		$scope.answers.splice($scope.answers.indexOf(list), 1);
			})
		}else{
	    	$scope.answers.splice($scope.answers.indexOf(list), 1);
		}
    }

    $scope.remove_multiple_answer = function(record,list){
    	if(list.id){
    		me.post_generic("/assessments/delete_multiple_answer/"+list.id,{},"dialog")
    		.success(function(response){
		    	record.splice(record.indexOf(list),1)
    		})
    	}else{
	    	record.splice(record.indexOf(list),1)
    	}
    }

    $scope.remove_multiple_list_answer = function(list){
    	$scope.answer_list_arr.splice($scope.answer_list_arr.indexOf(list),1)
    }

    $scope.remove_image = function(list,index){
    	if(list.id){
    		me.post_generic("/assessments/delete_image/"+list.id,{}, "dialog")
    		.success(function(response){
    			$scope.ImageSrc.splice($scope.ImageSrc.indexOf(list), 1);
    		})
    	}else{
			$scope.ImageSrcUpload.splice($scope.ImageSrcUpload.indexOf(list), 1);
			var fayl = document.getElementById('my-file-selector').files
			$scope.ImageSrcArr2 = []
			for(var y in fayl){
				if(typeof fayl[y] === 'object') {
					if(fayl[y].name != list.name)
						$scope.ImageSrcArr2.push(fayl[y])
				}
			}

			$scope.record.images = $scope.ImageSrcArr2
    	}
    }

    $scope.read_transaction_types = function(){
    	me.post_generic("/transaction_types/read/","","main")
    	.success(function(response){
    		$scope.transaction_types = response.data;
    	})
    }

    $scope.edit_is_related = false;
    $scope.edit_parent_question = function(){
    	if($scope.record.parent_question){
    		$scope.old_is_related = angular.copy($scope.record.parent_question.id)
    	}
    	
		$scope.edit_is_related = true;
		if($scope.record.is_general){
			var transaction_types = []
			for(x in $scope.record.transaction_types){
				transaction_types.push($scope.record.transaction_types[x].id)	
			}
		}else{
			transaction_types = $scope.record.transaction_type.id
		}
		CommonRead.get_questions($scope,transaction_types);
    }

    $scope.remove_parent_question = function(){
    	$scope.old_is_related = angular.copy($scope.record.parent_question.id)
    	delete($scope.record.parent_question)
    }

    $scope.generate_code = function(){
    	$scope.record.code = null;
    	if(!$scope.record.is_general) $scope.record.is_general = false;
		me.post_generic("/assessments/generate_code/",$scope.record,"dialog")
		.success(function(response){
			$scope.record.code = response;
		}).error(function(err){
			if(err == "No code."){
				$scope.record.code = null
				Notification.error_action(err,"transaction_type")
			}else{
				Notification.error(err)
			}
		})
    }

    $scope.insertSymbol = function(idx,insert,record,new_data,idx2,new_list){
    	if(new_data){
    		var variable = "#answer2_"
    	}else{
    		if(new_list){
    			var variable = "#answer_"
    		}else{
	    		var variable = "#answer_"+idx2+"_"
    		}
    	}
		var cursorPosStart = $(variable+idx).prop('selectionStart');
		var cursorPosEnd = $(variable+idx).prop('selectionEnd');
		var text = $(variable+idx).val();
		var textBefore = text.substring(0, cursorPosStart);
		var textAfter = text.substring(cursorPosEnd, text.length);
    	
		var syntax_symbol = insert.above_text ? insert.syntax : insert.symbol
		record.name = textBefore + syntax_symbol + textAfter
		record.answer_display = "\\(" + textBefore + syntax_symbol + textAfter + "\\)"

    	// var text = $('#answer_'+idx);
	    // text.val(text.val() + insert.symbol);
    }
    var indexedCategories = []
    $scope.insertSymbolList = function(insert,record){
    	var cursorPosStart = $('#answer_list_id').prop('selectionStart');
    	var cursorPosEnd = $('#answer_list_id').prop('selectionEnd');
    	var text = $('#answer_list_id').val();
    	var textBefore = text.substring(0, cursorPosStart);
    	var textAfter = text.substring(cursorPosEnd, text.length);

    	if(record.name == undefined)
    		record.name = ""

    	var syntax_symbol = insert.above_text ? insert.syntax : insert.symbol
    	record.name = textBefore + syntax_symbol + textAfter
    	record.answer_display = "\\(" + textBefore + syntax_symbol + textAfter + "\\)"
    }

    $scope.answerDisplay = function(record){
    	// record.answer_display = "\\(" + record.answer + "\\)"
    	// return record.answer.replace(/\w\S*/g, function(txt){
    	// 	return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    	// });
    	
    	record.name = record.name.toLowerCase().replace(/\si\s/g, ' I ');
		record.name = record.name.charAt(0).toUpperCase() + record.name.slice(1);
		record.answer_display = "\\(" + record.name + "\\)"
		return record.name
    }

    $scope.onEnter = function(list,arrIdx){
    	$scope.add_answer(list)
    }

    $scope.catergoryToFilter = function(){
    	indexedCategories = []
    	return $scope.math_symbols
    }

    $scope.filterCategory = function(category){
    	var categoryIsNew = indexedCategories.indexOf(category.category) == -1;
    	if(categoryIsNew){
    		indexedCategories.push(category.category)
    	}
    	return categoryIsNew;
    }

    // $scope.isGeneral = function(){
    // 	$scope.record = {};	
    // }

	$scope.read();
    me.main_loader = function(){$scope.read();}
    CommonRead.get_transaction_types($scope);
    CommonRead.get_transaction_types2($scope);
    CommonRead.get_display_terms($scope);
    CommonRead.get_math_symbols($scope);
	// $scope.read_transaction_types();
});


app.directive('fileModel', ['$parse', function($parse) {
    return {
        restrict: 'A',
        link: function($scope, element, attrs) {
            var model = $parse(attrs.fileModel);
            var modelSetter = model.assign;
            element.bind('change', function(e) {
                $scope.$apply(function(e) {
                    modelSetter($scope, element[0].files[0]);
                });
                $scope.setimage();
            });
        }
    }
}])

app.config(['$compileProvider', function($compileProvider){
	$compileProvider.aHrefSanitizationWhitelist(/^\s*(https?|local|data):/);
}]);

app.directive("mathjaxBind", function() {
    return {
        restrict: "A",
        controller: ["$scope", "$element", "$attrs", function($scope, $element, $attrs) {
            $scope.$watch($attrs.mathjaxBind, function(value) {
                $element.text(value == undefined ? "" : value);
                MathJax.Hub.Queue(["Typeset", MathJax.Hub, $element[0]]);
            });
        }]
    };
});

app.directive('ngEnter', function() {
    return function(scope, elem, attrs) {
      elem.bind("keydown keypress", function(event) {
        // 13 represents enter button
        if(event.which === 13 && event.shiftKey){
        	event.stopPropagation();
        }
        else if (event.which === 13) {
          scope.$apply(function() {
            scope.$eval(attrs.ngEnter);
          });

          event.preventDefault();
        }
      });
    };
});