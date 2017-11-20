var app = angular.module("import",['common_module']);

app.controller('importCtrl', function($scope, $http, $timeout, $element, $controller,CommonFunc,Notification,CommonRead) {
	angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
	var me = this;
	$scope.record = {}
	$scope.page_loader = {'main':false,'dialog':false}

	$scope.current_tab = 1;
	$scope.headers = []
	$scope.raw_rows = []
	$scope.final_rows = []

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
		me.open_dialog("/import/create_dialog/","dialog_whole","main")

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