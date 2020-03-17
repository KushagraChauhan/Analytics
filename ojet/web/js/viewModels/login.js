/**
 * @license
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */
/*
 * Your incidents ViewModel code goes here
 */
define(['ojs/ojcore',
 'knockout',
  'jquery',
  'ojs/ojrouter',
  'ojs/ojarraydataprovider',
  'ojs/ojmodule-element-utils',
  'ojs/ojknockouttemplateutils',
  'ojs/ojresponsiveutils',
  'ojs/ojresponsiveknockoututils',
  'ojs/ojoffcanvas',
  'appController',
  'ojs/ojmodel',
  'ojs/ojknockout',
  'ojs/ojinputtext',
  'ojs/ojvalidation-number',
  'ojs/ojbutton',
  'ojs/ojknockout-validation'],
 function(oj, ko, $, Router, ArrayDataProvider,moduleUtils, KnockoutTemplateUtils,ResponsiveUtils, ResponsiveKnockoutUtils,OffcanvasUtils,appControler) {


    function LoginModel() {
      var self = this;
      //login function ends here
      self.username = ko.observable();
      self.password = ko.observable();
      self.submittedValue = ko.observable();
      self.tracker = ko.observable();
      self.navData = ko.observable();
      var myresttoken = "My token";

     // document.getElementById("techeela").style.visibility = "hidden";
      document.getElementById("navTabBar").style.visibility = "hidden";
      document.getElementById("navTabBar2").style.visibility = "hidden";
       document.getElementById("userMenu").style.visibility = "hidden";
      self.showmy = function()
      {
        //var value = "Matching";
        var token = myresttoken;
        return token;
      }
          
          self.submitBt = function (data, event)
          {   
                
              var username = $("#text-user").val();
              var password = $("#text-password").val();

              // alert(username);
              // alert(password);
            var tracker = self.tracker();
            // ensure that no component in the page is invalid, before submitting the form.
            if (tracker.invalidHidden || tracker.invalidShown)
            {
              tracker.showMessages();
              tracker.focusOnFirstInvalid();
              self.submittedValue("");
              return;
            }
             // self.submittedValue(self.username() + " - " + self.password());
            //change this to a valid ajax call.
            $.ajax({
            url: "https://thp.techeela.net/api/login-gateway",
            data: {
              'email':username,
              'password':password
            },
            type: 'POST',
            dataType: 'json',
            success: function (data, textStatus, jqXHR) {
                var x = data;

                console.log("Find the data");
                var mytoken  =  x.success.token;
                myresttoken = mytoken;
                 console.log(JSON.stringify(mytoken));
                  console.log(myresttoken);
                  
      //Router Configuration
      //  self.router = oj.Router.rootInstance;
      //  self.router.configure({
      //    'login': {label: 'LogIn', isDefault: true},
      //     'dashboard': {label: 'Dashboard'},
      //     'incidents': {label: 'Incidents'},
      //     'customers': {label: 'Customers'},
      //     'about': {label: 'About'}
      //  });
     
                
      // self.loadModule = function () {
      //   self.moduleConfig = ko.pureComputed(function () {
      //     var name = self.router.moduleConfig.name();
      //     var viewPath = 'views/' + name + '.html';
      //     var modelPath = 'viewModels/' + name;
      //     return moduleUtils.createConfig({ viewPath: viewPath,
      //       viewModelPath: modelPath, params: { parentRouter: self.router } });
      //   });
      // };


      //           self.navData = [
      //           // {name: 'Login', id: 'login', 
      //           // iconClass: 'oj-navigationlist-item-icon demo-icon-font-24 demo-chart-icon-24'}
      //           {name: 'Dashboard', id: 'dashboard', 
      //            iconClass: 'oj-navigationlist-item-icon demo-icon-font-24 demo-chart-icon-24'},
      //           {name: 'Incidents', id: 'incidents', 
      //            iconClass: 'oj-navigationlist-item-icon demo-icon-font-24 demo-fire-icon-24'},
      //           {name: 'Customers', id: 'customers', 
      //            iconClass: 'oj-navigationlist-item-icon demo-icon-font-24 demo-people-icon-24'},
      //           {name: 'About', id: 'about', 
      //            iconClass: 'oj-navigationlist-item-icon demo-icon-font-24 demo-info-icon-24'}
      //           ];

                // alert(JSON.stringify(self.navData));
                var rootViewModel = ko.observable();
                var isLoggedIn = ko.observable();
                 // rootViewModel.navDataSource.reset(navData2, {idAttribute: 'id'});
                // rootViewModel.userLogin();
                rootViewModel = ko.dataFor(document.getElementById('globalBody'));
                oj.Router.rootInstance.go('dashboard');
                

          if (myresttoken != 0) {
            document.getElementById("navTabBar2").style.visibility = "hidden";
            document.getElementById("navTabBar").style.visibility = "visible";
            document.getElementById("userMenu").style.visibility = "visible";
          }
                //rootViewModel.navDataSource.reset(navData, {idAttribute: 'id'});
                rootViewModel.userLogin(self.username());
                rootViewModel.isLoggedIn('true');
                rootViewModel.restSessionId(jqXHR.getResponseHeader('REST_SESSIONID'));
                  // function afterlogin(){
                  //   if (rootViewModel.isLoggedIn(true)) {
                  //     oj.router.rootInstance.go('dashboard');
                  //   }
                  // }
                  // afterlogin();

                self.username(null);
                self.password(null);

                // oj.Router.sync();
// Router.defaults['urlAdapter'] = new Router.urlParamAdapter();  
               // self.login();
            
            }//Success Ends here

            });
            return true;
     }
        
       

    
        $("input").keypress(function (e) {
          if ((e.which && e.which == $.ui.keyCode.ENTER) || (e.keyCode && e.keyCode == $.ui.keyCode.ENTER)) {
            //validate the element before submitting
            var valid = true;
            if(e.target.type === "password"){
              valid = $("#"+e.target.id).ojInputPassword("validate");
            }
            else if (e.target.type === "text") {
              valid = $("#"+e.target.id).ojInputText("validate");
            }
            if(valid){
              self.submitBt();
              return false;
            }
            self.submittedValue("");
            return true;
          } else {
            return true;
          }
        });
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
      self.connected = function() {
        // Implement if needed
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
    }//View Model Ends here
      /*$(function ()
      {
        ko.applyBindings(new LoginModel(), document.getElementById('div1'));
        $("#text-password").focus();
      }); */
    /*
     * Returns a constructor for the ViewModel so that the ViewModel is constructed
     * each time the view is displayed.  Return an instance of the ViewModel if
     * only one instance of the ViewModel is needed.
     */
    return new LoginModel();
  }
);
