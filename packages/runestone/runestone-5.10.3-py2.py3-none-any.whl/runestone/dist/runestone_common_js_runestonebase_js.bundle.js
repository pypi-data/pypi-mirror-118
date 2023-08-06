(self["webpackChunkWebComponents"] = self["webpackChunkWebComponents"] || []).push([["runestone_common_js_runestonebase_js"],{

/***/ 2568:
/*!**********************************************!*\
  !*** ./runestone/common/js/runestonebase.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ RunestoneBase)
/* harmony export */ });
/* harmony import */ var _bookfuncs_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./bookfuncs.js */ 21294);
/* ********************************
 * |docname| - Runestone Base Class
 * ********************************
 * All runestone components should inherit from RunestoneBase. In addition all runestone components should do the following things:
 *
 * 1.   Ensure that they are wrapped in a div with the class runestone
 * 2.   Write their source AND their generated html to the database if the database is configured
 * 3.   Properly save and restore their answers using the checkServer mechanism in this base class. Each component must provide an implementation of:
 *
 *      -    checkLocalStorage
 *      -    setLocalStorage
 *      -    restoreAnswers
 *      -    disableInteraction
 *
 * 4.   provide a Selenium based unit test
 */


//import "./../styles/runestone-custom-sphinx-bootstrap.css";

class RunestoneBase {
    constructor(opts) {
        this.component_ready_promise = new Promise(resolve => this._component_ready_resolve_fn = resolve)
        this.optional = false;
        if (typeof window.allComponents === "undefined") {
            window.allComponents = [];
        }
        window.allComponents.push(this);
        if (opts) {
            this.sid = opts.sid;
            this.graderactive = opts.graderactive;
            this.showfeedback = true;
            if (opts.timed) {
                this.isTimed = true;
            }
            if (opts.enforceDeadline) {
                this.deadline = opts.deadline;
            }
            if ($(opts.orig).data("optional")) {
                this.optional = true;
            } else {
                this.optional = false;
            }
            if (opts.selector_id) {
                this.selector_id = opts.selector_id;
            }
            if (typeof opts.assessmentTaken !== "undefined") {
                this.assessmentTaken = opts.assessmentTaken;
            } else {
                // default to true as this opt is only provided from a timedAssessment
                this.assessmentTaken = true;
            }
            // This is for the selectquestion points
            // If a selectquestion is part of a timed exam it will get
            // the timedWrapper options.
            if (typeof opts.timedWrapper !== "undefined") {
                this.timedWrapper = opts.timedWrapper;
            } else {
                // However sometimes selectquestions
                // are used in regular assignments.  The hacky way to detect this
                // is to look for doAssignment in the URL and then grab
                // the assignment name from the heading.
                if (location.href.indexOf("doAssignment") >= 0) {
                    this.timedWrapper = $("h1#assignment_name").text()
                } else {
                    this.timedWrapper = null;
                }
            }
            if ($(opts.orig).data("question_label")) {
                this.question_label = $(opts.orig).data("question_label");
            }
        }
        this.jsonHeaders = new Headers({
            "Content-type": "application/json; charset=utf-8",
            Accept: "application/json",
        });
    }

    // .. _logBookEvent:
    //
    // logBookEvent
    // ------------
    // This function sends the provided ``eventInfo`` to the `hsblog endpoint` of the server. Awaiting this function returns either ``undefined`` (if Runestone services are not available) or the data returned by the server as a JavaScript object (already JSON-decoded).
    async logBookEvent(eventInfo) {
        if (this.graderactive) {
            return;
        }
        let post_return;
        eventInfo.course = eBookConfig.course;
        eventInfo.clientLoginStatus = eBookConfig.isLoggedIn;
        eventInfo.timezoneoffset = new Date().getTimezoneOffset() / 60;
        if (this.percent) {
            eventInfo.percent = this.percent;
        }
        if (eBookConfig.useRunestoneServices && eBookConfig.logLevel > 0) {
            post_return = this.postLogMessage(eventInfo)
        }
        if (!this.isTimed || eBookConfig.debug) {
            console.log("logging event " + JSON.stringify(eventInfo));
        }
        // When selectquestions are part of an assignment especially toggle questions
        // we need to count using the selector_id of the select question.
        // We  also need to log an event for that selector so that we will know
        // that interaction has taken place.  This is **independent** of how the
        // autograder will ultimately grade the question!
        if (this.selector_id) {
            eventInfo.div_id = this.selector_id.replace("-toggleSelectedQuestion", "");
            eventInfo.event = "selectquestion";
            eventInfo.act = "interaction"
            this.postLogMessage(eventInfo);
        }
        if (
            typeof _bookfuncs_js__WEBPACK_IMPORTED_MODULE_0__.pageProgressTracker.updateProgress === "function" &&
            eventInfo.act != "edit" &&
            this.optional == false
        ) {
            _bookfuncs_js__WEBPACK_IMPORTED_MODULE_0__.pageProgressTracker.updateProgress(eventInfo.div_id);
        }
        return post_return;
    }

    async postLogMessage(eventInfo) {
        var post_return;
        let request = new Request(eBookConfig.ajaxURL + "hsblog", {
            method: "POST",
            headers: this.jsonHeaders,
            body: JSON.stringify(eventInfo),
        });
        try {
            let response = await fetch(request);
            if (!response.ok) {
                throw new Error("Failed to save the log entry");
            }
            post_return = response.json();
        } catch (e) {
            if (this.isTimed) {
                alert(`Error: Your action was not saved! The error was ${e}`);
            }
            console.log(`Error: ${e}`);
        }
        return post_return;
    }
    // .. _logRunEvent:
    //
    // logRunEvent
    // -----------
    // This function sends the provided ``eventInfo`` to the `runlog endpoint`. When awaited, this function returns the data (decoded from JSON) the server sent back.
    async logRunEvent(eventInfo) {
        let post_promise = "done";
        if (this.graderactive) {
            return;
        }
        eventInfo.course = eBookConfig.course;
        eventInfo.clientLoginStatus = eBookConfig.isLoggedIn;
        eventInfo.timezoneoffset = new Date().getTimezoneOffset() / 60;
        if (this.forceSave || "to_save" in eventInfo === false) {
            eventInfo.save_code = "True";
        }
        if (eBookConfig.useRunestoneServices && eBookConfig.logLevel > 0) {
            let request = new Request(eBookConfig.ajaxURL + "runlog.json", {
                method: "POST",
                headers: this.jsonHeaders,
                body: JSON.stringify(eventInfo),
            });
            let response = await fetch(request);
            if (!response.ok) {
                throw new Error("Failed to log the run");
            }
            post_promise = await response.json();
        }
        if (!this.isTimed || eBookConfig.debug) {
            console.log("running " + JSON.stringify(eventInfo));
        }
        if (
            typeof _bookfuncs_js__WEBPACK_IMPORTED_MODULE_0__.pageProgressTracker.updateProgress === "function" &&
            this.optional == false
        ) {
            _bookfuncs_js__WEBPACK_IMPORTED_MODULE_0__.pageProgressTracker.updateProgress(eventInfo.div_id);
        }
        return post_promise;
    }
    /* Checking/loading from storage
    **WARNING:**  DO NOT `await` this function!
    This function, although async, does not explicitly resolve its promise by returning a value.  The reason for this is because it is called by the constructor for nearly every component.  In Javascript constructors cannot be async!

    One of the recommended ways to handle the async requirements from within a constructor is to use an attribute as a promise and resolve that attribute at the appropriate time.
    */
    async checkServer(
        // A string specifying the event name to use for querying the :ref:`getAssessResults` endpoint.
        eventInfo,
        // If true, this function will invoke ``indicate_component_ready()`` just before it returns. This is provided since most components are ready after this function completes its work.
        //
        // TODO: This defaults to false, to avoid causing problems with any components that haven't been updated and tested. After all Runestone components have been updated, default this to true and remove the extra parameter from most calls to this function.
        will_be_ready = false
    ) {
        // Check if the server has stored answer
        let self = this;
        this.checkServerComplete = new Promise(function (resolve, reject) {
            self.csresolver = resolve;
        });
        if (this.useRunestoneServices || this.graderactive) {
            let data = {};
            data.div_id = this.divid;
            data.course = eBookConfig.course;
            data.event = eventInfo;
            if (this.graderactive && this.deadline) {
                data.deadline = this.deadline;
                data.rawdeadline = this.rawdeadline;
                data.tzoff = this.tzoff;
            }
            if (this.sid) {
                data.sid = this.sid;
            }
            if (!eBookConfig.practice_mode && this.assessmentTaken) {
                let request = new Request(
                    eBookConfig.ajaxURL + "getAssessResults",
                    {
                        method: "POST",
                        body: JSON.stringify(data),
                        headers: this.jsonHeaders,
                    }
                );
                try {
                    let response = await fetch(request);
                    data = await response.json();
                    this.repopulateFromStorage(data);
                    this.csresolver("server");
                } catch (err) {
                    try {
                        this.checkLocalStorage();
                    } catch (err) {
                        console.log(err);
                    }
                }
            } else {
                this.loadData({});
                this.csresolver("not taken");
            }
        } else {
            this.checkLocalStorage(); // just go right to local storage
            this.csresolver("local");
        }

        if (will_be_ready) {
            this.indicate_component_ready();
        }
    }

    // This method assumes that ``this.componentDiv`` refers to the ``div`` containing the component, and that this component's ID is set.
    indicate_component_ready() {
        // Add a class to indicate the component is now ready.
        this.containerDiv.classList.add("runestone-component-ready");
        // Resolve the ``this.component_ready_promise``.
        this._component_ready_resolve_fn();
    }

    loadData(data) {
        // for most classes, loadData doesn't do anything. But for Parsons, and perhaps others in the future,
        // initialization can happen even when there's no history to be loaded
        return null;
    }

    /**
     * repopulateFromStorage is called after a successful API call is made to ``getAssessResults`` in
     * the checkServer method in this class
     *
     * ``restoreAnswers,`` ``setLocalStorage`` and ``checkLocalStorage`` are defined in the child classes.
     *
     * @param {*} data - a JSON object representing the data needed to restore a previous answer for a component
     * @param {*} status - the http status
     * @param {*} whatever - ignored
     */
    repopulateFromStorage(data) {
        // decide whether to use the server's answer (if there is one) or to load from storage
        if (data !== null && this.shouldUseServer(data)) {
            this.restoreAnswers(data);
            this.setLocalStorage(data);
        } else {
            this.checkLocalStorage();
        }
    }
    shouldUseServer(data) {
        // returns true if server data is more recent than local storage or if server storage is correct
        if (
            data.correct === "T" ||
            localStorage.length === 0 ||
            this.graderactive === true ||
            this.isTimed
        ) {
            return true;
        }
        let ex = localStorage.getItem(this.localStorageKey());
        if (ex === null) {
            return true;
        }
        let storedData;
        try {
            storedData = JSON.parse(ex);
        } catch (err) {
            // error while parsing; likely due to bad value stored in storage
            console.log(err.message);
            localStorage.removeItem(this.localStorageKey());
            // definitely don't want to use local storage here
            return true;
        }
        if (data.answer == storedData.answer) return true;
        let storageDate = new Date(storedData.timestamp);
        let serverDate = new Date(data.timestamp);
        return serverDate >= storageDate;
    }
    // Return the key which to be used when accessing local storage.
    localStorageKey() {
        return (
            eBookConfig.email +
            ":" +
            eBookConfig.course +
            ":" +
            this.divid +
            "-given"
        );
    }
    addCaption(elType) {
        //someElement.parentNode.insertBefore(newElement, someElement.nextSibling);
        if (!this.isTimed) {
            var capDiv = document.createElement("p");
            if (this.question_label) {
                this.caption = `Activity: ${this.question_label} ${this.caption}  <span class="runestone_caption_divid">(${this.divid})</span>`;
                $(capDiv).html(this.caption);
                $(capDiv).addClass(`${elType}_caption`);
            } else {
                $(capDiv).html(this.caption + " (" + this.divid + ")");
                $(capDiv).addClass(`${elType}_caption`);
                $(capDiv).addClass(`${elType}_caption_text`);
            }
            this.capDiv = capDiv;
            //this.outerDiv.parentNode.insertBefore(capDiv, this.outerDiv.nextSibling);
            this.containerDiv.appendChild(capDiv);
        }
    }

    hasUserActivity() {
        return this.isAnswered;
    }

    checkCurrentAnswer() {
        console.log(
            "Each component should provide an implementation of checkCurrentAnswer"
        );
    }

    async logCurrentAnswer() {
        console.log(
            "Each component should provide an implementation of logCurrentAnswer"
        );
    }
    renderFeedback() {
        console.log(
            "Each component should provide an implementation of renderFeedback"
        );
    }
    disableInteraction() {
        console.log(
            "Each component should provide an implementation of disableInteraction"
        );
    }

    toString() {
        return `${this.constructor.name}: ${this.divid}`
    }

    queueMathJax(component) {
        if (MathJax.version.substring(0, 1) === "2") {
            MathJax.Hub.Queue(["Typeset", MathJax.Hub, component]);
        } else {
            MathJax.typesetPromise([component])
        }
    }

}

window.RunestoneBase = RunestoneBase;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9XZWJDb21wb25lbnRzLy4vcnVuZXN0b25lL2NvbW1vbi9qcy9ydW5lc3RvbmViYXNlLmpzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRXFEO0FBQ3JEOztBQUVlO0FBQ2Y7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxpQkFBaUI7QUFDakI7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLDhDQUE4QztBQUM5QztBQUNBLFNBQVM7QUFDVDs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLG1CQUFtQiw2RUFBa0M7QUFDckQ7QUFDQTtBQUNBO0FBQ0EsWUFBWSw2RUFBa0M7QUFDOUM7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFNBQVM7QUFDVDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxTQUFTO0FBQ1Q7QUFDQSx5RUFBeUUsRUFBRTtBQUMzRTtBQUNBLGtDQUFrQyxFQUFFO0FBQ3BDO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLG1CQUFtQiw2RUFBa0M7QUFDckQ7QUFDQTtBQUNBLFlBQVksNkVBQWtDO0FBQzlDO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsU0FBUztBQUNUO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLGlCQUFpQjtBQUNqQjtBQUNBO0FBQ0EscUJBQXFCO0FBQ3JCO0FBQ0E7QUFDQTtBQUNBLGFBQWE7QUFDYixnQ0FBZ0M7QUFDaEM7QUFDQTtBQUNBLFNBQVM7QUFDVCxxQ0FBcUM7QUFDckM7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLGVBQWUsRUFBRTtBQUNqQixlQUFlLEVBQUU7QUFDakIsZUFBZSxFQUFFO0FBQ2pCO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFNBQVM7QUFDVDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsU0FBUztBQUNULG1DQUFtQztBQUNuQztBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsNENBQTRDLG9CQUFvQixHQUFHLGFBQWEsMkNBQTJDLFdBQVc7QUFDdEk7QUFDQSxzQ0FBc0MsT0FBTztBQUM3QyxhQUFhO0FBQ2I7QUFDQSxzQ0FBc0MsT0FBTztBQUM3QyxzQ0FBc0MsT0FBTztBQUM3QztBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0Esa0JBQWtCLHNCQUFzQixJQUFJLFdBQVc7QUFDdkQ7O0FBRUE7QUFDQTtBQUNBO0FBQ0EsU0FBUztBQUNUO0FBQ0E7QUFDQTs7QUFFQTs7QUFFQSIsImZpbGUiOiJydW5lc3RvbmVfY29tbW9uX2pzX3J1bmVzdG9uZWJhc2VfanMuYnVuZGxlLmpzP3Y9MmJhNGY4M2JhOGVhODc0ODg5MmMiLCJzb3VyY2VzQ29udGVudCI6WyIvKiAqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKlxuICogfGRvY25hbWV8IC0gUnVuZXN0b25lIEJhc2UgQ2xhc3NcbiAqICoqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqXG4gKiBBbGwgcnVuZXN0b25lIGNvbXBvbmVudHMgc2hvdWxkIGluaGVyaXQgZnJvbSBSdW5lc3RvbmVCYXNlLiBJbiBhZGRpdGlvbiBhbGwgcnVuZXN0b25lIGNvbXBvbmVudHMgc2hvdWxkIGRvIHRoZSBmb2xsb3dpbmcgdGhpbmdzOlxuICpcbiAqIDEuICAgRW5zdXJlIHRoYXQgdGhleSBhcmUgd3JhcHBlZCBpbiBhIGRpdiB3aXRoIHRoZSBjbGFzcyBydW5lc3RvbmVcbiAqIDIuICAgV3JpdGUgdGhlaXIgc291cmNlIEFORCB0aGVpciBnZW5lcmF0ZWQgaHRtbCB0byB0aGUgZGF0YWJhc2UgaWYgdGhlIGRhdGFiYXNlIGlzIGNvbmZpZ3VyZWRcbiAqIDMuICAgUHJvcGVybHkgc2F2ZSBhbmQgcmVzdG9yZSB0aGVpciBhbnN3ZXJzIHVzaW5nIHRoZSBjaGVja1NlcnZlciBtZWNoYW5pc20gaW4gdGhpcyBiYXNlIGNsYXNzLiBFYWNoIGNvbXBvbmVudCBtdXN0IHByb3ZpZGUgYW4gaW1wbGVtZW50YXRpb24gb2Y6XG4gKlxuICogICAgICAtICAgIGNoZWNrTG9jYWxTdG9yYWdlXG4gKiAgICAgIC0gICAgc2V0TG9jYWxTdG9yYWdlXG4gKiAgICAgIC0gICAgcmVzdG9yZUFuc3dlcnNcbiAqICAgICAgLSAgICBkaXNhYmxlSW50ZXJhY3Rpb25cbiAqXG4gKiA0LiAgIHByb3ZpZGUgYSBTZWxlbml1bSBiYXNlZCB1bml0IHRlc3RcbiAqL1xuXG5pbXBvcnQgeyBwYWdlUHJvZ3Jlc3NUcmFja2VyIH0gZnJvbSBcIi4vYm9va2Z1bmNzLmpzXCI7XG4vL2ltcG9ydCBcIi4vLi4vc3R5bGVzL3J1bmVzdG9uZS1jdXN0b20tc3BoaW54LWJvb3RzdHJhcC5jc3NcIjtcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgUnVuZXN0b25lQmFzZSB7XG4gICAgY29uc3RydWN0b3Iob3B0cykge1xuICAgICAgICB0aGlzLmNvbXBvbmVudF9yZWFkeV9wcm9taXNlID0gbmV3IFByb21pc2UocmVzb2x2ZSA9PiB0aGlzLl9jb21wb25lbnRfcmVhZHlfcmVzb2x2ZV9mbiA9IHJlc29sdmUpXG4gICAgICAgIHRoaXMub3B0aW9uYWwgPSBmYWxzZTtcbiAgICAgICAgaWYgKHR5cGVvZiB3aW5kb3cuYWxsQ29tcG9uZW50cyA9PT0gXCJ1bmRlZmluZWRcIikge1xuICAgICAgICAgICAgd2luZG93LmFsbENvbXBvbmVudHMgPSBbXTtcbiAgICAgICAgfVxuICAgICAgICB3aW5kb3cuYWxsQ29tcG9uZW50cy5wdXNoKHRoaXMpO1xuICAgICAgICBpZiAob3B0cykge1xuICAgICAgICAgICAgdGhpcy5zaWQgPSBvcHRzLnNpZDtcbiAgICAgICAgICAgIHRoaXMuZ3JhZGVyYWN0aXZlID0gb3B0cy5ncmFkZXJhY3RpdmU7XG4gICAgICAgICAgICB0aGlzLnNob3dmZWVkYmFjayA9IHRydWU7XG4gICAgICAgICAgICBpZiAob3B0cy50aW1lZCkge1xuICAgICAgICAgICAgICAgIHRoaXMuaXNUaW1lZCA9IHRydWU7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICBpZiAob3B0cy5lbmZvcmNlRGVhZGxpbmUpIHtcbiAgICAgICAgICAgICAgICB0aGlzLmRlYWRsaW5lID0gb3B0cy5kZWFkbGluZTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIGlmICgkKG9wdHMub3JpZykuZGF0YShcIm9wdGlvbmFsXCIpKSB7XG4gICAgICAgICAgICAgICAgdGhpcy5vcHRpb25hbCA9IHRydWU7XG4gICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgIHRoaXMub3B0aW9uYWwgPSBmYWxzZTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIGlmIChvcHRzLnNlbGVjdG9yX2lkKSB7XG4gICAgICAgICAgICAgICAgdGhpcy5zZWxlY3Rvcl9pZCA9IG9wdHMuc2VsZWN0b3JfaWQ7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICBpZiAodHlwZW9mIG9wdHMuYXNzZXNzbWVudFRha2VuICE9PSBcInVuZGVmaW5lZFwiKSB7XG4gICAgICAgICAgICAgICAgdGhpcy5hc3Nlc3NtZW50VGFrZW4gPSBvcHRzLmFzc2Vzc21lbnRUYWtlbjtcbiAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgLy8gZGVmYXVsdCB0byB0cnVlIGFzIHRoaXMgb3B0IGlzIG9ubHkgcHJvdmlkZWQgZnJvbSBhIHRpbWVkQXNzZXNzbWVudFxuICAgICAgICAgICAgICAgIHRoaXMuYXNzZXNzbWVudFRha2VuID0gdHJ1ZTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIC8vIFRoaXMgaXMgZm9yIHRoZSBzZWxlY3RxdWVzdGlvbiBwb2ludHNcbiAgICAgICAgICAgIC8vIElmIGEgc2VsZWN0cXVlc3Rpb24gaXMgcGFydCBvZiBhIHRpbWVkIGV4YW0gaXQgd2lsbCBnZXRcbiAgICAgICAgICAgIC8vIHRoZSB0aW1lZFdyYXBwZXIgb3B0aW9ucy5cbiAgICAgICAgICAgIGlmICh0eXBlb2Ygb3B0cy50aW1lZFdyYXBwZXIgIT09IFwidW5kZWZpbmVkXCIpIHtcbiAgICAgICAgICAgICAgICB0aGlzLnRpbWVkV3JhcHBlciA9IG9wdHMudGltZWRXcmFwcGVyO1xuICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICAvLyBIb3dldmVyIHNvbWV0aW1lcyBzZWxlY3RxdWVzdGlvbnNcbiAgICAgICAgICAgICAgICAvLyBhcmUgdXNlZCBpbiByZWd1bGFyIGFzc2lnbm1lbnRzLiAgVGhlIGhhY2t5IHdheSB0byBkZXRlY3QgdGhpc1xuICAgICAgICAgICAgICAgIC8vIGlzIHRvIGxvb2sgZm9yIGRvQXNzaWdubWVudCBpbiB0aGUgVVJMIGFuZCB0aGVuIGdyYWJcbiAgICAgICAgICAgICAgICAvLyB0aGUgYXNzaWdubWVudCBuYW1lIGZyb20gdGhlIGhlYWRpbmcuXG4gICAgICAgICAgICAgICAgaWYgKGxvY2F0aW9uLmhyZWYuaW5kZXhPZihcImRvQXNzaWdubWVudFwiKSA+PSAwKSB7XG4gICAgICAgICAgICAgICAgICAgIHRoaXMudGltZWRXcmFwcGVyID0gJChcImgxI2Fzc2lnbm1lbnRfbmFtZVwiKS50ZXh0KClcbiAgICAgICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgICAgICB0aGlzLnRpbWVkV3JhcHBlciA9IG51bGw7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfVxuICAgICAgICAgICAgaWYgKCQob3B0cy5vcmlnKS5kYXRhKFwicXVlc3Rpb25fbGFiZWxcIikpIHtcbiAgICAgICAgICAgICAgICB0aGlzLnF1ZXN0aW9uX2xhYmVsID0gJChvcHRzLm9yaWcpLmRhdGEoXCJxdWVzdGlvbl9sYWJlbFwiKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgICB0aGlzLmpzb25IZWFkZXJzID0gbmV3IEhlYWRlcnMoe1xuICAgICAgICAgICAgXCJDb250ZW50LXR5cGVcIjogXCJhcHBsaWNhdGlvbi9qc29uOyBjaGFyc2V0PXV0Zi04XCIsXG4gICAgICAgICAgICBBY2NlcHQ6IFwiYXBwbGljYXRpb24vanNvblwiLFxuICAgICAgICB9KTtcbiAgICB9XG5cbiAgICAvLyAuLiBfbG9nQm9va0V2ZW50OlxuICAgIC8vXG4gICAgLy8gbG9nQm9va0V2ZW50XG4gICAgLy8gLS0tLS0tLS0tLS0tXG4gICAgLy8gVGhpcyBmdW5jdGlvbiBzZW5kcyB0aGUgcHJvdmlkZWQgYGBldmVudEluZm9gYCB0byB0aGUgYGhzYmxvZyBlbmRwb2ludGAgb2YgdGhlIHNlcnZlci4gQXdhaXRpbmcgdGhpcyBmdW5jdGlvbiByZXR1cm5zIGVpdGhlciBgYHVuZGVmaW5lZGBgIChpZiBSdW5lc3RvbmUgc2VydmljZXMgYXJlIG5vdCBhdmFpbGFibGUpIG9yIHRoZSBkYXRhIHJldHVybmVkIGJ5IHRoZSBzZXJ2ZXIgYXMgYSBKYXZhU2NyaXB0IG9iamVjdCAoYWxyZWFkeSBKU09OLWRlY29kZWQpLlxuICAgIGFzeW5jIGxvZ0Jvb2tFdmVudChldmVudEluZm8pIHtcbiAgICAgICAgaWYgKHRoaXMuZ3JhZGVyYWN0aXZlKSB7XG4gICAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cbiAgICAgICAgbGV0IHBvc3RfcmV0dXJuO1xuICAgICAgICBldmVudEluZm8uY291cnNlID0gZUJvb2tDb25maWcuY291cnNlO1xuICAgICAgICBldmVudEluZm8uY2xpZW50TG9naW5TdGF0dXMgPSBlQm9va0NvbmZpZy5pc0xvZ2dlZEluO1xuICAgICAgICBldmVudEluZm8udGltZXpvbmVvZmZzZXQgPSBuZXcgRGF0ZSgpLmdldFRpbWV6b25lT2Zmc2V0KCkgLyA2MDtcbiAgICAgICAgaWYgKHRoaXMucGVyY2VudCkge1xuICAgICAgICAgICAgZXZlbnRJbmZvLnBlcmNlbnQgPSB0aGlzLnBlcmNlbnQ7XG4gICAgICAgIH1cbiAgICAgICAgaWYgKGVCb29rQ29uZmlnLnVzZVJ1bmVzdG9uZVNlcnZpY2VzICYmIGVCb29rQ29uZmlnLmxvZ0xldmVsID4gMCkge1xuICAgICAgICAgICAgcG9zdF9yZXR1cm4gPSB0aGlzLnBvc3RMb2dNZXNzYWdlKGV2ZW50SW5mbylcbiAgICAgICAgfVxuICAgICAgICBpZiAoIXRoaXMuaXNUaW1lZCB8fCBlQm9va0NvbmZpZy5kZWJ1Zykge1xuICAgICAgICAgICAgY29uc29sZS5sb2coXCJsb2dnaW5nIGV2ZW50IFwiICsgSlNPTi5zdHJpbmdpZnkoZXZlbnRJbmZvKSk7XG4gICAgICAgIH1cbiAgICAgICAgLy8gV2hlbiBzZWxlY3RxdWVzdGlvbnMgYXJlIHBhcnQgb2YgYW4gYXNzaWdubWVudCBlc3BlY2lhbGx5IHRvZ2dsZSBxdWVzdGlvbnNcbiAgICAgICAgLy8gd2UgbmVlZCB0byBjb3VudCB1c2luZyB0aGUgc2VsZWN0b3JfaWQgb2YgdGhlIHNlbGVjdCBxdWVzdGlvbi5cbiAgICAgICAgLy8gV2UgIGFsc28gbmVlZCB0byBsb2cgYW4gZXZlbnQgZm9yIHRoYXQgc2VsZWN0b3Igc28gdGhhdCB3ZSB3aWxsIGtub3dcbiAgICAgICAgLy8gdGhhdCBpbnRlcmFjdGlvbiBoYXMgdGFrZW4gcGxhY2UuICBUaGlzIGlzICoqaW5kZXBlbmRlbnQqKiBvZiBob3cgdGhlXG4gICAgICAgIC8vIGF1dG9ncmFkZXIgd2lsbCB1bHRpbWF0ZWx5IGdyYWRlIHRoZSBxdWVzdGlvbiFcbiAgICAgICAgaWYgKHRoaXMuc2VsZWN0b3JfaWQpIHtcbiAgICAgICAgICAgIGV2ZW50SW5mby5kaXZfaWQgPSB0aGlzLnNlbGVjdG9yX2lkLnJlcGxhY2UoXCItdG9nZ2xlU2VsZWN0ZWRRdWVzdGlvblwiLCBcIlwiKTtcbiAgICAgICAgICAgIGV2ZW50SW5mby5ldmVudCA9IFwic2VsZWN0cXVlc3Rpb25cIjtcbiAgICAgICAgICAgIGV2ZW50SW5mby5hY3QgPSBcImludGVyYWN0aW9uXCJcbiAgICAgICAgICAgIHRoaXMucG9zdExvZ01lc3NhZ2UoZXZlbnRJbmZvKTtcbiAgICAgICAgfVxuICAgICAgICBpZiAoXG4gICAgICAgICAgICB0eXBlb2YgcGFnZVByb2dyZXNzVHJhY2tlci51cGRhdGVQcm9ncmVzcyA9PT0gXCJmdW5jdGlvblwiICYmXG4gICAgICAgICAgICBldmVudEluZm8uYWN0ICE9IFwiZWRpdFwiICYmXG4gICAgICAgICAgICB0aGlzLm9wdGlvbmFsID09IGZhbHNlXG4gICAgICAgICkge1xuICAgICAgICAgICAgcGFnZVByb2dyZXNzVHJhY2tlci51cGRhdGVQcm9ncmVzcyhldmVudEluZm8uZGl2X2lkKTtcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gcG9zdF9yZXR1cm47XG4gICAgfVxuXG4gICAgYXN5bmMgcG9zdExvZ01lc3NhZ2UoZXZlbnRJbmZvKSB7XG4gICAgICAgIHZhciBwb3N0X3JldHVybjtcbiAgICAgICAgbGV0IHJlcXVlc3QgPSBuZXcgUmVxdWVzdChlQm9va0NvbmZpZy5hamF4VVJMICsgXCJoc2Jsb2dcIiwge1xuICAgICAgICAgICAgbWV0aG9kOiBcIlBPU1RcIixcbiAgICAgICAgICAgIGhlYWRlcnM6IHRoaXMuanNvbkhlYWRlcnMsXG4gICAgICAgICAgICBib2R5OiBKU09OLnN0cmluZ2lmeShldmVudEluZm8pLFxuICAgICAgICB9KTtcbiAgICAgICAgdHJ5IHtcbiAgICAgICAgICAgIGxldCByZXNwb25zZSA9IGF3YWl0IGZldGNoKHJlcXVlc3QpO1xuICAgICAgICAgICAgaWYgKCFyZXNwb25zZS5vaykge1xuICAgICAgICAgICAgICAgIHRocm93IG5ldyBFcnJvcihcIkZhaWxlZCB0byBzYXZlIHRoZSBsb2cgZW50cnlcIik7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICBwb3N0X3JldHVybiA9IHJlc3BvbnNlLmpzb24oKTtcbiAgICAgICAgfSBjYXRjaCAoZSkge1xuICAgICAgICAgICAgaWYgKHRoaXMuaXNUaW1lZCkge1xuICAgICAgICAgICAgICAgIGFsZXJ0KGBFcnJvcjogWW91ciBhY3Rpb24gd2FzIG5vdCBzYXZlZCEgVGhlIGVycm9yIHdhcyAke2V9YCk7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICBjb25zb2xlLmxvZyhgRXJyb3I6ICR7ZX1gKTtcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gcG9zdF9yZXR1cm47XG4gICAgfVxuICAgIC8vIC4uIF9sb2dSdW5FdmVudDpcbiAgICAvL1xuICAgIC8vIGxvZ1J1bkV2ZW50XG4gICAgLy8gLS0tLS0tLS0tLS1cbiAgICAvLyBUaGlzIGZ1bmN0aW9uIHNlbmRzIHRoZSBwcm92aWRlZCBgYGV2ZW50SW5mb2BgIHRvIHRoZSBgcnVubG9nIGVuZHBvaW50YC4gV2hlbiBhd2FpdGVkLCB0aGlzIGZ1bmN0aW9uIHJldHVybnMgdGhlIGRhdGEgKGRlY29kZWQgZnJvbSBKU09OKSB0aGUgc2VydmVyIHNlbnQgYmFjay5cbiAgICBhc3luYyBsb2dSdW5FdmVudChldmVudEluZm8pIHtcbiAgICAgICAgbGV0IHBvc3RfcHJvbWlzZSA9IFwiZG9uZVwiO1xuICAgICAgICBpZiAodGhpcy5ncmFkZXJhY3RpdmUpIHtcbiAgICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuICAgICAgICBldmVudEluZm8uY291cnNlID0gZUJvb2tDb25maWcuY291cnNlO1xuICAgICAgICBldmVudEluZm8uY2xpZW50TG9naW5TdGF0dXMgPSBlQm9va0NvbmZpZy5pc0xvZ2dlZEluO1xuICAgICAgICBldmVudEluZm8udGltZXpvbmVvZmZzZXQgPSBuZXcgRGF0ZSgpLmdldFRpbWV6b25lT2Zmc2V0KCkgLyA2MDtcbiAgICAgICAgaWYgKHRoaXMuZm9yY2VTYXZlIHx8IFwidG9fc2F2ZVwiIGluIGV2ZW50SW5mbyA9PT0gZmFsc2UpIHtcbiAgICAgICAgICAgIGV2ZW50SW5mby5zYXZlX2NvZGUgPSBcIlRydWVcIjtcbiAgICAgICAgfVxuICAgICAgICBpZiAoZUJvb2tDb25maWcudXNlUnVuZXN0b25lU2VydmljZXMgJiYgZUJvb2tDb25maWcubG9nTGV2ZWwgPiAwKSB7XG4gICAgICAgICAgICBsZXQgcmVxdWVzdCA9IG5ldyBSZXF1ZXN0KGVCb29rQ29uZmlnLmFqYXhVUkwgKyBcInJ1bmxvZy5qc29uXCIsIHtcbiAgICAgICAgICAgICAgICBtZXRob2Q6IFwiUE9TVFwiLFxuICAgICAgICAgICAgICAgIGhlYWRlcnM6IHRoaXMuanNvbkhlYWRlcnMsXG4gICAgICAgICAgICAgICAgYm9keTogSlNPTi5zdHJpbmdpZnkoZXZlbnRJbmZvKSxcbiAgICAgICAgICAgIH0pO1xuICAgICAgICAgICAgbGV0IHJlc3BvbnNlID0gYXdhaXQgZmV0Y2gocmVxdWVzdCk7XG4gICAgICAgICAgICBpZiAoIXJlc3BvbnNlLm9rKSB7XG4gICAgICAgICAgICAgICAgdGhyb3cgbmV3IEVycm9yKFwiRmFpbGVkIHRvIGxvZyB0aGUgcnVuXCIpO1xuICAgICAgICAgICAgfVxuICAgICAgICAgICAgcG9zdF9wcm9taXNlID0gYXdhaXQgcmVzcG9uc2UuanNvbigpO1xuICAgICAgICB9XG4gICAgICAgIGlmICghdGhpcy5pc1RpbWVkIHx8IGVCb29rQ29uZmlnLmRlYnVnKSB7XG4gICAgICAgICAgICBjb25zb2xlLmxvZyhcInJ1bm5pbmcgXCIgKyBKU09OLnN0cmluZ2lmeShldmVudEluZm8pKTtcbiAgICAgICAgfVxuICAgICAgICBpZiAoXG4gICAgICAgICAgICB0eXBlb2YgcGFnZVByb2dyZXNzVHJhY2tlci51cGRhdGVQcm9ncmVzcyA9PT0gXCJmdW5jdGlvblwiICYmXG4gICAgICAgICAgICB0aGlzLm9wdGlvbmFsID09IGZhbHNlXG4gICAgICAgICkge1xuICAgICAgICAgICAgcGFnZVByb2dyZXNzVHJhY2tlci51cGRhdGVQcm9ncmVzcyhldmVudEluZm8uZGl2X2lkKTtcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gcG9zdF9wcm9taXNlO1xuICAgIH1cbiAgICAvKiBDaGVja2luZy9sb2FkaW5nIGZyb20gc3RvcmFnZVxuICAgICoqV0FSTklORzoqKiAgRE8gTk9UIGBhd2FpdGAgdGhpcyBmdW5jdGlvbiFcbiAgICBUaGlzIGZ1bmN0aW9uLCBhbHRob3VnaCBhc3luYywgZG9lcyBub3QgZXhwbGljaXRseSByZXNvbHZlIGl0cyBwcm9taXNlIGJ5IHJldHVybmluZyBhIHZhbHVlLiAgVGhlIHJlYXNvbiBmb3IgdGhpcyBpcyBiZWNhdXNlIGl0IGlzIGNhbGxlZCBieSB0aGUgY29uc3RydWN0b3IgZm9yIG5lYXJseSBldmVyeSBjb21wb25lbnQuICBJbiBKYXZhc2NyaXB0IGNvbnN0cnVjdG9ycyBjYW5ub3QgYmUgYXN5bmMhXG5cbiAgICBPbmUgb2YgdGhlIHJlY29tbWVuZGVkIHdheXMgdG8gaGFuZGxlIHRoZSBhc3luYyByZXF1aXJlbWVudHMgZnJvbSB3aXRoaW4gYSBjb25zdHJ1Y3RvciBpcyB0byB1c2UgYW4gYXR0cmlidXRlIGFzIGEgcHJvbWlzZSBhbmQgcmVzb2x2ZSB0aGF0IGF0dHJpYnV0ZSBhdCB0aGUgYXBwcm9wcmlhdGUgdGltZS5cbiAgICAqL1xuICAgIGFzeW5jIGNoZWNrU2VydmVyKFxuICAgICAgICAvLyBBIHN0cmluZyBzcGVjaWZ5aW5nIHRoZSBldmVudCBuYW1lIHRvIHVzZSBmb3IgcXVlcnlpbmcgdGhlIDpyZWY6YGdldEFzc2Vzc1Jlc3VsdHNgIGVuZHBvaW50LlxuICAgICAgICBldmVudEluZm8sXG4gICAgICAgIC8vIElmIHRydWUsIHRoaXMgZnVuY3Rpb24gd2lsbCBpbnZva2UgYGBpbmRpY2F0ZV9jb21wb25lbnRfcmVhZHkoKWBgIGp1c3QgYmVmb3JlIGl0IHJldHVybnMuIFRoaXMgaXMgcHJvdmlkZWQgc2luY2UgbW9zdCBjb21wb25lbnRzIGFyZSByZWFkeSBhZnRlciB0aGlzIGZ1bmN0aW9uIGNvbXBsZXRlcyBpdHMgd29yay5cbiAgICAgICAgLy9cbiAgICAgICAgLy8gVE9ETzogVGhpcyBkZWZhdWx0cyB0byBmYWxzZSwgdG8gYXZvaWQgY2F1c2luZyBwcm9ibGVtcyB3aXRoIGFueSBjb21wb25lbnRzIHRoYXQgaGF2ZW4ndCBiZWVuIHVwZGF0ZWQgYW5kIHRlc3RlZC4gQWZ0ZXIgYWxsIFJ1bmVzdG9uZSBjb21wb25lbnRzIGhhdmUgYmVlbiB1cGRhdGVkLCBkZWZhdWx0IHRoaXMgdG8gdHJ1ZSBhbmQgcmVtb3ZlIHRoZSBleHRyYSBwYXJhbWV0ZXIgZnJvbSBtb3N0IGNhbGxzIHRvIHRoaXMgZnVuY3Rpb24uXG4gICAgICAgIHdpbGxfYmVfcmVhZHkgPSBmYWxzZVxuICAgICkge1xuICAgICAgICAvLyBDaGVjayBpZiB0aGUgc2VydmVyIGhhcyBzdG9yZWQgYW5zd2VyXG4gICAgICAgIGxldCBzZWxmID0gdGhpcztcbiAgICAgICAgdGhpcy5jaGVja1NlcnZlckNvbXBsZXRlID0gbmV3IFByb21pc2UoZnVuY3Rpb24gKHJlc29sdmUsIHJlamVjdCkge1xuICAgICAgICAgICAgc2VsZi5jc3Jlc29sdmVyID0gcmVzb2x2ZTtcbiAgICAgICAgfSk7XG4gICAgICAgIGlmICh0aGlzLnVzZVJ1bmVzdG9uZVNlcnZpY2VzIHx8IHRoaXMuZ3JhZGVyYWN0aXZlKSB7XG4gICAgICAgICAgICBsZXQgZGF0YSA9IHt9O1xuICAgICAgICAgICAgZGF0YS5kaXZfaWQgPSB0aGlzLmRpdmlkO1xuICAgICAgICAgICAgZGF0YS5jb3Vyc2UgPSBlQm9va0NvbmZpZy5jb3Vyc2U7XG4gICAgICAgICAgICBkYXRhLmV2ZW50ID0gZXZlbnRJbmZvO1xuICAgICAgICAgICAgaWYgKHRoaXMuZ3JhZGVyYWN0aXZlICYmIHRoaXMuZGVhZGxpbmUpIHtcbiAgICAgICAgICAgICAgICBkYXRhLmRlYWRsaW5lID0gdGhpcy5kZWFkbGluZTtcbiAgICAgICAgICAgICAgICBkYXRhLnJhd2RlYWRsaW5lID0gdGhpcy5yYXdkZWFkbGluZTtcbiAgICAgICAgICAgICAgICBkYXRhLnR6b2ZmID0gdGhpcy50em9mZjtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIGlmICh0aGlzLnNpZCkge1xuICAgICAgICAgICAgICAgIGRhdGEuc2lkID0gdGhpcy5zaWQ7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICBpZiAoIWVCb29rQ29uZmlnLnByYWN0aWNlX21vZGUgJiYgdGhpcy5hc3Nlc3NtZW50VGFrZW4pIHtcbiAgICAgICAgICAgICAgICBsZXQgcmVxdWVzdCA9IG5ldyBSZXF1ZXN0KFxuICAgICAgICAgICAgICAgICAgICBlQm9va0NvbmZpZy5hamF4VVJMICsgXCJnZXRBc3Nlc3NSZXN1bHRzXCIsXG4gICAgICAgICAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgICAgICAgICAgIG1ldGhvZDogXCJQT1NUXCIsXG4gICAgICAgICAgICAgICAgICAgICAgICBib2R5OiBKU09OLnN0cmluZ2lmeShkYXRhKSxcbiAgICAgICAgICAgICAgICAgICAgICAgIGhlYWRlcnM6IHRoaXMuanNvbkhlYWRlcnMsXG4gICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgICAgIHRyeSB7XG4gICAgICAgICAgICAgICAgICAgIGxldCByZXNwb25zZSA9IGF3YWl0IGZldGNoKHJlcXVlc3QpO1xuICAgICAgICAgICAgICAgICAgICBkYXRhID0gYXdhaXQgcmVzcG9uc2UuanNvbigpO1xuICAgICAgICAgICAgICAgICAgICB0aGlzLnJlcG9wdWxhdGVGcm9tU3RvcmFnZShkYXRhKTtcbiAgICAgICAgICAgICAgICAgICAgdGhpcy5jc3Jlc29sdmVyKFwic2VydmVyXCIpO1xuICAgICAgICAgICAgICAgIH0gY2F0Y2ggKGVycikge1xuICAgICAgICAgICAgICAgICAgICB0cnkge1xuICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy5jaGVja0xvY2FsU3RvcmFnZSgpO1xuICAgICAgICAgICAgICAgICAgICB9IGNhdGNoIChlcnIpIHtcbiAgICAgICAgICAgICAgICAgICAgICAgIGNvbnNvbGUubG9nKGVycik7XG4gICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgIHRoaXMubG9hZERhdGEoe30pO1xuICAgICAgICAgICAgICAgIHRoaXMuY3NyZXNvbHZlcihcIm5vdCB0YWtlblwiKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIHRoaXMuY2hlY2tMb2NhbFN0b3JhZ2UoKTsgLy8ganVzdCBnbyByaWdodCB0byBsb2NhbCBzdG9yYWdlXG4gICAgICAgICAgICB0aGlzLmNzcmVzb2x2ZXIoXCJsb2NhbFwiKTtcbiAgICAgICAgfVxuXG4gICAgICAgIGlmICh3aWxsX2JlX3JlYWR5KSB7XG4gICAgICAgICAgICB0aGlzLmluZGljYXRlX2NvbXBvbmVudF9yZWFkeSgpO1xuICAgICAgICB9XG4gICAgfVxuXG4gICAgLy8gVGhpcyBtZXRob2QgYXNzdW1lcyB0aGF0IGBgdGhpcy5jb21wb25lbnREaXZgYCByZWZlcnMgdG8gdGhlIGBgZGl2YGAgY29udGFpbmluZyB0aGUgY29tcG9uZW50LCBhbmQgdGhhdCB0aGlzIGNvbXBvbmVudCdzIElEIGlzIHNldC5cbiAgICBpbmRpY2F0ZV9jb21wb25lbnRfcmVhZHkoKSB7XG4gICAgICAgIC8vIEFkZCBhIGNsYXNzIHRvIGluZGljYXRlIHRoZSBjb21wb25lbnQgaXMgbm93IHJlYWR5LlxuICAgICAgICB0aGlzLmNvbnRhaW5lckRpdi5jbGFzc0xpc3QuYWRkKFwicnVuZXN0b25lLWNvbXBvbmVudC1yZWFkeVwiKTtcbiAgICAgICAgLy8gUmVzb2x2ZSB0aGUgYGB0aGlzLmNvbXBvbmVudF9yZWFkeV9wcm9taXNlYGAuXG4gICAgICAgIHRoaXMuX2NvbXBvbmVudF9yZWFkeV9yZXNvbHZlX2ZuKCk7XG4gICAgfVxuXG4gICAgbG9hZERhdGEoZGF0YSkge1xuICAgICAgICAvLyBmb3IgbW9zdCBjbGFzc2VzLCBsb2FkRGF0YSBkb2Vzbid0IGRvIGFueXRoaW5nLiBCdXQgZm9yIFBhcnNvbnMsIGFuZCBwZXJoYXBzIG90aGVycyBpbiB0aGUgZnV0dXJlLFxuICAgICAgICAvLyBpbml0aWFsaXphdGlvbiBjYW4gaGFwcGVuIGV2ZW4gd2hlbiB0aGVyZSdzIG5vIGhpc3RvcnkgdG8gYmUgbG9hZGVkXG4gICAgICAgIHJldHVybiBudWxsO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIHJlcG9wdWxhdGVGcm9tU3RvcmFnZSBpcyBjYWxsZWQgYWZ0ZXIgYSBzdWNjZXNzZnVsIEFQSSBjYWxsIGlzIG1hZGUgdG8gYGBnZXRBc3Nlc3NSZXN1bHRzYGAgaW5cbiAgICAgKiB0aGUgY2hlY2tTZXJ2ZXIgbWV0aG9kIGluIHRoaXMgY2xhc3NcbiAgICAgKlxuICAgICAqIGBgcmVzdG9yZUFuc3dlcnMsYGAgYGBzZXRMb2NhbFN0b3JhZ2VgYCBhbmQgYGBjaGVja0xvY2FsU3RvcmFnZWBgIGFyZSBkZWZpbmVkIGluIHRoZSBjaGlsZCBjbGFzc2VzLlxuICAgICAqXG4gICAgICogQHBhcmFtIHsqfSBkYXRhIC0gYSBKU09OIG9iamVjdCByZXByZXNlbnRpbmcgdGhlIGRhdGEgbmVlZGVkIHRvIHJlc3RvcmUgYSBwcmV2aW91cyBhbnN3ZXIgZm9yIGEgY29tcG9uZW50XG4gICAgICogQHBhcmFtIHsqfSBzdGF0dXMgLSB0aGUgaHR0cCBzdGF0dXNcbiAgICAgKiBAcGFyYW0geyp9IHdoYXRldmVyIC0gaWdub3JlZFxuICAgICAqL1xuICAgIHJlcG9wdWxhdGVGcm9tU3RvcmFnZShkYXRhKSB7XG4gICAgICAgIC8vIGRlY2lkZSB3aGV0aGVyIHRvIHVzZSB0aGUgc2VydmVyJ3MgYW5zd2VyIChpZiB0aGVyZSBpcyBvbmUpIG9yIHRvIGxvYWQgZnJvbSBzdG9yYWdlXG4gICAgICAgIGlmIChkYXRhICE9PSBudWxsICYmIHRoaXMuc2hvdWxkVXNlU2VydmVyKGRhdGEpKSB7XG4gICAgICAgICAgICB0aGlzLnJlc3RvcmVBbnN3ZXJzKGRhdGEpO1xuICAgICAgICAgICAgdGhpcy5zZXRMb2NhbFN0b3JhZ2UoZGF0YSk7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICB0aGlzLmNoZWNrTG9jYWxTdG9yYWdlKCk7XG4gICAgICAgIH1cbiAgICB9XG4gICAgc2hvdWxkVXNlU2VydmVyKGRhdGEpIHtcbiAgICAgICAgLy8gcmV0dXJucyB0cnVlIGlmIHNlcnZlciBkYXRhIGlzIG1vcmUgcmVjZW50IHRoYW4gbG9jYWwgc3RvcmFnZSBvciBpZiBzZXJ2ZXIgc3RvcmFnZSBpcyBjb3JyZWN0XG4gICAgICAgIGlmIChcbiAgICAgICAgICAgIGRhdGEuY29ycmVjdCA9PT0gXCJUXCIgfHxcbiAgICAgICAgICAgIGxvY2FsU3RvcmFnZS5sZW5ndGggPT09IDAgfHxcbiAgICAgICAgICAgIHRoaXMuZ3JhZGVyYWN0aXZlID09PSB0cnVlIHx8XG4gICAgICAgICAgICB0aGlzLmlzVGltZWRcbiAgICAgICAgKSB7XG4gICAgICAgICAgICByZXR1cm4gdHJ1ZTtcbiAgICAgICAgfVxuICAgICAgICBsZXQgZXggPSBsb2NhbFN0b3JhZ2UuZ2V0SXRlbSh0aGlzLmxvY2FsU3RvcmFnZUtleSgpKTtcbiAgICAgICAgaWYgKGV4ID09PSBudWxsKSB7XG4gICAgICAgICAgICByZXR1cm4gdHJ1ZTtcbiAgICAgICAgfVxuICAgICAgICBsZXQgc3RvcmVkRGF0YTtcbiAgICAgICAgdHJ5IHtcbiAgICAgICAgICAgIHN0b3JlZERhdGEgPSBKU09OLnBhcnNlKGV4KTtcbiAgICAgICAgfSBjYXRjaCAoZXJyKSB7XG4gICAgICAgICAgICAvLyBlcnJvciB3aGlsZSBwYXJzaW5nOyBsaWtlbHkgZHVlIHRvIGJhZCB2YWx1ZSBzdG9yZWQgaW4gc3RvcmFnZVxuICAgICAgICAgICAgY29uc29sZS5sb2coZXJyLm1lc3NhZ2UpO1xuICAgICAgICAgICAgbG9jYWxTdG9yYWdlLnJlbW92ZUl0ZW0odGhpcy5sb2NhbFN0b3JhZ2VLZXkoKSk7XG4gICAgICAgICAgICAvLyBkZWZpbml0ZWx5IGRvbid0IHdhbnQgdG8gdXNlIGxvY2FsIHN0b3JhZ2UgaGVyZVxuICAgICAgICAgICAgcmV0dXJuIHRydWU7XG4gICAgICAgIH1cbiAgICAgICAgaWYgKGRhdGEuYW5zd2VyID09IHN0b3JlZERhdGEuYW5zd2VyKSByZXR1cm4gdHJ1ZTtcbiAgICAgICAgbGV0IHN0b3JhZ2VEYXRlID0gbmV3IERhdGUoc3RvcmVkRGF0YS50aW1lc3RhbXApO1xuICAgICAgICBsZXQgc2VydmVyRGF0ZSA9IG5ldyBEYXRlKGRhdGEudGltZXN0YW1wKTtcbiAgICAgICAgcmV0dXJuIHNlcnZlckRhdGUgPj0gc3RvcmFnZURhdGU7XG4gICAgfVxuICAgIC8vIFJldHVybiB0aGUga2V5IHdoaWNoIHRvIGJlIHVzZWQgd2hlbiBhY2Nlc3NpbmcgbG9jYWwgc3RvcmFnZS5cbiAgICBsb2NhbFN0b3JhZ2VLZXkoKSB7XG4gICAgICAgIHJldHVybiAoXG4gICAgICAgICAgICBlQm9va0NvbmZpZy5lbWFpbCArXG4gICAgICAgICAgICBcIjpcIiArXG4gICAgICAgICAgICBlQm9va0NvbmZpZy5jb3Vyc2UgK1xuICAgICAgICAgICAgXCI6XCIgK1xuICAgICAgICAgICAgdGhpcy5kaXZpZCArXG4gICAgICAgICAgICBcIi1naXZlblwiXG4gICAgICAgICk7XG4gICAgfVxuICAgIGFkZENhcHRpb24oZWxUeXBlKSB7XG4gICAgICAgIC8vc29tZUVsZW1lbnQucGFyZW50Tm9kZS5pbnNlcnRCZWZvcmUobmV3RWxlbWVudCwgc29tZUVsZW1lbnQubmV4dFNpYmxpbmcpO1xuICAgICAgICBpZiAoIXRoaXMuaXNUaW1lZCkge1xuICAgICAgICAgICAgdmFyIGNhcERpdiA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoXCJwXCIpO1xuICAgICAgICAgICAgaWYgKHRoaXMucXVlc3Rpb25fbGFiZWwpIHtcbiAgICAgICAgICAgICAgICB0aGlzLmNhcHRpb24gPSBgQWN0aXZpdHk6ICR7dGhpcy5xdWVzdGlvbl9sYWJlbH0gJHt0aGlzLmNhcHRpb259ICA8c3BhbiBjbGFzcz1cInJ1bmVzdG9uZV9jYXB0aW9uX2RpdmlkXCI+KCR7dGhpcy5kaXZpZH0pPC9zcGFuPmA7XG4gICAgICAgICAgICAgICAgJChjYXBEaXYpLmh0bWwodGhpcy5jYXB0aW9uKTtcbiAgICAgICAgICAgICAgICAkKGNhcERpdikuYWRkQ2xhc3MoYCR7ZWxUeXBlfV9jYXB0aW9uYCk7XG4gICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgICQoY2FwRGl2KS5odG1sKHRoaXMuY2FwdGlvbiArIFwiIChcIiArIHRoaXMuZGl2aWQgKyBcIilcIik7XG4gICAgICAgICAgICAgICAgJChjYXBEaXYpLmFkZENsYXNzKGAke2VsVHlwZX1fY2FwdGlvbmApO1xuICAgICAgICAgICAgICAgICQoY2FwRGl2KS5hZGRDbGFzcyhgJHtlbFR5cGV9X2NhcHRpb25fdGV4dGApO1xuICAgICAgICAgICAgfVxuICAgICAgICAgICAgdGhpcy5jYXBEaXYgPSBjYXBEaXY7XG4gICAgICAgICAgICAvL3RoaXMub3V0ZXJEaXYucGFyZW50Tm9kZS5pbnNlcnRCZWZvcmUoY2FwRGl2LCB0aGlzLm91dGVyRGl2Lm5leHRTaWJsaW5nKTtcbiAgICAgICAgICAgIHRoaXMuY29udGFpbmVyRGl2LmFwcGVuZENoaWxkKGNhcERpdik7XG4gICAgICAgIH1cbiAgICB9XG5cbiAgICBoYXNVc2VyQWN0aXZpdHkoKSB7XG4gICAgICAgIHJldHVybiB0aGlzLmlzQW5zd2VyZWQ7XG4gICAgfVxuXG4gICAgY2hlY2tDdXJyZW50QW5zd2VyKCkge1xuICAgICAgICBjb25zb2xlLmxvZyhcbiAgICAgICAgICAgIFwiRWFjaCBjb21wb25lbnQgc2hvdWxkIHByb3ZpZGUgYW4gaW1wbGVtZW50YXRpb24gb2YgY2hlY2tDdXJyZW50QW5zd2VyXCJcbiAgICAgICAgKTtcbiAgICB9XG5cbiAgICBhc3luYyBsb2dDdXJyZW50QW5zd2VyKCkge1xuICAgICAgICBjb25zb2xlLmxvZyhcbiAgICAgICAgICAgIFwiRWFjaCBjb21wb25lbnQgc2hvdWxkIHByb3ZpZGUgYW4gaW1wbGVtZW50YXRpb24gb2YgbG9nQ3VycmVudEFuc3dlclwiXG4gICAgICAgICk7XG4gICAgfVxuICAgIHJlbmRlckZlZWRiYWNrKCkge1xuICAgICAgICBjb25zb2xlLmxvZyhcbiAgICAgICAgICAgIFwiRWFjaCBjb21wb25lbnQgc2hvdWxkIHByb3ZpZGUgYW4gaW1wbGVtZW50YXRpb24gb2YgcmVuZGVyRmVlZGJhY2tcIlxuICAgICAgICApO1xuICAgIH1cbiAgICBkaXNhYmxlSW50ZXJhY3Rpb24oKSB7XG4gICAgICAgIGNvbnNvbGUubG9nKFxuICAgICAgICAgICAgXCJFYWNoIGNvbXBvbmVudCBzaG91bGQgcHJvdmlkZSBhbiBpbXBsZW1lbnRhdGlvbiBvZiBkaXNhYmxlSW50ZXJhY3Rpb25cIlxuICAgICAgICApO1xuICAgIH1cblxuICAgIHRvU3RyaW5nKCkge1xuICAgICAgICByZXR1cm4gYCR7dGhpcy5jb25zdHJ1Y3Rvci5uYW1lfTogJHt0aGlzLmRpdmlkfWBcbiAgICB9XG5cbiAgICBxdWV1ZU1hdGhKYXgoY29tcG9uZW50KSB7XG4gICAgICAgIGlmIChNYXRoSmF4LnZlcnNpb24uc3Vic3RyaW5nKDAsIDEpID09PSBcIjJcIikge1xuICAgICAgICAgICAgTWF0aEpheC5IdWIuUXVldWUoW1wiVHlwZXNldFwiLCBNYXRoSmF4Lkh1YiwgY29tcG9uZW50XSk7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICBNYXRoSmF4LnR5cGVzZXRQcm9taXNlKFtjb21wb25lbnRdKVxuICAgICAgICB9XG4gICAgfVxuXG59XG5cbndpbmRvdy5SdW5lc3RvbmVCYXNlID0gUnVuZXN0b25lQmFzZTtcbiJdLCJzb3VyY2VSb290IjoiIn0=