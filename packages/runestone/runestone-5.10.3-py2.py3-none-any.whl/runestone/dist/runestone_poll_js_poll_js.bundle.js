(self["webpackChunkWebComponents"] = self["webpackChunkWebComponents"] || []).push([["runestone_poll_js_poll_js"],{

/***/ 55475:
/*!*************************************!*\
  !*** ./runestone/poll/css/poll.css ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
// extracted by mini-css-extract-plugin


/***/ }),

/***/ 37350:
/*!***********************************!*\
  !*** ./runestone/poll/js/poll.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "pollList": () => (/* binding */ pollList),
/* harmony export */   "default": () => (/* binding */ Poll)
/* harmony export */ });
/* harmony import */ var _common_js_runestonebase__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../common/js/runestonebase */ 2568);
/* harmony import */ var _css_poll_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../css/poll.css */ 55475);
/*
__author__ = Kirby Olson
__date__ = 6/12/2015  */





var pollList = {};

class Poll extends _common_js_runestonebase__WEBPACK_IMPORTED_MODULE_0__.default {
    constructor(opts) {
        super(opts);
        var orig = opts.orig; //entire <p> element
        this.origElem = orig;
        this.divid = orig.id;
        this.children = this.origElem.childNodes;
        this.optionList = [];
        this.optsArray = [];
        this.comment = false;
        if ($(this.origElem).is("[data-comment]")) {
            this.comment = true;
        }
        this.resultsViewer = $(orig).data("results");
        this.getQuestionText();
        this.getOptionText(); //populates optionList
        this.renderPoll(); //generates HTML
        // Checks localStorage to see if this poll has already been completed by this user.
        this.checkPollStorage();
        this.caption = "Poll";
        this.addCaption("runestone");
    }
    getQuestionText() {
        //finds the text inside the parent tag, but before the first <li> tag and sets it as the question
        var _this = this;
        var firstAnswer;
        for (var i = 0; i < this.children.length; i++) {
            if (this.children[i].tagName == "LI") {
                firstAnswer = _this.children[i];
                break;
            }
        }
        var delimiter = firstAnswer.outerHTML;
        var fulltext = $(this.origElem).html();
        var temp = fulltext.split(delimiter);
        this.question = temp[0];
    }
    getOptionText() {
        //Gets the text from each <li> tag and places it in this.optionList
        var _this = this;
        for (var i = 0; i < this.children.length; i++) {
            if (_this.children[i].tagName == "LI") {
                _this.optionList.push($(_this.children[i]).text());
            }
        }
    }
    renderPoll() {
        //generates the HTML that the user interacts with
        var _this = this;
        this.containerDiv = document.createElement("div");
        this.pollForm = document.createElement("form");
        this.resultsDiv = document.createElement("div");
        this.containerDiv.id = this.divid;
        $(this.containerDiv).addClass(this.origElem.getAttribute("class"));
        $(this.pollForm).html(
            `<span style='font-size: Large'>${this.question}</span>`
        );
        $(this.pollForm).attr({
            id: this.divid + "_form",
            method: "get",
            action: "",
            onsubmit: "return false;",
        });
        this.pollForm.appendChild(document.createElement("br"));
        for (var i = 0; i < this.optionList.length; i++) {
            var radio = document.createElement("input");
            var tmpid = _this.divid + "_opt_" + i;
            $(radio).attr({
                id: tmpid,
                name: this.divid + "_group1",
                type: "radio",
                value: i,
            });
            $(radio).click(this.submitPoll.bind(this));
            var label = document.createElement("label");
            $(label).attr("for", tmpid);
            $(label).text(this.optionList[i]);
            this.pollForm.appendChild(radio);
            this.optsArray.push(radio);
            this.pollForm.appendChild(label);
            this.pollForm.appendChild(document.createElement("br"));
        }
        if (this.comment) {
            this.renderTextField();
        }
        this.resultsDiv.id = this.divid + "_results";
        this.containerDiv.appendChild(this.pollForm);
        this.containerDiv.appendChild(this.resultsDiv);
        $(this.origElem).replaceWith(this.containerDiv);
    }
    renderTextField() {
        this.textfield = document.createElement("input");
        this.textfield.type = "text";
        $(this.textfield).addClass("form-control");
        this.textfield.style.width = "300px";
        this.textfield.name = this.divid + "_comment";
        this.textfield.placeholder = "Any comments?";
        this.pollForm.appendChild(this.textfield);
        this.pollForm.appendChild(document.createElement("br"));
    }
    submitPoll() {
        //checks the poll, sets localstorage and submits to the server
        var poll_val = null;
        for (var i = 0; i < this.optsArray.length; i++) {
            if (this.optsArray[i].checked) {
                poll_val = this.optsArray[i].value;
                break;
            }
        }
        if (poll_val === null) return;
        var comment_val = "";
        if (this.comment) {
            comment_val = this.textfield.value;
        }
        var act = "";
        if (comment_val !== "") {
            act = poll_val + ":" + comment_val;
        } else {
            act = poll_val;
        }
        var eventInfo = { event: "poll", act: act, div_id: this.divid };
        // log the response to the database
        this.logBookEvent(eventInfo); // in bookfuncs.js
        // log the fact that the user has answered the poll to local storage
        localStorage.setItem(this.divid, "true");
        if (!document.getElementById(`${this.divid}_sent`)) {
            $(this.pollForm).append(
                `<span id=${this.divid}_sent><strong>Thanks, your response has been recorded</strong></span>`
            );
        } else {
            $(`#${this.divid}_sent`).html(
                "<strong>Only Your last reponse is recorded</strong>"
            );
        }
        // show the results of the poll
        if (this.resultsViewer === "all") {
            var data = {};
            data.div_id = this.divid;
            data.course = eBookConfig.course;
            jQuery.get(
                eBookConfig.ajaxURL + "getpollresults",
                data,
                this.showPollResults
            );
        }
    }
    showPollResults(data) {
        //displays the results returned by the server
        var results = eval(data);
        var total = results[0];
        var opt_list = results[1];
        var count_list = results[2];
        var div_id = results[3];
        var my_vote = results[4];
        // resture current users vote
        if (my_vote > -1) {
            this.optsArray[my_vote].checked = "checked";
        }
        // show results summary if appropriate
        if (
            (this.resultsViewer === "all" &&
                localStorage.getItem(this.divid === "true")) ||
            eBookConfig.isInstructor
        ) {
            $(this.resultsDiv).html(
                `<b>Results:</b> ${total} responses <br><br>`
            );
            var list = $(document.createElement("div"));
            $(list).addClass("results-container");
            for (var i = 0; i < this.optionList.length; i++) {
                var count;
                var percent;
                if (count_list[i]) {
                    count = count_list[i];
                    percent = (count / total) * 100;
                } else {
                    count = 0;
                    percent = 0;
                }
                var text = count + " (" + Math.round(10 * percent) / 10 + "%)"; // round percent to 10ths
                var html;
                if (percent > 10) {
                    html =
                        `<div class="progresscounter">${i + 1}. </div>` +
                        "<div class='progress'>" +
                        "<div class='progress-bar progress-bar-success'" +
                        `style="width: ${percent}%; min-width: 2em;">` +
                        "<span class='poll-text'>" +
                        text +
                        "</span></div></div>";
                } else {
                    html =
                        `<div class="progresscounter">${i + 1}. </div>` +
                        "<div class='progress'>" +
                        "<div class='progress-bar progress-bar-success'" +
                        `style="width: ${percent}%; min-width: 2em;"></div>` +
                        "<span class='poll-text' style='margin: 0 0 0 10px;'>" +
                        text +
                        "</span></div>";
                }
                var el = $(html);
                list.append(el);
            }
            $(this.resultsDiv).append(list);
        }
        this.indicate_component_ready();
    }
    disableOptions() {}
    checkPollStorage() {
        //checks the localstorage to see if the poll has been completed already
        var _this = this;
        var len = localStorage.length;
        if (len > 0) {
            //If the poll has already been completed, show the results
            var data = {};
            data.div_id = this.divid;
            data.course = eBookConfig.course;
            jQuery.get(
                eBookConfig.ajaxURL + "getpollresults",
                data,
                this.showPollResults.bind(this)
            ).fail(this.indicate_component_ready.bind(this));
        } else {
            this.indicate_component_ready();
        }
    }
}

// Do not render poll data until login-complete event so we know instructor status
$(document).bind("runestone:login-complete", function () {
    $("[data-component=poll]").each(function (index) {
        try {
            pollList[this.id] = new Poll({ orig: this });
        } catch (err) {
            console.log(`Error rendering Poll Problem ${this.id}
                         Details: ${err}`);
            console.log(err.stack);
        }
    });
});

if (typeof window.component_factory === "undefined") {
    window.component_factory = {};
}
window.component_factory.poll = function (opts) {
    return new Poll(opts);
};


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9XZWJDb21wb25lbnRzLy4vcnVuZXN0b25lL3BvbGwvY3NzL3BvbGwuY3NzP2VmODUiLCJ3ZWJwYWNrOi8vV2ViQ29tcG9uZW50cy8uL3J1bmVzdG9uZS9wb2xsL2pzL3BvbGwuanMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7OztBQUFBOzs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDQUE7QUFDQTtBQUNBO0FBQ2E7O0FBRTZDO0FBQ2pDOztBQUVsQjs7QUFFUSxtQkFBbUIsNkRBQWE7QUFDL0M7QUFDQTtBQUNBLDZCQUE2QjtBQUM3QjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsNkJBQTZCO0FBQzdCLDBCQUEwQjtBQUMxQjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSx1QkFBdUIsMEJBQTBCO0FBQ2pEO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsdUJBQXVCLDBCQUEwQjtBQUNqRDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsOENBQThDLGNBQWM7QUFDNUQ7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLG9DQUFvQztBQUNwQyxTQUFTO0FBQ1Q7QUFDQSx1QkFBdUIsNEJBQTRCO0FBQ25EO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLHVCQUF1QiwyQkFBMkI7QUFDbEQ7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxTQUFTO0FBQ1Q7QUFDQTtBQUNBLHlCQUF5QjtBQUN6QjtBQUNBLHFDQUFxQztBQUNyQztBQUNBO0FBQ0Esd0NBQXdDLFdBQVc7QUFDbkQ7QUFDQSw0QkFBNEIsV0FBVztBQUN2QztBQUNBLFNBQVM7QUFDVCxrQkFBa0IsV0FBVztBQUM3QjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLG1DQUFtQyxNQUFNO0FBQ3pDO0FBQ0E7QUFDQTtBQUNBLDJCQUEyQiw0QkFBNEI7QUFDdkQ7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLGlCQUFpQjtBQUNqQjtBQUNBO0FBQ0E7QUFDQSwrRUFBK0U7QUFDL0U7QUFDQTtBQUNBO0FBQ0Esd0RBQXdELE1BQU07QUFDOUQ7QUFDQTtBQUNBLHlDQUF5QyxRQUFRLEVBQUUsZ0JBQWdCO0FBQ25FO0FBQ0E7QUFDQTtBQUNBLGlCQUFpQjtBQUNqQjtBQUNBLHdEQUF3RCxNQUFNO0FBQzlEO0FBQ0E7QUFDQSx5Q0FBeUMsUUFBUSxFQUFFLGdCQUFnQjtBQUNuRSwyRUFBMkU7QUFDM0U7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxTQUFTO0FBQ1Q7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQSwwQ0FBMEMsYUFBYTtBQUN2RCxTQUFTO0FBQ1Qsd0RBQXdEO0FBQ3hELG9DQUFvQyxJQUFJO0FBQ3hDO0FBQ0E7QUFDQSxLQUFLO0FBQ0wsQ0FBQzs7QUFFRDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EiLCJmaWxlIjoicnVuZXN0b25lX3BvbGxfanNfcG9sbF9qcy5idW5kbGUuanM/dj04NDY0NjQ4ZjM5ZDQwNWRlZmUwOSIsInNvdXJjZXNDb250ZW50IjpbIi8vIGV4dHJhY3RlZCBieSBtaW5pLWNzcy1leHRyYWN0LXBsdWdpblxuZXhwb3J0IHt9OyIsIi8qXG5fX2F1dGhvcl9fID0gS2lyYnkgT2xzb25cbl9fZGF0ZV9fID0gNi8xMi8yMDE1ICAqL1xuXCJ1c2Ugc3RyaWN0XCI7XG5cbmltcG9ydCBSdW5lc3RvbmVCYXNlIGZyb20gXCIuLi8uLi9jb21tb24vanMvcnVuZXN0b25lYmFzZVwiO1xuaW1wb3J0IFwiLi4vY3NzL3BvbGwuY3NzXCI7XG5cbmV4cG9ydCB2YXIgcG9sbExpc3QgPSB7fTtcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgUG9sbCBleHRlbmRzIFJ1bmVzdG9uZUJhc2Uge1xuICAgIGNvbnN0cnVjdG9yKG9wdHMpIHtcbiAgICAgICAgc3VwZXIob3B0cyk7XG4gICAgICAgIHZhciBvcmlnID0gb3B0cy5vcmlnOyAvL2VudGlyZSA8cD4gZWxlbWVudFxuICAgICAgICB0aGlzLm9yaWdFbGVtID0gb3JpZztcbiAgICAgICAgdGhpcy5kaXZpZCA9IG9yaWcuaWQ7XG4gICAgICAgIHRoaXMuY2hpbGRyZW4gPSB0aGlzLm9yaWdFbGVtLmNoaWxkTm9kZXM7XG4gICAgICAgIHRoaXMub3B0aW9uTGlzdCA9IFtdO1xuICAgICAgICB0aGlzLm9wdHNBcnJheSA9IFtdO1xuICAgICAgICB0aGlzLmNvbW1lbnQgPSBmYWxzZTtcbiAgICAgICAgaWYgKCQodGhpcy5vcmlnRWxlbSkuaXMoXCJbZGF0YS1jb21tZW50XVwiKSkge1xuICAgICAgICAgICAgdGhpcy5jb21tZW50ID0gdHJ1ZTtcbiAgICAgICAgfVxuICAgICAgICB0aGlzLnJlc3VsdHNWaWV3ZXIgPSAkKG9yaWcpLmRhdGEoXCJyZXN1bHRzXCIpO1xuICAgICAgICB0aGlzLmdldFF1ZXN0aW9uVGV4dCgpO1xuICAgICAgICB0aGlzLmdldE9wdGlvblRleHQoKTsgLy9wb3B1bGF0ZXMgb3B0aW9uTGlzdFxuICAgICAgICB0aGlzLnJlbmRlclBvbGwoKTsgLy9nZW5lcmF0ZXMgSFRNTFxuICAgICAgICAvLyBDaGVja3MgbG9jYWxTdG9yYWdlIHRvIHNlZSBpZiB0aGlzIHBvbGwgaGFzIGFscmVhZHkgYmVlbiBjb21wbGV0ZWQgYnkgdGhpcyB1c2VyLlxuICAgICAgICB0aGlzLmNoZWNrUG9sbFN0b3JhZ2UoKTtcbiAgICAgICAgdGhpcy5jYXB0aW9uID0gXCJQb2xsXCI7XG4gICAgICAgIHRoaXMuYWRkQ2FwdGlvbihcInJ1bmVzdG9uZVwiKTtcbiAgICB9XG4gICAgZ2V0UXVlc3Rpb25UZXh0KCkge1xuICAgICAgICAvL2ZpbmRzIHRoZSB0ZXh0IGluc2lkZSB0aGUgcGFyZW50IHRhZywgYnV0IGJlZm9yZSB0aGUgZmlyc3QgPGxpPiB0YWcgYW5kIHNldHMgaXQgYXMgdGhlIHF1ZXN0aW9uXG4gICAgICAgIHZhciBfdGhpcyA9IHRoaXM7XG4gICAgICAgIHZhciBmaXJzdEFuc3dlcjtcbiAgICAgICAgZm9yICh2YXIgaSA9IDA7IGkgPCB0aGlzLmNoaWxkcmVuLmxlbmd0aDsgaSsrKSB7XG4gICAgICAgICAgICBpZiAodGhpcy5jaGlsZHJlbltpXS50YWdOYW1lID09IFwiTElcIikge1xuICAgICAgICAgICAgICAgIGZpcnN0QW5zd2VyID0gX3RoaXMuY2hpbGRyZW5baV07XG4gICAgICAgICAgICAgICAgYnJlYWs7XG4gICAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgICAgdmFyIGRlbGltaXRlciA9IGZpcnN0QW5zd2VyLm91dGVySFRNTDtcbiAgICAgICAgdmFyIGZ1bGx0ZXh0ID0gJCh0aGlzLm9yaWdFbGVtKS5odG1sKCk7XG4gICAgICAgIHZhciB0ZW1wID0gZnVsbHRleHQuc3BsaXQoZGVsaW1pdGVyKTtcbiAgICAgICAgdGhpcy5xdWVzdGlvbiA9IHRlbXBbMF07XG4gICAgfVxuICAgIGdldE9wdGlvblRleHQoKSB7XG4gICAgICAgIC8vR2V0cyB0aGUgdGV4dCBmcm9tIGVhY2ggPGxpPiB0YWcgYW5kIHBsYWNlcyBpdCBpbiB0aGlzLm9wdGlvbkxpc3RcbiAgICAgICAgdmFyIF90aGlzID0gdGhpcztcbiAgICAgICAgZm9yICh2YXIgaSA9IDA7IGkgPCB0aGlzLmNoaWxkcmVuLmxlbmd0aDsgaSsrKSB7XG4gICAgICAgICAgICBpZiAoX3RoaXMuY2hpbGRyZW5baV0udGFnTmFtZSA9PSBcIkxJXCIpIHtcbiAgICAgICAgICAgICAgICBfdGhpcy5vcHRpb25MaXN0LnB1c2goJChfdGhpcy5jaGlsZHJlbltpXSkudGV4dCgpKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgIH1cbiAgICByZW5kZXJQb2xsKCkge1xuICAgICAgICAvL2dlbmVyYXRlcyB0aGUgSFRNTCB0aGF0IHRoZSB1c2VyIGludGVyYWN0cyB3aXRoXG4gICAgICAgIHZhciBfdGhpcyA9IHRoaXM7XG4gICAgICAgIHRoaXMuY29udGFpbmVyRGl2ID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudChcImRpdlwiKTtcbiAgICAgICAgdGhpcy5wb2xsRm9ybSA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoXCJmb3JtXCIpO1xuICAgICAgICB0aGlzLnJlc3VsdHNEaXYgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KFwiZGl2XCIpO1xuICAgICAgICB0aGlzLmNvbnRhaW5lckRpdi5pZCA9IHRoaXMuZGl2aWQ7XG4gICAgICAgICQodGhpcy5jb250YWluZXJEaXYpLmFkZENsYXNzKHRoaXMub3JpZ0VsZW0uZ2V0QXR0cmlidXRlKFwiY2xhc3NcIikpO1xuICAgICAgICAkKHRoaXMucG9sbEZvcm0pLmh0bWwoXG4gICAgICAgICAgICBgPHNwYW4gc3R5bGU9J2ZvbnQtc2l6ZTogTGFyZ2UnPiR7dGhpcy5xdWVzdGlvbn08L3NwYW4+YFxuICAgICAgICApO1xuICAgICAgICAkKHRoaXMucG9sbEZvcm0pLmF0dHIoe1xuICAgICAgICAgICAgaWQ6IHRoaXMuZGl2aWQgKyBcIl9mb3JtXCIsXG4gICAgICAgICAgICBtZXRob2Q6IFwiZ2V0XCIsXG4gICAgICAgICAgICBhY3Rpb246IFwiXCIsXG4gICAgICAgICAgICBvbnN1Ym1pdDogXCJyZXR1cm4gZmFsc2U7XCIsXG4gICAgICAgIH0pO1xuICAgICAgICB0aGlzLnBvbGxGb3JtLmFwcGVuZENoaWxkKGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoXCJiclwiKSk7XG4gICAgICAgIGZvciAodmFyIGkgPSAwOyBpIDwgdGhpcy5vcHRpb25MaXN0Lmxlbmd0aDsgaSsrKSB7XG4gICAgICAgICAgICB2YXIgcmFkaW8gPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KFwiaW5wdXRcIik7XG4gICAgICAgICAgICB2YXIgdG1waWQgPSBfdGhpcy5kaXZpZCArIFwiX29wdF9cIiArIGk7XG4gICAgICAgICAgICAkKHJhZGlvKS5hdHRyKHtcbiAgICAgICAgICAgICAgICBpZDogdG1waWQsXG4gICAgICAgICAgICAgICAgbmFtZTogdGhpcy5kaXZpZCArIFwiX2dyb3VwMVwiLFxuICAgICAgICAgICAgICAgIHR5cGU6IFwicmFkaW9cIixcbiAgICAgICAgICAgICAgICB2YWx1ZTogaSxcbiAgICAgICAgICAgIH0pO1xuICAgICAgICAgICAgJChyYWRpbykuY2xpY2sodGhpcy5zdWJtaXRQb2xsLmJpbmQodGhpcykpO1xuICAgICAgICAgICAgdmFyIGxhYmVsID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudChcImxhYmVsXCIpO1xuICAgICAgICAgICAgJChsYWJlbCkuYXR0cihcImZvclwiLCB0bXBpZCk7XG4gICAgICAgICAgICAkKGxhYmVsKS50ZXh0KHRoaXMub3B0aW9uTGlzdFtpXSk7XG4gICAgICAgICAgICB0aGlzLnBvbGxGb3JtLmFwcGVuZENoaWxkKHJhZGlvKTtcbiAgICAgICAgICAgIHRoaXMub3B0c0FycmF5LnB1c2gocmFkaW8pO1xuICAgICAgICAgICAgdGhpcy5wb2xsRm9ybS5hcHBlbmRDaGlsZChsYWJlbCk7XG4gICAgICAgICAgICB0aGlzLnBvbGxGb3JtLmFwcGVuZENoaWxkKGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoXCJiclwiKSk7XG4gICAgICAgIH1cbiAgICAgICAgaWYgKHRoaXMuY29tbWVudCkge1xuICAgICAgICAgICAgdGhpcy5yZW5kZXJUZXh0RmllbGQoKTtcbiAgICAgICAgfVxuICAgICAgICB0aGlzLnJlc3VsdHNEaXYuaWQgPSB0aGlzLmRpdmlkICsgXCJfcmVzdWx0c1wiO1xuICAgICAgICB0aGlzLmNvbnRhaW5lckRpdi5hcHBlbmRDaGlsZCh0aGlzLnBvbGxGb3JtKTtcbiAgICAgICAgdGhpcy5jb250YWluZXJEaXYuYXBwZW5kQ2hpbGQodGhpcy5yZXN1bHRzRGl2KTtcbiAgICAgICAgJCh0aGlzLm9yaWdFbGVtKS5yZXBsYWNlV2l0aCh0aGlzLmNvbnRhaW5lckRpdik7XG4gICAgfVxuICAgIHJlbmRlclRleHRGaWVsZCgpIHtcbiAgICAgICAgdGhpcy50ZXh0ZmllbGQgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KFwiaW5wdXRcIik7XG4gICAgICAgIHRoaXMudGV4dGZpZWxkLnR5cGUgPSBcInRleHRcIjtcbiAgICAgICAgJCh0aGlzLnRleHRmaWVsZCkuYWRkQ2xhc3MoXCJmb3JtLWNvbnRyb2xcIik7XG4gICAgICAgIHRoaXMudGV4dGZpZWxkLnN0eWxlLndpZHRoID0gXCIzMDBweFwiO1xuICAgICAgICB0aGlzLnRleHRmaWVsZC5uYW1lID0gdGhpcy5kaXZpZCArIFwiX2NvbW1lbnRcIjtcbiAgICAgICAgdGhpcy50ZXh0ZmllbGQucGxhY2Vob2xkZXIgPSBcIkFueSBjb21tZW50cz9cIjtcbiAgICAgICAgdGhpcy5wb2xsRm9ybS5hcHBlbmRDaGlsZCh0aGlzLnRleHRmaWVsZCk7XG4gICAgICAgIHRoaXMucG9sbEZvcm0uYXBwZW5kQ2hpbGQoZG9jdW1lbnQuY3JlYXRlRWxlbWVudChcImJyXCIpKTtcbiAgICB9XG4gICAgc3VibWl0UG9sbCgpIHtcbiAgICAgICAgLy9jaGVja3MgdGhlIHBvbGwsIHNldHMgbG9jYWxzdG9yYWdlIGFuZCBzdWJtaXRzIHRvIHRoZSBzZXJ2ZXJcbiAgICAgICAgdmFyIHBvbGxfdmFsID0gbnVsbDtcbiAgICAgICAgZm9yICh2YXIgaSA9IDA7IGkgPCB0aGlzLm9wdHNBcnJheS5sZW5ndGg7IGkrKykge1xuICAgICAgICAgICAgaWYgKHRoaXMub3B0c0FycmF5W2ldLmNoZWNrZWQpIHtcbiAgICAgICAgICAgICAgICBwb2xsX3ZhbCA9IHRoaXMub3B0c0FycmF5W2ldLnZhbHVlO1xuICAgICAgICAgICAgICAgIGJyZWFrO1xuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICAgIGlmIChwb2xsX3ZhbCA9PT0gbnVsbCkgcmV0dXJuO1xuICAgICAgICB2YXIgY29tbWVudF92YWwgPSBcIlwiO1xuICAgICAgICBpZiAodGhpcy5jb21tZW50KSB7XG4gICAgICAgICAgICBjb21tZW50X3ZhbCA9IHRoaXMudGV4dGZpZWxkLnZhbHVlO1xuICAgICAgICB9XG4gICAgICAgIHZhciBhY3QgPSBcIlwiO1xuICAgICAgICBpZiAoY29tbWVudF92YWwgIT09IFwiXCIpIHtcbiAgICAgICAgICAgIGFjdCA9IHBvbGxfdmFsICsgXCI6XCIgKyBjb21tZW50X3ZhbDtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIGFjdCA9IHBvbGxfdmFsO1xuICAgICAgICB9XG4gICAgICAgIHZhciBldmVudEluZm8gPSB7IGV2ZW50OiBcInBvbGxcIiwgYWN0OiBhY3QsIGRpdl9pZDogdGhpcy5kaXZpZCB9O1xuICAgICAgICAvLyBsb2cgdGhlIHJlc3BvbnNlIHRvIHRoZSBkYXRhYmFzZVxuICAgICAgICB0aGlzLmxvZ0Jvb2tFdmVudChldmVudEluZm8pOyAvLyBpbiBib29rZnVuY3MuanNcbiAgICAgICAgLy8gbG9nIHRoZSBmYWN0IHRoYXQgdGhlIHVzZXIgaGFzIGFuc3dlcmVkIHRoZSBwb2xsIHRvIGxvY2FsIHN0b3JhZ2VcbiAgICAgICAgbG9jYWxTdG9yYWdlLnNldEl0ZW0odGhpcy5kaXZpZCwgXCJ0cnVlXCIpO1xuICAgICAgICBpZiAoIWRvY3VtZW50LmdldEVsZW1lbnRCeUlkKGAke3RoaXMuZGl2aWR9X3NlbnRgKSkge1xuICAgICAgICAgICAgJCh0aGlzLnBvbGxGb3JtKS5hcHBlbmQoXG4gICAgICAgICAgICAgICAgYDxzcGFuIGlkPSR7dGhpcy5kaXZpZH1fc2VudD48c3Ryb25nPlRoYW5rcywgeW91ciByZXNwb25zZSBoYXMgYmVlbiByZWNvcmRlZDwvc3Ryb25nPjwvc3Bhbj5gXG4gICAgICAgICAgICApO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgJChgIyR7dGhpcy5kaXZpZH1fc2VudGApLmh0bWwoXG4gICAgICAgICAgICAgICAgXCI8c3Ryb25nPk9ubHkgWW91ciBsYXN0IHJlcG9uc2UgaXMgcmVjb3JkZWQ8L3N0cm9uZz5cIlxuICAgICAgICAgICAgKTtcbiAgICAgICAgfVxuICAgICAgICAvLyBzaG93IHRoZSByZXN1bHRzIG9mIHRoZSBwb2xsXG4gICAgICAgIGlmICh0aGlzLnJlc3VsdHNWaWV3ZXIgPT09IFwiYWxsXCIpIHtcbiAgICAgICAgICAgIHZhciBkYXRhID0ge307XG4gICAgICAgICAgICBkYXRhLmRpdl9pZCA9IHRoaXMuZGl2aWQ7XG4gICAgICAgICAgICBkYXRhLmNvdXJzZSA9IGVCb29rQ29uZmlnLmNvdXJzZTtcbiAgICAgICAgICAgIGpRdWVyeS5nZXQoXG4gICAgICAgICAgICAgICAgZUJvb2tDb25maWcuYWpheFVSTCArIFwiZ2V0cG9sbHJlc3VsdHNcIixcbiAgICAgICAgICAgICAgICBkYXRhLFxuICAgICAgICAgICAgICAgIHRoaXMuc2hvd1BvbGxSZXN1bHRzXG4gICAgICAgICAgICApO1xuICAgICAgICB9XG4gICAgfVxuICAgIHNob3dQb2xsUmVzdWx0cyhkYXRhKSB7XG4gICAgICAgIC8vZGlzcGxheXMgdGhlIHJlc3VsdHMgcmV0dXJuZWQgYnkgdGhlIHNlcnZlclxuICAgICAgICB2YXIgcmVzdWx0cyA9IGV2YWwoZGF0YSk7XG4gICAgICAgIHZhciB0b3RhbCA9IHJlc3VsdHNbMF07XG4gICAgICAgIHZhciBvcHRfbGlzdCA9IHJlc3VsdHNbMV07XG4gICAgICAgIHZhciBjb3VudF9saXN0ID0gcmVzdWx0c1syXTtcbiAgICAgICAgdmFyIGRpdl9pZCA9IHJlc3VsdHNbM107XG4gICAgICAgIHZhciBteV92b3RlID0gcmVzdWx0c1s0XTtcbiAgICAgICAgLy8gcmVzdHVyZSBjdXJyZW50IHVzZXJzIHZvdGVcbiAgICAgICAgaWYgKG15X3ZvdGUgPiAtMSkge1xuICAgICAgICAgICAgdGhpcy5vcHRzQXJyYXlbbXlfdm90ZV0uY2hlY2tlZCA9IFwiY2hlY2tlZFwiO1xuICAgICAgICB9XG4gICAgICAgIC8vIHNob3cgcmVzdWx0cyBzdW1tYXJ5IGlmIGFwcHJvcHJpYXRlXG4gICAgICAgIGlmIChcbiAgICAgICAgICAgICh0aGlzLnJlc3VsdHNWaWV3ZXIgPT09IFwiYWxsXCIgJiZcbiAgICAgICAgICAgICAgICBsb2NhbFN0b3JhZ2UuZ2V0SXRlbSh0aGlzLmRpdmlkID09PSBcInRydWVcIikpIHx8XG4gICAgICAgICAgICBlQm9va0NvbmZpZy5pc0luc3RydWN0b3JcbiAgICAgICAgKSB7XG4gICAgICAgICAgICAkKHRoaXMucmVzdWx0c0RpdikuaHRtbChcbiAgICAgICAgICAgICAgICBgPGI+UmVzdWx0czo8L2I+ICR7dG90YWx9IHJlc3BvbnNlcyA8YnI+PGJyPmBcbiAgICAgICAgICAgICk7XG4gICAgICAgICAgICB2YXIgbGlzdCA9ICQoZG9jdW1lbnQuY3JlYXRlRWxlbWVudChcImRpdlwiKSk7XG4gICAgICAgICAgICAkKGxpc3QpLmFkZENsYXNzKFwicmVzdWx0cy1jb250YWluZXJcIik7XG4gICAgICAgICAgICBmb3IgKHZhciBpID0gMDsgaSA8IHRoaXMub3B0aW9uTGlzdC5sZW5ndGg7IGkrKykge1xuICAgICAgICAgICAgICAgIHZhciBjb3VudDtcbiAgICAgICAgICAgICAgICB2YXIgcGVyY2VudDtcbiAgICAgICAgICAgICAgICBpZiAoY291bnRfbGlzdFtpXSkge1xuICAgICAgICAgICAgICAgICAgICBjb3VudCA9IGNvdW50X2xpc3RbaV07XG4gICAgICAgICAgICAgICAgICAgIHBlcmNlbnQgPSAoY291bnQgLyB0b3RhbCkgKiAxMDA7XG4gICAgICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICAgICAgY291bnQgPSAwO1xuICAgICAgICAgICAgICAgICAgICBwZXJjZW50ID0gMDtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgdmFyIHRleHQgPSBjb3VudCArIFwiIChcIiArIE1hdGgucm91bmQoMTAgKiBwZXJjZW50KSAvIDEwICsgXCIlKVwiOyAvLyByb3VuZCBwZXJjZW50IHRvIDEwdGhzXG4gICAgICAgICAgICAgICAgdmFyIGh0bWw7XG4gICAgICAgICAgICAgICAgaWYgKHBlcmNlbnQgPiAxMCkge1xuICAgICAgICAgICAgICAgICAgICBodG1sID1cbiAgICAgICAgICAgICAgICAgICAgICAgIGA8ZGl2IGNsYXNzPVwicHJvZ3Jlc3Njb3VudGVyXCI+JHtpICsgMX0uIDwvZGl2PmAgK1xuICAgICAgICAgICAgICAgICAgICAgICAgXCI8ZGl2IGNsYXNzPSdwcm9ncmVzcyc+XCIgK1xuICAgICAgICAgICAgICAgICAgICAgICAgXCI8ZGl2IGNsYXNzPSdwcm9ncmVzcy1iYXIgcHJvZ3Jlc3MtYmFyLXN1Y2Nlc3MnXCIgK1xuICAgICAgICAgICAgICAgICAgICAgICAgYHN0eWxlPVwid2lkdGg6ICR7cGVyY2VudH0lOyBtaW4td2lkdGg6IDJlbTtcIj5gICtcbiAgICAgICAgICAgICAgICAgICAgICAgIFwiPHNwYW4gY2xhc3M9J3BvbGwtdGV4dCc+XCIgK1xuICAgICAgICAgICAgICAgICAgICAgICAgdGV4dCArXG4gICAgICAgICAgICAgICAgICAgICAgICBcIjwvc3Bhbj48L2Rpdj48L2Rpdj5cIjtcbiAgICAgICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgICAgICBodG1sID1cbiAgICAgICAgICAgICAgICAgICAgICAgIGA8ZGl2IGNsYXNzPVwicHJvZ3Jlc3Njb3VudGVyXCI+JHtpICsgMX0uIDwvZGl2PmAgK1xuICAgICAgICAgICAgICAgICAgICAgICAgXCI8ZGl2IGNsYXNzPSdwcm9ncmVzcyc+XCIgK1xuICAgICAgICAgICAgICAgICAgICAgICAgXCI8ZGl2IGNsYXNzPSdwcm9ncmVzcy1iYXIgcHJvZ3Jlc3MtYmFyLXN1Y2Nlc3MnXCIgK1xuICAgICAgICAgICAgICAgICAgICAgICAgYHN0eWxlPVwid2lkdGg6ICR7cGVyY2VudH0lOyBtaW4td2lkdGg6IDJlbTtcIj48L2Rpdj5gICtcbiAgICAgICAgICAgICAgICAgICAgICAgIFwiPHNwYW4gY2xhc3M9J3BvbGwtdGV4dCcgc3R5bGU9J21hcmdpbjogMCAwIDAgMTBweDsnPlwiICtcbiAgICAgICAgICAgICAgICAgICAgICAgIHRleHQgK1xuICAgICAgICAgICAgICAgICAgICAgICAgXCI8L3NwYW4+PC9kaXY+XCI7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIHZhciBlbCA9ICQoaHRtbCk7XG4gICAgICAgICAgICAgICAgbGlzdC5hcHBlbmQoZWwpO1xuICAgICAgICAgICAgfVxuICAgICAgICAgICAgJCh0aGlzLnJlc3VsdHNEaXYpLmFwcGVuZChsaXN0KTtcbiAgICAgICAgfVxuICAgICAgICB0aGlzLmluZGljYXRlX2NvbXBvbmVudF9yZWFkeSgpO1xuICAgIH1cbiAgICBkaXNhYmxlT3B0aW9ucygpIHt9XG4gICAgY2hlY2tQb2xsU3RvcmFnZSgpIHtcbiAgICAgICAgLy9jaGVja3MgdGhlIGxvY2Fsc3RvcmFnZSB0byBzZWUgaWYgdGhlIHBvbGwgaGFzIGJlZW4gY29tcGxldGVkIGFscmVhZHlcbiAgICAgICAgdmFyIF90aGlzID0gdGhpcztcbiAgICAgICAgdmFyIGxlbiA9IGxvY2FsU3RvcmFnZS5sZW5ndGg7XG4gICAgICAgIGlmIChsZW4gPiAwKSB7XG4gICAgICAgICAgICAvL0lmIHRoZSBwb2xsIGhhcyBhbHJlYWR5IGJlZW4gY29tcGxldGVkLCBzaG93IHRoZSByZXN1bHRzXG4gICAgICAgICAgICB2YXIgZGF0YSA9IHt9O1xuICAgICAgICAgICAgZGF0YS5kaXZfaWQgPSB0aGlzLmRpdmlkO1xuICAgICAgICAgICAgZGF0YS5jb3Vyc2UgPSBlQm9va0NvbmZpZy5jb3Vyc2U7XG4gICAgICAgICAgICBqUXVlcnkuZ2V0KFxuICAgICAgICAgICAgICAgIGVCb29rQ29uZmlnLmFqYXhVUkwgKyBcImdldHBvbGxyZXN1bHRzXCIsXG4gICAgICAgICAgICAgICAgZGF0YSxcbiAgICAgICAgICAgICAgICB0aGlzLnNob3dQb2xsUmVzdWx0cy5iaW5kKHRoaXMpXG4gICAgICAgICAgICApLmZhaWwodGhpcy5pbmRpY2F0ZV9jb21wb25lbnRfcmVhZHkuYmluZCh0aGlzKSk7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICB0aGlzLmluZGljYXRlX2NvbXBvbmVudF9yZWFkeSgpO1xuICAgICAgICB9XG4gICAgfVxufVxuXG4vLyBEbyBub3QgcmVuZGVyIHBvbGwgZGF0YSB1bnRpbCBsb2dpbi1jb21wbGV0ZSBldmVudCBzbyB3ZSBrbm93IGluc3RydWN0b3Igc3RhdHVzXG4kKGRvY3VtZW50KS5iaW5kKFwicnVuZXN0b25lOmxvZ2luLWNvbXBsZXRlXCIsIGZ1bmN0aW9uICgpIHtcbiAgICAkKFwiW2RhdGEtY29tcG9uZW50PXBvbGxdXCIpLmVhY2goZnVuY3Rpb24gKGluZGV4KSB7XG4gICAgICAgIHRyeSB7XG4gICAgICAgICAgICBwb2xsTGlzdFt0aGlzLmlkXSA9IG5ldyBQb2xsKHsgb3JpZzogdGhpcyB9KTtcbiAgICAgICAgfSBjYXRjaCAoZXJyKSB7XG4gICAgICAgICAgICBjb25zb2xlLmxvZyhgRXJyb3IgcmVuZGVyaW5nIFBvbGwgUHJvYmxlbSAke3RoaXMuaWR9XG4gICAgICAgICAgICAgICAgICAgICAgICAgRGV0YWlsczogJHtlcnJ9YCk7XG4gICAgICAgICAgICBjb25zb2xlLmxvZyhlcnIuc3RhY2spO1xuICAgICAgICB9XG4gICAgfSk7XG59KTtcblxuaWYgKHR5cGVvZiB3aW5kb3cuY29tcG9uZW50X2ZhY3RvcnkgPT09IFwidW5kZWZpbmVkXCIpIHtcbiAgICB3aW5kb3cuY29tcG9uZW50X2ZhY3RvcnkgPSB7fTtcbn1cbndpbmRvdy5jb21wb25lbnRfZmFjdG9yeS5wb2xsID0gZnVuY3Rpb24gKG9wdHMpIHtcbiAgICByZXR1cm4gbmV3IFBvbGwob3B0cyk7XG59O1xuIl0sInNvdXJjZVJvb3QiOiIifQ==