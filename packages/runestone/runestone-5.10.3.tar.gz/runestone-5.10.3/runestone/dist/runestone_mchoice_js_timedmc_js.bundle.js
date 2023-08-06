(self["webpackChunkWebComponents"] = self["webpackChunkWebComponents"] || []).push([["runestone_mchoice_js_timedmc_js"],{

/***/ 25264:
/*!*******************************************!*\
  !*** ./runestone/mchoice/css/mchoice.css ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
// extracted by mini-css-extract-plugin


/***/ }),

/***/ 77147:
/*!*****************************************!*\
  !*** ./runestone/mchoice/js/mchoice.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "mcList": () => (/* binding */ mcList),
/* harmony export */   "default": () => (/* binding */ MultipleChoice)
/* harmony export */ });
/* harmony import */ var _common_js_runestonebase_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../common/js/runestonebase.js */ 2568);
/* harmony import */ var _css_mchoice_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../css/mchoice.css */ 25264);
/*==========================================
========      Master mchoice.js     =========
============================================
===  This file contains the JS for the   ===
=== Runestone multiple choice component. ===
============================================
===              Created By              ===
===           Isaiah Mayerchak           ===
===                 and                  ===
===             Kirby Olson              ===
===                6/4/15                ===
==========================================*/


//import "./../styles/runestone-custom-sphinx-bootstrap.css";


var mcList = {}; // Multiple Choice dictionary

// MC constructor
class MultipleChoice extends _common_js_runestonebase_js__WEBPACK_IMPORTED_MODULE_0__.default {
    constructor(opts) {
        super(opts);
        opts = opts || {};
        var orig = opts.orig; // entire <ul> element
        this.origElem = orig;
        this.useRunestoneServices = opts.useRunestoneServices;
        this.multipleanswers = false;
        this.divid = orig.id;
        if ($(this.origElem).data("multipleanswers") === true) {
            this.multipleanswers = true;
        }
        this.children = this.origElem.childNodes;
        this.random = false;
        if ($(this.origElem).is("[data-random]")) {
            this.random = true;
        }
        this.correct = null;
        this.answerList = [];
        this.correctList = [];
        this.correctIndexList = [];
        this.feedbackList = [];
        this.question = null;
        this.caption = "Multiple Choice";
        this.findAnswers();
        this.findQuestion();
        this.findFeedbacks();
        this.createCorrectList();
        this.createMCForm();
        this.addCaption("runestone");
        this.checkServer("mChoice", true);
    }

    /*====================================
    ==== Functions parsing variables  ====
    ====  out of intermediate HTML    ====
    ====================================*/
    findQuestion() {
        var delimiter;
        for (var i = 0; i < this.origElem.childNodes.length; i++) {
            if (this.origElem.childNodes[i].nodeName === "LI") {
                delimiter = this.origElem.childNodes[i].outerHTML;
                break;
            }
        }
        var fulltext = $(this.origElem).html();
        var temp = fulltext.split(delimiter);
        this.question = temp[0];
    }

    findAnswers() {
        // Creates answer objects and pushes them to answerList
        // format: ID, Correct bool, Content (text)
        var ChildAnswerList = [];
        for (var i = 0; i < this.children.length; i++) {
            if ($(this.children[i]).is("[data-component=answer]")) {
                ChildAnswerList.push(this.children[i]);
            }
        }
        for (var j = 0; j < ChildAnswerList.length; j++) {
            var answer_id = $(ChildAnswerList[j]).attr("id");
            var is_correct = false;
            if ($(ChildAnswerList[j]).is("[data-correct]")) {
                // If data-correct attribute exists, answer is correct
                is_correct = true;
            }
            var answer_text = $(ChildAnswerList[j]).html();
            var answer_object = {
                id: answer_id,
                correct: is_correct,
                content: answer_text,
            };
            this.answerList.push(answer_object);
        }
    }

    findFeedbacks() {
        for (var i = 0; i < this.children.length; i++) {
            if ($(this.children[i]).is("[data-component=feedback]")) {
                this.feedbackList.push(this.children[i].innerHTML);
            }
        }
    }

    createCorrectList() {
        // Creates array that holds the ID"s of correct answers
        // Also populates an array that holds the indeces of correct answers
        for (var i = 0; i < this.answerList.length; i++) {
            if (this.answerList[i].correct) {
                this.correctList.push(this.answerList[i].id);
                this.correctIndexList.push(i);
            }
        }
    }

    /*===========================================
    ====   Functions generating final HTML   ====
    ===========================================*/
    createMCForm() {
        this.renderMCContainer();
        this.renderMCForm(); // renders the form with options and buttons
        this.renderMCfeedbackDiv();
        // replaces intermediate HTML with rendered HTML
        $(this.origElem).replaceWith(this.containerDiv);
    }

    renderMCContainer() {
        this.containerDiv = document.createElement("div");
        $(this.containerDiv).html(this.question);
        $(this.containerDiv).addClass(this.origElem.getAttribute("class"));
        this.containerDiv.id = this.divid;
    }

    renderMCForm() {
        this.optsForm = document.createElement("form");
        this.optsForm.id = this.divid + "_form";
        $(this.optsForm).attr({
            method: "get",
            action: "",
            onsubmit: "return false;",
        });
        // generate form options
        this.renderMCFormOpts();
        this.renderMCFormButtons();
        // Append the form to the container
        this.containerDiv.appendChild(this.optsForm);
    }

    renderMCFormOpts() {
        // creates input DOM elements
        this.optionArray = []; // array with an object for each option containing the input and label for that option
        var input_type = "radio";
        if (this.multipleanswers) {
            input_type = "checkbox";
        }
        // this.indexArray is used to index through the answers
        // it is just 0-n normally, but the order is shuffled if the random option is present
        this.indexArray = [];
        for (var i = 0; i < this.answerList.length; i++) {
            this.indexArray.push(i);
        }
        if (this.random) {
            this.randomizeAnswers();
        }
        let self = this;
        let answerFunc = function () {
            self.isAnswered = true;
        };
        for (var j = 0; j < this.answerList.length; j++) {
            var k = this.indexArray[j];
            var optid = this.divid + "_opt_" + k;
            // Create the label for the input
            var label = document.createElement("label");
            // If the content begins with a ``<p>``, put the label inside of it. (Sphinx 2.0 puts all content in a ``<p>``, while Sphinx 1.8 doesn't).
            var content = this.answerList[k].content;
            var prefix = "";
            if (content.startsWith("<p>")) {
                prefix = "<p>";
                content = content.slice(3);
            }
            $(label).html(
                `${prefix}<input type="${input_type}" name="group1" value=${k} id=${optid}>${String.fromCharCode(
                    "A".charCodeAt(0) + j
                )}. ${content}`
            );
            // create the object to store in optionArray
            var optObj = {
                input: $(label).find("input")[0],
                label: label,
            };
            optObj.input.onclick = answerFunc;

            this.optionArray.push(optObj);
            // add the option to the form
            this.optsForm.appendChild(label);
            this.optsForm.appendChild(document.createElement("br"));
        }
    }

    renderMCFormButtons() {
        // submit and compare me buttons
        // Create submit button
        this.submitButton = document.createElement("button");
        this.submitButton.textContent = "Check Me";
        $(this.submitButton).attr({
            class: "btn btn-success",
            name: "do answer",
            type: "button",
        });
        if (this.multipleanswers) {
            this.submitButton.addEventListener(
                "click",
                function () {
                    this.processMCMASubmission(true);
                }.bind(this),
                false
            );
        } else {
            this.submitButton.addEventListener(
                "click",
                function (ev) {
                    ev.preventDefault();
                    this.processMCMFSubmission(true);
                }.bind(this),
                false
            );
        } // end else
        this.optsForm.appendChild(this.submitButton);
        // Create compare button
        if (this.useRunestoneServices) {
            this.compareButton = document.createElement("button");
            $(this.compareButton).attr({
                class: "btn btn-default",
                id: this.divid + "_bcomp",
                disabled: "",
                name: "compare",
            });
            this.compareButton.textContent = "Compare me";
            this.compareButton.addEventListener(
                "click",
                function () {
                    this.compareAnswers(this.divid);
                }.bind(this),
                false
            );
            this.optsForm.appendChild(this.compareButton);
        }
    }

    renderMCfeedbackDiv() {
        this.feedBackDiv = document.createElement("div");
        this.feedBackDiv.id = this.divid + "_feedback";
        this.containerDiv.appendChild(document.createElement("br"));
        this.containerDiv.appendChild(this.feedBackDiv);
    }

    randomizeAnswers() {
        // Makes the ordering of the answer choices random
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
            var temporaryFeedback = this.feedbackList[currentIndex];
            this.feedbackList[currentIndex] = this.feedbackList[randomIndex];
            this.feedbackList[randomIndex] = temporaryFeedback;
        }
    }

    /*===================================
    === Checking/loading from storage ===
    ===================================*/
    restoreAnswers(data) {
        // Restore answers from storage retrieval done in RunestoneBase
        // sometimes data.answer can be null
        if (!data.answer) {
            data.answer = "";
        }
        var answers = data.answer.split(",");
        for (var a = 0; a < answers.length; a++) {
            var index = answers[a];
            for (var b = 0; b < this.optionArray.length; b++) {
                if (this.optionArray[b].input.value == index) {
                    $(this.optionArray[b].input).attr("checked", "true");
                }
            }
        }
        if (this.multipleanswers) {
            this.processMCMASubmission(false);
        } else {
            this.processMCMFSubmission(false);
        }
    }

    checkLocalStorage() {
        // Repopulates MCMA questions with a user's previous answers,
        // which were stored into local storage.
        var storedData;
        var answers;
        if (this.graderactive) {
            return;
        }
        var len = localStorage.length;
        if (len > 0) {
            var ex = localStorage.getItem(this.localStorageKey());
            if (ex !== null) {
                try {
                    storedData = JSON.parse(ex);
                    answers = storedData.answer.split(",");
                } catch (err) {
                    // error while parsing; likely due to bad value stored in storage
                    console.log(err.message);
                    localStorage.removeItem(this.localStorageKey());
                    return;
                }
                for (var a = 0; a < answers.length; a++) {
                    var index = answers[a];
                    for (var b = 0; b < this.optionArray.length; b++) {
                        if (this.optionArray[b].input.value == index) {
                            $(this.optionArray[b].input).attr(
                                "checked",
                                "true"
                            );
                        }
                    }
                }
                if (this.useRunestoneServices) {
                    this.enableMCComparison();
                    this.getSubmittedOpts(); // to populate givenlog for logging
                    if (this.multipleanswers) {
                        this.logMCMAsubmission();
                    } else {
                        this.logMCMFsubmission();
                    }
                }
            }
        }
    }

    setLocalStorage(data) {
        var timeStamp = new Date();
        var storageObj = {
            answer: data.answer,
            timestamp: timeStamp,
            correct: data.correct,
        };
        localStorage.setItem(
            this.localStorageKey(),
            JSON.stringify(storageObj)
        );
    }

    /*===============================
    === Processing MC Submissions ===
    ===============================*/
    processMCMASubmission(logFlag) {
        // Called when the submit button is clicked
        this.getSubmittedOpts(); // make sure this.givenArray is populated
        this.scoreMCMASubmission();
        this.setLocalStorage({
            correct: this.correct ? "T" : "F",
            answer: this.givenArray.join(","),
        });
        if (logFlag) {
            this.logMCMAsubmission();
        }
        this.renderMCMAFeedBack();
        if (this.useRunestoneServices) {
            this.enableMCComparison();
        }
    }

    getSubmittedOpts() {
        var given;
        this.singlefeedback = ""; // Used for MCMF questions
        this.feedbackString = ""; // Used for MCMA questions
        this.givenArray = [];
        this.givenlog = "";
        var buttonObjs = this.optsForm.elements.group1;
        for (var i = 0; i < buttonObjs.length; i++) {
            if (buttonObjs[i].checked) {
                given = buttonObjs[i].value;
                this.givenArray.push(given);
                this.feedbackString += `<li value="${i + 1}">${this.feedbackList[i]
                    }</li>`;
                this.givenlog += given + ",";
                this.singlefeedback = this.feedbackList[i];
            }
        }
        this.givenArray.sort();
    }

    checkCurrentAnswer() {
        this.getSubmittedOpts();
        if (this.multipleanswers) {
            this.scoreMCMASubmission();
        } else {
            this.scoreMCMFSubmission();
        }
    }

    async logCurrentAnswer(sid) {
        if (this.multipleanswers) {
            await this.logMCMAsubmission(sid);
        } else {
            await this.logMCMFsubmission(sid);
        }
    }

    renderFeedback() {
        if (this.multipleanswers) {
            this.renderMCMAFeedBack();
        } else {
            this.renderMCMFFeedback();
        }
    }
    scoreMCMASubmission() {
        this.correctCount = 0;
        var correctIndex = 0;
        var givenIndex = 0;
        while (
            correctIndex < this.correctIndexList.length &&
            givenIndex < this.givenArray.length
        ) {
            if (
                this.givenArray[givenIndex] <
                this.correctIndexList[correctIndex]
            ) {
                givenIndex++;
            } else if (
                this.givenArray[givenIndex] ==
                this.correctIndexList[correctIndex]
            ) {
                this.correctCount++;
                givenIndex++;
                correctIndex++;
            } else {
                correctIndex++;
            }
        }
        var numGiven = this.givenArray.length;
        var numCorrect = this.correctCount;
        var numNeeded = this.correctList.length;
        this.answer = this.givenArray.join(",");
        this.correct = numCorrect === numNeeded && numNeeded === numGiven;
        if (numGiven === numNeeded) {
            this.percent = numCorrect / numNeeded;
        } else {
            this.percent = numCorrect / Math.max(numGiven, numNeeded);
        }
    }

    async logMCMAsubmission(sid) {
        var answer = this.answer;
        var correct = this.correct;
        var logAnswer =
            "answer:" + answer + ":" + (correct == "T" ? "correct" : "no");
        let data = {
            event: "mChoice",
            act: logAnswer,
            answer: answer,
            correct: correct,
            div_id: this.divid,
        };
        if (typeof sid !== "undefined") {
            data.sid = sid;
        }
        await this.logBookEvent(data);
    }

    renderMCMAFeedBack() {
        var answerStr = "answers";
        var numGiven = this.givenArray.length;
        if (numGiven === 1) {
            answerStr = "answer";
        }
        var numCorrect = this.correctCount;
        var numNeeded = this.correctList.length;
        var feedbackText = this.feedbackString;
        if (this.correct) {
            $(this.feedBackDiv).html(`✔️ <ol type="A">${feedbackText}</ul>`);
            $(this.feedBackDiv).attr("class", "alert alert-info");
        } else {
            $(this.feedBackDiv).html(
                `✖️ You gave ${numGiven} ${answerStr} and got ${numCorrect} correct of ${numNeeded} needed.<ol type="A">${feedbackText}</ul>`
            );
            $(this.feedBackDiv).attr("class", "alert alert-danger");
        }
    }

    processMCMFSubmission(logFlag) {
        // Called when the submit button is clicked
        this.getSubmittedOpts(); // make sure this.givenArray is populated
        this.scoreMCMFSubmission();
        this.setLocalStorage({
            correct: this.correct ? "T" : "F",
            answer: this.givenArray.join(","),
        });
        if (logFlag) {
            this.logMCMFsubmission();
        }
        this.renderMCMFFeedback();
        if (this.useRunestoneServices) {
            this.enableMCComparison();
        }
    }

    scoreMCMFSubmission() {
        if (this.givenArray[0] == this.correctIndexList[0]) {
            this.correct = true;
            this.percent = 1.0;
        } else if (this.givenArray[0] != null) {
            // if given is null then the question wasn"t answered and should be counted as skipped
            this.correct = false;
            this.percent = 0.0;
        }
    }

    async logMCMFsubmission(sid) {
        var answer = this.givenArray[0];
        var correct =
            this.givenArray[0] == this.correctIndexList[0] ? "T" : "F";
        var logAnswer =
            "answer:" + answer + ":" + (correct == "T" ? "correct" : "no"); // backward compatible
        let data = {
            event: "mChoice",
            act: logAnswer,
            answer: answer,
            correct: correct,
            div_id: this.divid,
        };
        if (typeof sid !== "undefined") {
            data.sid = sid;
        }
        await this.logBookEvent(data);
    }

    renderMCMFFeedback() {
        let correct = this.givenArray[0] == this.correctIndexList[0];
        let feedbackText = this.singlefeedback;

        if (correct) {
            $(this.feedBackDiv).html("✔️ " + feedbackText);
            $(this.feedBackDiv).attr("class", "alert alert-info"); // use blue for better red/green blue color blindness
        } else {
            if (feedbackText == null) {
                feedbackText = "";
            }
            $(this.feedBackDiv).html("✖️ " + feedbackText);
            $(this.feedBackDiv).attr("class", "alert alert-danger");
        }
    }
    enableMCComparison() {
        if (eBookConfig.enableCompareMe) {
            this.compareButton.disabled = false;
        }
    }
    instructorMchoiceModal(data) {
        // data.reslist -- student and their answers
        // data.answerDict    -- answers and count
        // data.correct - correct answer
        var res = "<table><tr><th>Student</th><th>Answer(s)</th></tr>";
        for (var i in data) {
            res +=
                "<tr><td>" +
                data[i][0] +
                "</td><td>" +
                data[i][1] +
                "</td></tr>";
        }
        res += "</table>";
        return res;
    }
    compareModal(data, status, whatever) {
        var datadict = JSON.parse(data)[0];
        var answers = datadict.answerDict;
        var misc = datadict.misc;
        var kl = Object.keys(answers).sort();
        var body = "<table>";
        body += "<tr><th>Answer</th><th>Percent</th></tr>";
        var theClass = "";
        for (var k in kl) {
            if (kl[k] === misc.correct) {
                theClass = "success";
            } else {
                theClass = "info";
            }
            body +=
                "<tr><td>" + kl[k] + "</td><td class='compare-me-progress'>";
            var pct = answers[kl[k]] + "%";
            body += "<div class='progress'>";
            body +=
                "    <div class='progress-bar progress-bar-" +
                theClass +
                "' style='width:" +
                pct +
                ";'>" +
                pct;
            body += "    </div>";
            body += "</div></td></tr>";
        }
        body += "</table>";
        if (misc.yourpct !== "unavailable") {
            body +=
                "<br /><p>You have " +
                misc.yourpct +
                "% correct for all questions</p>";
        }
        if (datadict.reslist !== undefined) {
            body += this.instructorMchoiceModal(datadict.reslist);
        }
        var html =
            "<div class='modal fade'>" +
            "    <div class='modal-dialog compare-modal'>" +
            "        <div class='modal-content'>" +
            "            <div class='modal-header'>" +
            "                <button type='button' class='close' data-dismiss='modal' aria-hidden='true'>&times;</button>" +
            "                <h4 class='modal-title'>Distribution of Answers</h4>" +
            "            </div>" +
            "            <div class='modal-body'>" +
            body +
            "            </div>" +
            "        </div>" +
            "    </div>" +
            "</div>";
        var el = $(html);
        el.modal();
    }
    compareAnswers() {
        var data = {};
        data.div_id = this.divid;
        data.course = eBookConfig.course;
        jQuery.get(
            eBookConfig.ajaxURL + "getaggregateresults",
            data,
            this.compareModal.bind(this)
        );
    }

    disableInteraction() {
        for (var i = 0; i < this.optionArray.length; i++) {
            this.optionArray[i].input.disabled = true;
        }
    }
}

/*=================================
== Find the custom HTML tags and ==
==   execute our code on them    ==
=================================*/
$(document).bind("runestone:login-complete", function () {
    $("[data-component=multiplechoice]").each(function (index) {
        // MC
        var opts = {
            orig: this,
            useRunestoneServices: eBookConfig.useRunestoneServices,
        };
        if ($(this).closest("[data-component=timedAssessment]").length == 0) {
            // If this element exists within a timed component, don't render it here
            mcList[this.id] = new MultipleChoice(opts);
        }
    });
});


/***/ }),

/***/ 95983:
/*!*****************************************!*\
  !*** ./runestone/mchoice/js/timedmc.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ TimedMC)
/* harmony export */ });
/* harmony import */ var _mchoice_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./mchoice.js */ 77147);


class TimedMC extends _mchoice_js__WEBPACK_IMPORTED_MODULE_0__.default {
    constructor(opts) {
        super(opts);
        $(this.containerDiv).addClass("alert alert-warning runestone");
        this.needsReinitialization = true;
        this.renderTimedIcon(this.MCContainer);
        this.hideButtons(); // Don't show per-question buttons in a timed assessment
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
    hideButtons() {
        //Just hiding the buttons doesn't prevent submitting the form when entering is clicked
        //We need to completely disable the buttons
        $(this.submitButton).attr("disabled", "true");
        $(this.submitButton).hide();
        $(this.compareButton).hide();
    }

    // These methods override the methods in the base class. Called from renderFeedback()
    //
    renderMCMAFeedBack() {
        this.feedbackTimedMC();
    }
    renderMCMFFeedback(whatever, whateverr) {
        this.feedbackTimedMC();
    }
    feedbackTimedMC() {
        for (var i = 0; i < this.indexArray.length; i++) {
            var tmpindex = this.indexArray[i];
            $(this.feedBackEachArray[i]).text(
                String.fromCharCode(65 + i) + ". " + this.feedbackList[i]
            );
            var tmpid = this.answerList[tmpindex].id;
            if (this.correctList.indexOf(tmpid) >= 0) {
                this.feedBackEachArray[i].classList.add(
                    "alert",
                    "alert-success"
                );
            } else {
                this.feedBackEachArray[i].classList.add(
                    "alert",
                    "alert-danger"
                );
            }
        }
    }
    renderMCFormOpts() {
        super.renderMCFormOpts();
        this.feedBackEachArray = [];
        for (var j = 0; j < this.answerList.length; j++) {
            var k = this.indexArray[j];
            var feedBackEach = document.createElement("div");
            feedBackEach.id = this.divid + "_eachFeedback_" + k;
            feedBackEach.classList.add("eachFeedback");
            this.feedBackEachArray.push(feedBackEach);
            this.optsForm.appendChild(feedBackEach);
        }
    }
    checkCorrectTimedMCMA() {
        if (
            this.correctCount === this.correctList.length &&
            this.correctList.length === this.givenArray.length
        ) {
            this.correct = true;
        } else if (this.givenArray.length !== 0) {
            this.correct = false;
        } else {
            // question was skipped
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
    checkCorrectTimedMCMF() {
        // Returns if the question was correct, incorrect, or skipped (return null in the last case)
        switch (this.correct) {
            case true:
                return "T";
            case false:
                return "F";
            default:
                return null;
        }
    }
    checkCorrectTimed() {
        if (this.multipleanswers) {
            return this.checkCorrectTimedMCMA();
        } else {
            return this.checkCorrectTimedMCMF();
        }
    }
    hideFeedback() {
        for (var i = 0; i < this.feedBackEachArray.length; i++) {
            $(this.feedBackEachArray[i]).hide();
        }
    }

    reinitializeListeners() {
        let self = this;
        let answerFunc = function () {
            self.isAnswered = true;
        };
        for (let opt of this.optionArray) {
            opt.input.onclick = answerFunc;
        }
    }
}

if (typeof window.component_factory === "undefined") {
    window.component_factory = {};
}

window.component_factory.multiplechoice = function (opts) {
    if (opts.timed) {
        return new TimedMC(opts);
    } else {
        return new _mchoice_js__WEBPACK_IMPORTED_MODULE_0__.default(opts);
    }
};


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9XZWJDb21wb25lbnRzLy4vcnVuZXN0b25lL21jaG9pY2UvY3NzL21jaG9pY2UuY3NzPzNjMWYiLCJ3ZWJwYWNrOi8vV2ViQ29tcG9uZW50cy8uL3J1bmVzdG9uZS9tY2hvaWNlL2pzL21jaG9pY2UuanMiLCJ3ZWJwYWNrOi8vV2ViQ29tcG9uZW50cy8uL3J1bmVzdG9uZS9tY2hvaWNlL2pzL3RpbWVkbWMuanMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7OztBQUFBOzs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUU2RDtBQUM3RDtBQUM0Qjs7QUFFckIsZ0JBQWdCOztBQUV2QjtBQUNlLDZCQUE2QixnRUFBYTtBQUN6RDtBQUNBO0FBQ0E7QUFDQSw2QkFBNkI7QUFDN0I7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLHVCQUF1QixxQ0FBcUM7QUFDNUQ7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsdUJBQXVCLDBCQUEwQjtBQUNqRDtBQUNBO0FBQ0E7QUFDQTtBQUNBLHVCQUF1Qiw0QkFBNEI7QUFDbkQ7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0EsdUJBQXVCLDBCQUEwQjtBQUNqRDtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBLHVCQUF1Qiw0QkFBNEI7QUFDbkQ7QUFDQTtB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Q0E7QUFDQTtBQUNBLHVCQUF1Qiw0QkFBNEI7QUFDbkQ7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFNBQVM7QUFDVDtBQUNBLFNBQVM7QUFDVDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsU0FBUztBQUNUO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsdUJBQXVCLG1DQUFtQztBQUMxRDtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTCxtQkFBbUIsZ0RBQWM7QUFDakM7QUFDQSIsImZpbGUiOiJydW5lc3RvbmVfbWNob2ljZV9qc190aW1lZG1jX2pzLmJ1bmRsZS5qcz92PTRjZjMyZGIyYzdmMDYxMTg0NjcyIiwic291cmNlc0NvbnRlbnQiOlsiLy8gZXh0cmFjdGVkIGJ5IG1pbmktY3NzLWV4dHJhY3QtcGx1Z2luXG5leHBvcnQge307IiwiLyo9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT1cbj09PT09PT09ICAgICAgTWFzdGVyIG1jaG9pY2UuanMgICAgID09PT09PT09PVxuPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT1cbj09PSAgVGhpcyBmaWxlIGNvbnRhaW5zIHRoZSBKUyBmb3IgdGhlICAgPT09XG49PT0gUnVuZXN0b25lIG11bHRpcGxlIGNob2ljZSBjb21wb25lbnQuID09PVxuPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT1cbj09PSAgICAgICAgICAgICAgQ3JlYXRlZCBCeSAgICAgICAgICAgICAgPT09XG49PT0gICAgICAgICAgIElzYWlhaCBNYXllcmNoYWsgICAgICAgICAgID09PVxuPT09ICAgICAgICAgICAgICAgICBhbmQgICAgICAgICAgICAgICAgICA9PT1cbj09PSAgICAgICAgICAgICBLaXJieSBPbHNvbiAgICAgICAgICAgICAgPT09XG49PT0gICAgICAgICAgICAgICAgNi80LzE1ICAgICAgICAgICAgICAgID09PVxuPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09Ki9cblxuaW1wb3J0IFJ1bmVzdG9uZUJhc2UgZnJvbSBcIi4uLy4uL2NvbW1vbi9qcy9ydW5lc3RvbmViYXNlLmpzXCI7XG4vL2ltcG9ydCBcIi4vLi4vc3R5bGVzL3J1bmVzdG9uZS1jdXN0b20tc3BoaW54LWJvb3RzdHJhcC5jc3NcIjtcbmltcG9ydCBcIi4uL2Nzcy9tY2hvaWNlLmNzc1wiO1xuXG5leHBvcnQgdmFyIG1jTGlzdCA9IHt9OyAvLyBNdWx0aXBsZSBDaG9pY2UgZGljdGlvbmFyeVxuXG4vLyBNQyBjb25zdHJ1Y3RvclxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgTXVsdGlwbGVDaG9pY2UgZXh0ZW5kcyBSdW5lc3RvbmVCYXNlIHtcbiAgICBjb25zdHJ1Y3RvcihvcHRzKSB7XG4gICAgICAgIHN1cGVyKG9wdHMpO1xuICAgICAgICBvcHRzID0gb3B0cyB8fCB7fTtcbiAgICAgICAgdmFyIG9yaWcgPSBvcHRzLm9yaWc7IC8vIGVudGlyZSA8dWw+IGVsZW1lbnRcbiAgICAgICAgdGhpcy5vcmlnRWxlbSA9IG9yaWc7XG4gICAgICAgIHRoaXMudXNlUnVuZXN0b25lU2VydmljZXMgPSBvcHRzLnVzZVJ1bmVzdG9uZVNlcnZpY2VzO1xuICAgICAgICB0aGlzLm11bHRpcGxlYW5zd2VycyA9IGZhbHNlO1xuICAgICAgICB0aGlzLmRpdmlkID0gb3JpZy5pZDtcbiAgICAgICAgaWYgKCQodGhpcy5vcmlnRWxlbSkuZGF0YShcIm11bHRpcGxlYW5zd2Vyc1wiKSA9PT0gdHJ1ZSkge1xuICAgICAgICAgICAgdGhpcy5tdWx0aXBsZWFuc3dlcnMgPSB0cnVlO1xuICAgICAgICB9XG4gICAgICAgIHRoaXMuY2hpbGRyZW4gPSB0aGlzLm9yaWdFbGVtLmNoaWxkTm9kZXM7XG4gICAgICAgIHRoaXMucmFuZG9tID0gZmFsc2U7XG4gICAgICAgIGlmICgkKHRoaXMub3JpZ0VsZW0pLmlzKFwiW2RhdGEtcmFuZG9tXVwiKSkge1xuICAgICAgICAgICAgdGhpcy5yYW5kb20gPSB0cnVlO1xuICAgICAgICB9XG4gICAgICAgIHRoaXMuY29ycmVjdCA9IG51bGw7XG4gICAgICAgIHRoaXMuYW5zd2VyTGlzdCA9IFtdO1xuICAgICAgICB0aGlzLmNvcnJlY3RMaXN0ID0gW107XG4gICAgICAgIHRoaXMuY29ycmVjdEluZGV4TGlzdCA9IFtdO1xuICAgICAgICB0aGlzLmZlZWRiYWNrTGlzdCA9IFtdO1xuICAgICAgICB0aGlzLnF1ZXN0aW9uID0gbnVsbDtcbiAgICAgICAgdGhpcy5jYXB0aW9uID0gXCJNdWx0aXBsZSBDaG9pY2VcIjtcbiAgICAgICAgdGhpcy5maW5kQW5zd2VycygpO1xuICAgICAgICB0aGlzLmZpbmRRdWVzdGlvbigpO1xuICAgICAgICB0aGlzLmZpbmRGZWVkYmFja3MoKTtcbiAgICAgICAgdGhpcy5jcmVhdGVDb3JyZWN0TGlzdCgpO1xuICAgICAgICB0aGlzLmNyZWF0ZU1DRm9ybSgpO1xuICAgICAgICB0aGlzLmFkZENhcHRpb24oXCJydW5lc3RvbmVcIik7XG4gICAgICAgIHRoaXMuY2hlY2tTZXJ2ZXIoXCJtQ2hvaWNlXCIsIHRydWUpO1xuICAgIH1cblxuICAgIC8qPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09XG4gICAgPT09PSBGdW5jdGlvbnMgcGFyc2luZyB2YXJpYWJsZXMgID09PT1cbiAgICA9PT09ICBvdXQgb2YgaW50ZXJtZWRpYXRlIEhUTUwgICAgPT09PVxuICAgID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PSovXG4gICAgZmluZFF1ZXN0aW9uKCkge1xuICAgICAgICB2YXIgZGVsaW1pdGVyO1xuICAgICAgICBmb3IgKHZhciBpID0gMDsgaSA8IHRoaXMub3JpZ0VsZW0uY2hpbGROb2Rlcy5sZW5ndGg7IGkrKykge1xuICAgICAgICAgICAgaWYgKHRoaXMub3JpZ0VsZW0uY2hpbGROb2Rlc1tpXS5ub2RlTmFtZSA9PT0gXCJMSVwiKSB7XG4gICAgICAgICAgICAgICAgZGVsaW1pdGVyID0gdGhpcy5vcmlnRWxlbS5jaGlsZE5vZGVzW2ldLm91dGVySFRNTDtcbiAgICAgICAgICAgICAgICBicmVhaztcbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgICB2YXIgZnVsbHRleHQgPSAkKHRoaXMub3JpZ0VsZW0pLmh0bWwoKTtcbiAgICAgICAgdmFyIHRlbXAgPSBmdWxsdGV4dC5zcGxpdChkZWxpbWl0ZXIpO1xuICAgICAgICB0aGlzLnF1ZXN0aW9uID0gdGVtcFswXTtcbiAgICB9XG5cbiAgICBmaW5kQW5zd2VycygpIHtcbiAgICAgICAgLy8gQ3JlYXRlcyBhbnN3ZXIgb2JqZWN0cyBhbmQgcHVzaGVzIHRoZW0gdG8gYW5zd2VyTGlzdFxuICAgICAgICAvLyBmb3JtYXQ6IElELCBDb3JyZWN0IGJvb2wsIENvbnRlbnQgKHRleHQpXG4gICAgICAgIHZhciBDaGlsZEFuc3dlckxpc3QgPSBbXTtcbiAgICAgICAgZm9yICh2YXIgaSA9IDA7IGkgPCB0aGlzLmNoaWxkcmVuLmxlbmd0aDsgaSsrKSB7XG4gICAgICAgICAgICBpZiAoJCh0aGlzLmNoaWxkcmVuW2ldKS5pcyhcIltkYXRhLWNvbXBvbmVudD1hbnN3ZXJdXCIpKSB7XG4gICAgICAgICAgICAgICAgQ2hpbGRBbnN3ZXJMaXN0LnB1c2godGhpcy5jaGlsZHJlbltpXSk7XG4gICAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgICAgZm9yICh2YXIgaiA9IDA7IGogPCBDaGlsZEFuc3dlckxpc3QubGVuZ3RoOyBqKyspIHtcbiAgICAgICAgICAgIHZhciBhbnN3ZXJfaWQgPSAkKENoaWxkQW5zd2VyTGlzdFtqXSkuYXR0cihcImlkXCIpO1xuICAgICAgICAgICAgdmFyIGlzX2NvcnJlY3QgPSBmYWxzZTtcbiAgICAgICAgICAgIGlmICgkKENoaWxkQW5zd2VyTGlzdFtqXSkuaXMoXCJbZGF0YS1jb3JyZWN0XVwiKSkge1xuICAgICAgICAgICAgICAgIC8vIElmIGRhdGEtY29ycmVjdCBhdHRyaWJ1dGUgZXhpc3RzLCBhbnN3ZXIgaXMgY29ycmVjdFxuICAgICAgICAgICAgICAgIGlzX2NvcnJlY3QgPSB0cnVlO1xuICAgICAgICAgICAgfVxuICAgICAgICAgICAgdmFyIGFuc3dlcl90ZXh0ID0gJChDaGlsZEFuc3dlckxpc3Rbal0pLmh0bWwoKTtcbiAgICAgICAgICAgIHZhciBhbnN3ZXJfb2JqZWN0ID0ge1xuICAgICAgICAgICAgICAgIGlkOiBhbnN3ZXJfaWQsXG4gICAgICAgICAgICAgICAgY29ycmVjdDogaXNfY29ycmVjdCxcbiAgICAgICAgICAgICAgICBjb250ZW50OiBhbnN3ZXJfdGV4dCxcbiAgICAgICAgICAgIH07XG4gICAgICAgICAgICB0aGlzLmFuc3dlckxpc3QucHVzaChhbnN3ZXJfb2JqZWN0KTtcbiAgICAgICAgfVxuICAgIH1cblxuICAgIGZpbmRGZWVkYmFja3MoKSB7XG4gICAgICAgIGZvciAodmFyIGkgPSAwOyBpIDwgdGhpcy5jaGlsZHJlbi5sZW5ndGg7IGkrKykge1xuICAgICAgICAgICAgaWYgKCQodGhpcy5jaGlsZHJlbltpXSkuaXMoXCJbZGF0YS1jb21wb25lbnQ9ZmVlZGJhY2tdXCIpKSB7XG4gICAgICAgICAgICAgICAgdGhpcy5mZWVkYmFja0xpc3QucHVzaCh0aGlzLmNoaWxkcmVuW2ldLmlubmVySFRNTCk7XG4gICAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICB9XG5cbiAgICBjcmVhdGVDb3JyZWN0TGlzdCgpIHtcbiAgICAgICAgLy8gQ3JlYXRlcyBhcnJheSB0aGF0IGhvbGRzIHRoZSBJRFwicyBvZiBjb3JyZWN0IGFuc3dlcnNcbiAgICAgICAgLy8gQWxzbyBwb3B1bGF0ZXMgYW4gYXJyYXkgdGhhdCBob2xkcyB0aGUgaW5kZWNlcyBvZiBjb3JyZWN0IGFuc3dlcnNcbiAgICAgICAgZm9yICh2YXIgaSA9IDA7IGkgPCB0aGlzLmFuc3dlckxpc3QubGVuZ3RoOyBpKyspIHtcbiAgICAgICAgICAgIGlmICh0aGlzLmFuc3dlckxpc3RbaV0uY29ycmVjdCkge1xuICAgICAgICAgICAgICAgIHRoaXMuY29ycmVjdExpc3QucHVzaCh0aGlzLmFuc3dlckxpc3RbaV0uaWQpO1xuICAgICAgICAgICAgICAgIHRoaXMuY29ycmVjdEluZGV4TGlzdC5wdXNoKGkpO1xuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgfVxuXG4gICAgLyo9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09XG4gICAgPT09PSAgIEZ1bmN0aW9ucyBnZW5lcmF0aW5nIGZpbmFsIEhUTUwgICA9PT09XG4gICAgPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PSovXG4gICAgY3JlYXRlTUNGb3JtKCkge1xuICAgICAgICB0aGlzLnJlbmRlck1DQ29udGFpbmVyKCk7XG4gICAgICAgIHRoaXMucmVuZGVyTUNGb3JtKCk7IC8vIHJlbmRlcnMgdGhlIGZvcm0gd2l0aCBvcHRpb25zIGFuZCBidXR0b25zXG4gICAgICAgIHRoaXMucmVuZGVyTUNmZWVkYmFja0RpdigpO1xuICAgICAgICAvLyByZXBsYWNlcyBpbnRlcm1lZGlhdGUgSFRNTCB3aXRoIHJlbmRlcmVkIEhUTUxcbiAgICAgICAgJCh0aGlzLm9yaWdFbGVtKS5yZXBsYWNlV2l0aCh0aGlzLmNvbnRhaW5lckRpdik7XG4gICAgfVxuXG4gICAgcmVuZGVyTUNDb250YWluZXIoKSB7XG4gICAgICAgIHRoaXMuY29udGFpbmVyRGl2ID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudChcImRpdlwiKTtcbiAgICAgICAgJCh0aGlzLmNvbnRhaW5lckRpdikuaHRtbCh0aGlzLnF1ZXN0aW9uKTtcbiAgICAgICAgJCh0aGlzLmNvbnRhaW5lckRpdikuYWRkQ2xhc3ModGhpcy5vcmlnRWxlbS5nZXRBdHRyaWJ1dGUoXCJjbGFzc1wiKSk7XG4gICAgICAgIHRoaXMuY29udGFpbmVyRGl2LmlkID0gdGhpcy5kaXZpZDtcbiAgICB9XG5cbiAgICByZW5kZXJNQ0Zvcm0oKSB7XG4gICAgICAgIHRoaXMub3B0c0Zvcm0gPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KFwiZm9ybVwiKTtcbiAgICAgICAgdGhpcy5vcHRzRm9ybS5pZCA9IHRoaXMuZGl2aWQgKyBcIl9mb3JtXCI7XG4gICAgICAgICQodGhpcy5vcHRzRm9ybSkuYXR0cih7XG4gICAgICAgICAgICBtZXRob2Q6IFwiZ2V0XCIsXG4gICAgICAgICAgICBhY3Rpb246IFwiXCIsXG4gICAgICAgICAgICBvbnN1Ym1pdDogXCJyZXR1cm4gZmFsc2U7XCIsXG4gICAgICAgIH0pO1xuICAgICAgICAvLyBnZW5lcmF0ZSBmb3JtIG9wdGlvbnNcbiAgICAgICAgdGhpcy5yZW5kZXJNQ0Zvcm1PcHRzKCk7XG4gICAgICAgIHRoaXMucmVuZGVyTUNGb3JtQnV0dG9ucygpO1xuICAgICAgICAvLyBBcHBlbmQgdGhlIGZvcm0gdG8gdGhlIGNvbnRhaW5lclxuICAgICAgICB0aGlzLmNvbnRhaW5lckRpdi5hcHBlbmRDaGlsZCh0aGlzLm9wdHNGb3JtKTtcbiAgICB9XG5cbiAgICByZW5kZXJNQ0Zvcm1PcHRzKCkge1xuICAgICAgICAvLyBjcmVhdGVzIGlucHV0IERPTSBlbGVtZW50c1xuICAgICAgICB0aGlzLm9wdGlvbkFycmF5ID0gW107IC8vIGFycmF5IHdpdGggYW4gb2JqZWN0IGZvciBlYWNoIG9wdGlvbiBjb250YWluaW5nIHRoZSBpbnB1dCBhbmQgbGFiZWwgZm9yIHRoYXQgb3B0aW9uXG4gICAgICAgIHZhciBpbnB1dF90eXBlID0gXCJyYWRpb1wiO1xuICAgICAgICBpZiAodGhpcy5tdWx0aXBsZWFuc3dlcnMpIHtcbiAgICAgICAgICAgIGlucHV0X3R5cGUgPSBcImNoZWNrYm94XCI7XG4gICAgICAgIH1cbiAgICAgICAgLy8gdGhpcy5pbmRleEFycmF5IGlzIHVzZWQgdG8gaW5kZXggdGhyb3VnaCB0aGUgYW5zd2Vyc1xuICAgICAgICAvLyBpdCBpcyBqdXN0IDAtbiBub3JtYWxseSwgYnV0IHRoZSBvcmRlciBpcyBzaHVmZmxlZCBpZiB0aGUgcmFuZG9tIG9wdGlvbiBpcyBwcmVzZW50XG4gICAgICAgIHRoaXMuaW5kZXhBcnJheSA9IFtdO1xuICAgICAgICBmb3IgKHZhciBpID0gMDsgaSA8IHRoaXMuYW5zd2VyTGlzdC5sZW5ndGg7IGkrKykge1xuICAgICAgICAgICAgdGhpcy5pbmRleEFycmF5LnB1c2goaSk7XG4gICAgICAgIH1cbiAgICAgICAgaWYgKHRoaXMucmFuZG9tKSB7XG4gICAgICAgICAgICB0aGlzLnJhbmRvbWl6ZUFuc3dlcnMoKTtcbiAgICAgICAgfVxuICAgICAgICBsZXQgc2VsZiA9IHRoaXM7XG4gICAgICAgIGxldCBhbnN3ZXJGdW5jID0gZnVuY3Rpb24gKCkge1xuICAgICAgICAgICAgc2VsZi5pc0Fuc3dlcmVkID0gdHJ1ZTtcbiAgICAgICAgfTtcbiAgICAgICAgZm9yICh2YXIgaiA9IDA7IGogPCB0aGlzLmFuc3dlckxpc3QubGVuZ3RoOyBqKyspIHtcbiAgICAgICAgICAgIHZhciBrID0gdGhpcy5pbmRleEFycmF5W2pdO1xuICAgICAgICAgICAgdmFyIG9wdGlkID0gdGhpcy5kaXZpZCArIFwiX29wdF9cIiArIGs7XG4gICAgICAgICAgICAvLyBDcmVhdGUgdGhlIGxhYmVsIGZvciB0aGUgaW5wdXRcbiAgICAgICAgICAgIHZhciBsYWJlbCA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoXCJsYWJlbFwiKTtcbiAgICAgICAgICAgIC8vIElmIHRoZSBjb250ZW50IGJlZ2lucyB3aXRoIGEgYGA8cD5gYCwgcHV0IHRoZSBsYWJlbCBpbnNpZGUgb2YgaXQuIChTcGhpbnggMi4wIHB1dHMgYWxsIGNvbnRlbnQgaW4gYSBgYDxwPmBgLCB3aGlsZSBTcGhpbnggMS44IGRvZXNuJ3QpLlxuICAgICAgICAgICAgdmFyIGNvbnRlbnQgPSB0aGlzLmFuc3dlckxpc3Rba10uY29udGVudDtcbiAgICAgICAgICAgIHZhciBwcmVmaXggPSBcIlwiO1xuICAgICAgICAgICAgaWYgKGNvbnRlbnQuc3RhcnRzV2l0aChcIjxwPlwiKSkge1xuICAgICAgICAgICAgICAgIHByZWZpeCA9IFwiPHA+XCI7XG4gICAgICAgICAgICAgICAgY29udGVudCA9IGNvbnRlbnQuc2xpY2UoMyk7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICAkKGxhYmVsKS5odG1sKFxuICAgICAgICAgICAgICAgIGAke3ByZWZpeH08aW5wdXQgdHlwZT1cIiR7aW5wdXRfdHlwZX1cIiBuYW1lPVwiZ3JvdXAxXCIgdmFsdWU9JHtrfSBpZD0ke29wdGlkfT4ke1N0cmluZy5mcm9tQ2hhckNvZGUoXG4gICAgICAgICAgICAgICAgICAgIFwiQVwiLmNoYXJDb2RlQXQoMCkgKyBqXG4gICAgICAgICAgICAgICAgKX0uICR7Y29udGVudH1gXG4gICAgICAgICAgICApO1xuICAgICAgICAgICAgLy8gY3JlYXRlIHRoZSBvYmplY3QgdG8gc3RvcmUgaW4gb3B0aW9uQXJyYXlcbiAgICAgICAgICAgIHZhciBvcHRPYmogPSB7XG4gICAgICAgICAgICAgICAgaW5wdXQ6ICQobGFiZWwpLmZpbmQoXCJpbnB1dFwiKVswXSxcbiAgICAgICAgICAgICAgICBsYWJlbDogbGFiZWwsXG4gICAgICAgICAgICB9O1xuICAgICAgICAgICAgb3B0T2JqLmlucHV0Lm9uY2xpY2sgPSBhbnN3ZXJGdW5jO1xuXG4gICAgICAgICAgICB0aGlzLm9wdGlvbkFycmF5LnB1c2gob3B0T2JqKTtcbiAgICAgICAgICAgIC8vIGFkZCB0aGUgb3B0aW9uIHRvIHRoZSBmb3JtXG4gICAgICAgICAgICB0aGlzLm9wdHNGb3JtLmFwcGVuZENoaWxkKGxhYmVsKTtcbiAgICAgICAgICAgIHRoaXMub3B0c0Zvcm0uYXBwZW5kQ2hpbGQoZG9jdW1lbnQuY3JlYXRlRWxlbWVudChcImJyXCIpKTtcbiAgICAgICAgfVxuICAgIH1cblxuICAgIHJlbmRlck1DRm9ybUJ1dHRvbnMoKSB7XG4gICAgICAgIC8vIHN1Ym1pdCBhbmQgY29tcGFyZSBtZSBidXR0b25zXG4gICAgICAgIC8vIENyZWF0ZSBzdWJtaXQgYnV0dG9uXG4gICAgICAgIHRoaXMuc3VibWl0QnV0dG9uID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudChcImJ1dHRvblwiKTtcbiAgICAgICAgdGhpcy5zdWJtaXRCdXR0b24udGV4dENvbnRlbnQgPSBcIkNoZWNrIE1lXCI7XG4gICAgICAgICQodGhpcy5zdWJtaXRCdXR0b24pLmF0dHIoe1xuICAgICAgICAgICAgY2xhc3M6IFwiYnRuIGJ0bi1zdWNjZXNzXCIsXG4gICAgICAgICAgICBuYW1lOiBcImRvIGFuc3dlclwiLFxuICAgICAgICAgICAgdHlwZTogXCJidXR0b25cIixcbiAgICAgICAgfSk7XG4gICAgICAgIGlmICh0aGlzLm11bHRpcGxlYW5zd2Vycykge1xuICAgICAgICAgICAgdGhpcy5zdWJtaXRCdXR0b24uYWRkRXZlbnRMaXN0ZW5lcihcbiAgICAgICAgICAgICAgICBcImNsaWNrXCIsXG4gICAgICAgICAgICAgICAgZnVuY3Rpb24gKCkge1xuICAgICAgICAgICAgICAgICAgICB0aGlzLnByb2Nlc3NNQ01BU3VibWlzc2lvbih0cnVlKTtcbiAgICAgICAgICAgICAgICB9LmJpbmQodGhpcyksXG4gICAgICAgICAgICAgICAgZmFsc2VcbiAgICAgICAgICAgICk7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICB0aGlzLnN1Ym1pdEJ1dHRvbi5hZGRFdmVudExpc3RlbmVyKFxuICAgICAgICAgICAgICAgIFwiY2xpY2tcIixcbiAgICAgICAgICAgICAgICBmdW5jdGlvbiAoZXYpIHtcbiAgICAgICAgICAgICAgICAgICAgZXYucHJldmVudERlZmF1bHQoKTtcbiAgICAgICAgICAgICAgICAgICAgdGhpcy5wcm9jZXNzTUNNRlN1Ym1pc3Npb24odHJ1ZSk7XG4gICAgICAgICAgICAgICAgfS5iaW5kKHRoaXMpLFxuICAgICAgICAgICAgICAgIGZhbHNlXG4gICAgICAgICAgICApO1xuICAgICAgICB9IC8vIGVuZCBlbHNlXG4gICAgICAgIHRoaXMub3B0c0Zvcm0uYXBwZW5kQ2hpbGQodGhpcy5zdWJtaXRCdXR0b24pO1xuICAgICAgICAvLyBDcmVhdGUgY29tcGFyZSBidXR0b25cbiAgICAgICAgaWYgKHRoaXMudXNlUnVuZXN0b25lU2VydmljZXMpIHtcbiAgICAgICAgICAgIHRoaXMuY29tcGFyZUJ1dHRvbiA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoXCJidXR0b25cIik7XG4gICAgICAgICAgICAkKHRoaXMuY29tcGFyZUJ1dHRvbikuYXR0cih7XG4gICAgICAgICAgICAgICAgY2xhc3M6IFwiYnRuIGJ0bi1kZWZhdWx0XCIsXG4gICAgICAgICAgICAgICAgaWQ6IHRoaXMuZGl2aWQgKyBcIl9iY29tcFwiLFxuICAgICAgICAgICAgICAgIGRpc2FibGVkOiBcIlwiLFxuICAgICAgICAgICAgICAgIG5hbWU6IFwiY29tcGFyZVwiLFxuICAgICAgICAgICAgfSk7XG4gICAgICAgICAgICB0aGlzLmNvbXBhcmVCdXR0b24udGV4dENvbnRlbnQgPSBcIkNvbXBhcmUgbWVcIjtcbiAgICAgICAgICAgIHRoaXMuY29tcGFyZUJ1dHRvbi5hZGRFdmVudExpc3RlbmVyKFxuICAgICAgICAgICAgICAgIFwiY2xpY2tcIixcbiAgICAgICAgICAgICAgICBmdW5jdGlvbiAoKSB7XG4gICAgICAgICAgICAgICAgICAgIHRoaXMuY29tcGFyZUFuc3dlcnModGhpcy5kaXZpZCk7XG4gICAgICAgICAgICAgICAgfS5iaW5kKHRoaXMpLFxuICAgICAgICAgICAgICAgIGZhbHNlXG4gICAgICAgICAgICApO1xuICAgICAgICAgICAgdGhpcy5vcHRzRm9ybS5hcHBlbmRDaGlsZCh0aGlzLmNvbXBhcmVCdXR0b24pO1xuICAgICAgICB9XG4gICAgfVxuXG4gICAgcmVuZGVyTUNmZWVkYmFja0RpdigpIHtcbiAgICAgICAgdGhpcy5mZWVkQmFja0RpdiA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoXCJkaXZcIik7XG4gICAgICAgIHRoaXMuZmVlZEJhY2tEaXYuaWQgPSB0aGlzLmRpdmlkICsgXCJfZmVlZGJhY2tcIjtcbiAgICAgICAgdGhpcy5jb250YWluZXJEaXYuYXBwZW5kQ2hpbGQoZG9jdW1lbnQuY3JlYXRlRWxlbWVudChcImJyXCIpKTtcbiAgICAgICAgdGhpcy5jb250YWluZXJEaXYuYXBwZW5kQ2hpbGQodGhpcy5mZWVkQmFja0Rpdik7XG4gICAgfVxuXG4gICAgcmFuZG9taXplQW5zd2VycygpIHtcbiAgICAgICAgLy8gTWFrZXMgdGhlIG9yZGVyaW5nIG9mIHRoZSBhbnN3ZXIgY2hvaWNlcyByYW5kb21cbiAgICAgICAgdmFyIGN1cnJlbnRJbmRleCA9IHRoaXMuaW5kZXhBcnJheS5sZW5ndGgsXG4gICAgICAgICAgICB0ZW1wb3JhcnlWYWx1ZSxcbiAgICAgICAgICAgIHJhbmRvbUluZGV4O1xuICAgICAgICAvLyBXaGlsZSB0aGVyZSByZW1haW4gZWxlbWVudHMgdG8gc2h1ZmZsZS4uLlxuICAgICAgICB3aGlsZSAoY3VycmVudEluZGV4ICE9PSAwKSB7XG4gICAgICAgICAgICAvLyBQaWNrIGEgcmVtYWluaW5nIGVsZW1lbnQuLi5cbiAgICAgICAgICAgIHJhbmRvbUluZGV4ID0gTWF0aC5mbG9vcihNYXRoLnJhbmRvbSgpICogY3VycmVudEluZGV4KTtcbiAgICAgICAgICAgIGN1cnJlbnRJbmRleCAtPSAxO1xuICAgICAgICAgICAgLy8gQW5kIHN3YXAgaXQgd2l0aCB0aGUgY3VycmVudCBlbGVtZW50LlxuICAgICAgICAgICAgdGVtcG9yYXJ5VmFsdWUgPSB0aGlzLmluZGV4QXJyYXlbY3VycmVudEluZGV4XTtcbiAgICAgICAgICAgIHRoaXMuaW5kZXhBcnJheVtjdXJyZW50SW5kZXhdID0gdGhpcy5pbmRleEFycmF5W3JhbmRvbUluZGV4XTtcbiAgICAgICAgICAgIHRoaXMuaW5kZXhBcnJheVtyYW5kb21JbmRleF0gPSB0ZW1wb3JhcnlWYWx1ZTtcbiAgICAgICAgICAgIHZhciB0ZW1wb3JhcnlGZWVkYmFjayA9IHRoaXMuZmVlZGJhY2tMaXN0W2N1cnJlbnRJbmRleF07XG4gICAgICAgICAgICB0aGlzLmZlZWRiYWNrTGlzdFtjdXJyZW50SW5kZXhdID0gdGhpcy5mZWVkYmFja0xpc3RbcmFuZG9tSW5kZXhdO1xuICAgICAgICAgICAgdGhpcy5mZWVkYmFja0xpc3RbcmFuZG9tSW5kZXhdID0gdGVtcG9yYXJ5RmVlZGJhY2s7XG4gICAgICAgIH1cbiAgICB9XG5cbiAgICAvKj09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09XG4gICAgPT09IENoZWNraW5nL2xvYWRpbmcgZnJvbSBzdG9yYWdlID09PVxuICAgID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09Ki9cbiAgICByZXN0b3JlQW5zd2VycyhkYXRhKSB7XG4gICAgICAgIC8vIFJlc3RvcmUgYW5zd2VycyBmcm9tIHN0b3JhZ2UgcmV0cmlldmFsIGRvbmUgaW4gUnVuZXN0b25lQmFzZVxuICAgICAgICAvLyBzb21ldGltZXMgZGF0YS5hbnN3ZXIgY2FuIGJlIG51bGxcbiAgICAgICAgaWYgKCFkYXRhLmFuc3dlcikge1xuICAgICAgICAgICAgZGF0YS5hbnN3ZXIgPSBcIlwiO1xuICAgICAgICB9XG4gICAgICAgIHZhciBhbnN3ZXJzID0gZGF0YS5hbnN3ZXIuc3BsaXQoXCIsXCIpO1xuICAgICAgICBmb3IgKHZhciBhID0gMDsgYSA8IGFuc3dlcnMubGVuZ3RoOyBhKyspIHtcbiAgICAgICAgICAgIHZhciBpbmRleCA9IGFuc3dlcnNbYV07XG4gICAgICAgICAgICBmb3IgKHZhciBiID0gMDsgYiA8IHRoaXMub3B0aW9uQXJyYXkubGVuZ3RoOyBiKyspIHtcbiAgICAgICAgICAgICAgICBpZiAodGhpcy5vcHRpb25BcnJheVtiXS5pbnB1dC52YWx1ZSA9PSBpbmRleCkge1xuICAgICAgICAgICAgICAgICAgICAkKHRoaXMub3B0aW9uQXJyYXlbYl0uaW5wdXQpLmF0dHIoXCJjaGVja2VkXCIsIFwidHJ1ZVwiKTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgICAgaWYgKHRoaXMubXVsdGlwbGVhbnN3ZXJzKSB7XG4gICAgICAgICAgICB0aGlzLnByb2Nlc3NNQ01BU3VibWlzc2lvbihmYWxzZSk7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICB0aGlzLnByb2Nlc3NNQ01GU3VibWlzc2lvbihmYWxzZSk7XG4gICAgICAgIH1cbiAgICB9XG5cbiAgICBjaGVja0xvY2FsU3RvcmFnZSgpIHtcbiAgICAgICAgLy8gUmVwb3B1bGF0ZXMgTUNNQSBxdWVzdGlvbnMgd2l0aCBhIHVzZXIncyBwcmV2aW91cyBhbnN3ZXJzLFxuICAgICAgICAvLyB3aGljaCB3ZXJlIHN0b3JlZCBpbnRvIGxvY2FsIHN0b3JhZ2UuXG4gICAgICAgIHZhciBzdG9yZWREYXRhO1xuICAgICAgICB2YXIgYW5zd2VycztcbiAgICAgICAgaWYgKHRoaXMuZ3JhZGVyYWN0aXZlKSB7XG4gICAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cbiAgICAgICAgdmFyIGxlbiA9IGxvY2FsU3RvcmFnZS5sZW5ndGg7XG4gICAgICAgIGlmIChsZW4gPiAwKSB7XG4gICAgICAgICAgICB2YXIgZXggPSBsb2NhbFN0b3JhZ2UuZ2V0SXRlbSh0aGlzLmxvY2FsU3RvcmFnZUtleSgpKTtcbiAgICAgICAgICAgIGlmIChleCAhPT0gbnVsbCkge1xuICAgICAgICAgICAgICAgIHRyeSB7XG4gICAgICAgICAgICAgICAgICAgIHN0b3JlZERhdGEgPSBKU09OLnBhcnNlKGV4KTtcbiAgICAgICAgICAgICAgICAgICAgYW5zd2VycyA9IHN0b3JlZERhdGEuYW5zd2VyLnNwbGl0KFwiLFwiKTtcbiAgICAgICAgICAgICAgICB9IGNhdGNoIChlcnIpIHtcbiAgICAgICAgICAgICAgICAgICAgLy8gZXJyb3Igd2hpbGUgcGFyc2luZzsgbGlrZWx5IGR1ZSB0byBiYWQgdmFsdWUgc3RvcmVkIGluIHN0b3JhZ2VcbiAgICAgICAgICAgICAgICAgICAgY29uc29sZS5sb2coZXJyLm1lc3NhZ2UpO1xuICAgICAgICAgICAgICAgICAgICBsb2NhbFN0b3JhZ2UucmVtb3ZlSXRlbSh0aGlzLmxvY2FsU3RvcmFnZUtleSgpKTtcbiAgICAgICAgICAgICAgICAgICAgcmV0dXJuO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICBmb3IgKHZhciBhID0gMDsgYSA8IGFuc3dlcnMubGVuZ3RoOyBhKyspIHtcbiAgICAgICAgICAgICAgICAgICAgdmFyIGluZGV4ID0gYW5zd2Vyc1thXTtcbiAgICAgICAgICAgICAgICAgICAgZm9yICh2YXIgYiA9IDA7IGIgPCB0aGlzLm9wdGlvbkFycmF5Lmxlbmd0aDsgYisrKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICBpZiAodGhpcy5vcHRpb25BcnJheVtiXS5pbnB1dC52YWx1ZSA9PSBpbmRleCkge1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgICQodGhpcy5vcHRpb25BcnJheVtiXS5pbnB1dCkuYXR0cihcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgXCJjaGVja2VkXCIsXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIFwidHJ1ZVwiXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgKTtcbiAgICAgICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICBpZiAodGhpcy51c2VSdW5lc3RvbmVTZXJ2aWNlcykge1xuICAgICAgICAgICAgICAgICAgICB0aGlzLmVuYWJsZU1DQ29tcGFyaXNvbigpO1xuICAgICAgICAgICAgICAgICAgICB0aGlzLmdldFN1Ym1pdHRlZE9wdHMoKTsgLy8gdG8gcG9wdWxhdGUgZ2l2ZW5sb2cgZm9yIGxvZ2dpbmdcbiAgICAgICAgICAgICAgICAgICAgaWYgKHRoaXMubXVsdGlwbGVhbnN3ZXJzKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICB0aGlzLmxvZ01DTUFzdWJtaXNzaW9uKCk7XG4gICAgICAgICAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgICAgICAgICB0aGlzLmxvZ01DTUZzdWJtaXNzaW9uKCk7XG4gICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICB9XG5cbiAgICBzZXRMb2NhbFN0b3JhZ2UoZGF0YSkge1xuICAgICAgICB2YXIgdGltZVN0YW1wID0gbmV3IERhdGUoKTtcbiAgICAgICAgdmFyIHN0b3JhZ2VPYmogPSB7XG4gICAgICAgICAgICBhbnN3ZXI6IGRhdGEuYW5zd2VyLFxuICAgICAgICAgICAgdGltZXN0YW1wOiB0aW1lU3RhbXAsXG4gICAgICAgICAgICBjb3JyZWN0OiBkYXRhLmNvcnJlY3QsXG4gICAgICAgIH07XG4gICAgICAgIGxvY2FsU3RvcmFnZS5zZXRJdGVtKFxuICAgICAgICAgICAgdGhpcy5sb2NhbFN0b3JhZ2VLZXkoKSxcbiAgICAgICAgICAgIEpTT04uc3RyaW5naWZ5KHN0b3JhZ2VPYmopXG4gICAgICAgICk7XG4gICAgfVxuXG4gICAgLyo9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09XG4gICAgPT09IFByb2Nlc3NpbmcgTUMgU3VibWlzc2lvbnMgPT09XG4gICAgPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PSovXG4gICAgcHJvY2Vzc01DTUFTdWJtaXNzaW9uKGxvZ0ZsYWcpIHtcbiAgICAgICAgLy8gQ2FsbGVkIHdoZW4gdGhlIHN1Ym1pdCBidXR0b24gaXMgY2xpY2tlZFxuICAgICAgICB0aGlzLmdldFN1Ym1pdHRlZE9wdHMoKTsgLy8gbWFrZSBzdXJlIHRoaXMuZ2l2ZW5BcnJheSBpcyBwb3B1bGF0ZWRcbiAgICAgICAgdGhpcy5zY29yZU1DTUFTdWJtaXNzaW9uKCk7XG4gICAgICAgIHRoaXMuc2V0TG9jYWxTdG9yYWdlKHtcbiAgICAgICAgICAgIGNvcnJlY3Q6IHRoaXMuY29ycmVjdCA/IFwiVFwiIDogXCJGXCIsXG4gICAgICAgICAgICBhbnN3ZXI6IHRoaXMuZ2l2ZW5BcnJheS5qb2luKFwiLFwiKSxcbiAgICAgICAgfSk7XG4gICAgICAgIGlmIChsb2dGbGFnKSB7XG4gICAgICAgICAgICB0aGlzLmxvZ01DTUFzdWJtaXNzaW9uKCk7XG4gICAgICAgIH1cbiAgICAgICAgdGhpcy5yZW5kZXJNQ01BRmVlZEJhY2soKTtcbiAgICAgICAgaWYgKHRoaXMudXNlUnVuZXN0b25lU2VydmljZXMpIHtcbiAgICAgICAgICAgIHRoaXMuZW5hYmxlTUNDb21wYXJpc29uKCk7XG4gICAgICAgIH1cbiAgICB9XG5cbiAgICBnZXRTdWJtaXR0ZWRPcHRzKCkge1xuICAgICAgICB2YXIgZ2l2ZW47XG4gICAgICAgIHRoaXMuc2luZ2xlZmVlZGJhY2sgPSBcIlwiOyAvLyBVc2VkIGZvciBNQ01GIHF1ZXN0aW9uc1xuICAgICAgICB0aGlzLmZlZWRiYWNrU3RyaW5nID0gXCJcIjsgLy8gVXNlZCBmb3IgTUNNQSBxdWVzdGlvbnNcbiAgICAgICAgdGhpcy5naXZlbkFycmF5ID0gW107XG4gICAgICAgIHRoaXMuZ2l2ZW5sb2cgPSBcIlwiO1xuICAgICAgICB2YXIgYnV0dG9uT2JqcyA9IHRoaXMub3B0c0Zvcm0uZWxlbWVudHMuZ3JvdXAxO1xuICAgICAgICBmb3IgKHZhciBpID0gMDsgaSA8IGJ1dHRvbk9ianMubGVuZ3RoOyBpKyspIHtcbiAgICAgICAgICAgIGlmIChidXR0b25PYmpzW2ldLmNoZWNrZWQpIHtcbiAgICAgICAgICAgICAgICBnaXZlbiA9IGJ1dHRvbk9ianNbaV0udmFsdWU7XG4gICAgICAgICAgICAgICAgdGhpcy5naXZlbkFycmF5LnB1c2goZ2l2ZW4pO1xuICAgICAgICAgICAgICAgIHRoaXMuZmVlZGJhY2tTdHJpbmcgKz0gYDxsaSB2YWx1ZT1cIiR7aSArIDF9XCI+JHt0aGlzLmZlZWRiYWNrTGlzdFtpXVxuICAgICAgICAgICAgICAgICAgICB9PC9saT5gO1xuICAgICAgICAgICAgICAgIHRoaXMuZ2l2ZW5sb2cgKz0gZ2l2ZW4gKyBcIixcIjtcbiAgICAgICAgICAgICAgICB0aGlzLnNpbmdsZWZlZWRiYWNrID0gdGhpcy5mZWVkYmFja0xpc3RbaV07XG4gICAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgICAgdGhpcy5naXZlbkFycmF5LnNvcnQoKTtcbiAgICB9XG5cbiAgICBjaGVja0N1cnJlbnRBbnN3ZXIoKSB7XG4gICAgICAgIHRoaXMuZ2V0U3VibWl0dGVkT3B0cygpO1xuICAgICAgICBpZiAodGhpcy5tdWx0aXBsZWFuc3dlcnMpIHtcbiAgICAgICAgICAgIHRoaXMuc2NvcmVNQ01BU3VibWlzc2lvbigpO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgdGhpcy5zY29yZU1DTUZTdWJtaXNzaW9uKCk7XG4gICAgICAgIH1cbiAgICB9XG5cbiAgICBhc3luYyBsb2dDdXJyZW50QW5zd2VyKHNpZCkge1xuICAgICAgICBpZiAodGhpcy5tdWx0aXBsZWFuc3dlcnMpIHtcbiAgICAgICAgICAgIGF3YWl0IHRoaXMubG9nTUNNQXN1Ym1pc3Npb24oc2lkKTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIGF3YWl0IHRoaXMubG9nTUNNRnN1Ym1pc3Npb24oc2lkKTtcbiAgICAgICAgfVxuICAgIH1cblxuICAgIHJlbmRlckZlZWRiYWNrKCkge1xuICAgICAgICBpZiAodGhpcy5tdWx0aXBsZWFuc3dlcnMpIHtcbiAgICAgICAgICAgIHRoaXMucmVuZGVyTUNNQUZlZWRCYWNrKCk7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICB0aGlzLnJlbmRlck1DTUZGZWVkYmFjaygpO1xuICAgICAgICB9XG4gICAgfVxuICAgIHNjb3JlTUNNQVN1Ym1pc3Npb24oKSB7XG4gICAgICAgIHRoaXMuY29ycmVjdENvdW50ID0gMDtcbiAgICAgICAgdmFyIGNvcnJlY3RJbmRleCA9IDA7XG4gICAgICAgIHZhciBnaXZlbkluZGV4ID0gMDtcbiAgICAgICAgd2hpbGUgKFxuICAgICAgICAgICAgY29ycmVjdEluZGV4IDwgdGhpcy5jb3JyZWN0SW5kZXhMaXN0Lmxlbmd0aCAmJlxuICAgICAgICAgICAgZ2l2ZW5JbmRleCA8IHRoaXMuZ2l2ZW5BcnJheS5sZW5ndGhcbiAgICAgICAgKSB7XG4gICAgICAgICAgICBpZiAoXG4gICAgICAgICAgICAgICAgdGhpcy5naXZlbkFycmF5W2dpdmVuSW5kZXhdIDxcbiAgICAgICAgICAgICAgICB0aGlzLmNvcnJlY3RJbmRleExpc3RbY29ycmVjdEluZGV4XVxuICAgICAgICAgICAgKSB7XG4gICAgICAgICAgICAgICAgZ2l2ZW5JbmRleCsrO1xuICAgICAgICAgICAgfSBlbHNlIGlmIChcbiAgICAgICAgICAgICAgICB0aGlzLmdpdmVuQXJyYXlbZ2l2ZW5JbmRleF0gPT1cbiAgICAgICAgICAgICAgICB0aGlzLmNvcnJlY3RJbmRleExpc3RbY29ycmVjdEluZGV4XVxuICAgICAgICAgICAgKSB7XG4gICAgICAgICAgICAgICAgdGhpcy5jb3JyZWN0Q291bnQrKztcbiAgICAgICAgICAgICAgICBnaXZlbkluZGV4Kys7XG4gICAgICAgICAgICAgICAgY29ycmVjdEluZGV4Kys7XG4gICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgIGNvcnJlY3RJbmRleCsrO1xuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICAgIHZhciBudW1HaXZlbiA9IHRoaXMuZ2l2ZW5BcnJheS5sZW5ndGg7XG4gICAgICAgIHZhciBudW1Db3JyZWN0ID0gdGhpcy5jb3JyZWN0Q291bnQ7XG4gICAgICAgIHZhciBudW1OZWVkZWQgPSB0aGlzLmNvcnJlY3RMaXN0Lmxlbmd0aDtcbiAgICAgICAgdGhpcy5hbnN3ZXIgPSB0aGlzLmdpdmVuQXJyYXkuam9pbihcIixcIik7XG4gICAgICAgIHRoaXMuY29ycmVjdCA9IG51bUNvcnJlY3QgPT09IG51bU5lZWRlZCAmJiBudW1OZWVkZWQgPT09IG51bUdpdmVuO1xuICAgICAgICBpZiAobnVtR2l2ZW4gPT09IG51bU5lZWRlZCkge1xuICAgICAgICAgICAgdGhpcy5wZXJjZW50ID0gbnVtQ29ycmVjdCAvIG51bU5lZWRlZDtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIHRoaXMucGVyY2VudCA9IG51bUNvcnJlY3QgLyBNYXRoLm1heChudW1HaXZlbiwgbnVtTmVlZGVkKTtcbiAgICAgICAgfVxuICAgIH1cblxuICAgIGFzeW5jIGxvZ01DTUFzdWJtaXNzaW9uKHNpZCkge1xuICAgICAgICB2YXIgYW5zd2VyID0gdGhpcy5hbnN3ZXI7XG4gICAgICAgIHZhciBjb3JyZWN0ID0gdGhpcy5jb3JyZWN0O1xuICAgICAgICB2YXIgbG9nQW5zd2VyID1cbiAgICAgICAgICAgIFwiYW5zd2VyOlwiICsgYW5zd2VyICsgXCI6XCIgKyAoY29ycmVjdCA9PSBcIlRcIiA/IFwiY29ycmVjdFwiIDogXCJub1wiKTtcbiAgICAgICAgbGV0IGRhdGEgPSB7XG4gICAgICAgICAgICBldmVudDogXCJtQ2hvaWNlXCIsXG4gICAgICAgICAgICBhY3Q6IGxvZ0Fuc3dlcixcbiAgICAgICAgICAgIGFuc3dlcjogYW5zd2VyLFxuICAgICAgICAgICAgY29ycmVjdDogY29ycmVjdCxcbiAgICAgICAgICAgIGRpdl9pZDogdGhpcy5kaXZpZCxcbiAgICAgICAgfTtcbiAgICAgICAgaWYgKHR5cGVvZiBzaWQgIT09IFwidW5kZWZpbmVkXCIpIHtcbiAgICAgICAgICAgIGRhdGEuc2lkID0gc2lkO1xuICAgICAgICB9XG4gICAgICAgIGF3YWl0IHRoaXMubG9nQm9va0V2ZW50KGRhdGEpO1xuICAgIH1cblxuICAgIHJlbmRlck1DTUFGZWVkQmFjaygpIHtcbiAgICAgICAgdmFyIGFuc3dlclN0ciA9IFwiYW5zd2Vyc1wiO1xuICAgICAgICB2YXIgbnVtR2l2ZW4gPSB0aGlzLmdpdmVuQXJyYXkubGVuZ3RoO1xuICAgICAgICBpZiAobnVtR2l2ZW4gPT09IDEpIHtcbiAgICAgICAgICAgIGFuc3dlclN0ciA9IFwiYW5zd2VyXCI7XG4gICAgICAgIH1cbiAgICAgICAgdmFyIG51bUNvcnJlY3QgPSB0aGlzLmNvcnJlY3RDb3VudDtcbiAgICAgICAgdmFyIG51bU5lZWRlZCA9IHRoaXMuY29ycmVjdExpc3QubGVuZ3RoO1xuICAgICAgICB2YXIgZmVlZGJhY2tUZXh0ID0gdGhpcy5mZWVkYmFja1N0cmluZztcbiAgICAgICAgaWYgKHRoaXMuY29ycmVjdCkge1xuICAgICAgICAgICAgJCh0aGlzLmZlZWRCYWNrRGl2KS5odG1sKGDinJTvuI8gPG9sIHR5cGU9XCJBXCI+JHtmZWVkYmFja1RleHR9PC91bD5gKTtcbiAgICAgICAgICAgICQodGhpcy5mZWVkQmFja0RpdikuYXR0cihcImNsYXNzXCIsIFwiYWxlcnQgYWxlcnQtaW5mb1wiKTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICQodGhpcy5mZWVkQmFja0RpdikuaHRtbChcbiAgICAgICAgICAgICAgICBg4pyW77iPIFlvdSBnYXZlICR7bnVtR2l2ZW59ICR7YW5zd2VyU3RyfSBhbmQgZ290ICR7bnVtQ29ycmVjdH0gY29ycmVjdCBvZiAke251bU5lZWRlZH0gbmVlZGVkLjxvbCB0eXBlPVwiQVwiPiR7ZmVlZGJhY2tUZXh0fTwvdWw+YFxuICAgICAgICAgICAgKTtcbiAgICAgICAgICAgICQodGhpcy5mZWVkQmFja0RpdikuYXR0cihcImNsYXNzXCIsIFwiYWxlcnQgYWxlcnQtZGFuZ2VyXCIpO1xuICAgICAgICB9XG4gICAgfVxuXG4gICAgcHJvY2Vzc01DTUZTdWJtaXNzaW9uKGxvZ0ZsYWcpIHtcbiAgICAgICAgLy8gQ2FsbGVkIHdoZW4gdGhlIHN1Ym1pdCBidXR0b24gaXMgY2xpY2tlZFxuICAgICAgICB0aGlzLmdldFN1Ym1pdHRlZE9wdHMoKTsgLy8gbWFrZSBzdXJlIHRoaXMuZ2l2ZW5BcnJheSBpcyBwb3B1bGF0ZWRcbiAgICAgICAgdGhpcy5zY29yZU1DTUZTdWJtaXNzaW9uKCk7XG4gICAgICAgIHRoaXMuc2V0TG9jYWxTdG9yYWdlKHtcbiAgICAgICAgICAgIGNvcnJlY3Q6IHRoaXMuY29ycmVjdCA/IFwiVFwiIDogXCJGXCIsXG4gICAgICAgICAgICBhbnN3ZXI6IHRoaXMuZ2l2ZW5BcnJheS5qb2luKFwiLFwiKSxcbiAgICAgICAgfSk7XG4gICAgICAgIGlmIChsb2dGbGFnKSB7XG4gICAgICAgICAgICB0aGlzLmxvZ01DTUZzdWJtaXNzaW9uKCk7XG4gICAgICAgIH1cbiAgICAgICAgdGhpcy5yZW5kZXJNQ01GRmVlZGJhY2soKTtcbiAgICAgICAgaWYgKHRoaXMudXNlUnVuZXN0b25lU2VydmljZXMpIHtcbiAgICAgICAgICAgIHRoaXMuZW5hYmxlTUNDb21wYXJpc29uKCk7XG4gICAgICAgIH1cbiAgICB9XG5cbiAgICBzY29yZU1DTUZTdWJtaXNzaW9uKCkge1xuICAgICAgICBpZiAodGhpcy5naXZlbkFycmF5WzBdID09IHRoaXMuY29ycmVjdEluZGV4TGlzdFswXSkge1xuICAgICAgICAgICAgdGhpcy5jb3JyZWN0ID0gdHJ1ZTtcbiAgICAgICAgICAgIHRoaXMucGVyY2VudCA9IDEuMDtcbiAgICAgICAgfSBlbHNlIGlmICh0aGlzLmdpdmVuQXJyYXlbMF0gIT0gbnVsbCkge1xuICAgICAgICAgICAgLy8gaWYgZ2l2ZW4gaXMgbnVsbCB0aGVuIHRoZSBxdWVzdGlvbiB3YXNuXCJ0IGFuc3dlcmVkIGFuZCBzaG91bGQgYmUgY291bnRlZCBhcyBza2lwcGVkXG4gICAgICAgICAgICB0aGlzLmNvcnJlY3QgPSBmYWxzZTtcbiAgICAgICAgICAgIHRoaXMucGVyY2VudCA9IDAuMDtcbiAgICAgICAgfVxuICAgIH1cblxuICAgIGFzeW5jIGxvZ01DTUZzdWJtaXNzaW9uKHNpZCkge1xuICAgICAgICB2YXIgYW5zd2VyID0gdGhpcy5naXZlbkFycmF5WzBdO1xuICAgICAgICB2YXIgY29ycmVjdCA9XG4gICAgICAgICAgICB0aGlzLmdpdmVuQXJyYXlbMF0gPT0gdGhpcy5jb3JyZWN0SW5kZXhMaXN0WzBdID8gXCJUXCIgOiBcIkZcIjtcbiAgICAgICAgdmFyIGxvZ0Fuc3dlciA9XG4gICAgICAgICAgICBcImFuc3dlcjpcIiArIGFuc3dlciArIFwiOlwiICsgKGNvcnJlY3QgPT0gXCJUXCIgPyBcImNvcnJlY3RcIiA6IFwibm9cIik7IC8vIGJhY2t3YXJkIGNvbXBhdGlibGVcbiAgICAgICAgbGV0IGRhdGEgPSB7XG4gICAgICAgICAgICBldmVudDogXCJtQ2hvaWNlXCIsXG4gICAgICAgICAgICBhY3Q6IGxvZ0Fuc3dlcixcbiAgICAgICAgICAgIGFuc3dlcjogYW5zd2VyLFxuICAgICAgICAgICAgY29ycmVjdDogY29ycmVjdCxcbiAgICAgICAgICAgIGRpdl9pZDogdGhpcy5kaXZpZCxcbiAgICAgICAgfTtcbiAgICAgICAgaWYgKHR5cGVvZiBzaWQgIT09IFwidW5kZWZpbmVkXCIpIHtcbiAgICAgICAgICAgIGRhdGEuc2lkID0gc2lkO1xuICAgICAgICB9XG4gICAgICAgIGF3YWl0IHRoaXMubG9nQm9va0V2ZW50KGRhdGEpO1xuICAgIH1cblxuICAgIHJlbmRlck1DTUZGZWVkYmFjaygpIHtcbiAgICAgICAgbGV0IGNvcnJlY3QgPSB0aGlzLmdpdmVuQXJyYXlbMF0gPT0gdGhpcy5jb3JyZWN0SW5kZXhMaXN0WzBdO1xuICAgICAgICBsZXQgZmVlZGJhY2tUZXh0ID0gdGhpcy5zaW5nbGVmZWVkYmFjaztcblxuICAgICAgICBpZiAoY29ycmVjdCkge1xuICAgICAgICAgICAgJCh0aGlzLmZlZWRCYWNrRGl2KS5odG1sKFwi4pyU77iPIFwiICsgZmVlZGJhY2tUZXh0KTtcbiAgICAgICAgICAgICQodGhpcy5mZWVkQmFja0RpdikuYXR0cihcImNsYXNzXCIsIFwiYWxlcnQgYWxlcnQtaW5mb1wiKTsgLy8gdXNlIGJsdWUgZm9yIGJldHRlciByZWQvZ3JlZW4gYmx1ZSBjb2xvciBibGluZG5lc3NcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIGlmIChmZWVkYmFja1RleHQgPT0gbnVsbCkge1xuICAgICAgICAgICAgICAgIGZlZWRiYWNrVGV4dCA9IFwiXCI7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICAkKHRoaXMuZmVlZEJhY2tEaXYpLmh0bWwoXCLinJbvuI8gXCIgKyBmZWVkYmFja1RleHQpO1xuICAgICAgICAgICAgJCh0aGlzLmZlZWRCYWNrRGl2KS5hdHRyKFwiY2xhc3NcIiwgXCJhbGVydCBhbGVydC1kYW5nZXJcIik7XG4gICAgICAgIH1cbiAgICB9XG4gICAgZW5hYmxlTUNDb21wYXJpc29uKCkge1xuICAgICAgICBpZiAoZUJvb2tDb25maWcuZW5hYmxlQ29tcGFyZU1lKSB7XG4gICAgICAgICAgICB0aGlzLmNvbXBhcmVCdXR0b24uZGlzYWJsZWQgPSBmYWxzZTtcbiAgICAgICAgfVxuICAgIH1cbiAgICBpbnN0cnVjdG9yTWNob2ljZU1vZGFsKGRhdGEpIHtcbiAgICAgICAgLy8gZGF0YS5yZXNsaXN0IC0tIHN0dWRlbnQgYW5kIHRoZWlyIGFuc3dlcnNcbiAgICAgICAgLy8gZGF0YS5hbnN3ZXJEaWN0ICAgIC0tIGFuc3dlcnMgYW5kIGNvdW50XG4gICAgICAgIC8vIGRhdGEuY29ycmVjdCAtIGNvcnJlY3QgYW5zd2VyXG4gICAgICAgIHZhciByZXMgPSBcIjx0YWJsZT48dHI+PHRoPlN0dWRlbnQ8L3RoPjx0aD5BbnN3ZXIocyk8L3RoPjwvdHI+XCI7XG4gICAgICAgIGZvciAodmFyIGkgaW4gZGF0YSkge1xuICAgICAgICAgICAgcmVzICs9XG4gICAgICAgICAgICAgICAgXCI8dHI+PHRkPlwiICtcbiAgICAgICAgICAgICAgICBkYXRhW2ldWzBdICtcbiAgICAgICAgICAgICAgICBcIjwvdGQ+PHRkPlwiICtcbiAgICAgICAgICAgICAgICBkYXRhW2ldWzFdICtcbiAgICAgICAgICAgICAgICBcIjwvdGQ+PC90cj5cIjtcbiAgICAgICAgfVxuICAgICAgICByZXMgKz0gXCI8L3RhYmxlPlwiO1xuICAgICAgICByZXR1cm4gcmVzO1xuICAgIH1cbiAgICBjb21wYXJlTW9kYWwoZGF0YSwgc3RhdHVzLCB3aGF0ZXZlcikge1xuICAgICAgICB2YXIgZGF0YWRpY3QgPSBKU09OLnBhcnNlKGRhdGEpWzBdO1xuICAgICAgICB2YXIgYW5zd2VycyA9IGRhdGFkaWN0LmFuc3dlckRpY3Q7XG4gICAgICAgIHZhciBtaXNjID0gZGF0YWRpY3QubWlzYztcbiAgICAgICAgdmFyIGtsID0gT2JqZWN0LmtleXMoYW5zd2Vycykuc29ydCgpO1xuICAgICAgICB2YXIgYm9keSA9IFwiPHRhYmxlPlwiO1xuICAgICAgICBib2R5ICs9IFwiPHRyPjx0aD5BbnN3ZXI8L3RoPjx0aD5QZXJjZW50PC90aD48L3RyPlwiO1xuICAgICAgICB2YXIgdGhlQ2xhc3MgPSBcIlwiO1xuICAgICAgICBmb3IgKHZhciBrIGluIGtsKSB7XG4gICAgICAgICAgICBpZiAoa2xba10gPT09IG1pc2MuY29ycmVjdCkge1xuICAgICAgICAgICAgICAgIHRoZUNsYXNzID0gXCJzdWNjZXNzXCI7XG4gICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgIHRoZUNsYXNzID0gXCJpbmZvXCI7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICBib2R5ICs9XG4gICAgICAgICAgICAgICAgXCI8dHI+PHRkPlwiICsga2xba10gKyBcIjwvdGQ+PHRkIGNsYXNzPSdjb21wYXJlLW1lLXByb2dyZXNzJz5cIjtcbiAgICAgICAgICAgIHZhciBwY3QgPSBhbnN3ZXJzW2tsW2tdXSArIFwiJVwiO1xuICAgICAgICAgICAgYm9keSArPSBcIjxkaXYgY2xhc3M9J3Byb2dyZXNzJz5cIjtcbiAgICAgICAgICAgIGJvZHkgKz1cbiAgICAgICAgICAgICAgICBcIiAgICA8ZGl2IGNsYXNzPSdwcm9ncmVzcy1iYXIgcHJvZ3Jlc3MtYmFyLVwiICtcbiAgICAgICAgICAgICAgICB0aGVDbGFzcyArXG4gICAgICAgICAgICAgICAgXCInIHN0eWxlPSd3aWR0aDpcIiArXG4gICAgICAgICAgICAgICAgcGN0ICtcbiAgICAgICAgICAgICAgICBcIjsnPlwiICtcbiAgICAgICAgICAgICAgICBwY3Q7XG4gICAgICAgICAgICBib2R5ICs9IFwiICAgIDwvZGl2PlwiO1xuICAgICAgICAgICAgYm9keSArPSBcIjwvZGl2PjwvdGQ+PC90cj5cIjtcbiAgICAgICAgfVxuICAgICAgICBib2R5ICs9IFwiPC90YWJsZT5cIjtcbiAgICAgICAgaWYgKG1pc2MueW91cnBjdCAhPT0gXCJ1bmF2YWlsYWJsZVwiKSB7XG4gICAgICAgICAgICBib2R5ICs9XG4gICAgICAgICAgICAgICAgXCI8YnIgLz48cD5Zb3UgaGF2ZSBcIiArXG4gICAgICAgICAgICAgICAgbWlzYy55b3VycGN0ICtcbiAgICAgICAgICAgICAgICBcIiUgY29ycmVjdCBmb3IgYWxsIHF1ZXN0aW9uczwvcD5cIjtcbiAgICAgICAgfVxuICAgICAgICBpZiAoZGF0YWRpY3QucmVzbGlzdCAhPT0gdW5kZWZpbmVkKSB7XG4gICAgICAgICAgICBib2R5ICs9IHRoaXMuaW5zdHJ1Y3Rvck1jaG9pY2VNb2RhbChkYXRhZGljdC5yZXNsaXN0KTtcbiAgICAgICAgfVxuICAgICAgICB2YXIgaHRtbCA9XG4gICAgICAgICAgICBcIjxkaXYgY2xhc3M9J21vZGFsIGZhZGUnPlwiICtcbiAgICAgICAgICAgIFwiICAgIDxkaXYgY2xhc3M9J21vZGFsLWRpYWxvZyBjb21wYXJlLW1vZGFsJz5cIiArXG4gICAgICAgICAgICBcIiAgICAgICAgPGRpdiBjbGFzcz0nbW9kYWwtY29udGVudCc+XCIgK1xuICAgICAgICAgICAgXCIgICAgICAgICAgICA8ZGl2IGNsYXNzPSdtb2RhbC1oZWFkZXInPlwiICtcbiAgICAgICAgICAgIFwiICAgICAgICAgICAgICAgIDxidXR0b24gdHlwZT0nYnV0dG9uJyBjbGFzcz0nY2xvc2UnIGRhdGEtZGlzbWlzcz0nbW9kYWwnIGFyaWEtaGlkZGVuPSd0cnVlJz4mdGltZXM7PC9idXR0b24+XCIgK1xuICAgICAgICAgICAgXCIgICAgICAgICAgICAgICAgPGg0IGNsYXNzPSdtb2RhbC10aXRsZSc+RGlzdHJpYnV0aW9uIG9mIEFuc3dlcnM8L2g0PlwiICtcbiAgICAgICAgICAgIFwiICAgICAgICAgICAgPC9kaXY+XCIgK1xuICAgICAgICAgICAgXCIgICAgICAgICAgICA8ZGl2IGNsYXNzPSdtb2RhbC1ib2R5Jz5cIiArXG4gICAgICAgICAgICBib2R5ICtcbiAgICAgICAgICAgIFwiICAgICAgICAgICAgPC9kaXY+XCIgK1xuICAgICAgICAgICAgXCIgICAgICAgIDwvZGl2PlwiICtcbiAgICAgICAgICAgIFwiICAgIDwvZGl2PlwiICtcbiAgICAgICAgICAgIFwiPC9kaXY+XCI7XG4gICAgICAgIHZhciBlbCA9ICQoaHRtbCk7XG4gICAgICAgIGVsLm1vZGFsKCk7XG4gICAgfVxuICAgIGNvbXBhcmVBbnN3ZXJzKCkge1xuICAgICAgICB2YXIgZGF0YSA9IHt9O1xuICAgICAgICBkYXRhLmRpdl9pZCA9IHRoaXMuZGl2aWQ7XG4gICAgICAgIGRhdGEuY291cnNlID0gZUJvb2tDb25maWcuY291cnNlO1xuICAgICAgICBqUXVlcnkuZ2V0KFxuICAgICAgICAgICAgZUJvb2tDb25maWcuYWpheFVSTCArIFwiZ2V0YWdncmVnYXRlcmVzdWx0c1wiLFxuICAgICAgICAgICAgZGF0YSxcbiAgICAgICAgICAgIHRoaXMuY29tcGFyZU1vZGFsLmJpbmQodGhpcylcbiAgICAgICAgKTtcbiAgICB9XG5cbiAgICBkaXNhYmxlSW50ZXJhY3Rpb24oKSB7XG4gICAgICAgIGZvciAodmFyIGkgPSAwOyBpIDwgdGhpcy5vcHRpb25BcnJheS5sZW5ndGg7IGkrKykge1xuICAgICAgICAgICAgdGhpcy5vcHRpb25BcnJheVtpXS5pbnB1dC5kaXNhYmxlZCA9IHRydWU7XG4gICAgICAgIH1cbiAgICB9XG59XG5cbi8qPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09XG49PSBGaW5kIHRoZSBjdXN0b20gSFRNTCB0YWdzIGFuZCA9PVxuPT0gICBleGVjdXRlIG91ciBjb2RlIG9uIHRoZW0gICAgPT1cbj09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PSovXG4kKGRvY3VtZW50KS5iaW5kKFwicnVuZXN0b25lOmxvZ2luLWNvbXBsZXRlXCIsIGZ1bmN0aW9uICgpIHtcbiAgICAkKFwiW2RhdGEtY29tcG9uZW50PW11bHRpcGxlY2hvaWNlXVwiKS5lYWNoKGZ1bmN0aW9uIChpbmRleCkge1xuICAgICAgICAvLyBNQ1xuICAgICAgICB2YXIgb3B0cyA9IHtcbiAgICAgICAgICAgIG9yaWc6IHRoaXMsXG4gICAgICAgICAgICB1c2VSdW5lc3RvbmVTZXJ2aWNlczogZUJvb2tDb25maWcudXNlUnVuZXN0b25lU2VydmljZXMsXG4gICAgICAgIH07XG4gICAgICAgIGlmICgkKHRoaXMpLmNsb3Nlc3QoXCJbZGF0YS1jb21wb25lbnQ9dGltZWRBc3Nlc3NtZW50XVwiKS5sZW5ndGggPT0gMCkge1xuICAgICAgICAgICAgLy8gSWYgdGhpcyBlbGVtZW50IGV4aXN0cyB3aXRoaW4gYSB0aW1lZCBjb21wb25lbnQsIGRvbid0IHJlbmRlciBpdCBoZXJlXG4gICAgICAgICAgICBtY0xpc3RbdGhpcy5pZF0gPSBuZXcgTXVsdGlwbGVDaG9pY2Uob3B0cyk7XG4gICAgICAgIH1cbiAgICB9KTtcbn0pO1xuIiwiaW1wb3J0IE11bHRpcGxlQ2hvaWNlIGZyb20gXCIuL21jaG9pY2UuanNcIjtcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgVGltZWRNQyBleHRlbmRzIE11bHRpcGxlQ2hvaWNlIHtcbiAgICBjb25zdHJ1Y3RvcihvcHRzKSB7XG4gICAgICAgIHN1cGVyKG9wdHMpO1xuICAgICAgICAkKHRoaXMuY29udGFpbmVyRGl2KS5hZGRDbGFzcyhcImFsZXJ0IGFsZXJ0LXdhcm5pbmcgcnVuZXN0b25lXCIpO1xuICAgICAgICB0aGlzLm5lZWRzUmVpbml0aWFsaXphdGlvbiA9IHRydWU7XG4gICAgICAgIHRoaXMucmVuZGVyVGltZWRJY29uKHRoaXMuTUNDb250YWluZXIpO1xuICAgICAgICB0aGlzLmhpZGVCdXR0b25zKCk7IC8vIERvbid0IHNob3cgcGVyLXF1ZXN0aW9uIGJ1dHRvbnMgaW4gYSB0aW1lZCBhc3Nlc3NtZW50XG4gICAgfVxuXG4gICAgcmVuZGVyVGltZWRJY29uKGNvbXBvbmVudCkge1xuICAgICAgICAvLyByZW5kZXJzIHRoZSBjbG9jayBpY29uIG9uIHRpbWVkIGNvbXBvbmVudHMuICAgIFRoZSBjb21wb25lbnQgcGFyYW1ldGVyXG4gICAgICAgIC8vIGlzIHRoZSBlbGVtZW50IHRoYXQgdGhlIGljb24gc2hvdWxkIGJlIGFwcGVuZGVkIHRvLlxuICAgICAgICB2YXIgdGltZUljb25EaXYgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KFwiZGl2XCIpO1xuICAgICAgICB2YXIgdGltZUljb24gPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KFwiaW1nXCIpO1xuICAgICAgICAkKHRpbWVJY29uKS5hdHRyKHtcbiAgICAgICAgICAgIHNyYzogXCIuLi9fc3RhdGljL2Nsb2NrLnBuZ1wiLFxuICAgICAgICAgICAgc3R5bGU6IFwid2lkdGg6MTVweDtoZWlnaHQ6MTVweFwiLFxuICAgICAgICB9KTtcbiAgICAgICAgdGltZUljb25EaXYuY2xhc3NOYW1lID0gXCJ0aW1lVGlwXCI7XG4gICAgICAgIHRpbWVJY29uRGl2LnRpdGxlID0gXCJcIjtcbiAgICAgICAgdGltZUljb25EaXYuYXBwZW5kQ2hpbGQodGltZUljb24pO1xuICAgICAgICAkKGNvbXBvbmVudCkucHJlcGVuZCh0aW1lSWNvbkRpdik7XG4gICAgfVxuICAgIGhpZGVCdXR0b25zKCkge1xuICAgICAgICAvL0p1c3QgaGlkaW5nIHRoZSBidXR0b25zIGRvZXNuJ3QgcHJldmVudCBzdWJtaXR0aW5nIHRoZSBmb3JtIHdoZW4gZW50ZXJpbmcgaXMgY2xpY2tlZFxuICAgICAgICAvL1dlIG5lZWQgdG8gY29tcGxldGVseSBkaXNhYmxlIHRoZSBidXR0b25zXG4gICAgICAgICQodGhpcy5zdWJtaXRCdXR0b24pLmF0dHIoXCJkaXNhYmxlZFwiLCBcInRydWVcIik7XG4gICAgICAgICQodGhpcy5zdWJtaXRCdXR0b24pLmhpZGUoKTtcbiAgICAgICAgJCh0aGlzLmNvbXBhcmVCdXR0b24pLmhpZGUoKTtcbiAgICB9XG5cbiAgICAvLyBUaGVzZSBtZXRob2RzIG92ZXJyaWRlIHRoZSBtZXRob2RzIGluIHRoZSBiYXNlIGNsYXNzLiBDYWxsZWQgZnJvbSByZW5kZXJGZWVkYmFjaygpXG4gICAgLy9cbiAgICByZW5kZXJNQ01BRmVlZEJhY2soKSB7XG4gICAgICAgIHRoaXMuZmVlZGJhY2tUaW1lZE1DKCk7XG4gICAgfVxuICAgIHJlbmRlck1DTUZGZWVkYmFjayh3aGF0ZXZlciwgd2hhdGV2ZXJyKSB7XG4gICAgICAgIHRoaXMuZmVlZGJhY2tUaW1lZE1DKCk7XG4gICAgfVxuICAgIGZlZWRiYWNrVGltZWRNQygpIHtcbiAgICAgICAgZm9yICh2YXIgaSA9IDA7IGkgPCB0aGlzLmluZGV4QXJyYXkubGVuZ3RoOyBpKyspIHtcbiAgICAgICAgICAgIHZhciB0bXBpbmRleCA9IHRoaXMuaW5kZXhBcnJheVtpXTtcbiAgICAgICAgICAgICQodGhpcy5mZWVkQmFja0VhY2hBcnJheVtpXSkudGV4dChcbiAgICAgICAgICAgICAgICBTdHJpbmcuZnJvbUNoYXJDb2RlKDY1ICsgaSkgKyBcIi4gXCIgKyB0aGlzLmZlZWRiYWNrTGlzdFtpXVxuICAgICAgICAgICAgKTtcbiAgICAgICAgICAgIHZhciB0bXBpZCA9IHRoaXMuYW5zd2VyTGlzdFt0bXBpbmRleF0uaWQ7XG4gICAgICAgICAgICBpZiAodGhpcy5jb3JyZWN0TGlzdC5pbmRleE9mKHRtcGlkKSA+PSAwKSB7XG4gICAgICAgICAgICAgICAgdGhpcy5mZWVkQmFja0VhY2hBcnJheVtpXS5jbGFzc0xpc3QuYWRkKFxuICAgICAgICAgICAgICAgICAgICBcImFsZXJ0XCIsXG4gICAgICAgICAgICAgICAgICAgIFwiYWxlcnQtc3VjY2Vzc1wiXG4gICAgICAgICAgICAgICAgKTtcbiAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgdGhpcy5mZWVkQmFja0VhY2hBcnJheVtpXS5jbGFzc0xpc3QuYWRkKFxuICAgICAgICAgICAgICAgICAgICBcImFsZXJ0XCIsXG4gICAgICAgICAgICAgICAgICAgIFwiYWxlcnQtZGFuZ2VyXCJcbiAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgfVxuICAgIHJlbmRlck1DRm9ybU9wdHMoKSB7XG4gICAgICAgIHN1cGVyLnJlbmRlck1DRm9ybU9wdHMoKTtcbiAgICAgICAgdGhpcy5mZWVkQmFja0VhY2hBcnJheSA9IFtdO1xuICAgICAgICBmb3IgKHZhciBqID0gMDsgaiA8IHRoaXMuYW5zd2VyTGlzdC5sZW5ndGg7IGorKykge1xuICAgICAgICAgICAgdmFyIGsgPSB0aGlzLmluZGV4QXJyYXlbal07XG4gICAgICAgICAgICB2YXIgZmVlZEJhY2tFYWNoID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudChcImRpdlwiKTtcbiAgICAgICAgICAgIGZlZWRCYWNrRWFjaC5pZCA9IHRoaXMuZGl2aWQgKyBcIl9lYWNoRmVlZGJhY2tfXCIgKyBrO1xuICAgICAgICAgICAgZmVlZEJhY2tFYWNoLmNsYXNzTGlzdC5hZGQoXCJlYWNoRmVlZGJhY2tcIik7XG4gICAgICAgICAgICB0aGlzLmZlZWRCYWNrRWFjaEFycmF5LnB1c2goZmVlZEJhY2tFYWNoKTtcbiAgICAgICAgICAgIHRoaXMub3B0c0Zvcm0uYXBwZW5kQ2hpbGQoZmVlZEJhY2tFYWNoKTtcbiAgICAgICAgfVxuICAgIH1cbiAgICBjaGVja0NvcnJlY3RUaW1lZE1DTUEoKSB7XG4gICAgICAgIGlmIChcbiAgICAgICAgICAgIHRoaXMuY29ycmVjdENvdW50ID09PSB0aGlzLmNvcnJlY3RMaXN0Lmxlbmd0aCAmJlxuICAgICAgICAgICAgdGhpcy5jb3JyZWN0TGlzdC5sZW5ndGggPT09IHRoaXMuZ2l2ZW5BcnJheS5sZW5ndGhcbiAgICAgICAgKSB7XG4gICAgICAgICAgICB0aGlzLmNvcnJlY3QgPSB0cnVlO1xuICAgICAgICB9IGVsc2UgaWYgKHRoaXMuZ2l2ZW5BcnJheS5sZW5ndGggIT09IDApIHtcbiAgICAgICAgICAgIHRoaXMuY29ycmVjdCA9IGZhbHNlO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgLy8gcXVlc3Rpb24gd2FzIHNraXBwZWRcbiAgICAgICAgICAgIHRoaXMuY29ycmVjdCA9IG51bGw7XG4gICAgICAgIH1cbiAgICAgICAgc3dpdGNoICh0aGlzLmNvcnJlY3QpIHtcbiAgICAgICAgICAgIGNhc2UgdHJ1ZTpcbiAgICAgICAgICAgICAgICByZXR1cm4gXCJUXCI7XG4gICAgICAgICAgICBjYXNlIGZhbHNlOlxuICAgICAgICAgICAgICAgIHJldHVybiBcIkZcIjtcbiAgICAgICAgICAgIGRlZmF1bHQ6XG4gICAgICAgICAgICAgICAgcmV0dXJuIG51bGw7XG4gICAgICAgIH1cbiAgICB9XG4gICAgY2hlY2tDb3JyZWN0VGltZWRNQ01GKCkge1xuICAgICAgICAvLyBSZXR1cm5zIGlmIHRoZSBxdWVzdGlvbiB3YXMgY29ycmVjdCwgaW5jb3JyZWN0LCBvciBza2lwcGVkIChyZXR1cm4gbnVsbCBpbiB0aGUgbGFzdCBjYXNlKVxuICAgICAgICBzd2l0Y2ggKHRoaXMuY29ycmVjdCkge1xuICAgICAgICAgICAgY2FzZSB0cnVlOlxuICAgICAgICAgICAgICAgIHJldHVybiBcIlRcIjtcbiAgICAgICAgICAgIGNhc2UgZmFsc2U6XG4gICAgICAgICAgICAgICAgcmV0dXJuIFwiRlwiO1xuICAgICAgICAgICAgZGVmYXVsdDpcbiAgICAgICAgICAgICAgICByZXR1cm4gbnVsbDtcbiAgICAgICAgfVxuICAgIH1cbiAgICBjaGVja0NvcnJlY3RUaW1lZCgpIHtcbiAgICAgICAgaWYgKHRoaXMubXVsdGlwbGVhbnN3ZXJzKSB7XG4gICAgICAgICAgICByZXR1cm4gdGhpcy5jaGVja0NvcnJlY3RUaW1lZE1DTUEoKTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIHJldHVybiB0aGlzLmNoZWNrQ29ycmVjdFRpbWVkTUNNRigpO1xuICAgICAgICB9XG4gICAgfVxuICAgIGhpZGVGZWVkYmFjaygpIHtcbiAgICAgICAgZm9yICh2YXIgaSA9IDA7IGkgPCB0aGlzLmZlZWRCYWNrRWFjaEFycmF5Lmxlbmd0aDsgaSsrKSB7XG4gICAgICAgICAgICAkKHRoaXMuZmVlZEJhY2tFYWNoQXJyYXlbaV0pLmhpZGUoKTtcbiAgICAgICAgfVxuICAgIH1cblxuICAgIHJlaW5pdGlhbGl6ZUxpc3RlbmVycygpIHtcbiAgICAgICAgbGV0IHNlbGYgPSB0aGlzO1xuICAgICAgICBsZXQgYW5zd2VyRnVuYyA9IGZ1bmN0aW9uICgpIHtcbiAgICAgICAgICAgIHNlbGYuaXNBbnN3ZXJlZCA9IHRydWU7XG4gICAgICAgIH07XG4gICAgICAgIGZvciAobGV0IG9wdCBvZiB0aGlzLm9wdGlvbkFycmF5KSB7XG4gICAgICAgICAgICBvcHQuaW5wdXQub25jbGljayA9IGFuc3dlckZ1bmM7XG4gICAgICAgIH1cbiAgICB9XG59XG5cbmlmICh0eXBlb2Ygd2luZG93LmNvbXBvbmVudF9mYWN0b3J5ID09PSBcInVuZGVmaW5lZFwiKSB7XG4gICAgd2luZG93LmNvbXBvbmVudF9mYWN0b3J5ID0ge307XG59XG5cbndpbmRvdy5jb21wb25lbnRfZmFjdG9yeS5tdWx0aXBsZWNob2ljZSA9IGZ1bmN0aW9uIChvcHRzKSB7XG4gICAgaWYgKG9wdHMudGltZWQpIHtcbiAgICAgICAgcmV0dXJuIG5ldyBUaW1lZE1DKG9wdHMpO1xuICAgIH0gZWxzZSB7XG4gICAgICAgIHJldHVybiBuZXcgTXVsdGlwbGVDaG9pY2Uob3B0cyk7XG4gICAgfVxufTtcbiJdLCJzb3VyY2VSb290IjoiIn0=