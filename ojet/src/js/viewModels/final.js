 var data2 = ko.observableArray();/*Most important thing to make the data array observable otherwise it will not show the data of the REST API*/
      var testvalue = "RED";
      self.value = ko.observable(testvalue);
      console.log(testvalue);
          function getData() {
                  // var data = [];/**/
                  $.getJSON("https://demo.groovenexus.info/wp-json/mobileapp/v1/mydatatest").
                  then(function(dataset) {
                      $.each(dataset, function (index, value) {
                          console.log(" I am dataset inside each " + JSON.stringify(dataset));
                          data2.push(value);
                          // PUSH THE VALUES INSIDE THE ARRAY.
                      });                
                  });
      }

      getData();
      // console.log("Test the gate");
      console.log(JSON.stringify(data2));
      //self.dataprovider = new ArrayDataProvider(data, {keyAttributes: 'EmployeeId', implicitSort: [{attribute: 'EmployeeId', direction: 'ascending'}]});

       self.dataProvider = new ArrayDataProvider(data2, {keyAttributes: 'id'});