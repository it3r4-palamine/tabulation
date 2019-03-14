var app = angular.module('common_services', [])


app.factory("CommonRequests", function($http, Notification) {
    return {
        read_common_records: function(scope, key, url, params, no_success) {
            if (!params) { params = {}; }
            return $http.post(url, params)
                .success(function(response) {
                    if (!no_success) {
                        scope[key] = response;
                    }
                })
        },
        accounts_basic: function(scope, params, key) {
            if (!params) { params = {}; }
            if (!key) { key = "accounts" }
            $http.post("/accounts/read_generic/", params)
                .success(function(response) {
                    scope[key] = response;
                })
        }
    }
});

app.factory("CommonFunc", function($http, Notification, SweetAlert) {
    return {
        arr2str: function(arr) {
            str = null;
            for (var i in arr) {
                var item = arr[i];
                if (!str) {
                    str = String(item)
                } else {
                    str += ", " + String(item)
                }
            }
            return str;
        },

        confirmation: function(title, text, type,confirmtext) {
            if (!title) {
                title = "Continue?"
            }
            if (!type) {
                type = "warning"
            }
            if(!confirmtext){
                if(title == "Continue?"){
                    confirmtext = "Yes";
                }else{
                    confirmtext = "Continue";
                }
            }

            var sweetalert = SweetAlert.swal({
                title: title,
                text: text,
                type: type,
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: confirmtext,
                cancelButtonText: "Cancel",
                closeOnConfirm: true
            });
            return sweetalert;
        },

        attention: function(title,message,type,confirmButton)
        {
            if (!type) {
                type = "warning"
            }

            if(!confirmButton)
            {
                confirmButton = "Okay"
            }

            confcolor = "#3f51b5"

            var sweetalert = SweetAlert.swal({
                title: title,
                text: message,
                type: type,
                showCancelButton: true,
                confirmButtonColor: confcolor,
                confirmButtonText: confirmButton,
                cancelButtonText: "Cancel",
                closeOnConfirm: true,
            });
            return sweetalert;
        },

        /*get the likely percentage of two string*/
        similar(a,b) {
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
        },

        first_day_of_date(date){
            date = moment([date.year(), date.month()]);
            return new Date(date)
        },
        last_day_of_date(date){
            date = new Date(moment(date).endOf('month'));
            return new Date(date)
        },
        isNumeric(n){
            return !isNaN(parseFloat(n)) && isFinite(n);
        }
    }
});

app.factory("Charts", function($http, CommonRequests) {
    return {
        read_account_types: function(scope, seperate) {
            $http.post("/accounts/account_types/")
                .success(function(response) {
                    scope.account_types = response;
                    if (seperate) {
                        scope.financial_position = response.slice(0, 26)
                        scope.financial_operation = response.slice(26, 33)
                    }
                });
        },
        chart_by: function(scope, key, param_value, search_by) {
            if (!search_by) { search_by = "page_id"; }
            params = {};
            params[search_by] = param_value;
            if (scope.chartofaccounts === undefined) { scope.chartofaccounts = {}; }
            if (scope.chartofaccounts[key] === undefined) { scope.chartofaccounts[key] = []; }
            if (scope.chartofaccounts[key][0] !== undefined) {
                return; }
            return $http.post("/accounts/read_generic/", params)
                .success(function(response) {
                    scope.chartofaccounts[key] = response;
                })
        },
    }
})

app.factory("Printt", function($http,$localStorage) {
    return {
        print: function(scope,record) {
            sessionStorage.clear();
            if(scope.current_module == "general_journal"){
                this.print_GJ(scope,record);
            }else if(scope.current_module == "sales_representative_report_detailed"){
                this.print_sales_representative_report_detailed(scope,record);
            }
        },

        print_GJ: function(scope,record){
            var post = scope.post_generic("/general_journal/load_to_edit/"+record.id,record,"main");
            post.success(function(response){
                response.record.id = record.id;
                $localStorage.printt = response;
                window.open("/print/general_journal/"+response.record.id+"/");
            })
        },

        print_sales_representative_report_detailed: function(scope,record){
            sessionStorage.data = JSON.stringify(angular.copy(record.records));
            sessionStorage.paymenttypes = JSON.stringify(angular.copy(record.paymenttypes));
            window.open("/print/sales_representative_report_detailed/");
        }
    }
})

app.factory("CommonRead", function($http, CommonRequests, Charts) {
    return {
        customers_for_transaction: function(scope,key) {
            if(!key){key = "customers"}
            return CommonRequests.read_common_records(scope, key, "/customer/read_for_transaction/", { "all": true });
        },
        get_transaction_types: function(scope) {
            var post = CommonRequests.read_common_records(scope, "transaction_types", "/transaction_types/read/",{},true);
            return post.success(function(response){
                response.data.unshift({'name' : 'ALL'});
                scope["transaction_types"] = response.data;
            })
        },

        get_transaction_types2: function(scope,params) {
            if(!params){
                params = {}
            }
            var post = CommonRequests.read_common_records(scope, "transaction_types2", "/transaction_types/read/",params,true);
            return post.success(function(response){
                scope["transaction_types2"] = response.data;
            })
        },

        get_company: function(scope) {
            data = {"exclude":true}
            var post = CommonRequests.read_common_records(scope, "company", "/company/read/",data,true);
            return post.success(function(response){
                response.data.unshift({'name' : 'ALL'});
                scope["company"] = response.data;
            })
        },

        get_company2: function(scope) {
            data = {"exclude":true}
            var post = CommonRequests.read_common_records(scope, "company2", "/company/read/",data,true);
            return post.success(function(response){
                scope["company2"] = response.data;
            })
        },

        get_schools : function(scope)
        {
            var post = CommonRequests.read_common_records(scope, "schools", "/settings/read_schools/",{},true);
            return post.success(function(response){
                scope["schools"] = response.data;
            })
        },

        get_schools2 : function(scope)
        {
            var post = CommonRequests.read_common_records(scope, "schools2", "/settings/read_schools/",{},true);
            return post.success(function(response){
                response.data.unshift({'name' : 'No School'});
                scope["schools"] = response.data;
            })
        },

        get_grade_level : function(scope)
        {
            var post = CommonRequests.read_common_records(scope, "grade_levels", "/settings/read_grade_levels/",{},true);
            return post.success(function(response){
                scope["grade_levels"] = response.data;
            })
        },

        get_users: function(scope) {
            var post = CommonRequests.read_common_records(scope, "users", "/users/read/",{},true);
            return post.success(function(response){
                response.data.unshift({'fullname' : 'ALL'});
                scope["users"] = response.data;
            })
        },

        get_users2: function(scope) {
            var post = CommonRequests.read_common_records(scope, "users2", "/users/read/",{},true);
            return post.success(function(response){
                scope["users2"] = response.data;
            })
        },

        get_timeslots : function(scope)
        {
            var post = CommonRequests.read_common_records(scope, "timeslots", "/timeslots/read_timeslots/", {}, true);
            return post.success(function(response){

                for (var i in response.records)
                {
                    response.records[i].time_start = new Date(response.records[i].time_start)
                    response.records[i].time_end = new Date(response.records[i].time_end)
                }

                scope["timeslots"] = response.records
            })
        },

        get_students : function(scope)
        {
            var post = CommonRequests.read_common_records(scope, "students", "/users/read_students/",{},true);
            return post.success(function(response){
                scope["students"] = response.records;
            })
        },

        get_math_symbols: function(scope) {
            var post = CommonRequests.read_common_records(scope, "math_symbols", "/settings/read_math_symbols/",{},true);
            return post.success(function(response){
                scope["math_symbols"] = response.data;
            })
        },

        get_questions: function(scope,transaction_types)
        {
            data = {"all": true};
            if(transaction_types){
                data['transaction_type'] = transaction_types
            }
            var post = CommonRequests.read_common_records(scope, "questions", "/assessments/read/",data,true);
            return post.success(function(response){
                scope["questions"] = response.data;
            })
        },

        get_programs : function(scope)
        {
            let response = scope.post_api("programs/read/");
            response.success(function(response){
                scope["programs"] = response.records;
            })
        },

        get_question_types : function(scope)
        {
            var post = CommonRequests.read_common_records(scope, "question_types", "/question_types/read/",{},true);
            return post.success(function(response){
                scope["question_types"] = response.records;
            })
        },

        get_subjects : function(scope)
        {
            let response = scope.post_api("subject/read/");
            response.success(function(response){
                scope["subjects"] = response.records;
            })
        },

        get_display_terms: function(scope) {
            var post = CommonRequests.read_common_records(scope, "display_terms", "/settings/display_settings_read/",{},true);
            return post.success(function(response){
                scope["display_terms"] = response.data;
            })
        },
    }
})

