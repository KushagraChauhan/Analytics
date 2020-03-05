/*
 * Your about ViewModel code goes here
 */
import * as ko from "knockout";
import rootViewModel from "../appController";
import * as ModuleElementUtils from "ojs/ojmodule-element-utils";
import * as AccUtils from "../accUtils";
import { ojModule } from "ojs/ojmodule-element";

class IncidentsViewModel {
  headerConfig: ko.Observable<ojModule["config"]>;

  constructor() {
    // header Config
    this.headerConfig = ko.observable({"view": [], "viewModel": null});

    ModuleElementUtils.createView({"viewPath": "views/header.html"}).then((view) => {
      this.headerConfig({"view": view, "viewModel": rootViewModel.getHeaderModel()});
    });
  }

  // below are a set of the ViewModel methods invoked by the oj-module component.
  // please reference the oj-module jsDoc for additional information.

  /**
   * Optional ViewModel method invoked after the View is inserted into the
   * document DOM.  The application can put logic that requires the DOM being
   * attached here.
   * This method might be called multiple times - after the View is created
   * and inserted into the DOM and after the View is reconnected
   * after being disconnected.
   */
  connected(): void {
    AccUtils.announce("Incidents page loaded.");
    document.title = "Incidents";
    // implement further logic if needed
  }

  /**
   * Optional ViewModel method invoked after the View is disconnected from the DOM.
   */
  disconnected(): void {
    // implement if needed
  }

  /**
   * Optional ViewModel method invoked after transition to the new View is complete.
   * That includes any possible animation between the old and the new View.
   */
  transitionCompleted(): void {
    // implement if needed
  }
}

export default IncidentsViewModel;
