var app = angular.module('common_services', []);


app.factory("CommonFunc", function($http, SweetAlert) {
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

        confirmation: function(title, text, type,confirmtext, confirmFunction, cancelFunction) {
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
            }, confirmFunction, cancelFunction);

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

app.factory("CommonRead", function($http, CommonRequests)
{
    return {

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

