var app = angular.module('common_filters',[])

app.filter("currency", function($http) {
  return function(number) {
    var precision = 2;
    var symbol = "";
    if(!precision) precision = 2;
    if(!symbol) symbol = "";

    if(number < 0){
      number = Math.abs(number);
      formatted_currency = accounting.formatMoney(number,"", precision,",",".","%s%v");
      formatted_currency = "("+formatted_currency+")";
    }else{
      formatted_currency = accounting.formatMoney(number,"", precision,",",".","%s%v");
    }
    return formatted_currency     
  };
})

app.filter("integer", function($http) {
  return function(number) {
    if(!number) number = 0;
    number = Math.abs(number);
    return number     
  };
})

app.filter("currency_dash", function($http) {
  return function(number) {
    var precision = 2;
    var symbol = "";
    if(!precision) precision = 2;
    if(!symbol) symbol = "";

    if(number < 0){
      number = Math.abs(number);
      formatted_currency = accounting.formatMoney(number,"", precision,",",".","%s%v");
      formatted_currency = "("+formatted_currency+")";
    }else if(number == 0){
      formatted_currency = "-";
    }else{
      formatted_currency = accounting.formatMoney(number,"", precision,",",".","%s%v");
    }
    return formatted_currency     
  };
})

app.filter('capitalize', function() {
    return function(input){
      return (!!input) ? input.charAt(0).toUpperCase() + input.substr(1).toLowerCase() : '';
    }
})

app.filter('break_capitalize', function() {
    return function(input){
      if (input)
        input = input.replace("_"," ")
      return (!!input) ? input.charAt(0).toUpperCase() + input.substr(1).toLowerCase() : '';
    }
})

app.filter("currency_qty", function($http) {
  return function(number) {
    return accounting.formatMoney(number,"", 2,",",".","%s%v");             
  };
})

.filter("secondsDuration", function(){

    return function(seconds, format)
    {
          if (!seconds) { seconds = 0; }

          var sec_num = parseInt(seconds, 10); 
          var hours   = Math.floor(sec_num / 3600);
          var minutes = Math.floor((sec_num - (hours * 3600)) / 60);
          var seconds = sec_num - (hours * 3600) - (minutes * 60);

          if (hours < 10 && hours >= 0) {hours   = "0"+hours;}
          if (minutes < 10) {minutes = "0"+minutes;}
          if (seconds < 10) {seconds = "0"+seconds;}

          return hours + ':' + minutes;
    } 
})

app.filter('secondstoDuration', [function() {
    return function(seconds, format) {

      // Convert Seconds to Time duration (HH:MM:SS) - for hours more than 24
      if(!seconds) { seconds = 0;}
      
      var sec_num = parseInt(seconds, 10); 
      var hours   = Math.floor(sec_num / 3600);
      var minutes = Math.floor((sec_num - (hours * 3600)) / 60);
      var seconds = sec_num - (hours * 3600) - (minutes * 60);

      if (hours < 10 && hours >= 0) {hours   = "0"+hours;}
      if (minutes < 10) {minutes = "0"+minutes;}
      if (seconds < 10) {seconds = "0"+seconds;}

      return hours + ':' + minutes + ':' + seconds;
      
      
    };
}])

app.filter('dateInMillis', function(){
    return function(dateString){
      return Date.parse(dateString);
    };
  });

app.filter('range', function () {
    return function (input, total) {

        var _total = 1;
        if (total !== null) {
            if (!isNaN(total)) {
                _total = total;
            }
        }

        _total = Math.ceil(_total);

        for (var i = 1; i < _total + 1; i++) {
            input.push(i);
        }

        return input;
    };
});

app.filter('cust_pagination', function () {
    return function (items, pageSize, step) {
        
        if (pageSize == null) {
             pageSize = 5;
        }
        
        var nPageSize = items.length;
        var nStep = 0;
        if (!isNaN(pageSize) && pageSize) {
            nPageSize = pageSize;

            if (!isNaN(step) && step) {
                nStep = step -1;
            }
        }
        
      if(nPageSize > 0){        
        var startIndex = nStep * nPageSize;
        var endIndex = startIndex + nPageSize;
        var arr = items.slice(startIndex, endIndex);
        return arr;
      }else{
        return items;
      }
    }
});
