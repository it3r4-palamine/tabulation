var app = angular.module("import",['common_module','file-model']);

app.controller('importCtrl', function($scope, $http, $timeout, $element, $controller,CommonFunc,Notification,CommonRead) {
	angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
	var me = this;
	$scope.record = {}
	$scope.page_loader = {'main':false,'dialog':false}

	$scope.current_tab = 1;
	$scope.headers = []
	$scope.raw_rows = []
	$scope.final_rows = []
	$scope.records = []
	$scope.uploaded_images = []

	$scope.$watch("current_tab",function(current,old){
		if(current == 2){
			$scope.arrange_csv();
		}
	})

	$scope.previous = function(){
		$scope.current_tab = 1
	}

	$scope.next = function(){
		$scope.current_tab = 2
	}

	$scope.submit = function(index){
		if(index == 0){
			$scope.error_count = 0;
			$scope.success_count = 0;
		}

		if(!$scope.final_rows[index] || $scope.final_rows[index] === undefined){
			var temp_final_rows = angular.copy($scope.final_rows);
			var temp_final_rows2 = []
			$scope.final_rows = [];
			var custom_selected = 0;
			for(i in temp_final_rows){
				if(temp_final_rows[i].error){
					temp_final_rows2.push(temp_final_rows[i]);
					$scope.error_count++;
				}else{
					$scope.success_count = 0;
				}
			}
			
			$scope.final_rows = temp_final_rows2;

			if($scope.error_count == 0){
				if(custom_selected){
					Notification.success("Selected record(s) successfully imported!")
				}else{
					Notification.success("Successfully imported!")
					$scope.final_rows = [];
					$scope.ids = []
					me.close_dialog();
				}
			}else if($scope.success_count == 0){
				Notification.error("Import failed. please check the error message in every line.")
			}else{
				Notification.error($scope.error_count+" failed to import. please check the error message in every line.")
			}
			return;
		}

		var data = angular.copy($scope.final_rows[index]);

		data["is_import"] = true;
		me.post_generic($scope.current_url,data,"dialog")
		.success(function(response){
			$scope.final_rows[index].error = false;

			$scope.submit(index + 1);
		})

		.error(function(err,status){
			if(status == 404){
				err = "Page not found."
			}
			$scope.final_rows[index].error = true;
			$scope.final_rows[index].error_message = err;
			$scope.submit(index + 1)
		})
	}

	$scope.arrange_csv = function(){
		var header = null;
		var result_row = {}
		var raw_rows = $scope.raw_rows;
		var csv_cell_value = "";
		$scope.final_rows = [];
		raw_rows.forEach(function(csv_row,index){
			result_row = {}
			for(var i in $scope.headers){
				header = $scope.headers[i];
				if(csv_row[header.selected]){
					csv_cell_value = csv_row[header.selected]
					if(header.type == "number"){
						csv_cell_value = accounting.unformat(csv_cell_value);
					}
					result_row[header.value] = csv_cell_value
				}
			}
			$scope.final_rows.push(result_row);
		});
	}

	$scope.remove_line = function(row){
		$scope.final_rows.splice($scope.final_rows.indexOf(row), 1);
	}

	$scope.reset_data = function(){
		$scope.current_tab = 1;
		$scope.final_rows = [];
		$scope.raw_rows = [];
		$scope.headers = [];
		$scope.current_url = ""
		$scope.title = ""
		if($scope.current_module == 'questions'){
			$scope.current_url = "/import/import_questions/";
			$scope.title = "Questions"
			if($scope.display_terms.length > 0 && $scope.display_terms[0].questions){
				$scope.title = $scope.display_terms[0].questions
			}
		}else if($scope.current_module == "choices"){
			$scope.current_url = "/import/import_choices/";
			$scope.title = "Choices"
		}else if($scope.current_module == "effects"){
			$scope.current_url = "/import/import_effects/";
			$scope.title = "Effects"
		}else if($scope.current_module == "recommendations"){
			$scope.current_url = "/import/import_recommendations/";
			$scope.title = "Recommendations"
		}else if($scope.current_module == "findings"){
			$scope.current_url = "/import/import_findings/";
			$scope.title = "Findings"
		}else if($scope.current_module == "image"){
			$scope.current_url = "/import/import_questions/";
			$scope.title = "Questions"
		}else{
			return false;
		}
		return true;
	}

	$scope.import_dialog = function(type){
		$scope.current_module = type;
		if(!$scope.reset_data()){
			Notification.error("This module doesn't have an import feature yet.");
			return;
		}

		$scope.read_module_columns()
		if(type == "image"){
			$scope.ImageSrc = []
			$scope.record = []
			// me.open_dialog("/import/upload_dialog/","dialog_whole","main")
			$("#myModal").modal('toggle');
		}else{
			me.open_dialog("/import/create_dialog/","dialog_whole","main")
		}

	}

	$scope.upload_close_dialog = function(){
		$("#myModal").modal('toggle');
	}

	$scope.add_answer = function(list,arrIdx){
		$scope.record.answer_keys[arrIdx].push(angular.copy(list))
	    $scope.answer_list[arrIdx] = {}
	    $scope.answer_list[arrIdx]['item_no'] = $scope.record.answer_keys[arrIdx].length + 1
	}

	$scope.remove_answer = function(list,index,arrIdx){
    	$scope.record.answer_keys[arrIdx].splice($scope.record.answer_keys[arrIdx].indexOf(list), 1);
    }

	$scope.remove_image = function(list,data,arrIdx){
		$scope.record.deleted[arrIdx] = true
		$scope.ImageSrc[arrIdx].upload = true
		// $scope.ImageSrc.splice($scope.ImageSrc.indexOf(list), 1);
		// var fayl = document.getElementById('my-file-selector').files
		// $scope.ImageSrcArr2 = []
		// for(var y in fayl){
		// 	if(typeof fayl[y] === 'object') {
		// 		if(fayl[y].name != list.name)
		// 			$scope.ImageSrcArr2.push(fayl[y])
		// 	}
		// }

		// $scope.record.images = $scope.ImageSrcArr2
    }

    $scope.insertSymbol = function(insert,record){
    	var syntax_symbol = insert.above_text ? insert.syntax : insert.symbol
    	record.answer += syntax_symbol
    	record.answer_display = "\\(" + record.answer + "\\)"
    }

    $scope.insertSymbolList = function(insert,record,idx){
    	if(record.answer == undefined)
    		$scope.answer_list[idx].answer = ""

    	var syntax_symbol = insert.above_text ? insert.syntax : insert.symbol
    	$scope.answer_list[idx].answer += syntax_symbol
    	$scope.answer_list[idx].answer_display = "\\(" + $scope.answer_list[idx].answer + "\\)"
    }

    $scope.answerDisplay = function(record){
    	record.answer = record.answer.toLowerCase().replace(/\si\s/g, ' I ');
		record.answer = record.answer.charAt(0).toUpperCase() + record.answer.slice(1);
		record.answer_display = "\\(" + record.answer + "\\)"
		return record.answer
    	// record.answer_display = "\\(" + record.answer + "\\)"
    }

    $scope.onEnter = function(list,arrIdx){
    	$scope.add_answer(list,arrIdx)
    }

    $scope.idx = 0
    $scope.create = function(){
    	$scope.upload($scope.idx)
    }

    $scope.upload = function(idx){
    	if(idx == $scope.record.images.length){
    		$('body').loadingModal('hide');
    		$('body').loadingModal('destroy') ;
    		Notification.success("Successfully uploaded.")
    		me.close_dialog()
    		$("#myModal").modal('toggle');
    	}else{
    		$('body').loadingModal({text: 'Uploading...'});
    		$('body').loadingModal('animation', 'cubeGrid');
    		$('body').loadingModal('backgroundColor', 'green');
    		var number = idx + 1;
    		if($scope.answer_list[idx] && Object.keys($scope.answer_list[idx]).length > 0) {
    			if($scope.answer_list[idx].answer && $scope.answer_list[idx].item_no){
    				$scope.record.answer_keys[idx].push(angular.copy($scope.answer_list[idx]))
    			}
    		}
    		$scope.answer_list[idx] = {}
    		if(!$scope.record.deleted)
    			$scope.record['deleted'][idx] = false
			else{
				if(!$scope.record.deleted[idx])
					$scope.record.deleted[idx] = false
			}

			if($scope.record.deleted[idx] == true){
				$scope.upload(++$scope.idx)
			}else{
	    		for(var ans in $scope.record.answer_keys[idx]){
	    			if(!$scope.record.answer_keys[idx][ans].item_no || $scope.record.answer_keys[idx][ans].item_no == ""){
	    				$('body').loadingModal('hide');
	    				$('body').loadingModal('destroy') ;
	    				return Notification.error("An item no. is missing for Image "+number+".")
	    			}

	    			if(!$scope.record.answer_keys[idx][ans].answer || $scope.record.answer_keys[idx][ans].answer == ""){
	    				$('body').loadingModal('hide');
	    				$('body').loadingModal('destroy') ;
	    				return Notification.error("An answer is missing for Image "+number+".")
	    			}
	    		}

	    		if(!$scope.record.code){
	    			$('body').loadingModal('hide');
	    			$('body').loadingModal('destroy') ;
	    			return Notification.error("Code is required for Image "+number+".")
	    		}
				else{
					if(!$scope.record.code[idx])
					{
						$('body').loadingModal('hide');
						$('body').loadingModal('destroy') ;
	    				return Notification.error("Code is required for Image "+number+".")
					}
				}

	    		if(!$scope.record.transaction_type){
	    			$('body').loadingModal('hide');
	    			$('body').loadingModal('destroy') ;
	    			return Notification.error("Transaction type is required for Image "+number+".")
	    		}
	    		else{
	    			if(!$scope.record.transaction_type[idx])
	    			{
	    				$('body').loadingModal('hide');
	    				$('body').loadingModal('destroy') ;
	    				return Notification.error("Transaction type is required for Image "+number+".")
	    			}
	    		}

	    		var datus = {
	    			images : $scope.record.images[idx],
	    			code : $scope.record.code[idx],
	    			transaction_type : $scope.record.transaction_type[idx].id,
	    		}

	    		var upload = new FormData();

	    		angular.forEach(datus, function(value, key){
	    			if(datus[key] === undefined){
	    			    value = ""
	    			}
	    			upload.append(key, value)
	    		});
	    		$http.post('/assessments/multiple_upload/', upload, { 
	    		    method: "post", 
	    		    transformRequest: angular.identity, 
	    		    headers: {'Content-Type': undefined} 
	    		}).success(function(response){ 
	    		    // $scope.ImageSrc[idx].upload = true
	    		    // $scope.upload(++$scope.idx)
	    		    $scope.saveData($scope.record.answer_keys[idx], response, idx)
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

    		// }

    	}
    }

    $scope.saveData = function(record, id, arrIdx) {
    	var data = {
    		datus : record,
    		id : id
    	}
    	me.post_generic("/assessments/multiple_upload_answer_keys/",data,"dialog")
    	.success(function(response){
    		// me.close_dialog();
    		// Notification.success(response);
    		// $scope.read();
    		$scope.ImageSrc[arrIdx].upload = true
		    $scope.upload(++$scope.idx)
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

	$scope.read_module_columns = function(){
		$http.post("/import/read_module_columns/"+$scope.current_module)
		.success(function(response){
			var arr = []
			for(i in response){
				row = response[i]
				row["value"] = i
				arr.push(row)
			}
			var sorted = sortByAttribute(angular.copy(arr),"sort");
			$scope.columns = {}
			for(i in sorted){
				$scope.columns[sorted[i].value] = sorted[i];
			}
		})
	}

	function sortByAttribute(array, ...attrs) {
      let predicates = attrs.map(pred => {
        let descending = pred.charAt(0) === '-' ? -1 : 1;
        pred = pred.replace(/^-/, '');
        return {
          getter: o => o[pred],
          descend: descending
        };
      });
      // schwartzian transform idiom implementation. aka: "decorate-sort-undecorate"
      return array.map(item => {
        return {
          src: item,
          compareValues: predicates.map(predicate => predicate.getter(item))
        };
      })
      .sort((o1, o2) => {
        let i = -1, result = 0;
        while (++i < predicates.length) {
          if (o1.compareValues[i] < o2.compareValues[i]) result = -1;
          if (o1.compareValues[i] > o2.compareValues[i]) result = 1;
          if (result *= predicates[i].descend) break;
        }
        return result;
      })
      .map(item => item.src);
    }

    $scope.import_file_change = function(event){
		var files = event.target.files;
        if (files.length){
			var r = new FileReader();
			r.onload = function(file){
				var csv_contents = file.target.result;
				var csv = $scope.get_csv_fields(csv_contents)
				$scope.$apply(function () {
					temp_headers = angular.copy(csv["headers"]);
					$scope.raw_rows = angular.copy(csv["raw_rows"]);

					$scope.headers = []
					for(i in temp_headers){
						for(x in temp_headers[i]["csv_headers"]){
							header = temp_headers[i]["csv_headers"][x];
							likely = $scope.similar(temp_headers[i].display.toLowerCase(),header.toLowerCase())
							if(likely >= 75){
								temp_headers[i].selected = header;
							}
						}
						$scope.headers.push(temp_headers[i]);	
					}
				});
		    };
			r.readAsText(files[0]); //activates onload after calling this function
        }else{
        	return "No File Read"
        }
	}

	$scope.similar = function(a,b){
		var lengthA = a.length;
		var lengthB = b.length;
		var equivalency = 0;
		var minLength = (a.length > b.length) ? b.length : a.length;    
		var maxLength = (a.length < b.length) ? b.length : a.length;    
		for(var i = 0; i < minLength; i++) {
		    if(a[i] == b[i]) {
		        equivalency++;
		    }
		}


		var weight = equivalency / maxLength;
		return (weight * 100)
	}

	$scope.get_csv_fields = function(csv){
		var parsed_csv = $scope.parseCSV(csv)
		var model_headers = $scope.get_fields()
		var csv_headers = parsed_csv[0];
		for(var i in model_headers){
			model_headers[i]["csv_headers"] = csv_headers
		}
		result = {
			"headers" : model_headers,
			"raw_rows" : $scope.csv_to_arr_of_objs(parsed_csv),
		}
		return result;
	}

	$scope.parseCSV = function(str) {
	    var arr = [];
	    var quote = false;
	    for (var row = col = c = 0; c < str.length; c++) {
	        var cc = str[c], nc = str[c+1];
	        arr[row] = arr[row] || [];
	        arr[row][col] = arr[row][col] || '';
	        
	        if (cc == '"' && quote && nc == '"') { arr[row][col] += cc; ++c; continue; }
	        if (cc == '"') { quote = !quote; continue; }
	        if (cc == ',' && !quote) { ++col; continue; }
	        if (cc == '\n' && !quote) { ++row; col = 0; continue; }
	        
	        arr[row][col] += cc;
	    }
	    return arr;
	}

	$scope.get_fields = function(){
		var headers = [];
		for(i in $scope.columns){
			row = $scope.columns[i];
			headers.push(row)
		}
		return headers
	}

	$scope.csv_to_arr_of_objs = function(raw_rows){
		var results = []
		var result_row = {}
		var raw_headers = raw_rows[0]; 
		raw_rows.forEach(function(csv_row,index){
			if(index == 0) return;
			result_row = {}
			for(var i in csv_row){
				result_row[raw_headers[i]] = csv_row[i];
			}
			results.push(result_row);
		})
		return results;
	}

	$scope.setimage = function() {
	    var file = $scope.record;
	    var fayl = document.getElementById('my-file-selector').files
	    $scope.record = []
	    $scope.record['answer_keys'] = []
	    $scope.record['deleted'] = []
	    $scope.record['images'] = []
	    $scope.answer_list = []
	    $scope.ImageSrc = []
	    $scope.ImageSrcArr = []
	    $scope.idx = 0
	    for(var y in fayl){
	    	if(typeof fayl[y] === 'object')
	    		$scope.record.images.push(fayl[y])
	    }

	    saveImage(0)

	    function saveImage(idx){
	    	if(idx == $scope.record.images.length){

	    	}else{
		    	$scope.record.answer_keys[idx] = []
		    	$scope.answer_list[idx] = {}
		    	$scope.answer_list[idx]['item_no'] = 1
		    	var current_name = $scope.record.images[idx].name
		    	var reader = new FileReader();
			    reader.readAsDataURL($scope.record.images[idx]);
			    reader.onload = function(e) {
			        $scope.$apply(function(){
	        			row = {}
			        	row['name'] = current_name
			        	row['image'] = e.target.result

	        			$scope.ImageSrc.push(row)

	        			saveImage(++idx)
			        })
			    }
	    	}
	    }
	}

	var indexedCategories = []
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

	CommonRead.get_display_terms($scope)
	CommonRead.get_transaction_types2($scope);
	CommonRead.get_math_symbols($scope);

});

app.directive('customOnChange', function() {
  return {
    restrict: 'A',
    link: function (scope, element, attrs) {
      var onChangeHandler = scope.$eval(attrs.customOnChange)
      element.bind('change', onChangeHandler);
    }
  };
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
}]);

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