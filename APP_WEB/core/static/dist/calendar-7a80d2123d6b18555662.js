/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ "./lib/calendar.js":
/*!*************************!*\
  !*** ./lib/calendar.js ***!
  \*************************/
/***/ (() => {

eval("var calendar_footer = document.getElementById('calendar-footer');\nvar days = document.querySelectorAll('.day.active');\ndays.forEach(function (day) {\n  day.addEventListener('click', function (evt) {\n    calendar_footer.innerHTML = evt.target.innerHTML;\n  });\n});\n\n//# sourceURL=webpack://finhelp/./lib/calendar.js?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = {};
/******/ 	__webpack_modules__["./lib/calendar.js"]();
/******/ 	
/******/ })()
;