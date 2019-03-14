var app = angular.module('common_services', [])

app.factory("Findings", function(CommonFunc,CommonRead) { 
    return {
        open_dialog: function(scope,record) {
            var me = this;
            scope.current_record = record;
            scope.findings_record = {};
            var post = scope.post_generic("/findings2/read_entry/"+scope.current_module+"/"+record.id+"/")
            post.success(function(response){
                scope.findings_record = scope.format_date(response.record,false,true)
                scope.findings_record["transaction_date"] = scope.current_record.date;
                scope.findings = response.data;

                me.read_staff(scope);
                scope.open_dialog("/findings2/open_entry_dialog/","width80 second_dialog");
            })
        },

        read_staff: function(scope){
            CommonRead.read_users_generic(scope,{
                "exclude_yahshuan": true,
                "use_current_company": true,
            },"staffs");
        },

        remove_line: function(lists,index){
            lists.splice(index,1);
            if(lists.length == 0){
                lists.push({});
            }
        },

        create: function(scope){
            var record = scope.format_date(angular.copy(scope.findings_record),["date","transaction_date"])
            var params = {
                "record": record,
                "findings": scope.findings
            }

            var post = scope.post_generic("/findings2/create_entry/",params,"dialog",true,false,true);
            post.success(function(response){
                var has_findings = false;
                for(var i in scope.findings){
                    if(scope.findings[i].selected){
                        has_findings = true;
                        break;
                    }
                }

                scope.current_record.has_findings = has_findings;
            })
        }
    }
})

app.factory("Attachment2", function(CommonFunc) { 
    return {
        open_dialog: function(scope,record) {
            scope.file_added = false;
            scope.current_record = record;
            var me = this;

            var post = this.read(scope);
            post.success(function(response){
                scope.open_dialog("/attachment2/open_dialog/","width80 second_dialog");
            })
        },
        read: function(scope){
            var post = scope.post_generic("/attachment2/read/"+scope.current_module+"/"+scope.current_record.id,{},"dialog")
            return post.success(function(response){
                scope.attachments = response;
            })
        },
        remove: function(scope,attachment){
            var me = this;
            var confirmation = CommonFunc.confirmation("Remove?",false,false,"Continue");
            confirmation.then(function(){
                var post = scope.post_generic("/attachment2/remove/"+scope.current_module+"/"+attachment.id,{},"dialog",true);
                post.success(function(){
                    me.read(scope);
                })
            })
        }
    }
})


app.factory("Wizard", function(CommonFunc,CommonRead,$state,$http) {
    var steps = [];
    var modules = [];
    var current_step = {};
    var current_page = 1;
    return {
        set_steps: function(list){
            this.steps = list; 
        },
        get_steps: function(){
            return this.steps;
        },
        set_modules: function(list){
            this.modules = list; 
        },
        get_modules: function(){
            return this.modules;
        },
        set_current_step: function(list){
            this.current_step = list; 
        },
        get_current_step: function(){
            return this.current_step;
        },
        set_current_page: function(list){
            this.current_page = list; 
        },
        get_current_page: function(){
            return this.current_page;
        },

        previous: function(first){
            this.current_page--;
            if(first){
                this.current_page = 1;
            }
            if(this.current_page < 1){
                this.current_page = 1;
            }
            this.current_step = this.steps[this.current_page - 1];
            $state.go(this.current_step.url)
        },
        next: function(last){
            this.current_page++;
            if(last){
                this.current_page = this.steps.length;
            }
            if(this.current_page > this.steps.length){
                this.current_page = this.steps.length;
            }
            this.current_step = this.steps[this.current_page - 1];
            $state.go(this.current_step.url)
        },
        instantiate: function(){
            /*if($state.current.name == "home"){
                this.reset();
                return;
            }*/
            if(!this.steps){
                this.reset();
            }
            if(this.steps.length == 0){
                this.read_modules();
            }
        },
        reset: function(){
            this.steps = [];
            this.current_step = {};
            this.current_page = 1;
        },
        read_modules: function(force,scope){
            var me = this;
            $http.post("/user_company/read_modules/")
            .success(function(response){
                conditions = {
                    "bank":["sales","purchases"],
                    "sales_order":["sales",],
                    "purchase_order":["purchases",],
                    "credit_memo":["sales",],
                    "pos":["sales","inventory"],
                }

                for(i in response){
                    if(conditions[response[i].name]){
                        response[i]["condition"] = conditions[response[i].name];
                    }
                }
                me.modules = response;
                if(scope){
                    scope.modules = response;
                }
                me.read_steps();
                scope.current_step = me.current_step;
            })
            /*
                Read modules here and return
            */
        },
        read_steps: function(){
            if(!this.steps || this.steps.length == 0){
                this.generate_steps();
            }
            this.current_page = 1;
            this.current_step = {};
            /*To get the current step base on active state.*/
            for(i in this.steps){
                if(this.steps[i].url == $state.current.name){
                    this.current_step = this.steps[i];
                    break;
                }
                this.current_page++;
            }
        },
        generate_steps: function(){
            var tempsteps = [
                {"display": "Company Information","url": "company"},
                {"display": "Centercode","url": "locations"},
                {"display": "Business Type","url": "business_type"},
                {"display": "Select account here base on business type selected.","url": "accounts"},
                {"display": "Setup Customer","url": "customers","condition":["sales",]},
                {"display": "Setup Supplier","url": "suppliers","condition":["purchases",]},
                {"display": "Setup Employee","url": "employees"},
                {"display": "Setup Items","url": "items"},
                {"display": "Setup Users","url": "users"},
            ]

            var steps = []
            for(i in tempsteps){
                var to_push = true;
                if(tempsteps[i]["condition"]){
                    var to_push = false;
                    for(x in tempsteps[i]["condition"]){
                        for(y in this.modules){
                            if(this.modules[y].name == tempsteps[i]["condition"][x]){
                                to_push = true;
                            }
                        }
                    }
                }
                if(to_push){
                    steps.push(tempsteps[i]);
                }
            }
            steps.unshift({"display": "Select applicable modules for your Company.","url": "home"});
            steps.push({"display": "End","url": "end"})
            this.set_steps(steps);
        }
    }

});

app.factory("Subsidiary", function(CommonFunc,CommonRead) { 
    return{
        open_dialog: function(scope,account_key,neww){
            var account = scope.current_row[account_key];
            var subsidiary_type = account.subsidiary_type;
            if(!subsidiary_type){
                scope.current_row["subsidiaries"] = [];
                return;
            }
            if(scope.current_row["subsidiaries"] === undefined){
                scope.current_row["subsidiaries"] = [];
            }

            subsidiary_type += "s";
            scope.subsidiary_title = "Customer";
            var post = false;
            if(scope[subsidiary_type] === undefined || !scope[subsidiary_type]){
                if(subsidiary_type == "customers"){
                    post = CommonRead.customers_generic(scope,"users");
                }else if(subsidiary_type == "suppliers"){
                    post = CommonRead.vendors_generic(scope,"users");
                }else{
                    post = CommonRead.employee_generic(scope,"users");
                }
                post.success(function(response){
                    if(!neww){
                        scope.open_dialog("/common/subsidiary_dialog_new/","dialog_height_60 dialog_width_60 second_dialog","dialog");
                    }else{
                        scope.open_dialog("/common/subsidiary_dialog_new2/","dialog_height_60 dialog_width_60 second_dialog","dialog");
                    }
                })
            }else{
                scope.users = scope[subsidiary_type];
                if(!neww){
                    scope.open_dialog("/common/subsidiary_dialog_new/","dialog_height_60 dialog_width_60 second_dialog","dialog");
                }else{
                    scope.open_dialog("/common/subsidiary_dialog_new2/","second_dialog","dialog");
                }
            }
        },
        new_line: function(scope){
            scope.current_row["subsidiaries"].push(angular.copy(scope.subsidiarylist));
            scope.subsidiarylist = {}
            scope.subsidiary_total();
        },
        remove_line: function(scope,list){
            scope.current_row['subsidiaries'].splice(scope.current_row['subsidiaries'].indexOf(list), 1);
            scope.subsidiary_total();
        },
        get_total: function(scope){
            var total = 0;
            for(i in scope.current_row["subsidiaries"]){
                total += scope.current_row["subsidiaries"][i]["amount"];
            }
            return total;
        },
    }
})

app.factory("Subsidiary2", function(CommonFunc,CommonRead) { 
    return{
        open_dialog: function(scope,account_key,neww){
            var account = scope.current_row[account_key];
            var subsidiary_type = account.subsidiary_type;
            if(!subsidiary_type || neww){
                scope.current_row["subsidiaries"] = [];
                if(!subsidiary_type){return;}  
                scope.current_row["quantity"] = 0;
                scope.current_row["price"] = 0;
                scope.current_row["amount"] = 0;
            }

            if(scope.current_module == "general_journal"){
                if(!scope.current_row["subsidiary_amount_type"]){
                    scope.current_row["subsidiary_amount_type"] = scope.subsidiary_amount_type[0];
                }
            }

            if(scope.current_row["subsidiaries"] === undefined){
                scope.current_row["subsidiaries"] = [];
            }
            if(scope.current_row["subsidiaries"].length == 0){
                this.new_line(scope.current_row);
            }
            
            subsidiary_type += "s";
            scope.subsidiary_title = "Customer";
            var post = false;
            if(scope[subsidiary_type] === undefined || !scope[subsidiary_type]){
                if(subsidiary_type == "customers"){
                    post = CommonRead.customers_generic(scope,"users");
                }else if(subsidiary_type == "suppliers"){
                    post = CommonRead.vendors_generic(scope,"users");
                }else{
                    post = CommonRead.employee_generic(scope,"users");
                }
                post.success(function(response){
                    scope.open_dialog("/common/subsidiary_dialog_new2/","width50 second_dialog","dialog");
                })
            }else{
                scope.users = scope[subsidiary_type];
                scope.open_dialog("/common/subsidiary_dialog_new2/","width50 second_dialog","dialog");
            }
        },
        new_line: function(row){
            if(row["subsidiaries"] === undefined || !row["subsidiaries"]){
                row["subsidiaries"] = [];
            }
            row["subsidiaries"].push({"amount": 0})
        },
        remove_line: function(row,index){
            row.subsidiaries.splice(index,1);
            if(row.subsidiaries.length == 0){
                this.new_line(row);
            }
            /*Calculate total here*/
        },
        get_total: function(row){
            var total = 0;
            for(i in row["subsidiaries"]){
                if(row["subsidiaries"][i]["user"] !== undefined){
                    total += row["subsidiaries"][i]["amount"];
                }
            }
            return total;
        }
    }
})

app.factory("RightClick", function(Notification){
    return {
        get_menu: function(scope, record, is_yahshuan){
            menu = []
            copy_menu = ['Copy', function ($itemScope, $event, modelValue, text, $li) {
                if (scope.current_module == "general_journal")
                    scope.load_to_edit(record,'copy',false)
                else
                    scope.load_to_edit(record,true,true,true)
            }]
            attach_menu = ['Attach', function ($itemScope, $event, modelValue, text, $li) {
                scope.attachment_dialog(record)
            }]

            /*For P.O and S.O*/
            po_so_close_menu = ['Close', function ($itemScope, $event, modelValue, text, $li) {
                scope.close(record)
            }]

            reverse_menu= ['Reverse', function ($itemScope, $event, modelValue, text, $li) {
                scope.load_to_edit(record,'reverse',false)
            }]
            related_menu = ['Related', function ($itemScope, $event, modelValue, text, $li) {
                scope.related_transactions(scope,record)
            }]

            findings_menu = ['Findings', function ($itemScope, $event, modelValue, text, $li) {
                scope.FindingsService.open_dialog(scope,record)
            }]

            view_manage_sessions_menu = ['View Session', function($itemScope, $event, modelValue, text, $li) {
                scope.open_session_handler_dialog(record)
            }]

            print_menu = ['Print', function($itemScope, $event, modelValue, text, $li){
                if(scope.current_module == "enrollment_list"){
                    scope.print_enrollment_form(record)
                }else if(scope.current_module == "evaluation_list"){
                    scope.print_student_session(record)
                }
            }]

            edit_menu = ["Edit", function($itemScope, $event, modelValue, text, $li){
                scope.create_edit_session(record)
            }]
            
            remove_menu = ['Delete', function ($itemScope, $event, modelValue, text, $li) {
                scope.delete_student_session(record);
            }]

            //Stock in and Stock Out
            close_menu = ['Close', function ($itemScope, $event, modelValue, text, $li) {
                scope.set_to_closed(record);
            }]
            receive_menu = ['Receive', function ($itemScope, $event, modelValue, text, $li) {
                scope.receive_transfer(record);
            }]
            reject_menu = ['Reject', function ($itemScope, $event, modelValue, text, $li) {
                scope.reject_transfer(record);
            }]

            show_ledger_menu = ['Show Ledger', function($itemScope, $event, modelValue, text, $li) {
                scope.show_ledger(record);
            }]

            status = 'Active'
            if(scope.current_module == 'employee' || scope.current_module == 'supplier' || scope.current_module == 'customer'){
                if(record.is_active){
                    status = 'Inactive'
                }
            }

            set_inactive_menu = ['Set '+status, function($itemScope, $event, modelValue, text, $li){
                scope.set_to_inactive(record);
            }]

            delete_menu = ['Delete', function($itemScope, $event, modelValue, text, $li) {
                if(scope.current_module == "enrollment_list"){
                    scope.delete_enrollment(record)
                }
            }]

            if (scope.key_in_list(scope.current_module, [
                "evaluation_list"])){
                menu.push(edit_menu);
            }

            if (scope.key_in_list(scope.current_module,[
                "monitoring",
                "purchase_order",
                "receive_inventory",
                "paybills","sales_order",
                "invoice",
                "credit_memo",
                "sales_collections",
                "general_journal"])) {
                menu.push(attach_menu)
            }
            if (scope.key_in_list(scope.current_module,["general_journal"])){
                menu.push(reverse_menu)
            }
            if (scope.key_in_list(scope.current_module,[
                "purchase_order",
                "receive_inventory",
                "paybills",
                "sales_order",
                "invoice",
                "sales_collections",
                "general_journal"])){
                menu.push(related_menu)
            }
            if (scope.key_in_list(scope.current_module,[
                "monitoring",
                "paybills",
                "invoice",
                "sales_order",
                "receive_inventory",
                "purchase_order",
                "sales_collections",
                "general_journal"])) {
                menu.push(copy_menu)
            }
            if (scope.key_in_list(scope.current_module,[
                "evaluation_list",
                "enrollment_list",
                "purchase_order",
                "receive_inventory",
                "paybills",
                "sales_order",
                "general_journal",
                "invoice"])){
                menu.push(print_menu)
            }
            if (scope.key_in_list(scope.current_module,[
                "purchase_order",
                "sales_order"])){
                menu.push(po_so_close_menu)
            }

            if (scope.key_in_list(scope.current_module,["stock_out"])) {
                menu.push(close_menu)
            }

            if (scope.key_in_list(scope.current_module,["stock_in"])) {
                menu.push(receive_menu)
            }

            if(is_yahshuan){
                if (scope.key_in_list(scope.current_module,[
                    "purchase_order",
                    "receive_inventory",
                    "paybills",
                    "sales_order",
                    "invoice",
                    "sales_collections",
                    "credit_memo",
                    "general_journal",
                    "monitoring"])){
                    menu.push(findings_menu)
                }
            }

            if (scope.key_in_list(scope.current_module,[
                "supplier",
                "customer",])){
                menu.push(show_ledger_menu)
            }

            if (scope.key_in_list(scope.current_module,[
                "employee",
                "supplier",
                "customer",])){
                menu.push(set_inactive_menu)
            }

            if(scope.key_in_list(scope.current_module,[
                "enrollment_list",])){
                menu.push(view_manage_sessions_menu)
            }
            
            menu.push(null)
            
            if (scope.key_in_list(scope.current_module,["stock_in"])) {
                menu.push(reject_menu)
            }
            
            if (scope.key_in_list(scope.current_module,[
                "purchase_order",
                "receive_inventory",
                "paybills",
                "sales_order",
                "invoice",
                "sales_collections"])) {
                menu.push(void_menu)
            }
            
            if  (scope.key_in_list(scope.current_module,[
                "monitoring",
                "purchase_order",
                "evaluation_list",
                "customer"])) {
                menu.push(remove_menu)
            }



            if(scope.key_in_list(scope.current_module,[
                "enrollment_list",])){
                menu.push(delete_menu)
            }

            return menu
        }
    }
})


app.factory("Notification", function(toastr) {

    return {
        success: function(title, body, timeout) {

            if (!title) {
                title = "Success"
            }

            if (!timeout) {
                timeout = 5000;
            }

            var config = {
                timeOut: timeout
            }

            return toastr.success(body, title, config);
        },
        error: function(title, body, timeout) {

            if (!title) {
                title = "Error"
            }

            if (!timeout) {
                timeout = 15000;
            }

            var config = {
                timeOut: timeout
            }

            return toastr.error(body, title, config);
        },

        error_action: function(title, body,id=null){
            if(body == 'transaction_type'){
                a = "<a class='pull-right' href='/transaction_types/#/transaction_type' target='_blank'><br><b><u>Set code here</a>"
            }

            var config = {
                allowHtml:true,
                closeButton: true,
            }

            return toastr.error(title+" "+a, config)
        },

        warning: function(title, body, timeout) {

            if (!title) {
                title = "Warning"
            }

            if (!timeout) {
                timeout = 15000;
            }

            var config = {
                timeOut: timeout
            }

            return toastr.warning(body, title, config);
        },
    }

});

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

        get_questions: function(scope,transaction_types) {
            data = {"all": true}
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
            let response = scope.post_api("program/read/");
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

        get_questions_new : function(scope)
        {
            let response = scope.post_api("question/read/");
            response.success(function (response) {
                scope["questions"] = response.records;
            });
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

