var app = angular.module('common_directives',[])

app.directive('currencyformat', function() {
    return {
          restrict: 'A',
          scope: {
            model : "=ngModel"
          },
          require: 'ngModel',
          link: function(scope, element, iAttrs, ngModelCtrl) {
              ngModelCtrl.$formatters.push(formatter);
              // scope.$watch('model', function() {ngModelCtrl.$setViewValue(scope.model)});
              ngModelCtrl.$parsers.push(parser);
              element.bind('focus', function() {onFocus();});
              element.bind('blur', function() {onBlur();});
              function formatter(modelValue) {
                element.attr("type","text");
                var plainNumber = accounting.unformat(modelValue)
                var precision = 2
                var symbol = ""
                if(!precision) precision = 2;
                if(!symbol) symbol = "";
                var formatted_number = accounting.formatMoney(plainNumber,"", precision,",",".","%s%v");             
                return formatted_number;
              }


              function parser(viewValue) {
                if(!viewValue || viewValue == "") viewValue = 0;
                return parseFloat(viewValue)
              }

              function onFocus(){
                var val = ngModelCtrl.$modelValue
                // if(!val && val != 0 && val != "") return;
                var plainNumber = accounting.unformat(val)
                if(plainNumber == "0") plainNumber = "";
                // element.attr("type","number");
                ngModelCtrl.$setViewValue(parseFloat(plainNumber));
                ngModelCtrl.$render();
                setTimeout(function(){scope.$apply();},100);
              }

              function onBlur(){
                  formatted_number = formatter(ngModelCtrl.$modelValue)
                  ngModelCtrl.$viewValue = formatted_number;
                  ngModelCtrl.$render();
                  setTimeout(function(){scope.$apply();},100);
              }
          }
    };
})

app.directive('quantity', function() {
    return {
          restrict: 'A',
          scope: {
            model : "=ngModel"
          },
          require: 'ngModel',
          link: function(scope, element, iAttrs, ngModelCtrl) {
              ngModelCtrl.$formatters.push(formatter);
              // scope.$watch('model', function() {ngModelCtrl.$setViewValue(scope.model)});
              ngModelCtrl.$parsers.push(parser);
              element.bind('focus', function() {onFocus();});
              element.bind('blur', function() {onBlur();});
              function formatter(modelValue) {
                element.attr("type","text");
                var plainNumber = accounting.unformat(modelValue)
                var formatted_number = accounting.formatMoney(plainNumber,"",2,",",".","%s%v");             
                return formatted_number;
              }

              function parser(viewValue) {
                if(!viewValue || viewValue == "") viewValue = 0;
                return parseFloat(viewValue)
              }

              function onFocus(){
                var val = ngModelCtrl.$modelValue
                // if(!val && val != 0 && val != "") return;
                var plainNumber = accounting.unformat(val)
                if(plainNumber == "0") plainNumber = "";
                element.attr("type","number");
                ngModelCtrl.$setViewValue(parseFloat(plainNumber));
                ngModelCtrl.$render();
                setTimeout(function(){scope.$apply();},100);
              }

              function onBlur(){
                  formatted_number = formatter(ngModelCtrl.$modelValue)
                  ngModelCtrl.$viewValue = formatted_number;
                  ngModelCtrl.$render();
                  setTimeout(function(){scope.$apply();},100);
              }
          }
    };
})

app.directive('handcursor', function() {
    return function(scope, element, attrs) {
        element.addClass("hand_cursor")
    };
})

app.directive('onEnter', function () {
    return function (scope, element, attrs) {
        element.bind("keydown keypress", function (event) {
            if(event.which === 13) {
                scope.$apply(function (){
                    scope.$eval(attrs.onEnter);
                });
                event.preventDefault();
            }
        });
    };
})

app.directive('pagination', function() {
    return {
        restrict: 'E',
        templateUrl: '/common/pagination/',
    };
})

app.directive('tabletools', function() {
    return {
        restrict: 'E',
        templateUrl: '/common/tabletools2/',
    };
})

app.directive('tabletools3', function() {
    return {
        restrict: 'E',
        templateUrl: '/common/tabletools3/',
    };
})

app.directive('tabletools4', function() {
    return {
        restrict: 'E',
        templateUrl: '/common/tabletools4/',
    };
})

app.directive('tabletoolstrans', function() {
    return {
        restrict: 'E',
        templateUrl: '/common/tabletoolstrans/',
    };
})

app.directive('tabletoolsdaterange', function() {
    return {
        restrict: 'E',
        templateUrl: '/common/tabletoolsdaterange/',
    };
})

app.directive('tabletoolsdaterange2', function() {
    return {
        restrict: 'E',
        templateUrl: '/common/tabletoolsdaterange2/',
    };
})

app.directive('windowresize', ['$window', function($window) {
    return {
        link: function(scope, elem, attrs) {
            scope.onResize = function(apply) {
                setTimeout(function() {
                    var height = $(elem).height();
                    if (height > 600) {
                        height = "90%";
                    } else if (height > 500) {
                        height = "85%";
                    } else if (height > 400) {
                        height = "80%";
                    } else if (height > 300) {
                        height = "75%";
                    } else {
                        height = "65%";
                    }

                    scope.modal_style = { 'height': height, 'overflow': 'auto' };
                    if (apply) {
                        scope.$apply(function() {});
                    }
                }, 10);
            }
            scope.onResize();
            angular.element($window).bind('resize', _.debounce(function() {
                scope.onResize(true);
            }, 100))
        }
    }
}])

app.directive('tableresize', ['$div', function($window) {
    return {
        link: function(scope, elem, attrs) {
            scope.onResize = function(apply) {
                setTimeout(function() {
                    var height = $(elem).height();
                    if (height > 600) {
                        height = "90%";
                    } else if (height > 500) {
                        height = "85%";
                    } else if (height > 400) {
                        height = "80%";
                    } else if (height > 300) {
                        height = "75%";
                    } else {
                        height = "65%";
                    }

                    scope.modal_style = { 'height': height, 'overflow': 'auto' };
                    if (apply) {
                        scope.$apply(function() {});
                    }
                }, 10);
            }
            scope.onResize();
            angular.element($window).bind('resize', _.debounce(function() {
                scope.onResize(true);
            }, 100))
        }
    }
}])

app.$inject = ['$scope', '$filter'];

app.directive("customSort", function() {
    return {
        restrict: 'A',
        transclude: true,
        scope: true,
        template: ' <a ng-click="sort_by(get_field());" style="color: #555555;">' +
            '    <span ng-transclude></span>' +
            '    <i ng-class="selectedCls()"></i>' +
            '</a>',
        link: function(scope,elem,attr) {
                // change sorting order
                scope.get_field = function(){
                    return elem.attr("order");
                }

                scope.sort_by = function(newSortingOrder) {
                    var sort = scope.main.sort;
                    if (sort.sort_by == newSortingOrder) {
                        sort.reverse = !sort.reverse;
                    }
                    sort.sort_by = newSortingOrder;
                    scope.main.main_loader();
                };

                scope.selectedCls = function() {
                    var column = scope.get_field()
                    if (column == scope.main.sort.sort_by) {
                        sortt = ('fa fa-chevron-' + ((scope.main.sort.reverse) ? 'down' : 'up'));
                        return sortt
                    } else {
                        return 'fa fa-sort'
                    }
                };
            }
    }
});

app.directive("ifshow", function() {
    return {
        restrict: 'A',
        transclude: true,
        scope: true,
        link: function(scope,elem,attr) {
          console.log(elem)
        }
    }
});

app.directive("notclicklast", function($compile) {
    return {
        restrict: 'A',
        link: function(scope,elem,attr) {
            var tds = $(elem).find("td")
            for(var i = 0; i < tds.length - 1; i++){
                var tdElem = $(tds[i])
                tdElem.attr("ng-click",attr.loader)
                tdElem.addClass("hand_cursor")
                $compile(tdElem)(scope);
            }
        }
    }
});

app.directive("multiselect", function($compile) {
    return {
        restrict: 'A',
        link: function(scope,elem,attr) {
            $(elem).multiselect({
            });
        }
    }
});

/*app.directive("chkrow", function($compile) {
    return {
        restrict: 'A',
        link: function(scope,elem,attr) {
            var tds = $(elem).find("td")
            console.log(tds);
            console.log(attr)
            console.log(console)
            console.log(elem)
            console.log("-------------------")
            return;
            chkindex = attr.chkrow;
            if(chkindex){
              chkindex = parseInt(chkindex)
            }
            chkelem = tds[chkindex];
            console.log(chkindex)
            console.log(chkelem)
            return;
            for(var i = 0; i < tds.length - 1; i++){
                var tdElem = $(tds[i])
                tdElem.attr("ng-click",attr.loader)
                tdElem.addClass("hand_cursor")
                $compile(tdElem)(scope);
            }
        }
    }
});*/

app.directive("pullBottom", function($compile) {
    return {
        restrict : "A",
        link: function(scope, elem, attrs) {
            $(elem).css("position","absolute");
            $(elem).css("bottom",0);
        }
    }
});

app.directive('fileUpload', function () {
    return {
        scope: true,        //create a new scope
        link: function (scope, el, attrs) {
            el.bind('change', function (event) {
                var files = event.target.files;
                //iterate files since 'multiple' may be specified on the element
                for (var i = 0;i<files.length;i++) {
                    //emit event upward
                    scope.$emit("fileSelected", { file: files[i] });
                }                                       
            });
        }
    };
});