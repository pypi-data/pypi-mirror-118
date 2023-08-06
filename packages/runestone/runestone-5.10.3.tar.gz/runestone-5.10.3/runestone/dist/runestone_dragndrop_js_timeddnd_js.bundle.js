(self["webpackChunkWebComponents"] = self["webpackChunkWebComponents"] || []).push([["runestone_dragndrop_js_timeddnd_js"],{

/***/ 80329:
/*!***********************************************!*\
  !*** ./runestone/dragndrop/css/dragndrop.css ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
// extracted by mini-css-extract-plugin


/***/ }),

/***/ 78273:
/*!*****************************************************!*\
  !*** ./runestone/dragndrop/js/dragndrop-i18n.en.js ***!
  \*****************************************************/
/***/ (() => {

$.i18n().load({
    en: {
        msg_dragndrop_correct_answer: "You are correct!",
        msg_dragndrop_incorrect_answer:
            "Incorret. You got $1 correct and $2 incorrect out of $3. You left $4 blank.",
        msg_dragndrop_check_me: "Check me",
        msg_dragndrop_reset: "Reset",
    },
});


/***/ }),

/***/ 26254:
/*!********************************************************!*\
  !*** ./runestone/dragndrop/js/dragndrop-i18n.pt-br.js ***!
  \********************************************************/
/***/ (() => {

$.i18n().load({
    "pt-br": {
        msg_dragndrop_correct_answer: "Correto!",
        msg_dragndrop_incorrect_answer:
            "Incorreto. Você teve $1 correto(s) e $2 incorreto(s) de $3. Você deixou $4 em branco.",
        msg_dragndrop_check_me: "Verificar",
        msg_dragndrop_reset: "Resetar",
    },
});


/***/ }),

/***/ 70225:
/*!*********************************************!*\
  !*** ./runestone/dragndrop/js/dragndrop.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ddList": () => (/* binding */ ddList),
/* harmony export */   "default": () => (/* binding */ DragNDrop)
/* harmony export */ });
/* harmony import */ var _common_js_runestonebase_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../common/js/runestonebase.js */ 2568);
/* harmony import */ var _css_dragndrop_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../css/dragndrop.css */ 80329);
/* harmony import */ var _dragndrop_i18n_en_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./dragndrop-i18n.en.js */ 78273);
/* harmony import */ var _dragndrop_i18n_en_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_dragndrop_i18n_en_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _dragndrop_i18n_pt_br_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./dragndrop-i18n.pt-br.js */ 26254);
/* harmony import */ var _dragndrop_i18n_pt_br_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_dragndrop_i18n_pt_br_js__WEBPACK_IMPORTED_MODULE_3__);
/*==========================================
=======     Master dragndrop.js     ========
============================================
===     This file contains the JS for    ===
=== the Runestone Drag n drop component. ===
============================================
===              Created by              ===
===           Isaiah Mayerchak           ===
===                7/6/15                ===
===              Brad MIller             ===
===                2/7/19                ===
==========================================*/







var ddList = {}; // Dictionary that contains all instances of dragndrop objects

class DragNDrop extends _common_js_runestonebase_js__WEBPACK_IMPORTED_MODULE_0__.default {
    constructor(opts) {
        super(opts);
        var orig = opts.orig; // entire <ul> element that will be replaced by new HTML
        this.origElem = orig;
        this.divid = orig.id;
        this.useRunestoneServices = opts.useRunestoneServices;
        this.random = false;
        if ($(this.origElem).is("[data-random]")) {
            this.random = true;
        }
        this.feedback = "";
        this.dragPairArray = [];
        this.question = "";
        this.populate(); // Populates this.dragPairArray, this.feedback and this.question
        this.createNewElements();
        this.caption = "Drag-N-Drop";
        this.addCaption("runestone");
    }
    /*======================
    === Update variables ===
    ======================*/
    populate() {
        for (var i = 0; i < this.origElem.childNodes.length; i++) {
            if (
                $(this.origElem.childNodes[i]).data("subcomponent") === "dropzone"
            ) {
                var tmp = $(this.origElem).find(
                    `#${$(this.origElem.childNodes[i]).attr("for")}`
                )[0];
                var replaceSpan = document.createElement("span");
                replaceSpan.innerHTML = tmp.innerHTML;
                replaceSpan.id = this.divid + tmp.id;
                $(replaceSpan).attr("draggable", "true");
                $(replaceSpan).addClass("draggable-drag");
                var otherReplaceSpan = document.createElement("span");
                otherReplaceSpan.innerHTML = this.origElem.childNodes[
                    i
                ].innerHTML;
                $(otherReplaceSpan).addClass("draggable-drop");
                this.setEventListeners(replaceSpan, otherReplaceSpan);
                var tmpArr = [];
                tmpArr.push(replaceSpan);
                tmpArr.push(otherReplaceSpan);
                this.dragPairArray.push(tmpArr);
            } else if (
                $(this.origElem.childNodes[i]).data("subcomponent") === "question"
            ) {
                this.question = this.origElem.childNodes[i].innerHTML;
            } else if (
                $(this.origElem.childNodes[i]).data("subcomponent") === "feedback"
            ) {
                this.feedback = this.origElem.childNodes[i].innerHTML;
            }
        }
    }
    /*========================================
    == Create new HTML elements and replace ==
    ==      original element with them      ==
    ========================================*/
    createNewElements() {
        this.containerDiv = document.createElement("div");
        this.containerDiv.id = this.divid;
        $(this.containerDiv).addClass(
            "alert alert-warning draggable-container"
        );
        $(this.containerDiv).text(this.question);
        this.containerDiv.appendChild(document.createElement("br"));
        this.dragDropWrapDiv = document.createElement("div"); // Holds the draggables/dropzones, prevents feedback from bleeding in
        $(this.dragDropWrapDiv).css("display", "block");
        this.containerDiv.appendChild(this.dragDropWrapDiv);
        this.draggableDiv = document.createElement("div");
        $(this.draggableDiv).addClass("rsdraggable dragzone");
        this.addDragDivListeners();
        this.dropZoneDiv = document.createElement("div");
        $(this.dropZoneDiv).addClass("rsdraggable");
        this.dragDropWrapDiv.appendChild(this.draggableDiv);
        this.dragDropWrapDiv.appendChild(this.dropZoneDiv);
        this.createButtons();
        this.checkServer("dragNdrop", true);
    }
    finishSettingUp() {
        this.appendReplacementSpans();
        this.renderFeedbackDiv();
        $(this.origElem).replaceWith(this.containerDiv);
        if (!this.hasStoredDropzones) {
            this.minheight = $(this.draggableDiv).height();
        }
        this.draggableDiv.style.minHeight = this.minheight.toString() + "px";
        if ($(this.dropZoneDiv).height() > this.minheight) {
            this.dragDropWrapDiv.style.minHeight =
                $(this.dropZoneDiv).height().toString() + "px";
        } else {
            this.dragDropWrapDiv.style.minHeight =
                this.minheight.toString() + "px";
        }
    }
    addDragDivListeners() {
        let self = this;
        this.draggableDiv.addEventListener(
            "dragover",
            function (ev) {
                ev.preventDefault();
                if ($(this.draggableDiv).hasClass("possibleDrop")) {
                    return;
                }
                $(this.draggableDiv).addClass("possibleDrop");
            }.bind(this)
        );
        this.draggableDiv.addEventListener(
            "drop",
            function (ev) {
                self.isAnswered = true;
                ev.preventDefault();
                if ($(this.draggableDiv).hasClass("possibleDrop")) {
                    $(this.draggableDiv).removeClass("possibleDrop");
                }
                var data = ev.dataTransfer.getData("draggableID");
                var draggedSpan = document.getElementById(data);
                if (
                    !$(this.draggableDiv).has(draggedSpan).length &&
                    !this.strangerDanger(draggedSpan)
                ) {
                    // Make sure element isn't already there--prevents erros w/appending child
                    this.draggableDiv.appendChild(draggedSpan);
                }
            }.bind(this)
        );
        this.draggableDiv.addEventListener(
            "dragleave",
            function (e) {
                if (!$(this.draggableDiv).hasClass("possibleDrop")) {
                    return;
                }
                $(this.draggableDiv).removeClass("possibleDrop");
            }.bind(this)
        );
    }
    createButtons() {
        this.buttonDiv = document.createElement("div");
        this.submitButton = document.createElement("button"); // Check me button
        this.submitButton.textContent = $.i18n("msg_dragndrop_check_me");
        $(this.submitButton).attr({
            class: "btn btn-success drag-button",
            name: "do answer",
            type: "button",
        });
        this.submitButton.onclick = function () {
            this.checkCurrentAnswer();
            this.renderFeedback();
            this.logCurrentAnswer();
        }.bind(this);
        this.resetButton = document.createElement("button"); // Check me button
        this.resetButton.textContent = $.i18n("msg_dragndrop_reset");
        $(this.resetButton).attr({
            class: "btn btn-default drag-button drag-reset",
            name: "do answer",
        });
        this.resetButton.onclick = function () {
            this.resetDraggables();
        }.bind(this);
        this.buttonDiv.appendChild(this.submitButton);
        this.buttonDiv.appendChild(this.resetButton);
        this.containerDiv.appendChild(this.buttonDiv);
    }
    appendReplacementSpans() {
        this.createIndexArray();
        this.randomizeIndexArray();
        for (let i = 0; i < this.dragPairArray.length; i++) {
            if (this.hasStoredDropzones) {
                if (
                    $.inArray(this.indexArray[i][0], this.pregnantIndexArray) <
                    0
                ) {
                    this.draggableDiv.appendChild(
                        this.dragPairArray[this.indexArray[i]][0]
                    );
                }
            } else {
                this.draggableDiv.appendChild(
                    this.dragPairArray[this.indexArray[i]][0]
                );
            }
        }
        this.randomizeIndexArray();
        for (let i = 0; i < this.dragPairArray.length; i++) {
            if (this.hasStoredDropzones) {
                if (this.pregnantIndexArray[this.indexArray[i]] !== "-1") {
                    this.dragPairArray[this.indexArray[i]][1].appendChild(
                        this.dragPairArray[
                        this.pregnantIndexArray[this.indexArray[i]]
                        ][0]
                    );
                }
            }
            this.dropZoneDiv.appendChild(
                this.dragPairArray[this.indexArray[i]][1]
            );
        }
    }
    setEventListeners(dgSpan, dpSpan) {
        // Adds HTML5 "drag and drop" UI functionality
        let self = this;
        dgSpan.addEventListener("dragstart", function (ev) {
            ev.dataTransfer.setData("draggableID", ev.target.id);
        });
        dgSpan.addEventListener("dragover", function (ev) {
            ev.preventDefault();
        });
        dgSpan.addEventListener(
            "drop",
            function (ev) {
                self.isAnswered = true;
                ev.preventDefault();
                var data = ev.dataTransfer.getData("draggableID");
                var draggedSpan = document.getElementById(data);
                if (
                    this.hasNoDragChild(ev.target) &&
                    draggedSpan != ev.target &&
                    !this.strangerDanger(draggedSpan)
                ) {
                    // Make sure element isn't already there--prevents erros w/appending child
                    this.draggableDiv.appendChild(draggedSpan);
                }
            }.bind(this)
        );
        dpSpan.addEventListener(
            "dragover",
            function (ev) {
                self.isAnswered = true;
                ev.preventDefault();
                if ($(ev.target).hasClass("possibleDrop")) {
                    return;
                }
                if (
                    $(ev.target).hasClass("draggable-drop") &&
                    this.hasNoDragChild(ev.target)
                ) {
                    $(ev.target).addClass("possibleDrop");
                }
            }.bind(this)
        );
        dpSpan.addEventListener("dragleave", function (ev) {
            self.isAnswered = true;
            ev.preventDefault();
            if (!$(ev.target).hasClass("possibleDrop")) {
                return;
            }
            $(ev.target).removeClass("possibleDrop");
        });
        dpSpan.addEventListener(
            "drop",
            function (ev) {
                self.isAnswered = true;
                ev.preventDefault();
                if ($(ev.target).hasClass("possibleDrop")) {
                    $(ev.target).removeClass("possibleDrop");
                }
                var data = ev.dataTransfer.getData("draggableID");
                var draggedSpan = document.getElementById(data);
                if (
                    $(ev.target).hasClass("draggable-drop") &&
                    this.hasNoDragChild(ev.target) &&
                    !this.strangerDanger(draggedSpan)
                ) {
                    // Make sure element isn't already there--prevents erros w/appending child
                    ev.target.appendChild(draggedSpan);
                }
            }.bind(this)
        );
    }
    renderFeedbackDiv() {
        if (!this.feedBackDiv) {
            this.feedBackDiv = document.createElement("div");
            this.feedBackDiv.id = this.divid + "_feedback";
            this.containerDiv.appendChild(document.createElement("br"));
            this.containerDiv.appendChild(this.feedBackDiv);
        }
    }
    /*=======================
    == Auxiliary functions ==
    =======================*/
    strangerDanger(testSpan) {
        // Returns true if the test span doesn't belong to this instance of DragNDrop
        var strangerDanger = true;
        for (var i = 0; i < this.dragPairArray.length; i++) {
            if (testSpan === this.dragPairArray[i][0]) {
                strangerDanger = false;
            }
        }
        return strangerDanger;
    }
    hasNoDragChild(parent) {
        // Ensures that each dropZoneDiv can have only one draggable child
        var counter = 0;
        for (var i = 0; i < parent.childNodes.length; i++) {
            if ($(parent.childNodes[i]).attr("draggable") === "true") {
                counter++;
            }
        }
        if (counter >= 1) {
            return false;
        } else {
            return true;
        }
    }
    createIndexArray() {
        this.indexArray = [];
        for (var i = 0; i < this.dragPairArray.length; i++) {
            this.indexArray.push(i);
        }
    }
    randomizeIndexArray() {
        // Shuffles around indices so the matchable elements aren't in a predictable order
        var currentIndex = this.indexArray.length,
            temporaryValue,
            randomIndex;
        // While there remain elements to shuffle...
        while (currentIndex !== 0) {
            // Pick a remaining element...
            randomIndex = Math.floor(Math.random() * currentIndex);
            currentIndex -= 1;
            // And swap it with the current element.
            temporaryValue = this.indexArray[currentIndex];
            this.indexArray[currentIndex] = this.indexArray[randomIndex];
            this.indexArray[randomIndex] = temporaryValue;
        }
    }
    /*==============================
    == Reset button functionality ==
    ==============================*/
    resetDraggables() {
        for (var i = 0; i < this.dragPairArray.length; i++) {
            for (
                var j = 0;
                j < this.dragPairArray[i][1].childNodes.length;
                j++
            ) {
                if (
                    $(this.dragPairArray[i][1].childNodes[j]).attr(
                        "draggable"
                    ) === "true"
                ) {
                    this.draggableDiv.appendChild(
                        this.dragPairArray[i][1].childNodes[j]
                    );
                }
            }
        }
        this.feedBackDiv.style.display = "none";
    }
    /*===========================
    == Evaluation and feedback ==
    ===========================*/

    checkCurrentAnswer() {
        this.correct = true;
        this.unansweredNum = 0;
        this.incorrectNum = 0;
        this.dragNum = this.dragPairArray.length;
        for (var i = 0; i < this.dragPairArray.length; i++) {
            if (
                !$(this.dragPairArray[i][1]).has(this.dragPairArray[i][0])
                    .length
            ) {
                this.correct = false;
                this.incorrectNum++;
            }
            if (this.hasNoDragChild(this.dragPairArray[i][1])) {
                this.unansweredNum++;
                this.incorrectNum -= 1;
            }
        }
        this.correctNum = this.dragNum - this.incorrectNum - this.unansweredNum;
        this.percent = this.correctNum / this.dragPairArray.length;
        this.setLocalStorage({ correct: this.correct ? "T" : "F" });
    }

    async logCurrentAnswer(sid) {
        let answer = this.pregnantIndexArray.join(";");
        let data = {
            event: "dragNdrop",
            act: answer,
            answer: answer,
            minHeight: this.minheight,
            div_id: this.divid,
            correct: this.correct,
            correctNum: this.correctNum,
            dragNum: this.dragNum,
        };
        if (typeof sid !== "undefined") {
            data.sid = sid;
        }
        await this.logBookEvent(data);
    }
    renderFeedback() {
        for (var i = 0; i < this.dragPairArray.length; i++) {
            if (
                !$(this.dragPairArray[i][1]).has(this.dragPairArray[i][0])
                    .length
            ) {
                $(this.dragPairArray[i][1]).addClass("drop-incorrect");
            } else {
                $(this.dragPairArray[i][1]).removeClass("drop-incorrect");
            }
        }

        if (!this.feedBackDiv) {
            this.renderFeedbackDiv();
        }
        this.feedBackDiv.style.display = "block";
        if (this.correct) {
            var msgCorrect = $.i18n("msg_dragndrop_correct_answer");
            $(this.feedBackDiv).html(msgCorrect);
            $(this.feedBackDiv).attr(
                "class",
                "alert alert-info draggable-feedback"
            );
        } else {
            var msgIncorrect = $.i18n(
                $.i18n("msg_dragndrop_incorrect_answer"),
                this.correctNum,
                this.incorrectNum,
                this.dragNum,
                this.unansweredNum
            );
            $(this.feedBackDiv).html(msgIncorrect + " " + this.feedback);
            $(this.feedBackDiv).attr(
                "class",
                "alert alert-danger draggable-feedback"
            );
        }
    }
    /*===================================
    === Checking/restoring from storage ===
    ===================================*/
    restoreAnswers(data) {
        // Restore answers from storage retrieval done in RunestoneBase
        this.hasStoredDropzones = true;
        this.minheight = data.minHeight;
        this.pregnantIndexArray = data.answer.split(";");
        this.finishSettingUp();
    }
    checkLocalStorage() {
        if (this.graderactive) {
            return;
        }
        var storedObj;
        this.hasStoredDropzones = false;
        var len = localStorage.length;
        if (len > 0) {
            var ex = localStorage.getItem(this.localStorageKey());
            if (ex !== null) {
                this.hasStoredDropzones = true;
                try {
                    storedObj = JSON.parse(ex);
                    this.minheight = storedObj.minHeight;
                } catch (err) {
                    // error while parsing; likely due to bad value stored in storage
                    console.log(err.message);
                    localStorage.removeItem(this.localStorageKey());
                    this.hasStoredDropzones = false;
                    this.finishSettingUp();
                    return;
                }
                this.pregnantIndexArray = storedObj.answer.split(";");
                if (this.useRunestoneServices) {
                    // store answer in database
                    var answer = this.pregnantIndexArray.join(";");
                    this.logBookEvent({
                        event: "dragNdrop",
                        act: answer,
                        answer: answer,
                        minHeight: this.minheight,
                        div_id: this.divid,
                        correct: storedObj.correct,
                    });
                }
            }
        }
        this.finishSettingUp();
    }

    setLocalStorage(data) {
        if (data.answer === undefined) {
            // If we didn't load from the server, we must generate the data
            this.pregnantIndexArray = [];
            for (var i = 0; i < this.dragPairArray.length; i++) {
                if (!this.hasNoDragChild(this.dragPairArray[i][1])) {
                    for (var j = 0; j < this.dragPairArray.length; j++) {
                        if (
                            $(this.dragPairArray[i][1]).has(
                                this.dragPairArray[j][0]
                            ).length
                        ) {
                            this.pregnantIndexArray.push(j);
                        }
                    }
                } else {
                    this.pregnantIndexArray.push(-1);
                }
            }
        }
        var timeStamp = new Date();
        var correct = data.correct;
        var storageObj = {
            answer: this.pregnantIndexArray.join(";"),
            minHeight: this.minheight,
            timestamp: timeStamp,
            correct: correct,
        };
        localStorage.setItem(
            this.localStorageKey(),
            JSON.stringify(storageObj)
        );
    }

    disableInteraction() {
        $(this.resetButton).hide();
        for (var i = 0; i < this.dragPairArray.length; i++) {
            // No more dragging
            $(this.dragPairArray[i][0]).attr("draggable", "false");
            $(this.dragPairArray[i][0]).css("cursor", "initial");
        }
    }
}

/*=================================
== Find the custom HTML tags and ==
==   execute our code on them    ==
=================================*/
$(document).bind("runestone:login-complete", function () {
    $("[data-component=dragndrop]").each(function (index) {
        var opts = {
            orig: this,
            useRunestoneServices: eBookConfig.useRunestoneServices,
        };
        if ($(this).closest("[data-component=timedAssessment]").length == 0) {
            // If this element exists within a timed component, don't render it here
            try {
                ddList[this.id] = new DragNDrop(opts);
            } catch (err) {
                console.log(`Error rendering DragNDrop Problem ${this.id}`);
            }
        }
    });
});


/***/ }),

/***/ 47496:
/*!********************************************!*\
  !*** ./runestone/dragndrop/js/timeddnd.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ TimedDragNDrop)
/* harmony export */ });
/* harmony import */ var _dragndrop_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./dragndrop.js */ 70225);




class TimedDragNDrop extends _dragndrop_js__WEBPACK_IMPORTED_MODULE_0__.default {
    constructor(opts) {
        super(opts);
        this.finishSettingUp();
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
        // Returns if the question was correct.    Used for timed assessment grading.
        if (this.unansweredNum === this.dragPairArray.length) {
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
window.component_factory["dragndrop"] = function (opts) {
    if (opts.timed) {
        return new TimedDragNDrop(opts);
    }
    return new _dragndrop_js__WEBPACK_IMPORTED_MODULE_0__.default(opts);
};


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9XZWJDb21wb25lbnRzLy4vcnVuZXN0b25lL2RyYWduZHJvcC9jc3MvZHJhZ25kcm9wLmNzcz84MTZkIiwid2VicGFjazovL1dlYkNvbXBvbmVudHMvLi9ydW5lc3RvbmUvZHJhZ25kcm9wL2pzL2RyYWduZHJvcC1pMThuLmVuLmpzIiwid2VicGFjazovL1dlYkNvbXBvbmVudHMvLi9ydW5lc3RvbmUvZHJhZ25kcm9wL2pzL2RyYWduZHJvcC1pMThuLnB0LWJyLmpzIiwid2VicGFjazovL1dlYkNvbXBvbmVudHMvLi9ydW5lc3RvbmUvZHJhZ25kcm9wL2pzL2RyYWduZHJvcC5qcyIsIndlYnBhY2s6Ly9XZWJDb21wb25lbnRzLy4vcnVuZXN0b25lL2RyYWduZHJvcC9qcy90aW1lZGRuZC5qcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7Ozs7Ozs7Ozs7O0FDQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0wsQ0FBQzs7Ozs7Ozs7Ozs7QUNSRDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTCxDQUFDOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQ1JEO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNhOztBQUVnRDtBQUMvQjtBQUNFO0FBQ0c7O0FBRTVCLGdCQUFnQjs7QUFFUix3QkFBd0IsZ0VBQWE7QUFDcEQ7QUFDQTtBQUNBLDZCQUE2QjtBQUM3QjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLHdCQUF3QjtBQUN4QjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsdUJBQXVCLHFDQUFxQztBQUM1RDtBQUNBO0FBQ0E7QUFDQTtBQUNBLHdCQUF3QiwyQ0FBMkM7QUFDbkU7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0EsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLDZEQUE2RDtBQUM3RDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsU0FBUztBQUNUO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7QUFDQSw2REFBNkQ7QUFDN0Q7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFNBQVM7QUFDVDtBQUNBO0FBQ0E7QUFDQTtBQUNBLFNBQVM7QUFDVCw0REFBNEQ7QUFDNUQ7QUFDQTtBQUNBO0FBQ0E7QUFDQSxTQUFTO0FBQ1Q7QUFDQTtBQUNBLFNBQVM7QUFDVDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLHVCQUF1QiwrQkFBK0I7QUFDdEQ7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLHVCQUF1QiwrQkFBK0I7QUFDdEQ7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxTQUFTO0FBQ1Q7QUFDQTtBQUNBLFNBQVM7QUFDVDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxTQUFTO0FBQ1Q7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsdUJBQXVCLCtCQUErQjtBQUN0RDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSx1QkFBdUIsOEJBQThCO0FBQ3JEO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFNBQVM7QUFDVDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsdUJBQXVCLCtCQUErQjtBQUN0RDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsdUJBQXVCLCtCQUErQjtBQUN0RDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLHVCQUF1QiwrQkFBK0I7QUFDdEQ7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLDhCQUE4QixvQ0FBb0M7QUFDbEU7O0FBRUE7QUFDQSxvREFBb0Q7QUFDcEQ7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSx1QkFBdUIsK0JBQStCO0FBQ3REO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxhQUFhO0FBQ2I7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxTQUFTO0FBQ1Q7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0Esc0RBQXNEO0FBQ3REO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsaUJBQWlCO0FBQ2pCLDJDQUEyQztBQUMzQztBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxtRUFBbUU7QUFDbkU7QUFDQTtBQUNBLGdFQUFnRTtBQUNoRTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLHFCQUFxQjtBQUNyQjtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsMkJBQTJCLCtCQUErQjtBQUMxRDtBQUNBLG1DQUFtQywrQkFBK0I7QUFDbEU7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLGlCQUFpQjtBQUNqQjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLG1EQUFtRDtBQUNuRDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBLHVCQUF1QiwrQkFBK0I7QUFDdEQ7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxhQUFhO0FBQ2IsaUVBQWlFLFFBQVE7QUFDekU7QUFDQTtBQUNBLEtBQUs7QUFDTCxDQUFDOzs7Ozs7Ozs7Ozs7Ozs7OztBQ3ZqQlk7O0FBRTBCOztBQUV4Qiw2QkFBNkIsa0RBQVM7QUFDckQ7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSwrQkFBK0I7QUFDL0IsU0FBUztBQUNUO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxlQUFlLGtEQUFTO0FBQ3hCIiwiZmlsZSI6InJ1bmVzdG9uZV9kcmFnbmRyb3BfanNfdGltZWRkbmRfanMuYnVuZGxlLmpzP3Y9YTExMzJmZDNmZWZkMzA3MGExN2QiLCJzb3VyY2VzQ29udGVudCI6WyIvLyBleHRyYWN0ZWQgYnkgbWluaS1jc3MtZXh0cmFjdC1wbHVnaW5cbmV4cG9ydCB7fTsiLCIkLmkxOG4oKS5sb2FkKHtcbiAgICBlbjoge1xuICAgICAgICBtc2dfZHJhZ25kcm9wX2NvcnJlY3RfYW5zd2VyOiBcIllvdSBhcmUgY29ycmVjdCFcIixcbiAgICAgICAgbXNnX2RyYWduZHJvcF9pbmNvcnJlY3RfYW5zd2VyOlxuICAgICAgICAgICAgXCJJbmNvcnJldC4gWW91IGdvdCAkMSBjb3JyZWN0IGFuZCAkMiBpbmNvcnJlY3Qgb3V0IG9mICQzLiBZb3UgbGVmdCAkNCBibGFuay5cIixcbiAgICAgICAgbXNnX2RyYWduZHJvcF9jaGVja19tZTogXCJDaGVjayBtZVwiLFxuICAgICAgICBtc2dfZHJhZ25kcm9wX3Jlc2V0OiBcIlJlc2V0XCIsXG4gICAgfSxcbn0pO1xuIiwiJC5pMThuKCkubG9hZCh7XG4gICAgXCJwdC1iclwiOiB7XG4gICAgICAgIG1zZ19kcmFnbmRyb3BfY29ycmVjdF9hbnN3ZXI6IFwiQ29ycmV0byFcIixcbiAgICAgICAgbXNnX2RyYWduZHJvcF9pbmNvcnJlY3RfYW5zd2VyOlxuICAgICAgICAgICAgXCJJbmNvcnJldG8uIFZvY8OqIHRldmUgJDEgY29ycmV0byhzKSBlICQyIGluY29ycmV0byhzKSBkZSAkMy4gVm9jw6ogZGVpeG91ICQ0IGVtIGJyYW5jby5cIixcbiAgICAgICAgbXNnX2RyYWduZHJvcF9jaGVja19tZTogXCJWZXJpZmljYXJcIixcbiAgICAgICAgbXNnX2RyYWduZHJvcF9yZXNldDogXCJSZXNldGFyXCIsXG4gICAgfSxcbn0pO1xuIiwiLyo9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT1cbj09PT09PT0gICAgIE1hc3RlciBkcmFnbmRyb3AuanMgICAgID09PT09PT09XG49PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PVxuPT09ICAgICBUaGlzIGZpbGUgY29udGFpbnMgdGhlIEpTIGZvciAgICA9PT1cbj09PSB0aGUgUnVuZXN0b25lIERyYWcgbiBkcm9wIGNvbXBvbmVudC4gPT09XG49PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PVxuPT09ICAgICAgICAgICAgICBDcmVhdGVkIGJ5ICAgICAgICAgICAgICA9PT1cbj09PSAgICAgICAgICAgSXNhaWFoIE1heWVyY2hhayAgICAgICAgICAgPT09XG49PT0gICAgICAgICAgICAgICAgNy82LzE1ICAgICAgICAgICAgICAgID09PVxuPT09ICAgICAgICAgICAgICBCcmFkIE1JbGxlciAgICAgICAgICAgICA9PT1cbj09PSAgICAgICAgICAgICAgICAyLzcvMTkgICAgICAgICAgICAgICAgPT09XG49PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT0qL1xuXCJ1c2Ugc3RyaWN0XCI7XG5cbmltcG9ydCBSdW5lc3RvbmVCYXNlIGZyb20gXCIuLi8uLi9jb21tb24vanMvcnVuZXN0b25lYmFzZS5qc1wiO1xuaW1wb3J0IFwiLi4vY3NzL2RyYWduZHJvcC5jc3NcIjtcbmltcG9ydCBcIi4vZHJhZ25kcm9wLWkxOG4uZW4uanNcIjtcbmltcG9ydCBcIi4vZHJhZ25kcm9wLWkxOG4ucHQtYnIuanNcIjtcblxuZXhwb3J0IHZhciBkZExpc3QgPSB7fTsgLy8gRGljdGlvbmFyeSB0aGF0IGNvbnRhaW5zIGFsbCBpbnN0YW5jZXMgb2YgZHJhZ25kcm9wIG9iamVjdHNcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgRHJhZ05Ecm9wIGV4dGVuZHMgUnVuZXN0b25lQmFzZSB7XG4gICAgY29uc3RydWN0b3Iob3B0cykge1xuICAgICAgICBzdXBlcihvcHRzKTtcbiAgICAgICAgdmFyIG9yaWcgPSBvcHRzLm9yaWc7IC8vIGVudGlyZSA8dWw+IGVsZW1lbnQgdGhhdCB3aWxsIGJlIHJlcGxhY2VkIGJ5IG5ldyBIVE1MXG4gICAgICAgIHRoaXMub3JpZ0VsZW0gPSBvcmlnO1xuICAgICAgICB0aGlzLmRpdmlkID0gb3JpZy5pZDtcbiAgICAgICAgdGhpcy51c2VSdW5lc3RvbmVTZXJ2aWNlcyA9IG9wdHMudXNlUnVuZXN0b25lU2VydmljZXM7XG4gICAgICAgIHRoaXMucmFuZG9tID0gZmFsc2U7XG4gICAgICAgIGlmICgkKHRoaXMub3JpZ0VsZW0pLmlzKFwiW2RhdGEtcmFuZG9tXVwiKSkge1xuICAgICAgICAgICAgdGhpcy5yYW5kb20gPSB0cnVlO1xuICAgICAgICB9XG4gICAgICAgIHRoaXMuZmVlZGJhY2sgPSBcIlwiO1xuICAgICAgICB0aGlzLmRyYWdQYWlyQXJyYXkgPSBbXTtcbiAgICAgICAgdGhpcy5xdWVzdGlvbiA9IFwiXCI7XG4gICAgICAgIHRoaXMucG9wdWxhdGUoKTsgLy8gUG9wdWxhdGVzIHRoaXMuZHJhZ1BhaXJBcnJheSwgdGhpcy5mZWVkYmFjayBhbmQgdGhpcy5xdWVzdGlvblxuICAgICAgICB0aGlzLmNyZWF0ZU5ld0VsZW1lbnRzKCk7XG4gICAgICAgIHRoaXMuY2FwdGlvbiA9IFwiRHJhZy1OLURyb3BcIjtcbiAgICAgICAgdGhpcy5hZGRDYXB0aW9uKFwicnVuZXN0b25lXCIpO1xuICAgIH1cbiAgICAvKj09PT09PT09PT09PT09PT09PT09PT1cbiAgICA9PT0gVXBkYXRlIHZhcmlhYmxlcyA9PT1cbiAgICA9PT09PT09PT09PT09PT09PT09PT09Ki9cbiAgICBwb3B1bGF0ZSgpIHtcbiAgICAgICAgZm9yICh2YXIgaSA9IDA7IGkgPCB0aGlzLm9yaWdFbGVtLmNoaWxkTm9kZXMubGVuZ3RoOyBpKyspIHtcbiAgICAgICAgICAgIGlmIChcbiAgICAgICAgICAgICAgICAkKHRoaXMub3JpZ0VsZW0uY2hpbGROb2Rlc1tpXSkuZGF0YShcInN1YmNvbXBvbmVudFwiKSA9PT0gXCJkcm9wem9uZVwiXG4gICAgICAgICAgICApIHtcbiAgICAgICAgICAgICAgICB2YXIgdG1wID0gJCh0aGlzLm9yaWdFbGVtKS5maW5kKFxuICAgICAgICAgICAgICAgICAgICBgIyR7JCh0aGlzLm9yaWdFbGVtLmNoaWxkTm9kZXNbaV0pLmF0dHIoXCJmb3JcIil9YFxuICAgICAgICAgICAgICAgIClbMF07XG4gICAgICAgICAgICAgICAgdmFyIHJlcGxhY2VTcGFuID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudChcInNwYW5cIik7XG4gICAgICAgICAgICAgICAgcmVwbGFjZVNwYW4uaW5uZXJIVE1MID0gdG1wLmlubmVySFRNTDtcbiAgICAgICAgICAgICAgICByZXBsYWNlU3Bhbi5pZCA9IHRoaXMuZGl2aWQgKyB0bXAuaWQ7XG4gICAgICAgICAgICAgICAgJChyZXBsYWNlU3BhbikuYXR0cihcImRyYWdnYWJsZVwiLCBcInRydWVcIik7XG4gICAgICAgICAgICAgICAgJChyZXBsYWNlU3BhbikuYWRkQ2xhc3MoXCJkcmFnZ2FibGUtZHJhZ1wiKTtcbiAgICAgICAgICAgICAgICB2YXIgb3RoZXJSZXBsYWNlU3BhbiA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoXCJzcGFuXCIpO1xuICAgICAgICAgICAgICAgIG90aGVyUmVwbGFjZVNwYW4uaW5uZXJIVE1MID0gdGhpcy5vcmlnRWxlbS5jaGlsZE5vZGVzW1xuICAgICAgICAgICAgICAgICAgICBpXG4gICAgICAgICAgICAgICAgXS5pbm5lckhUTUw7XG4gICAgICAgICAgICAgICAgJChvdGhlclJlcGxhY2VTcGFuKS5hZGRDbGFzcyhcImRyYWdnYWJsZS1kcm9wXCIpO1xuICAgICAgICAgICAgICAgIHRoaXMuc2V0RXZlbnRMaXN0ZW5lcnMocmVwbGFjZVNwYW4sIG90aGVyUmVwbGFjZVNwYW4pO1xuICAgICAgICAgICAgICAgIHZhciB0bXBBcnIgPSBbXTtcbiAgICAgICAgICAgICAgICB0bXBBcnIucHVzaChyZXBsYWNlU3Bhbik7XG4gICAgICAgICAgICAgICAgdG1wQXJyLnB1c2gob3RoZXJSZXBsYWNlU3Bhbik7XG4gICAgICAgICAgICAgICAgdGhpcy5kcmFnUGFpckFycmF5LnB1c2godG1wQXJyKTtcbiAgICAgICAgICAgIH0gZWxzZSBpZiAoXG4gICAgICAgICAgICAgICAgJCh0aGlzLm9yaWdFbGVtLmNoaWxkTm9kZXNbaV0pLmRhdGEoXCJzdWJjb21wb25lbnRcIikgPT09IFwicXVlc3Rpb25cIlxuICAgICAgICAgICAgKSB7XG4gICAgICAgICAgICAgICAgdGhpcy5xdWVzdGlvbiA9IHRoaXMub3JpZ0VsZW0uY2hpbGROb2Rlc1tpXS5pbm5lckhUTUw7XG4gICAgICAgICAgICB9IGVsc2UgaWYgKFxuICAgICAgICAgICAgICAgICQodGhpcy5vcmlnRWxlbS5jaGlsZE5vZGVzW2ldKS5kYXRhKFwic3ViY29tcG9uZW50XCIpID09PSBcImZlZWRiYWNrXCJcbiAgICAgICAgICAgICkge1xuICAgICAgICAgICAgICAgIHRoaXMuZmVlZGJhY2sgPSB0aGlzLm9yaWdFbGVtLmNoaWxkTm9kZXNbaV0uaW5uZXJIVE1MO1xuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgfVxuICAgIC8qPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PVxuICAgID09IENyZWF0ZSBuZXcgSFRNTCBlbGVtZW50cyBhbmQgcmVwbGFjZSA9PVxuICAgID09ICAgICAgb3JpZ2luYWwgZWxlbWVudCB3aXRoIHRoZW0gICAgICA9PVxuICAgID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT0qL1xuICAgIGNyZWF0ZU5ld0VsZW1lbnRzKCkge1xuICAgICAgICB0aGlzLmNvbnRhaW5lckRpdiA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoXCJkaXZcIik7XG4gICAgICAgIHRoaXMuY29udGFpbmVyRGl2LmlkID0gdGhpcy5kaXZpZDtcbiAgICAgICAgJCh0aGlzLmNvbnRhaW5lckRpdikuYWRkQ2xhc3MoXG4gICAgICAgICAgICBcImFsZXJ0IGFsZXJ0LXdhcm5pbmcgZHJhZ2dhYmxlLWNvbnRhaW5lclwiXG4gICAgICAgICk7XG4gICAgICAgICQodGhpcy5jb250YWluZXJEaXYpLnRleHQodGhpcy5xdWVzdGlvbik7XG4gICAgICAgIHRoaXMuY29udGFpbmVyRGl2LmFwcGVuZENoaWxkKGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoXCJiclwiKSk7XG4gICAgICAgIHRoaXMuZHJhZ0Ryb3BXcmFwRGl2ID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudChcImRpdlwiKTsgLy8gSG9sZHMgdGhlIGRyYWdnYWJsZXMvZHJvcHpvbmVzLCBwcmV2ZW50cyBmZWVkYmFjayBmcm9tIGJsZWVkaW5nIGluXG4gICAgICAgICQodGhpcy5kcmFnRHJvcFdyYXBEaXYpLmNzcyhcImRpc3BsYXlcIiwgXCJibG9ja1wiKTtcbiAgICAgICAgdGhpcy5jb250YWluZXJEaXYuYXBwZW5kQ2hpbGQodGhpcy5kcmFnRHJvcFdyYXBEaXYpO1xuICAgICAgICB0aGlzLmRyYWdnYWJsZURpdiA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoXCJkaXZcIik7XG4gICAgICAgICQodGhpcy5kcmFnZ2FibGVEaXYpLmFkZENsYXNzKFwicnNkcmFnZ2FibGUgZHJhZ3pvbmVcIik7XG4gICAgICAgIHRoaXMuYWRkRHJhZ0Rpdkxpc3RlbmVycygpO1xuICAgICAgICB0aGlzLmRyb3Bab25lRGl2ID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudChcImRpdlwiKTtcbiAgICAgICAgJCh0aGlzLmRyb3Bab25lRGl2KS5hZGRDbGFzcyhcInJzZHJhZ2dhYmxlXCIpO1xuICAgICAgICB0aGlzLmRyYWdEcm9wV3JhcERpdi5hcHBlbmRDaGlsZCh0aGlzLmRyYWdnYWJsZURpdik7XG4gICAgICAgIHRoaXMuZHJhZ0Ryb3BXcmFwRGl2LmFwcGVuZENoaWxkKHRoaXMuZHJvcFpvbmVEaXYpO1xuICAgICAgICB0aGlzLmNyZWF0ZUJ1dHRvbnMoKTtcbiAgICAgICAgdGhpcy5jaGVja1NlcnZlcihcImRyYWdOZHJvcFwiLCB0cnVlKTtcbiAgICB9XG4gICAgZmluaXNoU2V0dGluZ1VwKCkge1xuICAgICAgICB0aGlzLmFwcGVuZFJlcGxhY2VtZW50U3BhbnMoKTtcbiAgICAgICAgdGhpcy5yZW5kZXJGZWVkYmFja0RpdigpO1xuICAgICAgICAkKHRoaXMub3JpZ0VsZW0pLnJlcGxhY2VXaXRoKHRoaXMuY29udGFpbmVyRGl2KTtcbiAgICAgICAgaWYgKCF0aGlzLmhhc1N0b3JlZERyb3B6b25lcykge1xuICAgICAgICAgICAgdGhpcy5taW5oZWlnaHQgPSAkKHRoaXMuZHJhZ2dhYmxlRGl2KS5oZWlnaHQoKTtcbiAgICAgICAgfVxuICAgICAgICB0aGlzLmRyYWdnYWJsZURpdi5zdHlsZS5taW5IZWlnaHQgPSB0aGlzLm1pbmhlaWdodC50b1N0cmluZygpICsgXCJweFwiO1xuICAgICAgICBpZiAoJCh0aGlzLmRyb3Bab25lRGl2KS5oZWlnaHQoKSA+IHRoaXMubWluaGVpZ2h0KSB7XG4gICAgICAgICAgICB0aGlzLmRyYWdEcm9wV3JhcERpdi5zdHlsZS5taW5IZWlnaHQgPVxuICAgICAgICAgICAgICAgICQodGhpcy5kcm9wWm9uZURpdikuaGVpZ2h0KCkudG9TdHJpbmcoKSArIFwicHhcIjtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIHRoaXMuZHJhZ0Ryb3BXcmFwRGl2LnN0eWxlLm1pbkhlaWdodCA9XG4gICAgICAgICAgICAgICAgdGhpcy5taW5oZWlnaHQudG9TdHJpbmcoKSArIFwicHhcIjtcbiAgICAgICAgfVxuICAgIH1cbiAgICBhZGREcmFnRGl2TGlzdGVuZXJzKCkge1xuICAgICAgICBsZXQgc2VsZiA9IHRoaXM7XG4gICAgICAgIHRoaXMuZHJhZ2dhYmxlRGl2LmFkZEV2ZW50TGlzdGVuZXIoXG4gICAgICAgICAgICBcImRyYWdvdmVyXCIsXG4gICAgICAgICAgICBmdW5jdGlvbiAoZXYpIHtcbiAgICAgICAgICAgICAgICBldi5wcmV2ZW50RGVmYXVsdCgpO1xuICAgICAgICAgICAgICAgIGlmICgkKHRoaXMuZHJhZ2dhYmxlRGl2KS5oYXNDbGFzcyhcInBvc3NpYmxlRHJvcFwiKSkge1xuICAgICAgICAgICAgICAgICAgICByZXR1cm47XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgICQodGhpcy5kcmFnZ2FibGVEaXYpLmFkZENsYXNzKFwicG9zc2libGVEcm9wXCIpO1xuICAgICAgICAgICAgfS5iaW5kKHRoaXMpXG4gICAgICAgICk7XG4gICAgICAgIHRoaXMuZHJhZ2dhYmxlRGl2LmFkZEV2ZW50TGlzdGVuZXIoXG4gICAgICAgICAgICBcImRyb3BcIixcbiAgICAgICAgICAgIGZ1bmN0aW9uIChldikge1xuICAgICAgICAgICAgICAgIHNlbGYuaXNBbnN3ZXJlZCA9IHRydWU7XG4gICAgICAgICAgICAgICAgZXYucHJldmVudERlZmF1bHQoKTtcbiAgICAgICAgICAgICAgICBpZiAoJCh0aGlzLmRyYWdnYWJsZURpdikuaGFzQ2xhc3MoXCJwb3NzaWJsZURyb3BcIikpIHtcbiAgICAgICAgICAgICAgICAgICAgJCh0aGlzLmRyYWdnYWJsZURpdikucmVtb3ZlQ2xhc3MoXCJwb3NzaWJsZURyb3BcIik7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIHZhciBkYXRhID0gZXYuZGF0YVRyYW5zZmVyLmdldERhdGEoXCJkcmFnZ2FibGVJRFwiKTtcbiAgICAgICAgICAgICAgICB2YXIgZHJhZ2dlZFNwYW4gPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZChkYXRhKTtcbiAgICAgICAgICAgICAgICBpZiAoXG4gICAgICAgICAgICAgICAgICAgICEkKHRoaXMuZHJhZ2dhYmxlRGl2KS5oYXMoZHJhZ2dlZFNwYW4pLmxlbmd0aCAmJlxuICAgICAgICAgICAgICAgICAgICAhdGhpcy5zdHJhbmdlckRhbmdlcihkcmFnZ2VkU3BhbilcbiAgICAgICAgICAgICAgICApIHtcbiAgICAgICAgICAgICAgICAgICAgLy8gTWFrZSBzdXJlIGVsZW1lbnQgaXNuJ3QgYWxyZWFkeSB0aGVyZS0tcHJldmVudHMgZXJyb3Mgdy9hcHBlbmRpbmcgY2hpbGRcbiAgICAgICAgICAgICAgICAgICAgdGhpcy5kcmFnZ2FibGVEaXYuYXBwZW5kQ2hpbGQoZHJhZ2dlZFNwYW4pO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH0uYmluZCh0aGlzKVxuICAgICAgICApO1xuICAgICAgICB0aGlzLmRyYWdnYWJsZURpdi5hZGRFdmVudExpc3RlbmVyKFxuICAgICAgICAgICAgXCJkcmFnbGVhdmVcIixcbiAgICAgICAgICAgIGZ1bmN0aW9uIChlKSB7XG4gICAgICAgICAgICAgICAgaWYgKCEkKHRoaXMuZHJhZ2dhYmxlRGl2KS5oYXNDbGFzcyhcInBvc3NpYmxlRHJvcFwiKSkge1xuICAgICAgICAgICAgICAgICAgICByZXR1cm47XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgICQodGhpcy5kcmFnZ2FibGVEaXYpLnJlbW92ZUNsYXNzKFwicG9zc2libGVEcm9wXCIpO1xuICAgICAgICAgICAgfS5iaW5kKHRoaXMpXG4gICAgICAgICk7XG4gICAgfVxuICAgIGNyZWF0ZUJ1dHRvbnMoKSB7XG4gICAgICAgIHRoaXMuYnV0dG9uRGl2ID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudChcImRpdlwiKTtcbiAgICAgICAgdGhpcy5zdWJtaXRCdXR0b24gPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KFwiYnV0dG9uXCIpOyAvLyBDaGVjayBtZSBidXR0b25cbiAgICAgICAgdGhpcy5zdWJtaXRCdXR0b24udGV4dENvbnRlbnQgPSAkLmkxOG4oXCJtc2dfZHJhZ25kcm9wX2NoZWNrX21lXCIpO1xuICAgICAgICAkKHRoaXMuc3VibWl0QnV0dG9uKS5hdHRyKHtcbiAgICAgICAgICAgIGNsYXNzOiBcImJ0biBidG4tc3VjY2VzcyBkcmFnLWJ1dHRvblwiLFxuICAgICAgICAgICAgbmFtZTogXCJkbyBhbnN3ZXJcIixcbiAgICAgICAgICAgIHR5cGU6IFwiYnV0dG9uXCIsXG4gICAgICAgIH0pO1xuICAgICAgICB0aGlzLnN1Ym1pdEJ1dHRvbi5vbmNsaWNrID0gZnVuY3Rpb24gKCkge1xuICAgICAgICAgICAgdGhpcy5jaGVja0N1cnJlbnRBbnN3ZXIoKTtcbiAgICAgICAgICAgIHRoaXMucmVuZGVyRmVlZGJhY2soKTtcbiAgICAgICAgICAgIHRoaXMubG9nQ3VycmVudEFuc3dlcigpO1xuICAgICAgICB9LmJpbmQodGhpcyk7XG4gICAgICAgIHRoaXMucmVzZXRCdXR0b24gPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KFwiYnV0dG9uXCIpOyAvLyBDaGVjayBtZSBidXR0b25cbiAgICAgICAgdGhpcy5yZXNldEJ1dHRvbi50ZXh0Q29udGVudCA9ICQuaTE4bihcIm1zZ19kcmFnbmRyb3BfcmVzZXRcIik7XG4gICAgICAgICQodGhpcy5yZXNldEJ1dHRvbikuYXR0cih7XG4gICAgICAgICAgICBjbGFzczogXCJidG4gYnRuLWRlZmF1bHQgZHJhZy1idXR0b24gZHJhZy1yZXNldFwiLFxuICAgICAgICAgICAgbmFtZTogXCJkbyBhbnN3ZXJcIixcbiAgICAgICAgfSk7XG4gICAgICAgIHRoaXMucmVzZXRCdXR0b24ub25jbGljayA9IGZ1bmN0aW9uICgpIHtcbiAgICAgICAgICAgIHRoaXMucmVzZXREcmFnZ2FibGVzKCk7XG4gICAgICAgIH0uYmluZCh0aGlzKTtcbiAgICAgICAgdGhpcy5idXR0b25EaXYuYXBwZW5kQ2hpbGQodGhpcy5zdWJtaXRCdXR0b24pO1xuICAgICAgICB0aGlzLmJ1dHRvbkRpdi5hcHBlbmRDaGlsZCh0aGlzLnJlc2V0QnV0dG9uKTtcbiAgICAgICAgdGhpcy5jb250YWluZXJEaXYuYXBwZW5kQ2hpbGQodGhpcy5idXR0b25EaXYpO1xuICAgIH1cbiAgICBhcHBlbmRSZXBsYWNlbWVudFNwYW5zKCkge1xuICAgICAgICB0aGlzLmNyZWF0ZUluZGV4QXJyYXkoKTtcbiAgICAgICAgdGhpcy5yYW5kb21pemVJbmRleEFycmF5KCk7XG4gICAgICAgIGZvciAobGV0IGkgPSAwOyBpIDwgdGhpcy5kcmFnUGFpckFycmF5Lmxlbmd0aDsgaSsrKSB7XG4gICAgICAgICAgICBpZiAodGhpcy5oYXNTdG9yZWREcm9wem9uZXMpIHtcbiAgICAgICAgICAgICAgICBpZiAoXG4gICAgICAgICAgICAgICAgICAgICQuaW5BcnJheSh0aGlzLmluZGV4QXJyYXlbaV1bMF0sIHRoaXMucHJlZ25hbnRJbmRleEFycmF5KSA8XG4gICAgICAgICAgICAgICAgICAgIDBcbiAgICAgICAgICAgICAgICApIHtcbiAgICAgICAgICAgICAgICAgICAgdGhpcy5kcmFnZ2FibGVEaXYuYXBwZW5kQ2hpbGQoXG4gICAgICAgICAgICAgICAgICAgICAgICB0aGlzLmRyYWdQYWlyQXJyYXlbdGhpcy5pbmRleEFycmF5W2ldXVswXVxuICAgICAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgdGhpcy5kcmFnZ2FibGVEaXYuYXBwZW5kQ2hpbGQoXG4gICAgICAgICAgICAgICAgICAgIHRoaXMuZHJhZ1BhaXJBcnJheVt0aGlzLmluZGV4QXJyYXlbaV1dWzBdXG4gICAgICAgICAgICAgICAgKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgICB0aGlzLnJhbmRvbWl6ZUluZGV4QXJyYXkoKTtcbiAgICAgICAgZm9yIChsZXQgaSA9IDA7IGkgPCB0aGlzLmRyYWdQYWlyQXJyYXkubGVuZ3RoOyBpKyspIHtcbiAgICAgICAgICAgIGlmICh0aGlzLmhhc1N0b3JlZERyb3B6b25lcykge1xuICAgICAgICAgICAgICAgIGlmICh0aGlzLnByZWduYW50SW5kZXhBcnJheVt0aGlzLmluZGV4QXJyYXlbaV1dICE9PSBcIi0xXCIpIHtcbiAgICAgICAgICAgICAgICAgICAgdGhpcy5kcmFnUGFpckFycmF5W3RoaXMuaW5kZXhBcnJheVtpXV1bMV0uYXBwZW5kQ2hpbGQoXG4gICAgICAgICAgICAgICAgICAgICAgICB0aGlzLmRyYWdQYWlyQXJyYXlbXG4gICAgICAgICAgICAgICAgICAgICAgICB0aGlzLnByZWduYW50SW5kZXhBcnJheVt0aGlzLmluZGV4QXJyYXlbaV1dXG4gICAgICAgICAgICAgICAgICAgICAgICBdWzBdXG4gICAgICAgICAgICAgICAgICAgICk7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfVxuICAgICAgICAgICAgdGhpcy5kcm9wWm9uZURpdi5hcHBlbmRDaGlsZChcbiAgICAgICAgICAgICAgICB0aGlzLmRyYWdQYWlyQXJyYXlbdGhpcy5pbmRleEFycmF5W2ldXVsxXVxuICAgICAgICAgICAgKTtcbiAgICAgICAgfVxuICAgIH1cbiAgICBzZXRFdmVudExpc3RlbmVycyhkZ1NwYW4sIGRwU3Bhbikge1xuICAgICAgICAvLyBBZGRzIEhUTUw1IFwiZHJhZyBhbmQgZHJvcFwiIFVJIGZ1bmN0aW9uYWxpdHlcbiAgICAgICAgbGV0IHNlbGYgPSB0aGlzO1xuICAgICAgICBkZ1NwYW4uYWRkRXZlbnRMaXN0ZW5lcihcImRyYWdzdGFydFwiLCBmdW5jdGlvbiAoZXYpIHtcbiAgICAgICAgICAgIGV2LmRhdGFUcmFuc2Zlci5zZXREYXRhKFwiZHJhZ2dhYmxlSURcIiwgZXYudGFyZ2V0LmlkKTtcbiAgICAgICAgfSk7XG4gICAgICAgIGRnU3Bhbi5hZGRFdmVudExpc3RlbmVyKFwiZHJhZ292ZXJcIiwgZnVuY3Rpb24gKGV2KSB7XG4gICAgICAgICAgICBldi5wcmV2ZW50RGVmYXVsdCgpO1xuICAgICAgICB9KTtcbiAgICAgICAgZGdTcGFuLmFkZEV2ZW50TGlzdGVuZXIoXG4gICAgICAgICAgICBcImRyb3BcIixcbiAgICAgICAgICAgIGZ1bmN0aW9uIChldikge1xuICAgICAgICAgICAgICAgIHNlbGYuaXNBbnN3ZXJlZCA9IHRydWU7XG4gICAgICAgICAgICAgICAgZXYucHJldmVudERlZmF1bHQoKTtcbiAgICAgICAgICAgICAgICB2YXIgZGF0YSA9IGV2LmRhdGFUcmFuc2Zlci5nZXREYXRhKFwiZHJhZ2dhYmxlSURcIik7XG4gICAgICAgICAgICAgICAgdmFyIGRyYWdnZWRTcGFuID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoZGF0YSk7XG4gICAgICAgICAgICAgICAgaWYgKFxuICAgICAgICAgICAgICAgICAgICB0aGlzLmhhc05vRHJhZ0NoaWxkKGV2LnRhcmdldCkgJiZcbiAgICAgICAgICAgICAgICAgICAgZHJhZ2dlZFNwYW4gIT0gZXYudGFyZ2V0ICYmXG4gICAgICAgICAgICAgICAgICAgICF0aGlzLnN0cmFuZ2VyRGFuZ2VyKGRyYWdnZWRTcGFuKVxuICAgICAgICAgICAgICAgICkge1xuICAgICAgICAgICAgICAgICAgICAvLyBNYWtlIHN1cmUgZWxlbWVudCBpc24ndCBhbHJlYWR5IHRoZXJlLS1wcmV2ZW50cyBlcnJvcyB3L2FwcGVuZGluZyBjaGlsZFxuICAgICAgICAgICAgICAgICAgICB0aGlzLmRyYWdnYWJsZURpdi5hcHBlbmRDaGlsZChkcmFnZ2VkU3Bhbik7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfS5iaW5kKHRoaXMpXG4gICAgICAgICk7XG4gICAgICAgIGRwU3Bhbi5hZGRFdmVudExpc3RlbmVyKFxuICAgICAgICAgICAgXCJkcmFnb3ZlclwiLFxuICAgICAgICAgICAgZnVuY3Rpb24gKGV2KSB7XG4gICAgICAgICAgICAgICAgc2VsZi5pc0Fuc3dlcmVkID0gdHJ1ZTtcbiAgICAgICAgICAgICAgICBldi5wcmV2ZW50RGVmYXVsdCgpO1xuICAgICAgICAgICAgICAgIGlmICgkKGV2LnRhcmdldCkuaGFzQ2xhc3MoXCJwb3NzaWJsZURyb3BcIikpIHtcbiAgICAgICAgICAgICAgICAgICAgcmV0dXJuO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICBpZiAoXG4gICAgICAgICAgICAgICAgICAgICQoZXYudGFyZ2V0KS5oYXNDbGFzcyhcImRyYWdnYWJsZS1kcm9wXCIpICYmXG4gICAgICAgICAgICAgICAgICAgIHRoaXMuaGFzTm9EcmFnQ2hpbGQoZXYudGFyZ2V0KVxuICAgICAgICAgICAgICAgICkge1xuICAgICAgICAgICAgICAgICAgICAkKGV2LnRhcmdldCkuYWRkQ2xhc3MoXCJwb3NzaWJsZURyb3BcIik7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfS5iaW5kKHRoaXMpXG4gICAgICAgICk7XG4gICAgICAgIGRwU3Bhbi5hZGRFdmVudExpc3RlbmVyKFwiZHJhZ2xlYXZlXCIsIGZ1bmN0aW9uIChldikge1xuICAgICAgICAgICAgc2VsZi5pc0Fuc3dlcmVkID0gdHJ1ZTtcbiAgICAgICAgICAgIGV2LnByZXZlbnREZWZhdWx0KCk7XG4gICAgICAgICAgICBpZiAoISQoZXYudGFyZ2V0KS5oYXNDbGFzcyhcInBvc3NpYmxlRHJvcFwiKSkge1xuICAgICAgICAgICAgICAgIHJldHVybjtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgICQoZXYudGFyZ2V0KS5yZW1vdmVDbGFzcyhcInBvc3NpYmxlRHJvcFwiKTtcbiAgICAgICAgfSk7XG4gICAgICAgIGRwU3Bhbi5hZGRFdmVudExpc3RlbmVyKFxuICAgICAgICAgICAgXCJkcm9wXCIsXG4gICAgICAgICAgICBmdW5jdGlvbiAoZXYpIHtcbiAgICAgICAgICAgICAgICBzZWxmLmlzQW5zd2VyZWQgPSB0cnVlO1xuICAgICAgICAgICAgICAgIGV2LnByZXZlbnREZWZhdWx0KCk7XG4gICAgICAgICAgICAgICAgaWYgKCQoZXYudGFyZ2V0KS5oYXNDbGFzcyhcInBvc3NpYmxlRHJvcFwiKSkge1xuICAgICAgICAgICAgICAgICAgICAkKGV2LnRhcmdldCkucmVtb3ZlQ2xhc3MoXCJwb3NzaWJsZURyb3BcIik7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIHZhciBkYXRhID0gZXYuZGF0YVRyYW5zZmVyLmdldERhdGEoXCJkcmFnZ2FibGVJRFwiKTtcbiAgICAgICAgICAgICAgICB2YXIgZHJhZ2dlZFNwYW4gPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZChkYXRhKTtcbiAgICAgICAgICAgICAgICBpZiAoXG4gICAgICAgICAgICAgICAgICAgICQoZXYudGFyZ2V0KS5oYXNDbGFzcyhcImRyYWdnYWJsZS1kcm9wXCIpICYmXG4gICAgICAgICAgICAgICAgICAgIHRoaXMuaGFzTm9EcmFnQ2hpbGQoZXYudGFyZ2V0KSAmJlxuICAgICAgICAgICAgICAgICAgICAhdGhpcy5zdHJhbmdlckRhbmdlcihkcmFnZ2VkU3BhbilcbiAgICAgICAgICAgICAgICApIHtcbiAgICAgICAgICAgICAgICAgICAgLy8gTWFrZSBzdXJlIGVsZW1lbnQgaXNuJ3QgYWxyZWFkeSB0aGVyZS0tcHJldmVudHMgZXJyb3Mgdy9hcHBlbmRpbmcgY2hpbGRcbiAgICAgICAgICAgICAgICAgICAgZXYudGFyZ2V0LmFwcGVuZENoaWxkKGRyYWdnZWRTcGFuKTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9LmJpbmQodGhpcylcbiAgICAgICAgKTtcbiAgICB9XG4gICAgcmVuZGVyRmVlZGJhY2tEaXYoKSB7XG4gICAgICAgIGlmICghdGhpcy5mZWVkQmFja0Rpdikge1xuICAgICAgICAgICAgdGhpcy5mZWVkQmFja0RpdiA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoXCJkaXZcIik7XG4gICAgICAgICAgICB0aGlzLmZlZWRCYWNrRGl2LmlkID0gdGhpcy5kaXZpZCArIFwiX2ZlZWRiYWNrXCI7XG4gICAgICAgICAgICB0aGlzLmNvbnRhaW5lckRpdi5hcHBlbmRDaGlsZChkb2N1bWVudC5jcmVhdGVFbGVtZW50KFwiYnJcIikpO1xuICAgICAgICAgICAgdGhpcy5jb250YWluZXJEaXYuYXBwZW5kQ2hpbGQodGhpcy5mZWVkQmFja0Rpdik7XG4gICAgICAgIH1cbiAgICB9XG4gICAgLyo9PT09PT09PT09PT09PT09PT09PT09PVxuICAgID09IEF1eGlsaWFyeSBmdW5jdGlvbnMgPT1cbiAgICA9PT09PT09PT09PT09PT09PT09PT09PSovXG4gICAgc3RyYW5nZXJEYW5nZXIodGVzdFNwYW4pIHtcbiAgICAgICAgLy8gUmV0dXJucyB0cnVlIGlmIHRoZSB0ZXN0IHNwYW4gZG9lc24ndCBiZWxvbmcgdG8gdGhpcyBpbnN0YW5jZSBvZiBEcmFnTkRyb3BcbiAgICAgICAgdmFyIHN0cmFuZ2VyRGFuZ2VyID0gdHJ1ZTtcbiAgICAgICAgZm9yICh2YXIgaSA9IDA7IGkgPCB0aGlzLmRyYWdQYWlyQXJyYXkubGVuZ3RoOyBpKyspIHtcbiAgICAgICAgICAgIGlmICh0ZXN0U3BhbiA9PT0gdGhpcy5kcmFnUGFpckFycmF5W2ldWzBdKSB7XG4gICAgICAgICAgICAgICAgc3RyYW5nZXJEYW5nZXIgPSBmYWxzZTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gc3RyYW5nZXJEYW5nZXI7XG4gICAgfVxuICAgIGhhc05vRHJhZ0NoaWxkKHBhcmVudCkge1xuICAgICAgICAvLyBFbnN1cmVzIHRoYXQgZWFjaCBkcm9wWm9uZURpdiBjYW4gaGF2ZSBvbmx5IG9uZSBkcmFnZ2FibGUgY2hpbGRcbiAgICAgICAgdmFyIGNvdW50ZXIgPSAwO1xuICAgICAgICBmb3IgKHZhciBpID0gMDsgaSA8IHBhcmVudC5jaGlsZE5vZGVzLmxlbmd0aDsgaSsrKSB7XG4gICAgICAgICAgICBpZiAoJChwYXJlbnQuY2hpbGROb2Rlc1tpXSkuYXR0cihcImRyYWdnYWJsZVwiKSA9PT0gXCJ0cnVlXCIpIHtcbiAgICAgICAgICAgICAgICBjb3VudGVyKys7XG4gICAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgICAgaWYgKGNvdW50ZXIgPj0gMSkge1xuICAgICAgICAgICAgcmV0dXJuIGZhbHNlO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgcmV0dXJuIHRydWU7XG4gICAgICAgIH1cbiAgICB9XG4gICAgY3JlYXRlSW5kZXhBcnJheSgpIHtcbiAgICAgICAgdGhpcy5pbmRleEFycmF5ID0gW107XG4gICAgICAgIGZvciAodmFyIGkgPSAwOyBpIDwgdGhpcy5kcmFnUGFpckFycmF5Lmxlbmd0aDsgaSsrKSB7XG4gICAgICAgICAgICB0aGlzLmluZGV4QXJyYXkucHVzaChpKTtcbiAgICAgICAgfVxuICAgIH1cbiAgICByYW5kb21pemVJbmRleEFycmF5KCkge1xuICAgICAgICAvLyBTaHVmZmxlcyBhcm91bmQgaW5kaWNlcyBzbyB0aGUgbWF0Y2hhYmxlIGVsZW1lbnRzIGFyZW4ndCBpbiBhIHByZWRpY3RhYmxlIG9yZGVyXG4gICAgICAgIHZhciBjdXJyZW50SW5kZXggPSB0aGlzLmluZGV4QXJyYXkubGVuZ3RoLFxuICAgICAgICAgICAgdGVtcG9yYXJ5VmFsdWUsXG4gICAgICAgICAgICByYW5kb21JbmRleDtcbiAgICAgICAgLy8gV2hpbGUgdGhlcmUgcmVtYWluIGVsZW1lbnRzIHRvIHNodWZmbGUuLi5cbiAgICAgICAgd2hpbGUgKGN1cnJlbnRJbmRleCAhPT0gMCkge1xuICAgICAgICAgICAgLy8gUGljayBhIHJlbWFpbmluZyBlbGVtZW50Li4uXG4gICAgICAgICAgICByYW5kb21JbmRleCA9IE1hdGguZmxvb3IoTWF0aC5yYW5kb20oKSAqIGN1cnJlbnRJbmRleCk7XG4gICAgICAgICAgICBjdXJyZW50SW5kZXggLT0gMTtcbiAgICAgICAgICAgIC8vIEFuZCBzd2FwIGl0IHdpdGggdGhlIGN1cnJlbnQgZWxlbWVudC5cbiAgICAgICAgICAgIHRlbXBvcmFyeVZhbHVlID0gdGhpcy5pbmRleEFycmF5W2N1cnJlbnRJbmRleF07XG4gICAgICAgICAgICB0aGlzLmluZGV4QXJyYXlbY3VycmVudEluZGV4XSA9IHRoaXMuaW5kZXhBcnJheVtyYW5kb21JbmRleF07XG4gICAgICAgICAgICB0aGlzLmluZGV4QXJyYXlbcmFuZG9tSW5kZXhdID0gdGVtcG9yYXJ5VmFsdWU7XG4gICAgICAgIH1cbiAgICB9XG4gICAgLyo9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT1cbiAgICA9PSBSZXNldCBidXR0b24gZnVuY3Rpb25hbGl0eSA9PVxuICAgID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PSovXG4gICAgcmVzZXREcmFnZ2FibGVzKCkge1xuICAgICAgICBmb3IgKHZhciBpID0gMDsgaSA8IHRoaXMuZHJhZ1BhaXJBcnJheS5sZW5ndGg7IGkrKykge1xuICAgICAgICAgICAgZm9yIChcbiAgICAgICAgICAgICAgICB2YXIgaiA9IDA7XG4gICAgICAgICAgICAgICAgaiA8IHRoaXMuZHJhZ1BhaXJBcnJheVtpXVsxXS5jaGlsZE5vZGVzLmxlbmd0aDtcbiAgICAgICAgICAgICAgICBqKytcbiAgICAgICAgICAgICkge1xuICAgICAgICAgICAgICAgIGlmIChcbiAgICAgICAgICAgICAgICAgICAgJCh0aGlzLmRyYWdQYWlyQXJyYXlbaV1bMV0uY2hpbGROb2Rlc1tqXSkuYXR0cihcbiAgICAgICAgICAgICAgICAgICAgICAgIFwiZHJhZ2dhYmxlXCJcbiAgICAgICAgICAgICAgICAgICAgKSA9PT0gXCJ0cnVlXCJcbiAgICAgICAgICAgICAgICApIHtcbiAgICAgICAgICAgICAgICAgICAgdGhpcy5kcmFnZ2FibGVEaXYuYXBwZW5kQ2hpbGQoXG4gICAgICAgICAgICAgICAgICAgICAgICB0aGlzLmRyYWdQYWlyQXJyYXlbaV1bMV0uY2hpbGROb2Rlc1tqXVxuICAgICAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgICB0aGlzLmZlZWRCYWNrRGl2LnN0eWxlLmRpc3BsYXkgPSBcIm5vbmVcIjtcbiAgICB9XG4gICAgLyo9PT09PT09PT09PT09PT09PT09PT09PT09PT1cbiAgICA9PSBFdmFsdWF0aW9uIGFuZCBmZWVkYmFjayA9PVxuICAgID09PT09PT09PT09PT09PT09PT09PT09PT09PSovXG5cbiAgICBjaGVja0N1cnJlbnRBbnN3ZXIoKSB7XG4gICAgICAgIHRoaXMuY29ycmVjdCA9IHRydWU7XG4gICAgICAgIHRoaXMudW5hbnN3ZXJlZE51bSA9IDA7XG4gICAgICAgIHRoaXMuaW5jb3JyZWN0TnVtID0gMDtcbiAgICAgICAgdGhpcy5kcmFnTnVtID0gdGhpcy5kcmFnUGFpckFycmF5Lmxlbmd0aDtcbiAgICAgICAgZm9yICh2YXIgaSA9IDA7IGkgPCB0aGlzLmRyYWdQYWlyQXJyYXkubGVuZ3RoOyBpKyspIHtcbiAgICAgICAgICAgIGlmIChcbiAgICAgICAgICAgICAgICAhJCh0aGlzLmRyYWdQYWlyQXJyYXlbaV1bMV0pLmhhcyh0aGlzLmRyYWdQYWlyQXJyYXlbaV1bMF0pXG4gICAgICAgICAgICAgICAgICAgIC5sZW5ndGhcbiAgICAgICAgICAgICkge1xuICAgICAgICAgICAgICAgIHRoaXMuY29ycmVjdCA9IGZhbHNlO1xuICAgICAgICAgICAgICAgIHRoaXMuaW5jb3JyZWN0TnVtKys7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICBpZiAodGhpcy5oYXNOb0RyYWdDaGlsZCh0aGlzLmRyYWdQYWlyQXJyYXlbaV1bMV0pKSB7XG4gICAgICAgICAgICAgICAgdGhpcy51bmFuc3dlcmVkTnVtKys7XG4gICAgICAgICAgICAgICAgdGhpcy5pbmNvcnJlY3ROdW0gLT0gMTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgICB0aGlzLmNvcnJlY3ROdW0gPSB0aGlzLmRyYWdOdW0gLSB0aGlzLmluY29ycmVjdE51bSAtIHRoaXMudW5hbnN3ZXJlZE51bTtcbiAgICAgICAgdGhpcy5wZXJjZW50ID0gdGhpcy5jb3JyZWN0TnVtIC8gdGhpcy5kcmFnUGFpckFycmF5Lmxlbmd0aDtcbiAgICAgICAgdGhpcy5zZXRMb2NhbFN0b3JhZ2UoeyBjb3JyZWN0OiB0aGlzLmNvcnJlY3QgPyBcIlRcIiA6IFwiRlwiIH0pO1xuICAgIH1cblxuICAgIGFzeW5jIGxvZ0N1cnJlbnRBbnN3ZXIoc2lkKSB7XG4gICAgICAgIGxldCBhbnN3ZXIgPSB0aGlzLnByZWduYW50SW5kZXhBcnJheS5qb2luKFwiO1wiKTtcbiAgICAgICAgbGV0IGRhdGEgPSB7XG4gICAgICAgICAgICBldmVudDogXCJkcmFnTmRyb3BcIixcbiAgICAgICAgICAgIGFjdDogYW5zd2VyLFxuICAgICAgICAgICAgYW5zd2VyOiBhbnN3ZXIsXG4gICAgICAgICAgICBtaW5IZWlnaHQ6IHRoaXMubWluaGVpZ2h0LFxuICAgICAgICAgICAgZGl2X2lkOiB0aGlzLmRpdmlkLFxuICAgICAgICAgICAgY29ycmVjdDogdGhpcy5jb3JyZWN0LFxuICAgICAgICAgICAgY29ycmVjdE51bTogdGhpcy5jb3JyZWN0TnVtLFxuICAgICAgICAgICAgZHJhZ051bTogdGhpcy5kcmFnTnVtLFxuICAgICAgICB9O1xuICAgICAgICBpZiAodHlwZW9mIHNpZCAhPT0gXCJ1bmRlZmluZWRcIikge1xuICAgICAgICAgICAgZGF0YS5zaWQgPSBzaWQ7XG4gICAgICAgIH1cbiAgICAgICAgYXdhaXQgdGhpcy5sb2dCb29rRXZlbnQoZGF0YSk7XG4gICAgfVxuICAgIHJlbmRlckZlZWRiYWNrKCkge1xuICAgICAgICBmb3IgKHZhciBpID0gMDsgaSA8IHRoaXMuZHJhZ1BhaXJBcnJheS5sZW5ndGg7IGkrKykge1xuICAgICAgICAgICAgaWYgKFxuICAgICAgICAgICAgICAgICEkKHRoaXMuZHJhZ1BhaXJBcnJheVtpXVsxXSkuaGFzKHRoaXMuZHJhZ1BhaXJBcnJheVtpXVswXSlcbiAgICAgICAgICAgICAgICAgICAgLmxlbmd0aFxuICAgICAgICAgICAgKSB7XG4gICAgICAgICAgICAgICAgJCh0aGlzLmRyYWdQYWlyQXJyYXlbaV1bMV0pLmFkZENsYXNzKFwiZHJvcC1pbmNvcnJlY3RcIik7XG4gICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgICQodGhpcy5kcmFnUGFpckFycmF5W2ldWzFdKS5yZW1vdmVDbGFzcyhcImRyb3AtaW5jb3JyZWN0XCIpO1xuICAgICAgICAgICAgfVxuICAgICAgICB9XG5cbiAgICAgICAgaWYgKCF0aGlzLmZlZWRCYWNrRGl2KSB7XG4gICAgICAgICAgICB0aGlzLnJlbmRlckZlZWRiYWNrRGl2KCk7XG4gICAgICAgIH1cbiAgICAgICAgdGhpcy5mZWVkQmFja0Rpdi5zdHlsZS5kaXNwbGF5ID0gXCJibG9ja1wiO1xuICAgICAgICBpZiAodGhpcy5jb3JyZWN0KSB7XG4gICAgICAgICAgICB2YXIgbXNnQ29ycmVjdCA9ICQuaTE4bihcIm1zZ19kcmFnbmRyb3BfY29ycmVjdF9hbnN3ZXJcIik7XG4gICAgICAgICAgICAkKHRoaXMuZmVlZEJhY2tEaXYpLmh0bWwobXNnQ29ycmVjdCk7XG4gICAgICAgICAgICAkKHRoaXMuZmVlZEJhY2tEaXYpLmF0dHIoXG4gICAgICAgICAgICAgICAgXCJjbGFzc1wiLFxuICAgICAgICAgICAgICAgIFwiYWxlcnQgYWxlcnQtaW5mbyBkcmFnZ2FibGUtZmVlZGJhY2tcIlxuICAgICAgICAgICAgKTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIHZhciBtc2dJbmNvcnJlY3QgPSAkLmkxOG4oXG4gICAgICAgICAgICAgICAgJC5pMThuKFwibXNnX2RyYWduZHJvcF9pbmNvcnJlY3RfYW5zd2VyXCIpLFxuICAgICAgICAgICAgICAgIHRoaXMuY29ycmVjdE51bSxcbiAgICAgICAgICAgICAgICB0aGlzLmluY29ycmVjdE51bSxcbiAgICAgICAgICAgICAgICB0aGlzLmRyYWdOdW0sXG4gICAgICAgICAgICAgICAgdGhpcy51bmFuc3dlcmVkTnVtXG4gICAgICAgICAgICApO1xuICAgICAgICAgICAgJCh0aGlzLmZlZWRCYWNrRGl2KS5odG1sKG1zZ0luY29ycmVjdCArIFwiIFwiICsgdGhpcy5mZWVkYmFjayk7XG4gICAgICAgICAgICAkKHRoaXMuZmVlZEJhY2tEaXYpLmF0dHIoXG4gICAgICAgICAgICAgICAgXCJjbGFzc1wiLFxuICAgICAgICAgICAgICAgIFwiYWxlcnQgYWxlcnQtZGFuZ2VyIGRyYWdnYWJsZS1mZWVkYmFja1wiXG4gICAgICAgICAgICApO1xuICAgICAgICB9XG4gICAgfVxuICAgIC8qPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT1cbiAgICA9PT0gQ2hlY2tpbmcvcmVzdG9yaW5nIGZyb20gc3RvcmFnZSA9PT1cbiAgICA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PSovXG4gICAgcmVzdG9yZUFuc3dlcnMoZGF0YSkge1xuICAgICAgICAvLyBSZXN0b3JlIGFuc3dlcnMgZnJvbSBzdG9yYWdlIHJldHJpZXZhbCBkb25lIGluIFJ1bmVzdG9uZUJhc2VcbiAgICAgICAgdGhpcy5oYXNTdG9yZWREcm9wem9uZXMgPSB0cnVlO1xuICAgICAgICB0aGlzLm1pbmhlaWdodCA9IGRhdGEubWluSGVpZ2h0O1xuICAgICAgICB0aGlzLnByZWduYW50SW5kZXhBcnJheSA9IGRhdGEuYW5zd2VyLnNwbGl0KFwiO1wiKTtcbiAgICAgICAgdGhpcy5maW5pc2hTZXR0aW5nVXAoKTtcbiAgICB9XG4gICAgY2hlY2tMb2NhbFN0b3JhZ2UoKSB7XG4gICAgICAgIGlmICh0aGlzLmdyYWRlcmFjdGl2ZSkge1xuICAgICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG4gICAgICAgIHZhciBzdG9yZWRPYmo7XG4gICAgICAgIHRoaXMuaGFzU3RvcmVkRHJvcHpvbmVzID0gZmFsc2U7XG4gICAgICAgIHZhciBsZW4gPSBsb2NhbFN0b3JhZ2UubGVuZ3RoO1xuICAgICAgICBpZiAobGVuID4gMCkge1xuICAgICAgICAgICAgdmFyIGV4ID0gbG9jYWxTdG9yYWdlLmdldEl0ZW0odGhpcy5sb2NhbFN0b3JhZ2VLZXkoKSk7XG4gICAgICAgICAgICBpZiAoZXggIT09IG51bGwpIHtcbiAgICAgICAgICAgICAgICB0aGlzLmhhc1N0b3JlZERyb3B6b25lcyA9IHRydWU7XG4gICAgICAgICAgICAgICAgdHJ5IHtcbiAgICAgICAgICAgICAgICAgICAgc3RvcmVkT2JqID0gSlNPTi5wYXJzZShleCk7XG4gICAgICAgICAgICAgICAgICAgIHRoaXMubWluaGVpZ2h0ID0gc3RvcmVkT2JqLm1pbkhlaWdodDtcbiAgICAgICAgICAgICAgICB9IGNhdGNoIChlcnIpIHtcbiAgICAgICAgICAgICAgICAgICAgLy8gZXJyb3Igd2hpbGUgcGFyc2luZzsgbGlrZWx5IGR1ZSB0byBiYWQgdmFsdWUgc3RvcmVkIGluIHN0b3JhZ2VcbiAgICAgICAgICAgICAgICAgICAgY29uc29sZS5sb2coZXJyLm1lc3NhZ2UpO1xuICAgICAgICAgICAgICAgICAgICBsb2NhbFN0b3JhZ2UucmVtb3ZlSXRlbSh0aGlzLmxvY2FsU3RvcmFnZUtleSgpKTtcbiAgICAgICAgICAgICAgICAgICAgdGhpcy5oYXNTdG9yZWREcm9wem9uZXMgPSBmYWxzZTtcbiAgICAgICAgICAgICAgICAgICAgdGhpcy5maW5pc2hTZXR0aW5nVXAoKTtcbiAgICAgICAgICAgICAgICAgICAgcmV0dXJuO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICB0aGlzLnByZWduYW50SW5kZXhBcnJheSA9IHN0b3JlZE9iai5hbnN3ZXIuc3BsaXQoXCI7XCIpO1xuICAgICAgICAgICAgICAgIGlmICh0aGlzLnVzZVJ1bmVzdG9uZVNlcnZpY2VzKSB7XG4gICAgICAgICAgICAgICAgICAgIC8vIHN0b3JlIGFuc3dlciBpbiBkYXRhYmFzZVxuICAgICAgICAgICAgICAgICAgICB2YXIgYW5zd2VyID0gdGhpcy5wcmVnbmFudEluZGV4QXJyYXkuam9pbihcIjtcIik7XG4gICAgICAgICAgICAgICAgICAgIHRoaXMubG9nQm9va0V2ZW50KHtcbiAgICAgICAgICAgICAgICAgICAgICAgIGV2ZW50OiBcImRyYWdOZHJvcFwiLFxuICAgICAgICAgICAgICAgICAgICAgICAgYWN0OiBhbnN3ZXIsXG4gICAgICAgICAgICAgICAgICAgICAgICBhbnN3ZXI6IGFuc3dlcixcbiAgICAgICAgICAgICAgICAgICAgICAgIG1pbkhlaWdodDogdGhpcy5taW5oZWlnaHQsXG4gICAgICAgICAgICAgICAgICAgICAgICBkaXZfaWQ6IHRoaXMuZGl2aWQsXG4gICAgICAgICAgICAgICAgICAgICAgICBjb3JyZWN0OiBzdG9yZWRPYmouY29ycmVjdCxcbiAgICAgICAgICAgICAgICAgICAgfSk7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICAgIHRoaXMuZmluaXNoU2V0dGluZ1VwKCk7XG4gICAgfVxuXG4gICAgc2V0TG9jYWxTdG9yYWdlKGRhdGEpIHtcbiAgICAgICAgaWYgKGRhdGEuYW5zd2VyID09PSB1bmRlZmluZWQpIHtcbiAgICAgICAgICAgIC8vIElmIHdlIGRpZG4ndCBsb2FkIGZyb20gdGhlIHNlcnZlciwgd2UgbXVzdCBnZW5lcmF0ZSB0aGUgZGF0YVxuICAgICAgICAgICAgdGhpcy5wcmVnbmFudEluZGV4QXJyYXkgPSBbXTtcbiAgICAgICAgICAgIGZvciAodmFyIGkgPSAwOyBpIDwgdGhpcy5kcmFnUGFpckFycmF5Lmxlbmd0aDsgaSsrKSB7XG4gICAgICAgICAgICAgICAgaWYgKCF0aGlzLmhhc05vRHJhZ0NoaWxkKHRoaXMuZHJhZ1BhaXJBcnJheVtpXVsxXSkpIHtcbiAgICAgICAgICAgICAgICAgICAgZm9yICh2YXIgaiA9IDA7IGogPCB0aGlzLmRyYWdQYWlyQXJyYXkubGVuZ3RoOyBqKyspIHtcbiAgICAgICAgICAgICAgICAgICAgICAgIGlmIChcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAkKHRoaXMuZHJhZ1BhaXJBcnJheVtpXVsxXSkuaGFzKFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB0aGlzLmRyYWdQYWlyQXJyYXlbal1bMF1cbiAgICAgICAgICAgICAgICAgICAgICAgICAgICApLmxlbmd0aFxuICAgICAgICAgICAgICAgICAgICAgICAgKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy5wcmVnbmFudEluZGV4QXJyYXkucHVzaChqKTtcbiAgICAgICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgICAgIHRoaXMucHJlZ25hbnRJbmRleEFycmF5LnB1c2goLTEpO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgICB2YXIgdGltZVN0YW1wID0gbmV3IERhdGUoKTtcbiAgICAgICAgdmFyIGNvcnJlY3QgPSBkYXRhLmNvcnJlY3Q7XG4gICAgICAgIHZhciBzdG9yYWdlT2JqID0ge1xuICAgICAgICAgICAgYW5zd2VyOiB0aGlzLnByZWduYW50SW5kZXhBcnJheS5qb2luKFwiO1wiKSxcbiAgICAgICAgICAgIG1pbkhlaWdodDogdGhpcy5taW5oZWlnaHQsXG4gICAgICAgICAgICB0aW1lc3RhbXA6IHRpbWVTdGFtcCxcbiAgICAgICAgICAgIGNvcnJlY3Q6IGNvcnJlY3QsXG4gICAgICAgIH07XG4gICAgICAgIGxvY2FsU3RvcmFnZS5zZXRJdGVtKFxuICAgICAgICAgICAgdGhpcy5sb2NhbFN0b3JhZ2VLZXkoKSxcbiAgICAgICAgICAgIEpTT04uc3RyaW5naWZ5KHN0b3JhZ2VPYmopXG4gICAgICAgICk7XG4gICAgfVxuXG4gICAgZGlzYWJsZUludGVyYWN0aW9uKCkge1xuICAgICAgICAkKHRoaXMucmVzZXRCdXR0b24pLmhpZGUoKTtcbiAgICAgICAgZm9yICh2YXIgaSA9IDA7IGkgPCB0aGlzLmRyYWdQYWlyQXJyYXkubGVuZ3RoOyBpKyspIHtcbiAgICAgICAgICAgIC8vIE5vIG1vcmUgZHJhZ2dpbmdcbiAgICAgICAgICAgICQodGhpcy5kcmFnUGFpckFycmF5W2ldWzBdKS5hdHRyKFwiZHJhZ2dhYmxlXCIsIFwiZmFsc2VcIik7XG4gICAgICAgICAgICAkKHRoaXMuZHJhZ1BhaXJBcnJheVtpXVswXSkuY3NzKFwiY3Vyc29yXCIsIFwiaW5pdGlhbFwiKTtcbiAgICAgICAgfVxuICAgIH1cbn1cblxuLyo9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT1cbj09IEZpbmQgdGhlIGN1c3RvbSBIVE1MIHRhZ3MgYW5kID09XG49PSAgIGV4ZWN1dGUgb3VyIGNvZGUgb24gdGhlbSAgICA9PVxuPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09Ki9cbiQoZG9jdW1lbnQpLmJpbmQoXCJydW5lc3RvbmU6bG9naW4tY29tcGxldGVcIiwgZnVuY3Rpb24gKCkge1xuICAgICQoXCJbZGF0YS1jb21wb25lbnQ9ZHJhZ25kcm9wXVwiKS5lYWNoKGZ1bmN0aW9uIChpbmRleCkge1xuICAgICAgICB2YXIgb3B0cyA9IHtcbiAgICAgICAgICAgIG9yaWc6IHRoaXMsXG4gICAgICAgICAgICB1c2VSdW5lc3RvbmVTZXJ2aWNlczogZUJvb2tDb25maWcudXNlUnVuZXN0b25lU2VydmljZXMsXG4gICAgICAgIH07XG4gICAgICAgIGlmICgkKHRoaXMpLmNsb3Nlc3QoXCJbZGF0YS1jb21wb25lbnQ9dGltZWRBc3Nlc3NtZW50XVwiKS5sZW5ndGggPT0gMCkge1xuICAgICAgICAgICAgLy8gSWYgdGhpcyBlbGVtZW50IGV4aXN0cyB3aXRoaW4gYSB0aW1lZCBjb21wb25lbnQsIGRvbid0IHJlbmRlciBpdCBoZXJlXG4gICAgICAgICAgICB0cnkge1xuICAgICAgICAgICAgICAgIGRkTGlzdFt0aGlzLmlkXSA9IG5ldyBEcmFnTkRyb3Aob3B0cyk7XG4gICAgICAgICAgICB9IGNhdGNoIChlcnIpIHtcbiAgICAgICAgICAgICAgICBjb25zb2xlLmxvZyhgRXJyb3IgcmVuZGVyaW5nIERyYWdORHJvcCBQcm9ibGVtICR7dGhpcy5pZH1gKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgIH0pO1xufSk7XG4iLCJcInVzZSBzdHJpY3RcIjtcblxuaW1wb3J0IERyYWdORHJvcCBmcm9tIFwiLi9kcmFnbmRyb3AuanNcIjtcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgVGltZWREcmFnTkRyb3AgZXh0ZW5kcyBEcmFnTkRyb3Age1xuICAgIGNvbnN0cnVjdG9yKG9wdHMpIHtcbiAgICAgICAgc3VwZXIob3B0cyk7XG4gICAgICAgIHRoaXMuZmluaXNoU2V0dGluZ1VwKCk7XG4gICAgICAgIHRoaXMucmVuZGVyVGltZWRJY29uKHRoaXMuY29udGFpbmVyRGl2KTtcbiAgICAgICAgdGhpcy5oaWRlQnV0dG9ucygpO1xuICAgIH1cbiAgICBoaWRlQnV0dG9ucygpIHtcbiAgICAgICAgJCh0aGlzLnN1Ym1pdEJ1dHRvbikuaGlkZSgpO1xuICAgIH1cbiAgICByZW5kZXJUaW1lZEljb24oY29tcG9uZW50KSB7XG4gICAgICAgIC8vIHJlbmRlcnMgdGhlIGNsb2NrIGljb24gb24gdGltZWQgY29tcG9uZW50cy4gICAgVGhlIGNvbXBvbmVudCBwYXJhbWV0ZXJcbiAgICAgICAgLy8gaXMgdGhlIGVsZW1lbnQgdGhhdCB0aGUgaWNvbiBzaG91bGQgYmUgYXBwZW5kZWQgdG8uXG4gICAgICAgIHZhciB0aW1lSWNvbkRpdiA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoXCJkaXZcIik7XG4gICAgICAgIHZhciB0aW1lSWNvbiA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoXCJpbWdcIik7XG4gICAgICAgICQodGltZUljb24pLmF0dHIoe1xuICAgICAgICAgICAgc3JjOiBcIi4uL19zdGF0aWMvY2xvY2sucG5nXCIsXG4gICAgICAgICAgICBzdHlsZTogXCJ3aWR0aDoxNXB4O2hlaWdodDoxNXB4XCIsXG4gICAgICAgIH0pO1xuICAgICAgICB0aW1lSWNvbkRpdi5jbGFzc05hbWUgPSBcInRpbWVUaXBcIjtcbiAgICAgICAgdGltZUljb25EaXYudGl0bGUgPSBcIlwiO1xuICAgICAgICB0aW1lSWNvbkRpdi5hcHBlbmRDaGlsZCh0aW1lSWNvbik7XG4gICAgICAgICQoY29tcG9uZW50KS5wcmVwZW5kKHRpbWVJY29uRGl2KTtcbiAgICB9XG4gICAgY2hlY2tDb3JyZWN0VGltZWQoKSB7XG4gICAgICAgIC8vIFJldHVybnMgaWYgdGhlIHF1ZXN0aW9uIHdhcyBjb3JyZWN0LiAgICBVc2VkIGZvciB0aW1lZCBhc3Nlc3NtZW50IGdyYWRpbmcuXG4gICAgICAgIGlmICh0aGlzLnVuYW5zd2VyZWROdW0gPT09IHRoaXMuZHJhZ1BhaXJBcnJheS5sZW5ndGgpIHtcbiAgICAgICAgICAgIHRoaXMuY29ycmVjdCA9IG51bGw7XG4gICAgICAgIH1cbiAgICAgICAgc3dpdGNoICh0aGlzLmNvcnJlY3QpIHtcbiAgICAgICAgICAgIGNhc2UgdHJ1ZTpcbiAgICAgICAgICAgICAgICByZXR1cm4gXCJUXCI7XG4gICAgICAgICAgICBjYXNlIGZhbHNlOlxuICAgICAgICAgICAgICAgIHJldHVybiBcIkZcIjtcbiAgICAgICAgICAgIGRlZmF1bHQ6XG4gICAgICAgICAgICAgICAgcmV0dXJuIG51bGw7XG4gICAgICAgIH1cbiAgICB9XG4gICAgaGlkZUZlZWRiYWNrKCkge1xuICAgICAgICAkKHRoaXMuZmVlZEJhY2tEaXYpLmhpZGUoKTtcbiAgICB9XG59XG5cbmlmICh0eXBlb2Ygd2luZG93LmNvbXBvbmVudF9mYWN0b3J5ID09PSBcInVuZGVmaW5lZFwiKSB7XG4gICAgd2luZG93LmNvbXBvbmVudF9mYWN0b3J5ID0ge307XG59XG53aW5kb3cuY29tcG9uZW50X2ZhY3RvcnlbXCJkcmFnbmRyb3BcIl0gPSBmdW5jdGlvbiAob3B0cykge1xuICAgIGlmIChvcHRzLnRpbWVkKSB7XG4gICAgICAgIHJldHVybiBuZXcgVGltZWREcmFnTkRyb3Aob3B0cyk7XG4gICAgfVxuICAgIHJldHVybiBuZXcgRHJhZ05Ecm9wKG9wdHMpO1xufTtcbiJdLCJzb3VyY2VSb290IjoiIn0=