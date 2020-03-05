/*
 * Your application specific code will go here
 */
import * as ko from "knockout";
import Router = require("ojs/ojrouter");
import * as ModuleElementUtils from "ojs/ojmodule-element-utils";
import ArrayDataProvider = require("ojs/ojarraydataprovider");
import * as KnockoutTemplateUtils from "ojs/ojknockouttemplateutils";
import "ojs/ojknockout";
import "ojs/ojmodule-element";
import { RouterState } from "ojs/ojrouterstate";
import * as OffcanvasUtils from "ojs/ojoffcanvas";
import { ojNavigationList } from "ojs/ojnavigationlist";
import { ojModule, ModuleViewModel } from "ojs/ojmodule-element";

class NavDataItem {
  id: string;
  name: string;
  iconClass: string;

  constructor ( { id, name, iconClass } : {
    id: string;
    name: string;
    iconClass: string
  }) {
    this.id = id;
    this.name = name;
    this.iconClass = iconClass;
  }
}

class HeaderModel implements ModuleViewModel {
  pageTitle: string;
  toggleDrawer: Function;
  adjustContentPadding: Function;

  constructor({ pageTitle, toggleDrawer, adjustContentPadding } : {
    pageTitle: string;
    toggleDrawer: Function;
    adjustContentPadding: Function;
  }) {
    this.pageTitle = pageTitle;
    this.toggleDrawer = toggleDrawer;
    this.adjustContentPadding = adjustContentPadding;
  }

  transitionCompleted(): null {
    // adjust content padding after header bindings have been applied
    this.adjustContentPadding();
    return null;
  }
}

class RootViewModel {
  KnockoutTemplateUtils: typeof KnockoutTemplateUtils;
  manner: ko.Observable<string>;
  message: ko.Observable<string|undefined>;
  waitForAnnouncement: boolean;
  navDrawerOn: boolean;
  router: Router;
  moduleConfig: ko.Observable<ojModule["config"]>;
  navDataProvider: ojNavigationList<string, NavDataItem>["data"];

  constructor() {
      this.KnockoutTemplateUtils = KnockoutTemplateUtils;

      // handle announcements sent when pages change, for Accessibility.
      this.manner = ko.observable("polite");
      this.message = ko.observable();
      this.waitForAnnouncement = false;
      this.navDrawerOn = false;

      let globalBodyElement: HTMLElement = document.getElementById("globalBody") as HTMLElement;
      globalBodyElement.addEventListener("announce", this.announcementHandler, false);

      // router setup
      this.router = Router.rootInstance;

      this.router.configure({
       "dashboard": {label: "Dashboard", isDefault: true},
       "incidents": {label: "Incidents"},
       "customers": {label: "Customers"},
       "profile": {label: "Profile"},
       "about": {label: "About"}
      });

      Router.defaults.urlAdapter = new Router.urlParamAdapter();

      this.moduleConfig = ko.observable({"view": [], "viewModel": null});

      // navigation setup
      let navData: NavDataItem[] = [
        new NavDataItem({name: "Dashboard", id: "dashboard",
        iconClass: "oj-navigationlist-item-icon demo-icon-font-24 demo-chart-icon-24"}),
        new NavDataItem({name: "Incidents", id: "incidents",
        iconClass: "oj-navigationlist-item-icon demo-icon-font-24 demo-fire-icon-24"}),
        new NavDataItem({name: "Customers", id: "customers",
        iconClass: "oj-navigationlist-item-icon demo-icon-font-24 demo-people-icon-24"}),
        new NavDataItem({name: "Profile", id: "profile",
        iconClass: "oj-navigationlist-item-icon demo-icon-font-24 demo-person-icon-24"}),
        new NavDataItem({name: "About", id: "about",
        iconClass: "oj-navigationlist-item-icon demo-icon-font-24 demo-info-icon-24"})
      ];

      this.navDataProvider = new ArrayDataProvider(navData, {keyAttributes: "id"});

      // drawer setup
      // add a close listener so we can move focus back to the toggle button when the drawer closes
      let navDrawerElement: HTMLElement = document.getElementById("navDrawer") as HTMLElement;
      navDrawerElement.addEventListener("ojclose", this.onNavDrawerClose);
    }

    /*
      @waitForAnnouncement - set to true when the announcement is happening.
      If the nav-drawer is ON, it is reset to false in "ojclose" event handler of nav-drawer.
      If the nav-drawer is OFF, then the flag is reset here itthis in the timeout callback.
    */
    announcementHandler = (event: any): void => {
      this.waitForAnnouncement = true;
      setTimeout((): void => {
        this.message(event.detail.message);
        this.manner(event.detail.manner);
        if (!this.navDrawerOn) {
          this.waitForAnnouncement = false;
        }
      }, 200);
    }

    loadModule(): void {
      ko.computed((): void => {
        let name: string = this.router.moduleConfig.name();
        let viewPath: string = `views/${name}.html`;
        let modelPath: string = `viewModels/${name}`;
        let masterPromise: Promise<any> = Promise.all([
          ModuleElementUtils.createView({"viewPath": viewPath}),
          ModuleElementUtils.createViewModel({"viewModelPath": modelPath})
        ]);
        masterPromise.then((values) => {
            this.moduleConfig({"view": values[0],"viewModel": values[1].default});
          }
        );
      });
    }

    toggleDrawer = (): Promise<boolean> => {
      this.navDrawerOn = true;
      return OffcanvasUtils.toggle({selector: "#navDrawer", modality: "modal", content: "#pageContent"});
    }

    /*
      - If there is no aria-live announcement, bring focus to the nav-drawer button immediately.
      - If there is any aria-live announcement in progress, add timeout to bring focus to the nav-drawer button.
      - When the nav-drawer is ON and annoucement happens, then after nav-drawer closes reset "waitForAnnouncement" property to false.
    */
    onNavDrawerClose = (event: any): void => {
      this.navDrawerOn = false;

      let drawerToggleButton: HTMLElement = document.getElementById("drawerToggleButton") as HTMLElement;

      if ( !this.waitForAnnouncement ) {
        drawerToggleButton.focus();
        return;
      }

      setTimeout((): void => {
        drawerToggleButton.focus();
        this.waitForAnnouncement = false;
      }, 2500);
    }

    getHeaderModel(): HeaderModel {
      let currentState: RouterState = this.router.currentState() as RouterState;
      let pageTitle: string = currentState.label as string;
      let toggleDrawer: Function = this.toggleDrawer;
      let adjustContentPadding: Function = this.adjustContentPadding;
      return new HeaderModel( { pageTitle, toggleDrawer, adjustContentPadding } );
    }

    // method for adjusting the content area top/bottom paddings to avoid overlap with any fixed regions.
    // this method should be called whenever your fixed region height may change.  The application
    // can also adjust content paddings with css classes if the fixed region height is not changing between
    // views.
    adjustContentPadding(): void {
      let topElem: HTMLElement = document.getElementsByClassName("oj-applayout-fixed-top")[0] as HTMLElement;
      let contentElem: HTMLElement = document.getElementsByClassName("oj-applayout-content")[0] as HTMLElement;
      let bottomElem: HTMLElement = document.getElementsByClassName("oj-applayout-fixed-bottom")[0] as HTMLElement;

      if (topElem) {
        contentElem.style.paddingTop = `${topElem.offsetHeight}px`;
      }
      if (bottomElem) {
        contentElem.style.paddingBottom = `${bottomElem.offsetHeight}px`;
      }
      // add oj-complete marker class to signal that the content area can be unhidden.
      // see the override.css file to see when the content area is hidden.
      contentElem.classList.add("oj-complete");
    }
}

export default new RootViewModel();