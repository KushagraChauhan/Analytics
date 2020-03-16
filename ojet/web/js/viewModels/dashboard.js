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
  'ojs/ojinputtext',
  'ojs/ojbutton', 
  'ojs/ojtoolbar', 
  'ojs/ojchart'],
 function(accUtils, ko, $, Bootstrap,ArrayDataProvider) {


    function IncidentsViewModel() {
      var self = this;
       self.startdate = ko.observable();
      self.enddate = ko.observable();
      self.submittedValue = ko.observable();
      self.submitBt = function (data, event){
        var startdate = $("#startdate").val();
              var enddate = $("#enddate").val();
              self.submittedValue(self.startdate() + " - " + self.enddate());
              return true;
      }
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
 
 //technology data starts here..
 //
 //
 //
 var data = ko.observableArray();/*Most important thing to make the data array observable otherwise it will not show the data of the REST API*/
          function getData() {
                  // var data = [];/**/
                  $.getJSON("https://analytics.techeela.net/categorydata?startdate=2020-01-10&enddate=2020-01-15&category='Technology'").
                  then(function(dataset) {
                      $.each(dataset, function (index, value) {
                           console.table((dataset));
                          data.push(value);
                          // PUSH THE VALUES INSIDE THE ARRAY.
                      });                 
                  });
      }

      getData();
      this.dataProvider = new ArrayDataProvider(data, { keyAttributes: 'id' });
//usergroup data starts here..
//
//
//

      var data2 = ko.observableArray();/*Most important thing to make the data array observable otherwise it will not show the data of the REST API*/
          function usergroupData() {
                  // var data = [];/**/
                  $.getJSON("https://analytics.techeela.net/usergroupdata?startdate=2020-01-09&enddate=2020-01-14&category='Technology'").
                  then(function(dataset) {
                      $.each(dataset, function (index, value) {
                           console.table((dataset));
                          data2.push(value);
                          // PUSH THE VALUES INSIDE THE ARRAY.
                      });                 
                  });
      }

      usergroupData();
      this.dataProvider2 = new ArrayDataProvider(data2, { keyAttributes: 'id' });

//location data starts here
//
//
//
      var data3 = ko.observableArray();/*Most important thing to make the data array observable otherwise it will not show the data of the REST API*/
          function locationData() {
                  // var data = [];/**/
                  $.getJSON("https://analytics.techeela.net/categorydata?startdate=2020-01-09&enddate=2020-01-12&category='Location'").
                  then(function(dataset) {
                      $.each(dataset, function (index, value) {
                           console.table((dataset));
                          data3.push(value);
                          // PUSH THE VALUES INSIDE THE ARRAY.
                      });                 
                  });
      }

      locationData();
      this.dataProvider3 = new ArrayDataProvider(data3, { keyAttributes: 'id' });
      // console.log("Test the gate");
      

 //industry data starts here
//
//
//
      var data4 = ko.observableArray();/*Most important thing to make the data array observable otherwise it will not show the data of the REST API*/
          function industryData() {
                  // var data = [];/**/
                  $.getJSON("https://analytics.techeela.net/categorydata?startdate=2020-01-09&enddate=2020-01-12&category='Industry'").
                  then(function(dataset) {
                      $.each(dataset, function (index, value) {
                          console.table((dataset));
                          data4.push(value);
                          // PUSH THE VALUES INSIDE THE ARRAY.
                      });                 
                  });
      }

      industryData();
      this.dataProvider4 = new ArrayDataProvider(data4, { keyAttributes: 'id' });
            

  //practice data starts here
//
//
//
      var data5 = ko.observableArray();/*Most important thing to make the data array observable otherwise it will not show the data of the REST API*/
          function practiceData() {
                  // var data = [];/**/
                  $.getJSON("https://analytics.techeela.net/categorydata?startdate=2020-01-09&enddate=2020-01-12&category='Practice'").
                  then(function(dataset) {
                      $.each(dataset, function (index, value) {
                          console.table((dataset));
                          data5.push(value);
                         console.log(value.change);
                         
                          // PUSH THE VALUES INSIDE THE ARRAY.
                      });                 
                  });
      }
      

      practiceData();
      this.dataProvider5 = new ArrayDataProvider(data5, { keyAttributes: 'id' });  
  

           this.buttonLabel = ko.observable("Button");


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



      

    }//Incident Model Ends here

    

    /*
     * Returns an instance of the ViewModel providing one instance of the ViewModel. If needed,
     * return a constructor for the ViewModel so that the ViewModel is constructed
     * each time the view is displayed.
     */
    return IncidentsViewModel;
  }
);
