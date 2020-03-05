/**
 * @license
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 * @ignore
 */
/*
 * Your application specific code will go here
 */
define(['knockout', 'ojs/ojmodule-element-utils', 'ojs/ojrouter', 'ojs/ojarraydataprovider', 'ojs/ojoffcanvas', 'ojs/ojknockouttemplateutils', 'ojs/ojknockout', 'ojs/ojmodule-element',   'ojs/ojbutton'],
  function(ko, moduleUtils, Router, ArrayDataProvider, OffcanvasUtils, KnockoutTemplateUtils) {
     function ControllerViewModel() {
      var self = this;

      self.KnockoutTemplateUtils = KnockoutTemplateUtils;

      // Handle announcements sent when pages change, for Accessibility.
      self.manner = ko.observable('polite');
      self.message = ko.observable();
      self.waitForAnnouncement = false;
      self.navDrawerOn = false;

      document.getElementById('globalBody').addEventListener('announce', announcementHandler, false);

      /*
        @waitForAnnouncement - set to true when the announcement is happening.
        If the nav-drawer is ON, it is reset to false in 'ojclose' event handler of nav-drawer.
        If the nav-drawer is OFF, then the flag is reset here itself in the timeout callback.
      */
      function announcementHandler(event) {
        self.waitForAnnouncement = true;
        setTimeout(function() {
          self.message(event.detail.message);
          self.manner(event.detail.manner);
          if (!self.navDrawerOn) {
            self.waitForAnnouncement = false;
          }
        }, 200);
      };

      // Router setup
      self.router = Router.rootInstance;
      self.router.configure({
       'dashboard': {label: 'Dashboard', isDefault: true},
       'incidents': {label: 'Incidents'},
       'customers': {label: 'Customers'},
       'profile': {label: 'Profile'},
       'about': {label: 'About'}
      });
      Router.defaults['urlAdapter'] = new Router.urlParamAdapter();

      self.loadModule = function () {
        self.moduleConfig = ko.pureComputed(function () {
          var name = self.router.moduleConfig.name();
          var viewPath = 'views/' + name + '.html';
          var modelPath = 'viewModels/' + name;
          return moduleUtils.createConfig({ viewPath: viewPath,
            viewModelPath: modelPath, params: { parentRouter: self.router } });
        });
      };

      // Navigation setup
      var navData = [
      {name: 'Dashboard', id: 'dashboard',
       iconClass: 'oj-navigationlist-item-icon demo-icon-font-24 demo-chart-icon-24'},
      {name: 'Incidents', id: 'incidents',
       iconClass: 'oj-navigationlist-item-icon demo-icon-font-24 demo-fire-icon-24'},
      {name: 'Customers', id: 'customers',
       iconClass: 'oj-navigationlist-item-icon demo-icon-font-24 demo-people-icon-24'},
      {name: 'Profile', id: 'profile',
       iconClass: 'oj-navigationlist-item-icon demo-icon-font-24 demo-person-icon-24'},
      {name: 'About', id: 'about',
       iconClass: 'oj-navigationlist-item-icon demo-icon-font-24 demo-info-icon-24'}
      ];
      self.navDataProvider = new ArrayDataProvider(navData, {keyAttributes: 'id'});

      // Drawer setup
      self.toggleDrawer = function() {
        self.navDrawerOn = true;
        return OffcanvasUtils.toggle({selector: '#navDrawer', modality: 'modal', content: '#pageContent'});
      }
      // Add a close listener so we can move focus back to the toggle button when the drawer closes
      document.getElementById('navDrawer').addEventListener("ojclose", onNavDrawerClose);

      /*
        - If there is no aria-live announcement, bring focus to the nav-drawer button immediately.
        - If there is any aria-live announcement in progress, add timeout to bring focus to the nav-drawer button.
        - When the nav-drawer is ON and annoucement happens, then after nav-drawer closes reset 'waitForAnnouncement' property to false.
      */
      function onNavDrawerClose(event) {
        self.navDrawerOn = false;
        if(!self.waitForAnnouncement) {
          document.getElementById('drawerToggleButton').focus();
          return;
        }

        setTimeout(function() {
          document.getElementById('drawerToggleButton').focus();
          self.waitForAnnouncement = false;
        }, 2500);
      }

      // Header Setup
      self.getHeaderModel = function() {
        this.pageTitle = self.router.currentState().label;
        this.transitionCompleted = function() {
          // Adjust content padding after header bindings have been applied
          self.adjustContentPadding();
        }
        this.toggleDrawer = self.toggleDrawer;
      };

      // Method for adjusting the content area top/bottom paddings to avoid overlap with any fixed regions.
      // This method should be called whenever your fixed region height may change.  The application
      // can also adjust content paddings with css classes if the fixed region height is not changing between
      // views.
      self.adjustContentPadding = function () {
        var topElem = document.getElementsByClassName('oj-applayout-fixed-top')[0];
        var contentElem = document.getElementsByClassName('oj-applayout-content')[0];
        var bottomElem = document.getElementsByClassName('oj-applayout-fixed-bottom')[0];

        if (topElem) {
          contentElem.style.paddingTop = topElem.offsetHeight+'px';
        }
        if (bottomElem) {
          contentElem.style.paddingBottom = bottomElem.offsetHeight+'px';
        }
        // Add oj-complete marker class to signal that the content area can be unhidden.
        // See the override.css file to see when the content area is hidden.
        contentElem.classList.add('oj-complete');
      }
    }

    return new ControllerViewModel();
  }
);
