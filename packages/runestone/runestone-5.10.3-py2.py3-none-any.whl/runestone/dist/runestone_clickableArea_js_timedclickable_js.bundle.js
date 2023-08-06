(self["webpackChunkWebComponents"] = self["webpackChunkWebComponents"] || []).push([["runestone_clickableArea_js_timedclickable_js"],{

/***/ 51168:
/*!***************************************************!*\
  !*** ./runestone/clickableArea/css/clickable.css ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
// extracted by mini-css-extract-plugin


/***/ }),

/***/ 5464:
/*!*************************************************!*\
  !*** ./runestone/clickableArea/js/clickable.js ***!
  \*************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CAList": () => (/* binding */ CAList),
/* harmony export */   "default": () => (/* binding */ ClickableArea)
/* harmony export */ });
/* harmony import */ var _common_js_runestonebase_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../common/js/runestonebase.js */ 2568);
/* harmony import */ var _css_clickable_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../css/clickable.css */ 51168);
/*==========================================
=======     Master clickable.js     ========
============================================
===   This file contains the JS for the  ===
===  Runestone clickable area component. ===
============================================
===              Created by              ===
===           Isaiah Mayerchak           ===
===                7/1/15                ===
==========================================*/





var CAList = {}; // Object that contains all instances of ClickableArea objects

class ClickableArea extends _common_js_runestonebase_js__WEBPACK_IMPORTED_MODULE_0__.default {
    constructor(opts) {
        super(opts);
        var orig = opts.orig; // entire <div> element that will be replaced by new HTML
        this.origElem = orig;
        this.divid = orig.id;
        this.useRunestoneServices = opts.useRunestoneServices;
        this.clickableArray = []; // holds all clickable elements
        this.correctArray = []; // holds the IDs of all correct clickable span elements, used for eval
        this.incorrectArray = []; // holds IDs of all incorrect clickable span elements, used for eval
        //For use with Sphinx-rendered html
        this.isTable = false;
        if ($(this.origElem).data("cc") !== undefined) {
            if ($(this.origElem).is("[data-table]")) {
                this.isTable = true;
                this.ccArray = $(this.origElem).data("cc").split(";");
                this.ciArray = $(this.origElem).data("ci").split(";");
            } else {
                this.ccArray = $(this.origElem).data("cc").split(",");
                this.ciArray = $(this.origElem).data("ci").split(",");
            }
        }
        // For use in the recursive replace function
        this.clickIndex = 0; // Index of this.clickedIndexArray that we're checking against
        this.clickableCounter = 0; // Index of the current clickable element
        this.getQuestion();
        this.getFeedback();
        this.renderNewElements();
        this.caption = "Clickable";
        this.addCaption("runestone");
        this.checkServer("clickableArea", true);
    }
    /*===========================
    == Update basic attributes ==
    ===========================*/
    getQuestion() {
        for (var i = 0; i < this.origElem.childNodes.length; i++) {
            if ($(this.origElem.childNodes[i]).is("[data-question]")) {
                this.question = this.origElem.childNodes[i];
                break;
            }
        }
    }
    getFeedback() {
        this.feedback = "";
        for (var i = 0; i < this.origElem.childNodes.length; i++) {
            if ($(this.origElem.childNodes[i]).is("[data-feedback]")) {
                this.feedback = this.origElem.childNodes[i];
            }
        }
        if (this.feedback !== "") {
            // Get the feedback element out of the container if the user has defined feedback
            $(this.feedback).remove();
            this.feedback = this.feedback.innerHTML;
        }
    }
    /*===========================================
    ====   Functions generating final HTML   ====
    ===========================================*/
    renderNewElements() {
        // wrapper function for generating everything
        this.containerDiv = document.createElement("div");
        this.containerDiv.id = this.origElem.id;
        this.containerDiv.appendChild(this.question);
        $(this.containerDiv).addClass(this.origElem.getAttribute("class"));
        this.newDiv = document.createElement("div");
        var newContent = $(this.origElem).html();
        while (newContent[0] === "\n") {
            newContent = newContent.slice(1);
        }
        this.newDiv.innerHTML = newContent;
        this.containerDiv.appendChild(this.newDiv);
        this.createButtons();
        this.createFeedbackDiv();
        $(this.origElem).replaceWith(this.containerDiv);
    }
    createButtons() {
        this.submitButton = document.createElement("button"); // Check me button
        this.submitButton.textContent = "Check Me";
        $(this.submitButton).attr({
            class: "btn btn-success",
            name: "do answer",
            type: "button",
        });
        this.submitButton.onclick = function () {
            this.checkCurrentAnswer();
            this.logCurrentAnswer();
            this.renderFeedback();
        }.bind(this);
        this.containerDiv.appendChild(this.submitButton);
    }
    createFeedbackDiv() {
        this.feedBackDiv = document.createElement("div");
        this.containerDiv.appendChild(document.createElement("br"));
        this.containerDiv.appendChild(this.feedBackDiv);
    }
    /*===================================
    === Checking/restoring from storage ===
    ===================================*/
    restoreAnswers(data) {
        // Restore answers from storage retrieval done in RunestoneBase or from local storage
        if (data.answer !== undefined) {
            // if we got data from the server
            this.hasStoredAnswers = true;
            this.clickedIndexArray = data.answer.split(";");
        }
        if (this.ccArray === undefined) {
            this.modifyClickables(this.newDiv.childNodes);
        } else {
            // For use with Sphinx-rendered HTML
            this.ccCounter = 0;
            this.ccIndex = 0;
            this.ciIndex = 0;
            if (!this.isTable) {
                this.modifyViaCC(this.newDiv.children);
            } else {
                this.modifyTableViaCC(this.newDiv.children);
            }
        }
    }
    checkLocalStorage() {
        if (this.graderactive) {
            return;
        }
        var storageObj;
        // Gets previous answer data from local storage if it exists
        this.hasStoredAnswers = false;
        var len = localStorage.length;
        if (len > 0) {
            var ex = localStorage.getItem(this.localStorageKey());
            if (ex !== null) {
                this.hasStoredAnswers = true;
                try {
                    storageObj = JSON.parse(ex);
                    this.clickedIndexArray = storageObj.answer.split(";");
                } catch (err) {
                    // error while parsing; likely due to bad value stored in storage
                    console.log(err.message);
                    localStorage.removeItem(this.localStorageKey());
                    this.hasStoredAnswers = false;
                    this.restoreAnswers({});
                    return;
                }
                if (this.useRunestoneServices) {
                    // log answer to server
                    this.givenIndexArray = [];
                    for (var i = 0; i < this.clickableArray.length; i++) {
                        if (
                            $(this.clickableArray[i]).hasClass(
                                "clickable-clicked"
                            )
                        ) {
                            this.givenIndexArray.push(i);
                        }
                    }
                    this.logBookEvent({
                        event: "clickableArea",
                        act: this.clickedIndexArray.join(";"),
                        div_id: this.divid,
                        correct: storageObj.correct,
                    });
                }
            }
        }
        this.restoreAnswers({}); // pass empty object
    }
    setLocalStorage(data) {
        // Array of the indices of clicked elements is passed to local storage
        var answer;
        if (data.answer !== undefined) {
            // If we got data from the server, we can just use that
            answer = this.clickedIndexArray.join(";");
        } else {
            this.givenIndexArray = [];
            for (var i = 0; i < this.clickableArray.length; i++) {
                if ($(this.clickableArray[i]).hasClass("clickable-clicked")) {
                    this.givenIndexArray.push(i);
                }
            }
            answer = this.givenIndexArray.join(";");
        }
        var timeStamp = new Date();
        var correct = data.correct;
        var storageObject = {
            answer: answer,
            correct: correct,
            timestamp: timeStamp,
        };
        localStorage.setItem(
            this.localStorageKey(),
            JSON.stringify(storageObject)
        );
    }
    /*==========================
    === Auxilliary functions ===
    ==========================*/
    modifyClickables(childNodes) {
        // Strips the data-correct/data-incorrect labels and updates the correct/incorrect arrays
        for (var i = 0; i < childNodes.length; i++) {
            if (
                $(childNodes[i]).is("[data-correct]") ||
                $(childNodes[i]).is("[data-incorrect]")
            ) {
                this.manageNewClickable(childNodes[i]);
                if ($(childNodes[i]).is("[data-correct]")) {
                    $(childNodes[i]).removeAttr("data-correct");
                    this.correctArray.push(childNodes[i]);
                } else {
                    $(childNodes[i]).removeAttr("data-incorrect");
                    this.incorrectArray.push(childNodes[i]);
                }
            }
            if (childNodes[i].childNodes.length !== 0) {
                this.modifyClickables(childNodes[i].childNodes);
            }
        }
    }
    modifyViaCC(children) {
        for (var i = 0; i < children.length; i++) {
            if (children[i].children.length !== 0) {
                this.modifyViaCC(children[i].children);
            } else {
                this.ccCounter++;
                if (this.ccCounter === Math.floor(this.ccArray[this.ccIndex])) {
                    this.manageNewClickable(children[i]);
                    this.correctArray.push(children[i]);
                    this.ccIndex++;
                } else if (
                    this.ccCounter === Math.floor(this.ciArray[this.ciIndex])
                ) {
                    this.manageNewClickable(children[i]);
                    this.incorrectArray.push(children[i]);
                    this.ciIndex++;
                }
            }
        }
    }
    modifyTableViaCC(children) {
        // table version of modifyViaCC
        var tComponentArr = [];
        for (let i = 0; i < children.length; i++) {
            if (children[i].nodeName === "TABLE") {
                let tmp = children[i];
                for (let j = 0; j < tmp.children.length; j++) {
                    if (tmp.children[j].nodeName === "THEAD") {
                        tComponentArr.push(tmp.children[j]);
                    } else if (tmp.children[j].nodeName === "TBODY") {
                        tComponentArr.push(tmp.children[j]);
                    } else if (tmp.children[j].nodeName === "TFOOT") {
                        tComponentArr.push(tmp.children[j]);
                    }
                }
            }
        }
        for (var t = 0; t < tComponentArr.length; t++) {
            for (let i = 0; i < tComponentArr[t].children.length; i++) {
                this.ccCounter++;
                // First check if the entire row needs to be clickable
                if (
                    this.ccIndex < this.ccArray.length &&
                    this.ccCounter ===
                    Math.floor(this.ccArray[this.ccIndex].split(",")[0]) &&
                    Math.floor(this.ccArray[this.ccIndex].split(",")[1]) === 0
                ) {
                    this.manageNewClickable(tComponentArr[t].children[i]);
                    this.correctArray.push(tComponentArr[t].children[i]);
                    this.ccIndex++;
                } else if (
                    this.ciIndex < this.ciArray.length &&
                    this.ccCounter ===
                    Math.floor(this.ciArray[this.ciIndex].split(",")[0]) &&
                    Math.floor(this.ciArray[this.ciIndex].split(",")[1]) === 0
                ) {
                    this.manageNewClickable(tComponentArr[t].children[i]);
                    this.incorrectArray.push(tComponentArr[t].children[i]);
                    this.ciIndex++;
                } else {
                    // If not, check the individual data cells
                    for (
                        let j = 0;
                        j < tComponentArr[t].children[i].children.length;
                        j++
                    ) {
                        let tmp = j + 1;
                        if (
                            this.ccIndex < this.ccArray.length &&
                            tmp ===
                            Math.floor(
                                this.ccArray[this.ccIndex].split(",")[1]
                            ) &&
                            this.ccCounter ===
                            Math.floor(
                                this.ccArray[this.ccIndex].split(",")[0]
                            )
                        ) {
                            this.manageNewClickable(
                                tComponentArr[t].children[i].children[j]
                            );
                            this.correctArray.push(
                                tComponentArr[t].children[i].children[j]
                            );
                            this.ccIndex++;
                        } else if (
                            this.ciIndex < this.ciArray.length &&
                            tmp ===
                            Math.floor(
                                this.ciArray[this.ciIndex].split(",")[1]
                            ) &&
                            this.ccCounter ===
                            Math.floor(
                                this.ciArray[this.ciIndex].split(",")[0]
                            )
                        ) {
                            this.manageNewClickable(
                                tComponentArr[t].children[i].children[j]
                            );
                            this.incorrectArray.push(
                                tComponentArr[t].children[i].children[j]
                            );
                            this.ciIndex++;
                        }
                    }
                }
            }
        }
    }
    manageNewClickable(clickable) {
        // adds the "clickable" functionality
        $(clickable).addClass("clickable");
        if (this.hasStoredAnswers) {
            // Check if the element we're about to append to the pre was in local storage as clicked via its index
            if (
                this.clickedIndexArray[this.clickIndex].toString() ===
                this.clickableCounter.toString()
            ) {
                $(clickable).addClass("clickable-clicked");
                this.clickIndex++;
                if (this.clickIndex === this.clickedIndexArray.length) {
                    // Stop doing this if the index array is used up
                    this.hasStoredAnswers = false;
                }
            }
        }
        let self = this;
        clickable.onclick = function () {
            self.isAnswered = true;
            if ($(this).hasClass("clickable-clicked")) {
                $(this).removeClass("clickable-clicked");
                $(this).removeClass("clickable-incorrect");
            } else {
                $(this).addClass("clickable-clicked");
            }
        };
        this.clickableArray.push(clickable);
        this.clickableCounter++;
    }
    /*======================================
    == Evaluation and displaying feedback ==
    ======================================*/
    checkCurrentAnswer() {
        // Evaluation is done by iterating over the correct/incorrect arrays and checking by class
        this.correct = true;
        this.correctNum = 0;
        this.incorrectNum = 0;
        for (let i = 0; i < this.correctArray.length; i++) {
            if (!$(this.correctArray[i]).hasClass("clickable-clicked")) {
                this.correct = false;
            } else {
                this.correctNum++;
            }
        }
        for (let i = 0; i < this.incorrectArray.length; i++) {
            if ($(this.incorrectArray[i]).hasClass("clickable-clicked")) {
                this.correct = false;
                this.incorrectNum++;
            } else {
                $(this.incorrectArray[i]).removeClass("clickable-incorrect");
            }
        }
        this.percent =
            (this.correctNum - this.incorrectNum) / this.correctArray.length;
        this.setLocalStorage({ correct: this.correct ? "T" : "F" });
    }

    async logCurrentAnswer(sid) {
        let data = {
            event: "clickableArea",
            act: this.givenIndexArray.join(";"),
            div_id: this.divid,
            correct: this.correct ? "T" : "F",
        };
        if (typeof sid !== "undefined") {
            data.sid = sid;
        }
        await this.logBookEvent(data);
    }

    renderFeedback() {
        if (this.correct) {
            $(this.feedBackDiv).html("You are Correct!");
            $(this.feedBackDiv).attr("class", "alert alert-info");
        } else {
            for (let i = 0; i < this.incorrectArray.length; i++) {
                if ($(this.incorrectArray[i]).hasClass("clickable-clicked")) {
                    $(this.incorrectArray[i]).addClass("clickable-incorrect");
                } else {
                    $(this.incorrectArray[i]).removeClass(
                        "clickable-incorrect"
                    );
                }
            }
            $(this.feedBackDiv).html(
                "Incorrect. You clicked on " +
                this.correctNum +
                " of the " +
                this.correctArray.length.toString() +
                " correct elements and " +
                this.incorrectNum +
                " of the " +
                this.incorrectArray.length.toString() +
                " incorrect elements. " +
                this.feedback
            );
            $(this.feedBackDiv).attr("class", "alert alert-danger");
        }
    }

    disableInteraction() {
        for (var i = 0; i < this.clickableArray.length; i++) {
            $(this.clickableArray[i]).css("cursor", "initial");
            this.clickableArray[i].onclick = function () {
                return;
            };
        }
    }
}

/*=================================
== Find the custom HTML tags and ==
==   execute our code on them    ==
=================================*/
$(document).bind("runestone:login-complete", function () {
    $("[data-component=clickablearea]").each(function (index) {
        if ($(this).closest("[data-component=timedAssessment]").length == 0) {
            // If this element exists within a timed component, don't render it here
            try {
                CAList[this.id] = new ClickableArea({
                    orig: this,
                    useRunestoneServices: eBookConfig.useRunestoneServices,
                });
            } catch (err) {
                console.log(`Error rendering ClickableArea Problem ${this.id}
                             Details: ${err}`);
            }
        }
    });
});


/***/ }),

/***/ 61581:
/*!******************************************************!*\
  !*** ./runestone/clickableArea/js/timedclickable.js ***!
  \******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ TimedClickableArea)
/* harmony export */ });
/* harmony import */ var _clickable_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./clickable.js */ 5464);


("use strict");

class TimedClickableArea extends _clickable_js__WEBPACK_IMPORTED_MODULE_0__.default {
    constructor(opts) {
        super(opts);
        this.restoreAnswers({});
        this.renderTimedIcon(this.containerDiv);
        this.hideButtons();
    }

    hideButtons() {
        $(this.submitButton).hide();
    }

    renderTimedIcon(component) {
        // renders the clock icon on timed components.    The component parameter
        // is the element that the icon should be appended to.
        var timeIconDiv = document.createElement("div");
        var timeIcon = document.createElement("img");
        $(timeIcon).attr({
            src: "../_static/clock.png",
            style: "width:15px;height:15px",
        });
        timeIconDiv.className = "timeTip";
        timeIconDiv.title = "";
        timeIconDiv.appendChild(timeIcon);
        $(component).prepend(timeIconDiv);
    }

    checkCorrectTimed() {
        // Returns if the question was correct, incorrect, or skipped (return null in the last case)
        if (this.correctNum === 0 && this.incorrectNum === 0) {
            this.correct = null;
        }
        switch (this.correct) {
            case true:
                return "T";
            case false:
                return "F";
            default:
                return null;
        }
    }

    hideFeedback() {
        $(this.feedBackDiv).hide();
    }
}

if (typeof window.component_factory === "undefined") {
    window.component_factory = {};
}
window.component_factory.clickablearea = function (opts) {
    if (opts.timed) {
        return new TimedClickableArea(opts);
    }
    return new _clickable_js__WEBPACK_IMPORTED_MODULE_0__.default(opts);
};


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9XZWJDb21wb25lbnRzLy4vcnVuZXN0b25lL2NsaWNrYWJsZUFyZWEvY3NzL2NsaWNrYWJsZS5jc3M/MTlmYSIsIndlYnBhY2s6Ly9XZWJDb21wb25lbnRzLy4vcnVuZXN0b25lL2NsaWNrYWJsZUFyZWEvanMvY2xpY2thYmxlLmpzIiwid2VicGFjazovL1dlYkNvbXBvbmVudHMvLi9ydW5lc3RvbmUvY2xpY2thYmxlQXJlYS9qcy90aW1lZGNsaWNrYWJsZS5qcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUNBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNhOztBQUVnRDtBQUMvQjs7QUFFdkIsZ0JBQWdCOztBQUVSLDRCQUE0QixnRUFBYTtBQUN4RDtBQUNBO0FBQ0EsNkJBQTZCO0FBQzdCO0FBQ0E7QUFDQTtBQUNBLGlDQUFpQztBQUNqQywrQkFBK0I7QUFDL0IsaUNBQWlDO0FBQ2pDO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxtRUFBbUU7QUFDbkUsbUVBQW1FO0FBQ25FLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsNEJBQTRCO0FBQzVCLGtDQUFrQztBQUNsQztBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsdUJBQXVCLHFDQUFxQztBQUM1RDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsdUJBQXVCLHFDQUFxQztBQUM1RDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLDZEQUE2RDtBQUM3RDtBQUNB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YWJsZV9qcy5idW5kbGUuanM/dj0yMjNiOGZjZDU0NjE4YzVlZjM1OSIsInNvdXJjZXNDb250ZW50IjpbIi8vIGV4dHJhY3RlZCBieSBtaW5pLWNzcy1leHRyYWN0LXBsdWdpblxuZXhwb3J0IHt9OyIsIi8qPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09XG49PT09PT09ICAgICBNYXN0ZXIgY2xpY2thYmxlLmpzICAgICA9PT09PT09PVxuPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT1cbj09PSAgIFRoaXMgZmlsZSBjb250YWlucyB0aGUgSlMgZm9yIHRoZSAgPT09XG49PT0gIFJ1bmVzdG9uZSBjbGlja2FibGUgYXJlYSBjb21wb25lbnQuID09PVxuPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT1cbj09PSAgICAgICAgICAgICAgQ3JlYXRlZCBieSAgICAgICAgICAgICAgPT09XG49PT0gICAgICAgICAgIElzYWlhaCBNYXllcmNoYWsgICAgICAgICAgID09PVxuPT09ICAgICAgICAgICAgICAgIDcvMS8xNSAgICAgICAgICAgICAgICA9PT1cbj09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PSovXG5cInVzZSBzdHJpY3RcIjtcblxuaW1wb3J0IFJ1bmVzdG9uZUJhc2UgZnJvbSBcIi4uLy4uL2NvbW1vbi9qcy9ydW5lc3RvbmViYXNlLmpzXCI7XG5pbXBvcnQgXCIuLi9jc3MvY2xpY2thYmxlLmNzc1wiO1xuXG5leHBvcnQgdmFyIENBTGlzdCA9IHt9OyAvLyBPYmplY3QgdGhhdCBjb250YWlucyBhbGwgaW5zdGFuY2VzIG9mIENsaWNrYWJsZUFyZWEgb2JqZWN0c1xuXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBDbGlja2FibGVBcmVhIGV4dGVuZHMgUnVuZXN0b25lQmFzZSB7XG4gICAgY29uc3RydWN0b3Iob3B0cykge1xuICAgICAgICBzdXBlcihvcHRzKTtcbiAgICAgICAgdmFyIG9yaWcgPSBvcHRzLm9yaWc7IC8vIGVudGlyZSA8ZGl2PiBlbGVtZW50IHRoYXQgd2lsbCBiZSByZXBsYWNlZCBieSBuZXcgSFRNTFxuICAgICAgICB0aGlzLm9yaWdFbGVtID0gb3JpZztcbiAgICAgICAgdGhpcy5kaXZpZCA9IG9yaWcuaWQ7XG4gICAgICAgIHRoaXMudXNlUnVuZXN0b25lU2VydmljZXMgPSBvcHRzLnVzZVJ1bmVzdG9uZVNlcnZpY2VzO1xuICAgICAgICB0aGlzLmNsaWNrYWJsZUFycmF5ID0gW107IC8vIGhvbGRzIGFsbCBjbGlja2FibGUgZWxlbWVudHNcbiAgICAgICAgdGhpcy5jb3JyZWN0QXJyYXkgPSBbXTsgLy8gaG9sZHMgdGhlIElEcyBvZiBhbGwgY29ycmVjdCBjbGlja2FibGUgc3BhbiBlbGVtZW50cywgdXNlZCBmb3IgZXZhbFxuICAgICAgICB0aGlzLmluY29ycmVjdEFycmF5ID0gW107IC8vIGhvbGRzIElEcyBvZiBhbGwgaW5jb3JyZWN0IGNsaWNrYWJsZSBzcGFuIGVsZW1lbnRzLCB1c2VkIGZvciBldmFsXG4gICAgICAgIC8vRm9yIHVzZSB3aXRoIFNwaGlueC1yZW5kZXJlZCBodG1sXG4gICAgICAgIHRoaXMuaXNUYWJsZSA9IGZhbHNlO1xuICAgICAgICBpZiAoJCh0aGlzLm9yaWdFbGVtKS5kYXRhKFwiY2NcIikgIT09IHVuZGVmaW5lZCkge1xuICAgICAgICAgICAgaWYgKCQodGhpcy5vcmlnRWxlbSkuaXMoXCJbZGF0YS10YWJsZV1cIikpIHtcbiAgICAgICAgICAgICAgICB0aGlzLmlzVGFibGUgPSB0cnVlO1xuICAgICAgICAgICAgICAgIHRoaXMuY2NBcnJheSA9ICQodGhpcy5vcmlnRWxlbSkuZGF0YShcImNjXCIpLnNwbGl0KFwiO1wiKTtcbiAgICAgICAgICAgICAgICB0aGlzLmNpQXJyYXkgPSAkKHRoaXMub3JpZ0VsZW0pLmRhdGEoXCJjaVwiKS5zcGxpdChcIjtcIik7XG4gICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgIHRoaXMuY2NBcnJheSA9ICQodGhpcy5vcmlnRWxlbSkuZGF0YShcImNjXCIpLnNwbGl0KFwiLFwiKTtcbiAgICAgICAgICAgICAgICB0aGlzLmNpQXJyYXkgPSAkKHRoaXMub3JpZ0VsZW0pLmRhdGEoXCJjaVwiKS5zcGxpdChcIixcIik7XG4gICAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgICAgLy8gRm9yIHVzZSBpbiB0aGUgcmVjdXJzaXZlIHJlcGxhY2UgZnVuY3Rpb25cbiAgICAgICAgdGhpcy5jbGlja0luZGV4ID0gMDsgLy8gSW5kZXggb2YgdGhpcy5jbGlja2VkSW5kZXhBcnJheSB0aGF0IHdlJ3JlIGNoZWNraW5nIGFnYWluc3RcbiAgICAgICAgdGhpcy5jbGlja2FibGVDb3VudGVyID0gMDsgLy8gSW5kZXggb2YgdGhlIGN1cnJlbnQgY2xpY2thYmxlIGVsZW1lbnRcbiAgICAgICAgdGhpcy5nZXRRdWVzdGlvbigpO1xuICAgICAgICB0aGlzLmdldEZlZWRiYWNrKCk7XG4gICAgICAgIHRoaXMucmVuZGVyTmV3RWxlbWVudHMoKTtcbiAgICAgICAgdGhpcy5jYXB0aW9uID0gXCJDbGlja2FibGVcIjtcbiAgICAgICAgdGhpcy5hZGRDYXB0aW9uKFwicnVuZXN0b25lXCIpO1xuICAgICAgICB0aGlzLmNoZWNrU2VydmVyKFwiY2xpY2thYmxlQXJlYVwiLCB0cnVlKTtcbiAgICB9XG4gICAgLyo9PT09PT09PT09PT09PT09PT09PT09PT09PT1cbiAgICA9PSBVcGRhdGUgYmFzaWMgYXR0cmlidXRlcyA9PVxuICAgID09PT09PT09PT09PT09PT09PT09PT09PT09PSovXG4gICAgZ2V0UXVlc3Rpb24oKSB7XG4gICAgICAgIGZvciAodmFyIGkgPSAwOyBpIDwgdGhpcy5vcmlnRWxlbS5jaGlsZE5vZGVzLmxlbmd0aDsgaSsrKSB7XG4gICAgICAgICAgICBpZiAoJCh0aGlzLm9yaWdFbGVtLmNoaWxkTm9kZXNbaV0pLmlzKFwiW2RhdGEtcXVlc3Rpb25dXCIpKSB7XG4gICAgICAgICAgICAgICAgdGhpcy5xdWVzdGlvbiA9IHRoaXMub3JpZ0VsZW0uY2hpbGROb2Rlc1tpXTtcbiAgICAgICAgICAgICAgICBicmVhaztcbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgIH1cbiAgICBnZXRGZWVkYmFjaygpIHtcbiAgICAgICAgdGhpcy5mZWVkYmFjayA9IFwiXCI7XG4gICAgICAgIGZvciAodmFyIGkgPSAwOyBpIDwgdGhpcy5vcmlnRWxlbS5jaGlsZE5vZGVzLmxlbmd0aDsgaSsrKSB7XG4gICAgICAgICAgICBpZiAoJCh0aGlzLm9yaWdFbGVtLmNoaWxkTm9kZXNbaV0pLmlzKFwiW2RhdGEtZmVlZGJhY2tdXCIpKSB7XG4gICAgICAgICAgICAgICAgdGhpcy5mZWVkYmFjayA9IHRoaXMub3JpZ0VsZW0uY2hpbGROb2Rlc1tpXTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgICBpZiAodGhpcy5mZWVkYmFjayAhPT0gXCJcIikge1xuICAgICAgICAgICAgLy8gR2V0IHRoZSBmZWVkYmFjayBlbGVtZW50IG91dCBvZiB0aGUgY29udGFpbmVyIGlmIHRoZSB1c2VyIGhhcyBkZWZpbmVkIGZlZWRiYWNrXG4gICAgICAgICAgICAkKHRoaXMuZmVlZGJhY2spLnJlbW92ZSgpO1xuICAgICAgICAgICAgdGhpcy5mZWVkYmFjayA9IHRoaXMuZmVlZGJhY2suaW5uZXJIVE1MO1xuICAgICAgICB9XG4gICAgfVxuICAgIC8qPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PVxuICAgID09PT0gICBGdW5jdGlvbnMgZ2VuZXJhdGluZyBmaW5hbCBIVE1MICAgPT09PVxuICAgID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT0qL1xuICAgIHJlbmRlck5ld0VsZW1lbnRzKCkge1xuICAgICAgICAvLyB3cmFwcGVyIGZ1bmN0aW9uIGZvciBnZW5lcmF0aW5nIGV2ZXJ5dGhpbmdcbiAgICAgICAgdGhpcy5jb250YWluZXJEaXYgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KFwiZGl2XCIpO1xuICAgICAgICB0aGlzLmNvbnRhaW5lckRpdi5pZCA9IHRoaXMub3JpZ0VsZW0uaWQ7XG4gICAgICAgIHRoaXMuY29udGFpbmVyRGl2LmFwcGVuZENoaWxkKHRoaXMucXVlc3Rpb24pO1xuICAgICAgICAkKHRoaXMuY29udGFpbmVyRGl2KS5hZGRDbGFzcyh0aGlzLm9yaWdFbGVtLmdldEF0dHJpYnV0ZShcImNsYXNzXCIpKTtcbiAgICAgICAgdGhpcy5uZXdEaXYgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KFwiZGl2XCIpO1xuICAgICAgICB2YXIgbmV3Q29udGVudCA9ICQodGhpcy5vcmlnRWxlbSkuaHRtbCgpO1xuICAgICAgICB3aGlsZSAobmV3Q29udGVudFswXSA9PT0gXCJcXG5cIikge1xuICAgICAgICAgICAgbmV3Q29udGVudCA9IG5ld0NvbnRlbnQuc2xpY2UoMSk7XG4gICAgICAgIH1cbiAgICAgICAgdGhpcy5uZXdEaXYuaW5uZXJIVE1MID0gbmV3Q29udGVudDtcbiAgICAgICAgdGhpcy5jb250YWluZXJEaXYuYXBwZW5kQ2hpbGQodGhpcy5uZXdEaXYpO1xuICAgICAgICB0aGlzLmNyZWF0ZUJ1dHRvbnMoKTtcbiAgICAgICAgdGhpcy5jcmVhdGVGZWVkYmFja0RpdigpO1xuICAgICAgICAkKHRoaXMub3JpZ0VsZW0pLnJlcGxhY2VXaXRoKHRoaXMuY29udGFpbmVyRGl2KTtcbiAgICB9XG4gICAgY3JlYXRlQnV0dG9ucygpIHtcbiAgICAgICAgdGhpcy5zdWJtaXRCdXR0b24gPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KFwiYnV0dG9uXCIpOyAvLyBDaGVjayBtZSBidXR0b25cbiAgICAgICAgdGhpcy5zdWJtaXRCdXR0b24udGV4dENvbnRlbnQgPSBcIkNoZWNrIE1lXCI7XG4gICAgICAgICQodGhpcy5zdWJtaXRCdXR0b24pLmF0dHIoe1xuICAgICAgICAgICAgY2xhc3M6IFwiYnRuIGJ0bi1zdWNjZXNzXCIsXG4gICAgICAgICAgICBuYW1lOiBcImRvIGFuc3dlclwiLFxuICAgICAgICAgICAgdHlwZTogXCJidXR0b25cIixcbiAgICAgICAgfSk7XG4gICAgICAgIHRoaXMuc3VibWl0QnV0dG9uLm9uY2xpY2sgPSBmdW5jdGlvbiAoKSB7XG4gICAgICAgICAgICB0aGlzLmNoZWNrQ3VycmVudEFuc3dlcigpO1xuICAgICAgICAgICAgdGhpcy5sb2dDdXJyZW50QW5zd2VyKCk7XG4gICAgICAgICAgICB0aGlzLnJlbmRlckZlZWRiYWNrKCk7XG4gICAgICAgIH0uYmluZCh0aGlzKTtcbiAgICAgICAgdGhpcy5jb250YWluZXJEaXYuYXBwZW5kQ2hpbGQodGhpcy5zdWJtaXRCdXR0b24pO1xuICAgIH1cbiAgICBjcmVhdGVGZWVkYmFja0RpdigpIHtcbiAgICAgICAgdGhpcy5mZWVkQmFja0RpdiA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoXCJkaXZcIik7XG4gICAgICAgIHRoaXMuY29udGFpbmVyRGl2LmFwcGVuZENoaWxkKGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoXCJiclwiKSk7XG4gICAgICAgIHRoaXMuY29udGFpbmVyRGl2LmFwcGVuZENoaWxkKHRoaXMuZmVlZEJhY2tEaXYpO1xuICAgIH1cbiAgICAvKj09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09XG4gICAgPT09IENoZWNraW5nL3Jlc3RvcmluZyBmcm9tIHN0b3JhZ2UgPT09XG4gICAgPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT0qL1xuICAgIHJlc3RvcmVBbnN3ZXJzKGRhdGEpIHtcbiAgICAgICAgLy8gUmVzdG9yZSBhbnN3ZXJzIGZyb20gc3RvcmFnZSByZXRyaWV2YWwgZG9uZSBpbiBSdW5lc3RvbmVCYXNlIG9yIGZyb20gbG9jYWwgc3RvcmFnZVxuICAgICAgICBpZiAoZGF0YS5hbnN3ZXIgIT09IHVuZGVmaW5lZCkge1xuICAgICAgICAgICAgLy8gaWYgd2UgZ290IGRhdGEgZnJvbSB0aGUgc2VydmVyXG4gICAgICAgICAgICB0aGlzLmhhc1N0b3JlZEFuc3dlcnMgPSB0cnVlO1xuICAgICAgICAgICAgdGhpcy5jbGlja2VkSW5kZXhBcnJheSA9IGRhdGEuYW5zd2VyLnNwbGl0KFwiO1wiKTtcbiAgICAgICAgfVxuICAgICAgICBpZiAodGhpcy5jY0FycmF5ID09PSB1bmRlZmluZWQpIHtcbiAgICAgICAgICAgIHRoaXMubW9kaWZ5Q2xpY2thYmxlcyh0aGlzLm5ld0Rpdi5jaGlsZE5vZGVzKTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIC8vIEZvciB1c2Ugd2l0aCBTcGhpbngtcmVuZGVyZWQgSFRNTFxuICAgICAgICAgICAgdGhpcy5jY0NvdW50ZXIgPSAwO1xuICAgICAgICAgICAgdGhpcy5jY0luZGV4ID0gMDtcbiAgICAgICAgICAgIHRoaXMuY2lJbmRleCA9IDA7XG4gICAgICAgICAgICBpZiAoIXRoaXMuaXNUYWJsZSkge1xuICAgICAgICAgICAgICAgIHRoaXMubW9kaWZ5VmlhQ0ModGhpcy5uZXdEaXYuY2hpbGRyZW4pO1xuICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICB0aGlzLm1vZGlmeVRhYmxlVmlhQ0ModGhpcy5uZXdEaXYuY2hpbGRyZW4pO1xuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgfVxuICAgIGNoZWNrTG9jYWxTdG9yYWdlKCkge1xuICAgICAgICBpZiAodGhpcy5ncmFkZXJhY3RpdmUpIHtcbiAgICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuICAgICAgICB2YXIgc3RvcmFnZU9iajtcbiAgICAgICAgLy8gR2V0cyBwcmV2aW91cyBhbnN3ZXIgZGF0YSBmcm9tIGxvY2FsIHN0b3JhZ2UgaWYgaXQgZXhpc3RzXG4gICAgICAgIHRoaXMuaGFzU3RvcmVkQW5zd2VycyA9IGZhbHNlO1xuICAgICAgICB2YXIgbGVuID0gbG9jYWxTdG9yYWdlLmxlbmd0aDtcbiAgICAgICAgaWYgKGxlbiA+IDApIHtcbiAgICAgICAgICAgIHZhciBleCA9IGxvY2FsU3RvcmFnZS5nZXRJdGVtKHRoaXMubG9jYWxTdG9yYWdlS2V5KCkpO1xuICAgICAgICAgICAgaWYgKGV4ICE9PSBudWxsKSB7XG4gICAgICAgICAgICAgICAgdGhpcy5oYXNTdG9yZWRBbnN3ZXJzID0gdHJ1ZTtcbiAgICAgICAgICAgICAgICB0cnkge1xuICAgICAgICAgICAgICAgICAgICBzdG9yYWdlT2JqID0gSlNPTi5wYXJzZShleCk7XG4gICAgICAgICAgICAgICAgICAgIHRoaXMuY2xpY2tlZEluZGV4QXJyYXkgPSBzdG9yYWdlT2JqLmFuc3dlci5zcGxpdChcIjtcIik7XG4gICAgICAgICAgICAgICAgfSBjYXRjaCAoZXJyKSB7XG4gICAgICAgICAgICAgICAgICAgIC8vIGVycm9yIHdoaWxlIHBhcnNpbmc7IGxpa2VseSBkdWUgdG8gYmFkIHZhbHVlIHN0b3JlZCBpbiBzdG9yYWdlXG4gICAgICAgICAgICAgICAgICAgIGNvbnNvbGUubG9nKGVyci5tZXNzYWdlKTtcbiAgICAgICAgICAgICAgICAgICAgbG9jYWxTdG9yYWdlLnJlbW92ZUl0ZW0odGhpcy5sb2NhbFN0b3JhZ2VLZXkoKSk7XG4gICAgICAgICAgICAgICAgICAgIHRoaXMuaGFzU3RvcmVkQW5zd2VycyA9IGZhbHNlO1xuICAgICAgICAgICAgICAgICAgICB0aGlzLnJlc3RvcmVBbnN3ZXJzKHt9KTtcbiAgICAgICAgICAgICAgICAgICAgcmV0dXJuO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICBpZiAodGhpcy51c2VSdW5lc3RvbmVTZXJ2aWNlcykge1xuICAgICAgICAgICAgICAgICAgICAvLyBsb2cgYW5zd2VyIHRvIHNlcnZlclxuICAgICAgICAgICAgICAgICAgICB0aGlzLmdpdmVuSW5kZXhBcnJheSA9IFtdO1xuICAgICAgICAgICAgICAgICAgICBmb3IgKHZhciBpID0gMDsgaSA8IHRoaXMuY2xpY2thYmxlQXJyYXkubGVuZ3RoOyBpKyspIHtcbiAgICAgICAgICAgICAgICAgICAgICAgIGlmIChcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAkKHRoaXMuY2xpY2thYmxlQXJyYXlbaV0pLmhhc0NsYXNzKFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBcImNsaWNrYWJsZS1jbGlja2VkXCJcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICApXG4gICAgICAgICAgICAgICAgICAgICAgICApIHtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICB0aGlzLmdpdmVuSW5kZXhBcnJheS5wdXNoKGkpO1xuICAgICAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgICAgIHRoaXMubG9nQm9va0V2ZW50KHtcbiAgICAgICAgICAgICAgICAgICAgICAgIGV2ZW50OiBcImNsaWNrYWJsZUFyZWFcIixcbiAgICAgICAgICAgICAgICAgICAgICAgIGFjdDogdGhpcy5jbGlja2VkSW5kZXhBcnJheS5qb2luKFwiO1wiKSxcbiAgICAgICAgICAgICAgICAgICAgICAgIGRpdl9pZDogdGhpcy5kaXZpZCxcbiAgICAgICAgICAgICAgICAgICAgICAgIGNvcnJlY3Q6IHN0b3JhZ2VPYmouY29ycmVjdCxcbiAgICAgICAgICAgICAgICAgICAgfSk7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICAgIHRoaXMucmVzdG9yZUFuc3dlcnMoe30pOyAvLyBwYXNzIGVtcHR5IG9iamVjdFxuICAgIH1cbiAgICBzZXRMb2NhbFN0b3JhZ2UoZGF0YSkge1xuICAgICAgICAvLyBBcnJheSBvZiB0aGUgaW5kaWNlcyBvZiBjbGlja2VkIGVsZW1lbnRzIGlzIHBhc3NlZCB0byBsb2NhbCBzdG9yYWdlXG4gICAgICAgIHZhciBhbnN3ZXI7XG4gICAgICAgIGlmIChkYXRhLmFuc3dlciAhPT0gdW5kZWZpbmVkKSB7XG4gICAgICAgICAgICAvLyBJZiB3ZSBnb3QgZGF0YSBmcm9tIHRoZSBzZXJ2ZXIsIHdlIGNhbiBqdXN0IHVzZSB0aGF0XG4gICAgICAgICAgICBhbnN3ZXIgPSB0aGlzLmNsaWNrZWRJbmRleEFycmF5LmpvaW4oXCI7XCIpO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgdGhpcy5naXZlbkluZGV4QXJyYXkgPSBbXTtcbiAgICAgICAgICAgIGZvciAodmFyIGkgPSAwOyBpIDwgdGhpcy5jbGlja2FibGVBcnJheS5sZW5ndGg7IGkrKykge1xuICAgICAgICAgICAgICAgIGlmICgkKHRoaXMuY2xpY2thYmxlQXJyYXlbaV0pLmhhc0NsYXNzKFwiY2xpY2thYmxlLWNsaWNrZWRcIikpIHtcbiAgICAgICAgICAgICAgICAgICAgdGhpcy5naXZlbkluZGV4QXJyYXkucHVzaChpKTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICBhbnN3ZXIgPSB0aGlzLmdpdmVuSW5kZXhBcnJheS5qb2luKFwiO1wiKTtcbiAgICAgICAgfVxuICAgICAgICB2YXIgdGltZVN0YW1wID0gbmV3IERhdGUoKTtcbiAgICAgICAgdmFyIGNvcnJlY3QgPSBkYXRhLmNvcnJlY3Q7XG4gICAgICAgIHZhciBzdG9yYWdlT2JqZWN0ID0ge1xuICAgICAgICAgICAgYW5zd2VyOiBhbnN3ZXIsXG4gICAgICAgICAgICBjb3JyZWN0OiBjb3JyZWN0LFxuICAgICAgICAgICAgdGltZXN0YW1wOiB0aW1lU3RhbXAsXG4gICAgICAgIH07XG4gICAgICAgIGxvY2FsU3RvcmFnZS5zZXRJdGVtKFxuICAgICAgICAgICAgdGhpcy5sb2NhbFN0b3JhZ2VLZXkoKSxcbiAgICAgICAgICAgIEpTT04uc3RyaW5naWZ5KHN0b3JhZ2VPYmplY3QpXG4gICAgICAgICk7XG4gICAgfVxuICAgIC8qPT09PT09PT09PT09PT09PT09PT09PT09PT1cbiAgICA9PT0gQXV4aWxsaWFyeSBmdW5jdGlvbnMgPT09XG4gICAgPT09PT09PT09PT09PT09PT09PT09PT09PT0qL1xuICAgIG1vZGlmeUNsaWNrYWJsZXMoY2hpbGROb2Rlcykge1xuICAgICAgICAvLyBTdHJpcHMgdGhlIGRhdGEtY29ycmVjdC9kYXRhLWluY29ycmVjdCBsYWJlbHMgYW5kIHVwZGF0ZXMgdGhlIGNvcnJlY3QvaW5jb3JyZWN0IGFycmF5c1xuICAgICAgICBmb3IgKHZhciBpID0gMDsgaSA8IGNoaWxkTm9kZXMubGVuZ3RoOyBpKyspIHtcbiAgICAgICAgICAgIGlmIChcbiAgICAgICAgICAgICAgICAkKGNoaWxkTm9kZXNbaV0pLmlzKFwiW2RhdGEtY29ycmVjdF1cIikgfHxcbiAgICAgICAgICAgICAgICAkKGNoaWxkTm9kZXNbaV0pLmlzKFwiW2RhdGEtaW5jb3JyZWN0XVwiKVxuICAgICAgICAgICAgKSB7XG4gICAgICAgICAgICAgICAgdGhpcy5tYW5hZ2VOZXdDbGlja2FibGUoY2hpbGROb2Rlc1tpXSk7XG4gICAgICAgICAgICAgICAgaWYgKCQoY2hpbGROb2Rlc1tpXSkuaXMoXCJbZGF0YS1jb3JyZWN0XVwiKSkge1xuICAgICAgICAgICAgICAgICAgICAkKGNoaWxkTm9kZXNbaV0pLnJlbW92ZUF0dHIoXCJkYXRhLWNvcnJlY3RcIik7XG4gICAgICAgICAgICAgICAgICAgIHRoaXMuY29ycmVjdEFycmF5LnB1c2goY2hpbGROb2Rlc1tpXSk7XG4gICAgICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICAgICAgJChjaGlsZE5vZGVzW2ldKS5yZW1vdmVBdHRyKFwiZGF0YS1pbmNvcnJlY3RcIik7XG4gICAgICAgICAgICAgICAgICAgIHRoaXMuaW5jb3JyZWN0QXJyYXkucHVzaChjaGlsZE5vZGVzW2ldKTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICBpZiAoY2hpbGROb2Rlc1tpXS5jaGlsZE5vZGVzLmxlbmd0aCAhPT0gMCkge1xuICAgICAgICAgICAgICAgIHRoaXMubW9kaWZ5Q2xpY2thYmxlcyhjaGlsZE5vZGVzW2ldLmNoaWxkTm9kZXMpO1xuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgfVxuICAgIG1vZGlmeVZpYUNDKGNoaWxkcmVuKSB7XG4gICAgICAgIGZvciAodmFyIGkgPSAwOyBpIDwgY2hpbGRyZW4ubGVuZ3RoOyBpKyspIHtcbiAgICAgICAgICAgIGlmIChjaGlsZHJlbltpXS5jaGlsZHJlbi5sZW5ndGggIT09IDApIHtcbiAgICAgICAgICAgICAgICB0aGlzLm1vZGlmeVZpYUNDKGNoaWxkcmVuW2ldLmNoaWxkcmVuKTtcbiAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgdGhpcy5jY0NvdW50ZXIrKztcbiAgICAgICAgICAgICAgICBpZiAodGhpcy5jY0NvdW50ZXIgPT09IE1hdGguZmxvb3IodGhpcy5jY0FycmF5W3RoaXMuY2NJbmRleF0pKSB7XG4gICAgICAgICAgICAgICAgICAgIHRoaXMubWFuYWdlTmV3Q2xpY2thYmxlKGNoaWxkcmVuW2ldKTtcbiAgICAgICAgICAgICAgICAgICAgdGhpcy5jb3JyZWN0QXJyYXkucHVzaChjaGlsZHJlbltpXSk7XG4gICAgICAgICAgICAgICAgICAgIHRoaXMuY2NJbmRleCsrO1xuICAgICAgICAgICAgICAgIH0gZWxzZSBpZiAoXG4gICAgICAgICAgICAgICAgICAgIHRoaXMuY2NDb3VudGVyID09PSBNYXRoLmZsb29yKHRoaXMuY2lBcnJheVt0aGlzLmNpSW5kZXhdKVxuICAgICAgICAgICAgICAgICkge1xuICAgICAgICAgICAgICAgICAgICB0aGlzLm1hbmFnZU5ld0NsaWNrYWJsZShjaGlsZHJlbltpXSk7XG4gICAgICAgICAgICAgICAgICAgIHRoaXMuaW5jb3JyZWN0QXJyYXkucHVzaChjaGlsZHJlbltpXSk7XG4gICAgICAgICAgICAgICAgICAgIHRoaXMuY2lJbmRleCsrO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgIH1cbiAgICBtb2RpZnlUYWJsZVZpYUNDKGNoaWxkcmVuKSB7XG4gICAgICAgIC8vIHRhYmxlIHZlcnNpb24gb2YgbW9kaWZ5VmlhQ0NcbiAgICAgICAgdmFyIHRDb21wb25lbnRBcnIgPSBbXTtcbiAgICAgICAgZm9yIChsZXQgaSA9IDA7IGkgPCBjaGlsZHJlbi5sZW5ndGg7IGkrKykge1xuICAgICAgICAgICAgaWYgKGNoaWxkcmVuW2ldLm5vZGVOYW1lID09PSBcIlRBQkxFXCIpIHtcbiAgICAgICAgICAgICAgICBsZXQgdG1wID0gY2hpbGRyZW5baV07XG4gICAgICAgICAgICAgICAgZm9yIChsZXQgaiA9IDA7IGogPCB0bXAuY2hpbGRyZW4ubGVuZ3RoOyBqKyspIHtcbiAgICAgICAgICAgICAgICAgICAgaWYgKHRtcC5jaGlsZHJlbltqXS5ub2RlTmFtZSA9PT0gXCJUSEVBRFwiKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICB0Q29tcG9uZW50QXJyLnB1c2godG1wLmNoaWxkcmVuW2pdKTtcbiAgICAgICAgICAgICAgICAgICAgfSBlbHNlIGlmICh0bXAuY2hpbGRyZW5bal0ubm9kZU5hbWUgPT09IFwiVEJPRFlcIikge1xuICAgICAgICAgICAgICAgICAgICAgICAgdENvbXBvbmVudEFyci5wdXNoKHRtcC5jaGlsZHJlbltqXSk7XG4gICAgICAgICAgICAgICAgICAgIH0gZWxzZSBpZiAodG1wLmNoaWxkcmVuW2pdLm5vZGVOYW1lID09PSBcIlRGT09UXCIpIHtcbiAgICAgICAgICAgICAgICAgICAgICAgIHRDb21wb25lbnRBcnIucHVzaCh0bXAuY2hpbGRyZW5bal0pO1xuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICAgIGZvciAodmFyIHQgPSAwOyB0IDwgdENvbXBvbmVudEFyci5sZW5ndGg7IHQrKykge1xuICAgICAgICAgICAgZm9yIChsZXQgaSA9IDA7IGkgPCB0Q29tcG9uZW50QXJyW3RdLmNoaWxkcmVuLmxlbmd0aDsgaSsrKSB7XG4gICAgICAgICAgICAgICAgdGhpcy5jY0NvdW50ZXIrKztcbiAgICAgICAgICAgICAgICAvLyBGaXJzdCBjaGVjayBpZiB0aGUgZW50aXJlIHJvdyBuZWVkcyB0byBiZSBjbGlja2FibGVcbiAgICAgICAgICAgICAgICBpZiAoXG4gICAgICAgICAgICAgICAgICAgIHRoaXMuY2NJbmRleCA8IHRoaXMuY2NBcnJheS5sZW5ndGggJiZcbiAgICAgICAgICAgICAgICAgICAgdGhpcy5jY0NvdW50ZXIgPT09XG4gICAgICAgICAgICAgICAgICAgIE1hdGguZmxvb3IodGhpcy5jY0FycmF5W3RoaXMuY2NJbmRleF0uc3BsaXQoXCIsXCIpWzBdKSAmJlxuICAgICAgICAgICAgICAgICAgICBNYXRoLmZsb29yKHRoaXMuY2NBcnJheVt0aGlzLmNjSW5kZXhdLnNwbGl0KFwiLFwiKVsxXSkgPT09IDBcbiAgICAgICAgICAgICAgICApIHtcbiAgICAgICAgICAgICAgICAgICAgdGhpcy5tYW5hZ2VOZXdDbGlja2FibGUodENvbXBvbmVudEFyclt0XS5jaGlsZHJlbltpXSk7XG4gICAgICAgICAgICAgICAgICAgIHRoaXMuY29ycmVjdEFycmF5LnB1c2godENvbXBvbmVudEFyclt0XS5jaGlsZHJlbltpXSk7XG4gICAgICAgICAgICAgICAgICAgIHRoaXMuY2NJbmRleCsrO1xuICAgICAgICAgICAgICAgIH0gZWxzZSBpZiAoXG4gICAgICAgICAgICAgICAgICAgIHRoaXMuY2lJbmRleCA8IHRoaXMuY2lBcnJheS5sZW5ndGggJiZcbiAgICAgICAgICAgICAgICAgICAgdGhpcy5jY0NvdW50ZXIgPT09XG4gICAgICAgICAgICAgICAgICAgIE1hdGguZmxvb3IodGhpcy5jaUFycmF5W3RoaXMuY2lJbmRleF0uc3BsaXQoXCIsXCIpWzBdKSAmJlxuICAgICAgICAgICAgICAgICAgICBNYXRoLmZsb29yKHRoaXMuY2lBcnJheVt0aGlzLmNpSW5kZXhdLnNwbGl0KFwiLFwiKVsxXSkgPT09IDBcbiAgICAgICAgICAgICAgICApIHtcbiAgICAgICAgICAgICAgICAgICAgdGhpcy5tYW5hZ2VOZXdDbGlja2FibGUodENvbXBvbmVudEFyclt0XS5jaGlsZHJlbltpXSk7XG4gICAgICAgICAgICAgICAgICAgIHRoaXMuaW5jb3JyZWN0QXJyYXkucHVzaCh0Q29tcG9uZW50QXJyW3RdLmNoaWxkcmVuW2ldKTtcbiAgICAgICAgICAgICAgICAgICAgdGhpcy5jaUluZGV4Kys7XG4gICAgICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICAgICAgLy8gSWYgbm90LCBjaGVjayB0aGUgaW5kaXZpZHVhbCBkYXRhIGNlbGxzXG4gICAgICAgICAgICAgICAgICAgIGZvciAoXG4gICAgICAgICAgICAgICAgICAgICAgICBsZXQgaiA9IDA7XG4gICAgICAgICAgICAgICAgICAgICAgICBqIDwgdENvbXBvbmVudEFyclt0XS5jaGlsZHJlbltpXS5jaGlsZHJlbi5sZW5ndGg7XG4gICAgICAgICAgICAgICAgICAgICAgICBqKytcbiAgICAgICAgICAgICAgICAgICAgKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICBsZXQgdG1wID0gaiArIDE7XG4gICAgICAgICAgICAgICAgICAgICAgICBpZiAoXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy5jY0luZGV4IDwgdGhpcy5jY0FycmF5Lmxlbmd0aCAmJlxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIHRtcCA9PT1cbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBNYXRoLmZsb29yKFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB0aGlzLmNjQXJyYXlbdGhpcy5jY0luZGV4XS5zcGxpdChcIixcIilbMV1cbiAgICAgICAgICAgICAgICAgICAgICAgICAgICApICYmXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy5jY0NvdW50ZXIgPT09XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgTWF0aC5mbG9vcihcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy5jY0FycmF5W3RoaXMuY2NJbmRleF0uc3BsaXQoXCIsXCIpWzBdXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgKVxuICAgICAgICAgICAgICAgICAgICAgICAgKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy5tYW5hZ2VOZXdDbGlja2FibGUoXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHRDb21wb25lbnRBcnJbdF0uY2hpbGRyZW5baV0uY2hpbGRyZW5bal1cbiAgICAgICAgICAgICAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIHRoaXMuY29ycmVjdEFycmF5LnB1c2goXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHRDb21wb25lbnRBcnJbdF0uY2hpbGRyZW5baV0uY2hpbGRyZW5bal1cbiAgICAgICAgICAgICAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIHRoaXMuY2NJbmRleCsrO1xuICAgICAgICAgICAgICAgICAgICAgICAgfSBlbHNlIGlmIChcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICB0aGlzLmNpSW5kZXggPCB0aGlzLmNpQXJyYXkubGVuZ3RoICYmXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgdG1wID09PVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIE1hdGguZmxvb3IoXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHRoaXMuY2lBcnJheVt0aGlzLmNpSW5kZXhdLnNwbGl0KFwiLFwiKVsxXVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICkgJiZcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICB0aGlzLmNjQ291bnRlciA9PT1cbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBNYXRoLmZsb29yKFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB0aGlzLmNpQXJyYXlbdGhpcy5jaUluZGV4XS5zcGxpdChcIixcIilbMF1cbiAgICAgICAgICAgICAgICAgICAgICAgICAgICApXG4gICAgICAgICAgICAgICAgICAgICAgICApIHtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICB0aGlzLm1hbmFnZU5ld0NsaWNrYWJsZShcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgdENvbXBvbmVudEFyclt0XS5jaGlsZHJlbltpXS5jaGlsZHJlbltqXVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICk7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy5pbmNvcnJlY3RBcnJheS5wdXNoKFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB0Q29tcG9uZW50QXJyW3RdLmNoaWxkcmVuW2ldLmNoaWxkcmVuW2pdXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgKTtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICB0aGlzLmNpSW5kZXgrKztcbiAgICAgICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgIH1cbiAgICBtYW5hZ2VOZXdDbGlja2FibGUoY2xpY2thYmxlKSB7XG4gICAgICAgIC8vIGFkZHMgdGhlIFwiY2xpY2thYmxlXCIgZnVuY3Rpb25hbGl0eVxuICAgICAgICAkKGNsaWNrYWJsZSkuYWRkQ2xhc3MoXCJjbGlja2FibGVcIik7XG4gICAgICAgIGlmICh0aGlzLmhhc1N0b3JlZEFuc3dlcnMpIHtcbiAgICAgICAgICAgIC8vIENoZWNrIGlmIHRoZSBlbGVtZW50IHdlJ3JlIGFib3V0IHRvIGFwcGVuZCB0byB0aGUgcHJlIHdhcyBpbiBsb2NhbCBzdG9yYWdlIGFzIGNsaWNrZWQgdmlhIGl0cyBpbmRleFxuICAgICAgICAgICAgaWYgKFxuICAgICAgICAgICAgICAgIHRoaXMuY2xpY2tlZEluZGV4QXJyYXlbdGhpcy5jbGlja0luZGV4XS50b1N0cmluZygpID09PVxuICAgICAgICAgICAgICAgIHRoaXMuY2xpY2thYmxlQ291bnRlci50b1N0cmluZygpXG4gICAgICAgICAgICApIHtcbiAgICAgICAgICAgICAgICAkKGNsaWNrYWJsZSkuYWRkQ2xhc3MoXCJjbGlja2FibGUtY2xpY2tlZFwiKTtcbiAgICAgICAgICAgICAgICB0aGlzLmNsaWNrSW5kZXgrKztcbiAgICAgICAgICAgICAgICBpZiAodGhpcy5jbGlja0luZGV4ID09PSB0aGlzLmNsaWNrZWRJbmRleEFycmF5Lmxlbmd0aCkge1xuICAgICAgICAgICAgICAgICAgICAvLyBTdG9wIGRvaW5nIHRoaXMgaWYgdGhlIGluZGV4IGFycmF5IGlzIHVzZWQgdXBcbiAgICAgICAgICAgICAgICAgICAgdGhpcy5oYXNTdG9yZWRBbnN3ZXJzID0gZmFsc2U7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICAgIGxldCBzZWxmID0gdGhpcztcbiAgICAgICAgY2xpY2thYmxlLm9uY2xpY2sgPSBmdW5jdGlvbiAoKSB7XG4gICAgICAgICAgICBzZWxmLmlzQW5zd2VyZWQgPSB0cnVlO1xuICAgICAgICAgICAgaWYgKCQodGhpcykuaGFzQ2xhc3MoXCJjbGlja2FibGUtY2xpY2tlZFwiKSkge1xuICAgICAgICAgICAgICAgICQodGhpcykucmVtb3ZlQ2xhc3MoXCJjbGlja2FibGUtY2xpY2tlZFwiKTtcbiAgICAgICAgICAgICAgICAkKHRoaXMpLnJlbW92ZUNsYXNzKFwiY2xpY2thYmxlLWluY29ycmVjdFwiKTtcbiAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgJCh0aGlzKS5hZGRDbGFzcyhcImNsaWNrYWJsZS1jbGlja2VkXCIpO1xuICAgICAgICAgICAgfVxuICAgICAgICB9O1xuICAgICAgICB0aGlzLmNsaWNrYWJsZUFycmF5LnB1c2goY2xpY2thYmxlKTtcbiAgICAgICAgdGhpcy5jbGlja2FibGVDb3VudGVyKys7XG4gICAgfVxuICAgIC8qPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT1cbiAgICA9PSBFdmFsdWF0aW9uIGFuZCBkaXNwbGF5aW5nIGZlZWRiYWNrID09XG4gICAgPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT0qL1xuICAgIGNoZWNrQ3VycmVudEFuc3dlcigpIHtcbiAgICAgICAgLy8gRXZhbHVhdGlvbiBpcyBkb25lIGJ5IGl0ZXJhdGluZyBvdmVyIHRoZSBjb3JyZWN0L2luY29ycmVjdCBhcnJheXMgYW5kIGNoZWNraW5nIGJ5IGNsYXNzXG4gICAgICAgIHRoaXMuY29ycmVjdCA9IHRydWU7XG4gICAgICAgIHRoaXMuY29ycmVjdE51bSA9IDA7XG4gICAgICAgIHRoaXMuaW5jb3JyZWN0TnVtID0gMDtcbiAgICAgICAgZm9yIChsZXQgaSA9IDA7IGkgPCB0aGlzLmNvcnJlY3RBcnJheS5sZW5ndGg7IGkrKykge1xuICAgICAgICAgICAgaWYgKCEkKHRoaXMuY29ycmVjdEFycmF5W2ldKS5oYXNDbGFzcyhcImNsaWNrYWJsZS1jbGlja2VkXCIpKSB7XG4gICAgICAgICAgICAgICAgdGhpcy5jb3JyZWN0ID0gZmFsc2U7XG4gICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgIHRoaXMuY29ycmVjdE51bSsrO1xuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICAgIGZvciAobGV0IGkgPSAwOyBpIDwgdGhpcy5pbmNvcnJlY3RBcnJheS5sZW5ndGg7IGkrKykge1xuICAgICAgICAgICAgaWYgKCQodGhpcy5pbmNvcnJlY3RBcnJheVtpXSkuaGFzQ2xhc3MoXCJjbGlja2FibGUtY2xpY2tlZFwiKSkge1xuICAgICAgICAgICAgICAgIHRoaXMuY29ycmVjdCA9IGZhbHNlO1xuICAgICAgICAgICAgICAgIHRoaXMuaW5jb3JyZWN0TnVtKys7XG4gICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgICQodGhpcy5pbmNvcnJlY3RBcnJheVtpXSkucmVtb3ZlQ2xhc3MoXCJjbGlja2FibGUtaW5jb3JyZWN0XCIpO1xuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICAgIHRoaXMucGVyY2VudCA9XG4gICAgICAgICAgICAodGhpcy5jb3JyZWN0TnVtIC0gdGhpcy5pbmNvcnJlY3ROdW0pIC8gdGhpcy5jb3JyZWN0QXJyYXkubGVuZ3RoO1xuICAgICAgICB0aGlzLnNldExvY2FsU3RvcmFnZSh7IGNvcnJlY3Q6IHRoaXMuY29ycmVjdCA/IFwiVFwiIDogXCJGXCIgfSk7XG4gICAgfVxuXG4gICAgYXN5bmMgbG9nQ3VycmVudEFuc3dlcihzaWQpIHtcbiAgICAgICAgbGV0IGRhdGEgPSB7XG4gICAgICAgICAgICBldmVudDogXCJjbGlja2FibGVBcmVhXCIsXG4gICAgICAgICAgICBhY3Q6IHRoaXMuZ2l2ZW5JbmRleEFycmF5LmpvaW4oXCI7XCIpLFxuICAgICAgICAgICAgZGl2X2lkOiB0aGlzLmRpdmlkLFxuICAgICAgICAgICAgY29ycmVjdDogdGhpcy5jb3JyZWN0ID8gXCJUXCIgOiBcIkZcIixcbiAgICAgICAgfTtcbiAgICAgICAgaWYgKHR5cGVvZiBzaWQgIT09IFwidW5kZWZpbmVkXCIpIHtcbiAgICAgICAgICAgIGRhdGEuc2lkID0gc2lkO1xuICAgICAgICB9XG4gICAgICAgIGF3YWl0IHRoaXMubG9nQm9va0V2ZW50KGRhdGEpO1xuICAgIH1cblxuICAgIHJlbmRlckZlZWRiYWNrKCkge1xuICAgICAgICBpZiAodGhpcy5jb3JyZWN0KSB7XG4gICAgICAgICAgICAkKHRoaXMuZmVlZEJhY2tEaXYpLmh0bWwoXCJZb3UgYXJlIENvcnJlY3QhXCIpO1xuICAgICAgICAgICAgJCh0aGlzLmZlZWRCYWNrRGl2KS5hdHRyKFwiY2xhc3NcIiwgXCJhbGVydCBhbGVydC1pbmZvXCIpO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgZm9yIChsZXQgaSA9IDA7IGkgPCB0aGlzLmluY29ycmVjdEFycmF5Lmxlbmd0aDsgaSsrKSB7XG4gICAgICAgICAgICAgICAgaWYgKCQodGhpcy5pbmNvcnJlY3RBcnJheVtpXSkuaGFzQ2xhc3MoXCJjbGlja2FibGUtY2xpY2tlZFwiKSkge1xuICAgICAgICAgICAgICAgICAgICAkKHRoaXMuaW5jb3JyZWN0QXJyYXlbaV0pLmFkZENsYXNzKFwiY2xpY2thYmxlLWluY29ycmVjdFwiKTtcbiAgICAgICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgICAgICAkKHRoaXMuaW5jb3JyZWN0QXJyYXlbaV0pLnJlbW92ZUNsYXNzKFxuICAgICAgICAgICAgICAgICAgICAgICAgXCJjbGlja2FibGUtaW5jb3JyZWN0XCJcbiAgICAgICAgICAgICAgICAgICAgKTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICAkKHRoaXMuZmVlZEJhY2tEaXYpLmh0bWwoXG4gICAgICAgICAgICAgICAgXCJJbmNvcnJlY3QuIFlvdSBjbGlja2VkIG9uIFwiICtcbiAgICAgICAgICAgICAgICB0aGlzLmNvcnJlY3ROdW0gK1xuICAgICAgICAgICAgICAgIFwiIG9mIHRoZSBcIiArXG4gICAgICAgICAgICAgICAgdGhpcy5jb3JyZWN0QXJyYXkubGVuZ3RoLnRvU3RyaW5nKCkgK1xuICAgICAgICAgICAgICAgIFwiIGNvcnJlY3QgZWxlbWVudHMgYW5kIFwiICtcbiAgICAgICAgICAgICAgICB0aGlzLmluY29ycmVjdE51bSArXG4gICAgICAgICAgICAgICAgXCIgb2YgdGhlIFwiICtcbiAgICAgICAgICAgICAgICB0aGlzLmluY29ycmVjdEFycmF5Lmxlbmd0aC50b1N0cmluZygpICtcbiAgICAgICAgICAgICAgICBcIiBpbmNvcnJlY3QgZWxlbWVudHMuIFwiICtcbiAgICAgICAgICAgICAgICB0aGlzLmZlZWRiYWNrXG4gICAgICAgICAgICApO1xuICAgICAgICAgICAgJCh0aGlzLmZlZWRCYWNrRGl2KS5hdHRyKFwiY2xhc3NcIiwgXCJhbGVydCBhbGVydC1kYW5nZXJcIik7XG4gICAgICAgIH1cbiAgICB9XG5cbiAgICBkaXNhYmxlSW50ZXJhY3Rpb24oKSB7XG4gICAgICAgIGZvciAodmFyIGkgPSAwOyBpIDwgdGhpcy5jbGlja2FibGVBcnJheS5sZW5ndGg7IGkrKykge1xuICAgICAgICAgICAgJCh0aGlzLmNsaWNrYWJsZUFycmF5W2ldKS5jc3MoXCJjdXJzb3JcIiwgXCJpbml0aWFsXCIpO1xuICAgICAgICAgICAgdGhpcy5jbGlja2FibGVBcnJheVtpXS5vbmNsaWNrID0gZnVuY3Rpb24gKCkge1xuICAgICAgICAgICAgICAgIHJldHVybjtcbiAgICAgICAgICAgIH07XG4gICAgICAgIH1cbiAgICB9XG59XG5cbi8qPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09XG49PSBGaW5kIHRoZSBjdXN0b20gSFRNTCB0YWdzIGFuZCA9PVxuPT0gICBleGVjdXRlIG91ciBjb2RlIG9uIHRoZW0gICAgPT1cbj09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PSovXG4kKGRvY3VtZW50KS5iaW5kKFwicnVuZXN0b25lOmxvZ2luLWNvbXBsZXRlXCIsIGZ1bmN0aW9uICgpIHtcbiAgICAkKFwiW2RhdGEtY29tcG9uZW50PWNsaWNrYWJsZWFyZWFdXCIpLmVhY2goZnVuY3Rpb24gKGluZGV4KSB7XG4gICAgICAgIGlmICgkKHRoaXMpLmNsb3Nlc3QoXCJbZGF0YS1jb21wb25lbnQ9dGltZWRBc3Nlc3NtZW50XVwiKS5sZW5ndGggPT0gMCkge1xuICAgICAgICAgICAgLy8gSWYgdGhpcyBlbGVtZW50IGV4aXN0cyB3aXRoaW4gYSB0aW1lZCBjb21wb25lbnQsIGRvbid0IHJlbmRlciBpdCBoZXJlXG4gICAgICAgICAgICB0cnkge1xuICAgICAgICAgICAgICAgIENBTGlzdFt0aGlzLmlkXSA9IG5ldyBDbGlja2FibGVBcmVhKHtcbiAgICAgICAgICAgICAgICAgICAgb3JpZzogdGhpcyxcbiAgICAgICAgICAgICAgICAgICAgdXNlUnVuZXN0b25lU2VydmljZXM6IGVCb29rQ29uZmlnLnVzZVJ1bmVzdG9uZVNlcnZpY2VzLFxuICAgICAgICAgICAgICAgIH0pO1xuICAgICAgICAgICAgfSBjYXRjaCAoZXJyKSB7XG4gICAgICAgICAgICAgICAgY29uc29sZS5sb2coYEVycm9yIHJlbmRlcmluZyBDbGlja2FibGVBcmVhIFByb2JsZW0gJHt0aGlzLmlkfVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICBEZXRhaWxzOiAke2Vycn1gKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgIH0pO1xufSk7XG4iLCJpbXBvcnQgQ2xpY2thYmxlQXJlYSBmcm9tIFwiLi9jbGlja2FibGUuanNcIjtcblxuKFwidXNlIHN0cmljdFwiKTtcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgVGltZWRDbGlja2FibGVBcmVhIGV4dGVuZHMgQ2xpY2thYmxlQXJlYSB7XG4gICAgY29uc3RydWN0b3Iob3B0cykge1xuICAgICAgICBzdXBlcihvcHRzKTtcbiAgICAgICAgdGhpcy5yZXN0b3JlQW5zd2Vycyh7fSk7XG4gICAgICAgIHRoaXMucmVuZGVyVGltZWRJY29uKHRoaXMuY29udGFpbmVyRGl2KTtcbiAgICAgICAgdGhpcy5oaWRlQnV0dG9ucygpO1xuICAgIH1cblxuICAgIGhpZGVCdXR0b25zKCkge1xuICAgICAgICAkKHRoaXMuc3VibWl0QnV0dG9uKS5oaWRlKCk7XG4gICAgfVxuXG4gICAgcmVuZGVyVGltZWRJY29uKGNvbXBvbmVudCkge1xuICAgICAgICAvLyByZW5kZXJzIHRoZSBjbG9jayBpY29uIG9uIHRpbWVkIGNvbXBvbmVudHMuICAgIFRoZSBjb21wb25lbnQgcGFyYW1ldGVyXG4gICAgICAgIC8vIGlzIHRoZSBlbGVtZW50IHRoYXQgdGhlIGljb24gc2hvdWxkIGJlIGFwcGVuZGVkIHRvLlxuICAgICAgICB2YXIgdGltZUljb25EaXYgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KFwiZGl2XCIpO1xuICAgICAgICB2YXIgdGltZUljb24gPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KFwiaW1nXCIpO1xuICAgICAgICAkKHRpbWVJY29uKS5hdHRyKHtcbiAgICAgICAgICAgIHNyYzogXCIuLi9fc3RhdGljL2Nsb2NrLnBuZ1wiLFxuICAgICAgICAgICAgc3R5bGU6IFwid2lkdGg6MTVweDtoZWlnaHQ6MTVweFwiLFxuICAgICAgICB9KTtcbiAgICAgICAgdGltZUljb25EaXYuY2xhc3NOYW1lID0gXCJ0aW1lVGlwXCI7XG4gICAgICAgIHRpbWVJY29uRGl2LnRpdGxlID0gXCJcIjtcbiAgICAgICAgdGltZUljb25EaXYuYXBwZW5kQ2hpbGQodGltZUljb24pO1xuICAgICAgICAkKGNvbXBvbmVudCkucHJlcGVuZCh0aW1lSWNvbkRpdik7XG4gICAgfVxuXG4gICAgY2hlY2tDb3JyZWN0VGltZWQoKSB7XG4gICAgICAgIC8vIFJldHVybnMgaWYgdGhlIHF1ZXN0aW9uIHdhcyBjb3JyZWN0LCBpbmNvcnJlY3QsIG9yIHNraXBwZWQgKHJldHVybiBudWxsIGluIHRoZSBsYXN0IGNhc2UpXG4gICAgICAgIGlmICh0aGlzLmNvcnJlY3ROdW0gPT09IDAgJiYgdGhpcy5pbmNvcnJlY3ROdW0gPT09IDApIHtcbiAgICAgICAgICAgIHRoaXMuY29ycmVjdCA9IG51bGw7XG4gICAgICAgIH1cbiAgICAgICAgc3dpdGNoICh0aGlzLmNvcnJlY3QpIHtcbiAgICAgICAgICAgIGNhc2UgdHJ1ZTpcbiAgICAgICAgICAgICAgICByZXR1cm4gXCJUXCI7XG4gICAgICAgICAgICBjYXNlIGZhbHNlOlxuICAgICAgICAgICAgICAgIHJldHVybiBcIkZcIjtcbiAgICAgICAgICAgIGRlZmF1bHQ6XG4gICAgICAgICAgICAgICAgcmV0dXJuIG51bGw7XG4gICAgICAgIH1cbiAgICB9XG5cbiAgICBoaWRlRmVlZGJhY2soKSB7XG4gICAgICAgICQodGhpcy5mZWVkQmFja0RpdikuaGlkZSgpO1xuICAgIH1cbn1cblxuaWYgKHR5cGVvZiB3aW5kb3cuY29tcG9uZW50X2ZhY3RvcnkgPT09IFwidW5kZWZpbmVkXCIpIHtcbiAgICB3aW5kb3cuY29tcG9uZW50X2ZhY3RvcnkgPSB7fTtcbn1cbndpbmRvdy5jb21wb25lbnRfZmFjdG9yeS5jbGlja2FibGVhcmVhID0gZnVuY3Rpb24gKG9wdHMpIHtcbiAgICBpZiAob3B0cy50aW1lZCkge1xuICAgICAgICByZXR1cm4gbmV3IFRpbWVkQ2xpY2thYmxlQXJlYShvcHRzKTtcbiAgICB9XG4gICAgcmV0dXJuIG5ldyBDbGlja2FibGVBcmVhKG9wdHMpO1xufTtcbiJdLCJzb3VyY2VSb290IjoiIn0=