/**
 * @license
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 * @ignore
 */
/*
 * Your incidents ViewModel code goes here
 */
define(['accUtils',
  'knockout',
  'jquery',
  'ojs/ojbootstrap',
  'ojs/ojarraydataprovider', 
  'ojs/ojknockout',
  'ojs/ojnavigationlist',
  'ojs/ojswitcher',
  'ojs/ojradioset', 
  'ojs/ojlabel',
  'ojs/ojbutton', 
  'ojs/ojtoolbar', 
  'ojs/ojchart'],
 function(accUtils, ko, $, Bootstrap,ArrayDataProvider) {

    function IncidentsViewModel() {
      var self = this;
      // Below are a set of the ViewModel methods invoked by the oj-module component.
      // Please reference the oj-module jsDoc for additional information.

      /**
       * Optional ViewModel method invoked after the View is inserted into the
       * document DOM.  The application can put logic that requires the DOM being
       * attached here.
       * This method might be called multiple times - after the View is created
       * and inserted into the DOM and after the View is reconnected
       * after being disconnected.
       */
          var data2 = ko.observableArray();/*Most important thing to make the data array observable otherwise it will not show the data of the REST API*/
          function getData() {
                  // var data = [];/**/
                  $.getJSON("https://analytics.techeela.net/usergroupdata?startdate=2020-01-09&enddate=2020-01-14").
                  then(function(dataset) {
                      $.each(dataset, function (index, value) {
                          console.log(JSON.stringify(dataset));
                          data2.push(value);
                          // PUSH THE VALUES INSIDE THE ARRAY.
                      });                 
                  });
      }

      getData();
      // console.log("Test the gate");
      console.log(JSON.stringify(data2));


    var data3 = ko.observableArray();/*Most important thing to make the data array observable otherwise it will not show the data of the REST API*/
          function vkData() {
                  // var data = [];/**/
                  $.getJSON("https://demo.groovenexus.info/wp-json/mobileapp/v1/mydatatest").
                  then(function(dataset) {
                      $.each(dataset, function (index, value) {
                          console.log(" I am dataset inside each " + JSON.stringify(dataset));
                          data3.push(value);
                          // PUSH THE VALUES INSIDE THE ARRAY.
                      });                 
                  });
      }

     vkData();
      // console.log("Test the gate");
      console.log(JSON.stringify(data3));


       var data4 = ko.observableArray();/*Most important thing to make the data array observable otherwise it will not show the data of the REST API*/
          function techData() {
                  // var data = [];/**/
                  $.getJSON("https://analytics.techeela.net/categorydata?enddate=2020-01-14&startdate=2020-01-09&category='Technology'").
                  then(function(dataset) {
                      $.each(dataset, function (index, value) {
                          console.log(" I am dataset inside each " + JSON.stringify(dataset));
                          data4.push(value);
                          // PUSH THE VALUES INSIDE THE ARRAY.
                      });                 
                  });
      }

     techData();
      // console.log("Test the gate");
      console.log(JSON.stringify(data4));

      var data5 = ko.observableArray();
       function employeeData() {
          $.getJSON("https://analytics.techeela.net/userdaywise?startdate=2020-01-09&enddate=2020-01-14&usergroup='Employee'").
                  then(function(dataset) {
                      $.each(dataset, function (index, value) {
                          console.log(" I am dataset inside each " + JSON.stringify(dataset));
                          data5.push(value);
                          // PUSH THE VALUES INSIDE THE ARRAY.
                      });                 
                  });
       }
       employeeData();

       var data6 = ko.observableArray();
       function prospectData() {
          $.getJSON("https://analytics.techeela.net/userdaywise?startdate=2020-01-09&enddate=2020-01-14&usergroup='Prospect'").
                  then(function(dataset) {
                      $.each(dataset, function (index, value) {
                          console.log(" I am dataset inside each " + JSON.stringify(dataset));
                          data6.push(value);
                          // PUSH THE VALUES INSIDE THE ARRAY.
                      });                 
                  });
       }
       prospectData();

       var data7 = ko.observableArray();
       function customerData() {
          $.getJSON("https://analytics.techeela.net/userdaywise?startdate=2020-01-09&enddate=2020-01-14&usergroup='Customer'").
                  then(function(dataset) {
                      $.each(dataset, function (index, value) {
                          console.log(" I am dataset inside each " + JSON.stringify(dataset));
                          data7.push(value);
                          // PUSH THE VALUES INSIDE THE ARRAY.
                      });                 
                  });
       }
       customerData();

          //line area chart JS begins here
          /* toggle button variables */
   // self.stackValue = ko.observable('off');
   //  self.orientationValue = ko.observable('vertical');
   //         self.dataProvider = new ArrayDataProvider(data2, {keyAttributes: 'id'});

           //self.bardataProvider = new ArrayDataProvider(JSON.parse(data), {keyAttributes: 'id'});

       //   // // //  /*Js for the chart with animation for charts tab */
       //   // // //  /* toggle button variables */
          this.stackValue = ko.observable('off');
           this.orientationValue = ko.observable('vertical');
            self.dataProvider = new ArrayDataProvider(data2, {keyAttributes: 'id'});
          this.hiddenCategories = ko.observableArray([]);
           this.categoryInfo = ko.pureComputed(function() {
          var categories = this.hiddenCategories();
             return categories.length > 0 ? categories.join(', ') : 'none';
          }.bind(this));

        
          this.orientationValue = ko.observable('vertical');
          this.dataProvider3 = new ArrayDataProvider(data3, {keyAttributes: 'id'});

          this.stackValue = ko.observable('off');
           this.orientationValue = ko.observable('vertical');
            self.dataProvider2 = new ArrayDataProvider(data4, {keyAttributes: 'id'});
          this.hiddenCategories = ko.observableArray([]);
           this.categoryInfo = ko.pureComputed(function() {
          var categories = this.hiddenCategories();
             return categories.length > 0 ? categories.join(', ') : 'none';
          }.bind(this));
        //bar chart for search based term  
        /* toggle button variables */
        /* self.stackValue = ko.observable('off');
           self.orientationValue = ko.observable('vertical');
          self.dataProvider = new ArrayDataProvider(JSON.parse(data), {keyAttributes: 'id'});*/

     this.orientationValue = ko.observable('vertical');
          this.linechartdataprovider = new ArrayDataProvider(data5, {keyAttributes: 'id'});

      this.orientationValue = ko.observable('vertical');
          this.prospectdataprovider = new ArrayDataProvider(data6, {keyAttributes: 'id'});  

      this.orientationValue = ko.observable('vertical');
          this.customerdataprovider = new ArrayDataProvider(data7, {keyAttributes: 'id'});       

      self.selectedItem = ko.observable("home");
      self.currentEdge = ko.observable("top");
      self.valueChangedHandler = function (event) {
        var value = event.detail.value,
            previousValue = event.detail.previousValue,
            demoContianer = document.getElementById('demo-container');
        demoContianer.className = demoContianer.className.replace('demo-edge-' + previousValue, 'demo-edge-' + value);
      }
      // Populate some content
      var tabContentNodes = document.querySelectorAll('.demo-tab-content');
      var textNode = document.createElement('p');
      textNode.appendChild(document.createTextNode('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam pharetra, risus ac interdum sollicitudin, sem erat ultrices ipsum, eget vehicula nibh augue sollicitudin ligula. Sed ullamcorper cursus feugiat. Mauris tristique aliquam dictum. Nulla facilisi. Nulla ut sapien sapien. Phasellus tristique arcu id ipsum mattis id aliquam risus sollicitudin.'));
      Array.prototype.forEach.call(tabContentNodes, function(tabContent) {
          for (var i = 0; i < 7; i++) {
            tabContent.appendChild(textNode.cloneNode(true));
          }
      });





      self.connected = function() {
        accUtils.announce('Incidents page loaded.', 'assertive');
        document.title = "Experience Center";
        // Implement further logic if needed
      };

      /**
       * Optional ViewModel method invoked after the View is disconnected from the DOM.
       */
      self.disconnected = function() {
        // Implement if needed
      };

      /**
       * Optional ViewModel method invoked after transition to the new View is complete.
       * That includes any possible animation between the old and the new View.
       */
      self.transitionCompleted = function() {
        // Implement if needed
      };



      function download()
  {
      var headers = {
      id: 'Id'.replace(/,/g, ''), // remove commas to avoid errors
      series: "Series",
      group: "Group",
      value: "Value"
  };

  var jsonObj = JSON.parse(data);
  itemsNotFormatted  = jsonObj;
  alert(itemsNotFormatted);
  /*itemsNotFormatted = [
      {
          id: '2',
          series: 'Data Analytics',
          group: 'B',
          value: '45',
      },
      {
          id: '3',
          series: 'Machine Learning',
          group: 'A',
          value: '50',
      },
      {
          id: '4',
          series: 'Machine Learning',
          group: 'B',
          value: '50',
      },
      {
          id: '5',
          series: 'IT Staffing',
          group: 'A',
          value: '50',
      },
      {
          id: '6',
          series: 'IT Staffing',
          group: 'B',
          value: '50',
      },
      {
          id: '7',
          series: 'Training',
          group: 'A',
          value: '50',
      },
      {
          id: '8',
          series: 'Training',
          group: 'B',
          value: '50',
      }
  ];*/
  var itemsFormatted = [];
  //alert(itemsNotFormatted);

  //format the data
  itemsNotFormatted.forEach((item) => {
   // alert(item);
      itemsFormatted.push({
          id: item.id/*.replace(/,/g, '')*/, // remove commas to avoid errors,
          series: item.series,
          group: item.group,
          value: item.value
      });
  });

/*  for (i in itemsNotFormatted) {
    // x +=itemsNotFormatted[i];
    console.log(itemsNotFormatted);
    itemsFormatted.push({
          //id: itemsNotFormatted[i].id.replace(/,/g, ''), // remove commas to avoid errors,
          series:itemsNotFormatted[i].series,
          group: itemsNotFormatted[i].group,
          value: itemsNotFormatted[i].value
      });
  }*/
  // alert(itemsFormatted);

  var fileTitle = 'orders'; // or 'my-unique-title'
    // exportCSVFile(headers, itemsFormatted, fileTitle);
    exportCSVFile(headers, itemsFormatted, fileTitle);
      }

    

  

      
/*    var a = ko.observableArray(data);
    var normalArray = a();*/

    // function download(){
    // var myarray = [
    // {
    //   "id": 0,
    //   "series": "Data Analytics",
    //   "group": "Group A",
    //   "value": 42
    // },
    // {
    //   "id": 1,
    //   "series": "Data Analytics",
    //   "group": "Group B",
    //   "value": 34
    // }];

    //     myarray.forEach(function(item) {
    //    var items = Object.keys(item);
    //     items.forEach(function(key) {
    //    // console.log('this is a key-> ' + key + ' & this is its value-> ' + item[key]);
    //     //alert('this is a key-> ' + key + ' & this is its value-> ' + item[key]);
    //     });
    //   });

      //var a = ko.observableArray();
      //var normalArray = a();
/*      var a = new oj.Collection();
      var normalArray = a.toJSON(data);*/
      // alert("It will work");
      // alert(JSON.stringify(self.bardataProvider));
      // //alert(normalArray.length);
      // var t1=JSON.stringify(self.bardataProvider);
      // // alert(t1['data']);
      // console.log(data);
      // console.log(self.bardataProvider);
      // console.log(t1);
      // console.log(t1.data);
      // console.log(t1["data"]);
      // const rows=data;
    //   const rows = [
    // ["name1", "city1", "some other info"],
    // ["name2", "city2", "more info"]
    // ];

    // let csvContent = "data:text/csv;charset=utf-8,";

    //   rows.forEach(function(rowArray) {
    //    let row = rowArray.join(",");
    //    csvContent += row + "\r\n";
    //   });


    //   var encodedUri = encodeURI(csvContent);
    //   window.open(encodedUri);

      // }
      //Custom javascript code begins here
      self.clickedButton = ko.observable("(None clicked yet)");
      self.buttonClick = function(event){
      download();
      }.bind(self);

    }//Incident Model Ends here

      
    /*
     * Returns an instance of the ViewModel providing one instance of the ViewModel. If needed,
     * return a constructor for the ViewModel so that the ViewModel is constructed
     * each time the view is displayed.
     */
    return IncidentsViewModel;
  }
);
  