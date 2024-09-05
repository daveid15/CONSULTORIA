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

/***/ "./lib/sidebar.js":
/*!************************!*\
  !*** ./lib/sidebar.js ***!
  \************************/
/***/ (() => {

eval("var floatButton = document.getElementById('expand-side-bar');\nfloatButton.addEventListener('click', function () {\n  var sidebar = document.getElementById('sidebar');\n\n  if (sidebar.classList.contains('to-left')) {\n    sidebar.classList.remove('to-left');\n  } else {\n    sidebar.classList.add('to-left');\n  }\n});\ndocument.querySelectorAll(\"img.svg\").forEach(function (img) {\n  var imgURL = img.getAttribute(\"src\");\n  fetch(imgURL).then(function (response) {\n    response.text().then(function (svg) {\n      var svgElement = new DOMParser().parseFromString(svg, \"image/svg+xml\");\n      img.replaceWith(svgElement.documentElement);\n    });\n  });\n});\n\n//# sourceURL=webpack://finhelp/./lib/sidebar.js?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = {};
/******/ 	__webpack_modules__["./lib/sidebar.js"]();
/******/ 	
/******/ })()
;