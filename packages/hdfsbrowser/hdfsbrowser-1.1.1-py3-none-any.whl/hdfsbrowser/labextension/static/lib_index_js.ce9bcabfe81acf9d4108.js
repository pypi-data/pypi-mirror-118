"use strict";
(self["webpackChunk_swan_cern_hdfsbrowser"] = self["webpackChunk_swan_cern_hdfsbrowser"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _widgets_HdfsBrowserWidget__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./widgets/HdfsBrowserWidget */ "./lib/widgets/HdfsBrowserWidget.js");





/**
 * Initialization data for the hdfsbrowser extension.
 */
const plugin = {
    id: '@swan-cern/hdfsbrowser',
    requires: [
        _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_2__.IMainMenu, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer
    ],
    activate: activate,
    autoStart: true,
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);
/**
 * Activate the running plugin.
 */
function activate(app, mainMenu, restorer) {
    // Add a menu for the plugin
    mainMenu.addMenu(createHadoopMenu(app, restorer), { rank: 60 });
    console.log('JupyterLab hdfsbrowser is activated!');
}
/**
 * Create menu with commands and menu items
 */
function createHadoopMenu(app, restorer) {
    const category = 'Hadoop';
    const namespace = 'hadoop';
    const hdfsbrowserwidget = 'hadoop-extension-hdfsbrowser-jupyterlab';
    const hdfsbrowseropen = 'hadoop:hdfsbrowseropen';
    app.commands.addCommand(hdfsbrowseropen, {
        label: 'HDFS Browser',
        execute: () => {
            // Restore widget if it was not closed (disposed)
            let hdfsBrowserWidget = tracker.find(value => {
                return value.id === hdfsbrowserwidget || false;
            });
            // If disposed, create new
            if (!hdfsBrowserWidget) {
                const content = new _widgets_HdfsBrowserWidget__WEBPACK_IMPORTED_MODULE_4__.HdfsBrowserWidget();
                hdfsBrowserWidget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({ content });
                hdfsBrowserWidget.id = hdfsbrowserwidget;
                hdfsBrowserWidget.title.label = 'HDFS Browser';
                hdfsBrowserWidget.title.closable = true;
            }
            // Track the state of the widget for later restoration
            if (!tracker.has(hdfsBrowserWidget)) {
                tracker.add(hdfsBrowserWidget);
            }
            if (!hdfsBrowserWidget.isAttached) {
                // Attach the widget to the main work area if it's not there
                app.shell.add(hdfsBrowserWidget, 'main');
            }
            hdfsBrowserWidget.content.update();
            // Activate the widget
            app.shell.activateById(hdfsBrowserWidget.id);
        }
    });
    // Initialize hadoop menu
    let menu = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Menu({
        commands: app.commands
    });
    menu.title.label = category;
    menu.addItem({
        command: hdfsbrowseropen,
        args: {},
    });
    // Track and restore the widget state e.g. after refresh
    let tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
        namespace: namespace
    });
    restorer.restore(tracker, {
        command: hdfsbrowseropen,
        name: () => hdfsbrowserwidget
    });
    return menu;
}


/***/ }),

/***/ "./lib/widgets/HdfsBrowserWidget.js":
/*!******************************************!*\
  !*** ./lib/widgets/HdfsBrowserWidget.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "HdfsBrowserWidget": () => (/* binding */ HdfsBrowserWidget)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * A class that exposes the git plugin Widget.
 */
class HdfsBrowserWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.IFrame {
    /**
     * Construct a console panel.
     */
    constructor() {
        super();
        this.sandbox = [
            'allow-same-origin',
            'allow-scripts'
        ];
        this.url = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings().baseUrl + "hdfsbrowser/explorer.html";
    }
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js.ce9bcabfe81acf9d4108.js.map