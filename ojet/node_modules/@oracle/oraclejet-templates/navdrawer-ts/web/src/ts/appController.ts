import * as ko from "knockout";
import * as ModuleUtils from "ojs/ojmodule-element-utils";
import * as ResponsiveUtils from "ojs/ojresponsiveutils";
import * as ResponsiveKnockoutUtils from "ojs/ojresponsiveknockoututils";
import * as OffcanvasUtils from "ojs/ojoffcanvas";
import Router = require ("ojs/ojrouter");
import ArrayDataProvider = require("ojs/ojarraydataprovider");
import "ojs/ojknockout";
import "ojs/ojmodule-element";
import { ojNavigationList } from "ojs/ojnavigationlist";
import { ojModule } from "ojs/ojmodule-element";

class FooterLink {
  name: string;
  id: string;
  linkTarget: string;
  constructor( { name, id, linkTarget } : {
    name: string;
    id: string;
    linkTarget: string;
   }) {
    this.name = name;
    this.id = id;
    this.linkTarget = linkTarget;
  }
}

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

class RootViewModel {
  smScreen: ko.Observable<boolean>;
  mdScreen: ko.Observable<boolean>;
  router: Router;
  moduleConfig: ko.Observable<ojModule["config"]>;
  navDataSource: ojNavigationList<string, NavDataItem>["data"];
  drawerParams: {
    selector: string;
    content: string;
    edge?: "start" | "end" | "top" | "bottom";
    displayMode?: "push" | "overlay";
    autoDismiss?: "focusLoss" | "none";
    size?: string;
    modality?: "modal" | "modeless";
  };
  appName: ko.Observable<string>;
  userLogin: ko.Observable<string>;
  footerLinks: ko.ObservableArray<FooterLink>;

  constructor() {
    // media queries for repsonsive layouts
    let smQuery: string | null = ResponsiveUtils.getFrameworkQuery("sm-only");
    if (smQuery){
      this.smScreen = ResponsiveKnockoutUtils.createMediaQueryObservable(smQuery);
    }

    let mdQuery: string | null = ResponsiveUtils.getFrameworkQuery("md-up");
    if (mdQuery){
      this.mdScreen = ResponsiveKnockoutUtils.createMediaQueryObservable(mdQuery);
    }
    
    // router setup
    this.router = Router.rootInstance;
    this.router.configure({
      "dashboard": {label: "Dashboard", isDefault: true},
      "incidents": {label: "Incidents"},
      "customers": {label: "Customers"},
      "about": {label: "About"}
    });

    Router.defaults.urlAdapter = new Router.urlParamAdapter();

    // module config
    this.moduleConfig = ko.observable({"view": [], "viewModel": null});

    // navigation setup
    let navData: NavDataItem[] = [
      new NavDataItem({name: "Dashboard", id: "dashboard", iconClass: "oj-navigationlist-item-icon demo-icon-font-24 demo-chart-icon-24"}),
      new NavDataItem({name: "Incidents", id: "incidents", iconClass: "oj-navigationlist-item-icon demo-icon-font-24 demo-fire-icon-24"}),
      new NavDataItem({name: "Customers", id: "customers", iconClass: "oj-navigationlist-item-icon demo-icon-font-24 demo-people-icon-24"}),
      new NavDataItem({name: "About", id: "about", iconClass: "oj-navigationlist-item-icon demo-icon-font-24 demo-info-icon-24"})
    ];
    this.navDataSource = new ArrayDataProvider(navData, {idAttribute: "id"});

    // drawer

    this.drawerParams = {
      displayMode: "push",
      selector: "#navDrawer",
      content: "#pageContent"
    };

    // close offcanvas on medium and larger screens
    this.mdScreen.subscribe(() => {
      OffcanvasUtils.close(this.drawerParams);
    });

    // add a close listener so we can move focus back to the toggle button when the drawer closes
    let navDrawerElement: HTMLElement = document.querySelector("#navDrawer") as HTMLElement;
    navDrawerElement.addEventListener("ojclose", () => {
      let drawerToggleButtonElment: HTMLElement = document.querySelector("#drawerToggleButton") as HTMLElement;
      drawerToggleButtonElment.focus();
    });

    // header

    // application Name used in Branding Area
    this.appName = ko.observable("App Name");
    // user Info used in Global Navigation area

    this.userLogin = ko.observable("john.hancock@oracle.com");
    // footer
    this.footerLinks = ko.observableArray([
      new FooterLink({ name: "About Oracle", id: "aboutOracle", linkTarget: "http://www.oracle.com/us/corporate/index.html#menu-about" }),
      new FooterLink({ name: "Contact Us", id: "contactUs", linkTarget: "http://www.oracle.com/us/corporate/contact/index.html" }),
      new FooterLink({ name: "Legal Notices", id: "legalNotices", linkTarget: "http://www.oracle.com/us/legal/index.html" }),
      new FooterLink({ name: "Terms Of Use", id: "termsOfUse", linkTarget: "http://www.oracle.com/us/legal/terms/index.html" }),
      new FooterLink({ name: "Your Privacy Rights", id: "yourPrivacyRights", linkTarget: "http://www.oracle.com/us/legal/privacy/index.html" })
    ]);
  }

  // called by navigation drawer toggle button and after selection of nav drawer item
  toggleDrawer = (): Promise<boolean> => {
    return OffcanvasUtils.toggle(this.drawerParams);
  }

  loadModule(): void {
    ko.computed(() => {
      let name: string = this.router.moduleConfig.name();
      let viewPath: string = `views/${name}.html`;
      let modelPath: string = `viewModels/${name}`;
      let masterPromise: Promise<any> = Promise.all([
        ModuleUtils.createView({"viewPath": viewPath}),
        ModuleUtils.createViewModel({"viewModelPath": modelPath})
      ]);
      masterPromise.then((values) => {
          this.moduleConfig({"view": values[0],"viewModel": values[1].default});
      });
    });
  }
}

export default new RootViewModel();