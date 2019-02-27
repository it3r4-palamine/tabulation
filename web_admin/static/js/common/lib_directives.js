/**
 * icheck - Directive for custom checkbox icheck
 */



function dropzone($cookies) {
    return {
        restrict: 'C',
        link: function(scope, element, attrs) {
            scopemain = scope.$parent.main;
            scopemain.upload_type = attrs.uploadType;
            var config = {
                paramName: "file",
                maxFileSize : 10,
                parallelUploads : 100,
                uploadMultiple: true,
                autoProcessQueue : false,
                addRemoveLinks : true,
                headers: { "X-CSRFToken": $cookies.get("csrftoken")},
                init: function() {
                    var submitButton = document.querySelector("#upload_now")
                    submitButton.addEventListener("click", function() {
                        scope.processDropzone();
                    });
                },
            };

            var eventHandlers = {
                'addedfile': function(file) {
                    scope.file = file;
                    scope.$apply(function() {
                        scopemain.file_added = true;
                    });
                },
                'success': function (file, response) { //add 'complete' event here.
                    if(scopemain.upload_type == "attachment_transaction"){
                        scopemain.attachment_read();
                        scopemain.current_record.has_attachment = true;
                    }
                    this.removeFile(file);
                },
                'error': function (file, response) {
                    scopemain.notify(response,"error")
                    this.removeFile(file);
                }
            };


            config["url"] = "/attachment2/upload/"+scopemain.current_module+"/"+scopemain.current_record.id;
            dropzone = new Dropzone(element[0],config);
            

            angular.forEach(eventHandlers, function(handler, event) {
                dropzone.on(event, handler);
            });
            
            scope.processDropzone = function() {
                dropzone.processQueue();
            };
        }
    }
}

function custPagination(){
    return {
        transclude: true,
        scope: {
            pItems: "=",
            pBoundarylinks: "=",
            pSize: "=",
            pStep: "="
        },
        controller: function ($scope) {

            $scope.pFirstStep = 1;
            $scope.pTotalStep = 1;
            $scope.pStep = 1;
            
            $scope.setTotalStep = function () {
                var val = 5;
                if (!isNaN($scope.pSize)) {
                    var _val = 1;
                    if ($scope.pSize > 0) {
                        _val = $scope.pSize;
                    }
                    val = $scope.pItems.length / _val;
                    val = Math.ceil(val);
                    
                }
                $scope.pTotalStep = val;
            }

            $scope.handleStep = function (step) {
                $scope.pStep = step;
            };

            $scope.previous = function(){
                $scope.pStep--;      
                $scope.validate_page();
            }

            $scope.next = function(){
                $scope.pStep++;      
                $scope.validate_page();
            }

            $scope.validate_page = function(){
                if($scope.pStep < 1){
                    $scope.pStep = 1;
                }

                if($scope.pStep >= $scope.pTotalStep){
                    $scope.pStep = $scope.pTotalStep;
                }
            }

            $scope.$watchGroup(['pItems', 'pSize'], function (n, o) {
                $scope.setTotalStep();
            });
            
            
            $scope.setTotalStep();
        },
        templateUrl: '/common/pagination_front/'
    };
}

angular.module('lib_directives', ["ngCookies"])
    .directive('dropzone', ['$cookies', dropzone])
    .directive("custPagination", custPagination)