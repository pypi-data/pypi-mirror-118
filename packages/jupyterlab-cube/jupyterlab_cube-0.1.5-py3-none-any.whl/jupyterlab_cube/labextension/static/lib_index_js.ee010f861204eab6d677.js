"use strict";
(self["webpackChunkjupyterlab_cube"] = self["webpackChunkjupyterlab_cube"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "OutputWidget": () => (/* binding */ OutputWidget),
/* harmony export */   "rendererFactory": () => (/* binding */ rendererFactory),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _visualizer__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./visualizer */ "./lib/visualizer.js");
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react-dom */ "webpack/sharing/consume/default/react-dom");
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react_dom__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_2__);




/**
 * The default mime type for the extension.
 */
const MIME_TYPE = 'application/osscar.cube';
/**
 * The class name added to the extension.
 */
const CLASS_NAME = 'mimerenderer-cube';
/**
 * A widget for rendering cube.
 */
class OutputWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    /**
     * Construct a new output widget.
     */
    constructor(options) {
        super();
        this._mimeType = options.mimeType;
        this.addClass(CLASS_NAME);
    }
    /**
     * Render cube into this widget's node.
     */
    renderModel(model) {
        const data = model.data[this._mimeType];
        return new Promise((resolve, reject) => {
            react_dom__WEBPACK_IMPORTED_MODULE_1__.render(react__WEBPACK_IMPORTED_MODULE_2___default().createElement(_visualizer__WEBPACK_IMPORTED_MODULE_3__.Visualizer, { data: data }), this.node, () => {
                resolve();
            });
        });
    }
}
/**
 * A mime renderer factory for cube data.
 */
const rendererFactory = {
    safe: true,
    mimeTypes: [MIME_TYPE],
    createRenderer: (options) => new OutputWidget(options),
};
/**
 * Extension definition.
 */
const extension = {
    id: 'jupyterlab-cube:plugin',
    rendererFactory,
    rank: 100,
    dataType: 'string',
    fileTypes: [
        {
            name: 'cube',
            mimeTypes: [MIME_TYPE],
            extensions: ['.cube', '.cub'],
            iconClass: 'jp-MaterialIcon jp-CubeIcon',
        },
    ],
    documentWidgetFactoryOptions: {
        name: 'cube viewer',
        primaryFileType: 'cube',
        fileTypes: ['cube'],
        defaultFor: ['cube'],
    },
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ }),

/***/ "./lib/uploadbuttons.js":
/*!******************************!*\
  !*** ./lib/uploadbuttons.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ UploadButtons)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _material_ui_core_styles__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @material-ui/core/styles */ "./node_modules/@material-ui/core/esm/styles/makeStyles.js");
/* harmony import */ var _material_ui_core_styles__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @material-ui/core/styles */ "./node_modules/@material-ui/core/esm/styles/createStyles.js");
/* harmony import */ var _material_ui_core_Button__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @material-ui/core/Button */ "./node_modules/@material-ui/core/esm/Button/Button.js");



const useStyles = (0,_material_ui_core_styles__WEBPACK_IMPORTED_MODULE_1__.default)((theme) => (0,_material_ui_core_styles__WEBPACK_IMPORTED_MODULE_2__.default)({
    root: {
        '& > *': {
            margin: theme.spacing(1),
        },
    },
    input: {
        display: 'none',
    },
}));
function UploadButtons(Props) {
    const classes = useStyles();
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: classes.root },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { accept: ".pdb, .cif, .ent, .gz, .sdf", className: classes.input, id: "contained-button-file", multiple: true, type: "file", onChange: Props.onChange }),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("label", { htmlFor: "contained-button-file" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_Button__WEBPACK_IMPORTED_MODULE_3__.default, { variant: "contained", color: "primary", component: "span" }, "Upload Structure"))));
}


/***/ }),

/***/ "./lib/visualizer.js":
/*!***************************!*\
  !*** ./lib/visualizer.js ***!
  \***************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Visualizer": () => (/* binding */ Visualizer)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _osscar_ngl__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @osscar/ngl */ "webpack/sharing/consume/default/@osscar/ngl/@osscar/ngl");
/* harmony import */ var _osscar_ngl__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_osscar_ngl__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! underscore */ "webpack/sharing/consume/default/underscore/underscore");
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(underscore__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _material_ui_core_Grid__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @material-ui/core/Grid */ "./node_modules/@material-ui/core/esm/Grid/Grid.js");
/* harmony import */ var _material_ui_core_Slider__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @material-ui/core/Slider */ "./node_modules/@material-ui/core/esm/Slider/Slider.js");
/* harmony import */ var _uploadbuttons__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./uploadbuttons */ "./lib/uploadbuttons.js");
/* harmony import */ var _material_ui_core_Switch__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @material-ui/core/Switch */ "./node_modules/@material-ui/core/esm/Switch/Switch.js");
/* harmony import */ var material_ui_color__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! material-ui-color */ "webpack/sharing/consume/default/material-ui-color/material-ui-color");
/* harmony import */ var material_ui_color__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(material_ui_color__WEBPACK_IMPORTED_MODULE_3__);








const palette = {
    black: 'black',
    red: '#ff0000',
    blue: '#0000ff',
    green: '#00ff00',
    yellow: 'yellow',
    cyan: 'cyan',
    lime: 'lime',
    gray: 'gray',
    orange: 'orange',
    purple: 'purple',
    white: 'white',
    pink: 'pink',
    darkblue: 'darkblue',
};
const marks1 = [
    {
        value: 0,
        label: '0%',
    },
    {
        value: 20,
        label: '20%',
    },
    {
        value: 40,
        label: '40%',
    },
    {
        value: 60,
        label: '60%',
    },
    {
        value: 80,
        label: '80%',
    },
    {
        value: 100,
        label: '100%',
    },
];
const marks2 = [
    {
        value: -0.02,
        label: '-0.02',
    },
    {
        value: -0.01,
        label: '-0.01',
    },
    {
        value: 0,
        label: '0',
    },
    {
        value: 0.01,
        label: '0.01',
    },
    {
        value: 0.02,
        label: '0.02',
    },
];
class Visualizer extends (react__WEBPACK_IMPORTED_MODULE_0___default().Component) {
    constructor(props, context) {
        super(props, context);
        this.toggle_backgroundColor = () => {
            if (this.dark) {
                this._stage.setParameters({ backgroundColor: 'white' });
            }
            else {
                this._stage.setParameters({ backgroundColor: 'black' });
            }
            this.dark = !this.dark;
        };
        this.handlePaletteSelection = (color) => {
            this._stage.setParameters({ backgroundColor: String(color) });
        };
        this.handleOpacityChange = (event, value) => {
            const transparency = value / 100.0;
            this._stage
                .getRepresentationsByName('positive_surface')
                .setParameters({ opacity: transparency });
            this._stage
                .getRepresentationsByName('negative_surface')
                .setParameters({ opacity: transparency });
        };
        this.handleIsovalueChange = (event, value) => {
            const val = value;
            this._stage
                .getRepresentationsByName('positive_surface')
                .setParameters({ isolevel: val[1] });
            this._stage
                .getRepresentationsByName('negative_surface')
                .setParameters({ isolevel: val[0] });
        };
        this.loadStructure = (event) => {
            this._stage.loadFile(event.target.files[0]).then((o) => {
                o.addRepresentation('ball+stick', {
                    name: 'structure',
                    visible: true,
                });
            });
        };
        this.toggleSpin = (event) => {
            this.setState({ spin: event.target.checked });
            this._stage.toggleSpin();
        };
        this.dark = true;
        this.uuid = underscore__WEBPACK_IMPORTED_MODULE_2__.uniqueId('ngl_');
        this.state = { value: 'black', spin: false };
        window.requestAnimationFrame(() => {
            _osscar_ngl__WEBPACK_IMPORTED_MODULE_1__.DatasourceRegistry.add('data', new _osscar_ngl__WEBPACK_IMPORTED_MODULE_1__.StaticDatasource('//cdn.rawgit.com/arose/ngl/v2.0.0-dev.32/data/'));
            // Create NGL Stage object
            this._stage = new _osscar_ngl__WEBPACK_IMPORTED_MODULE_1__.Stage(this.uuid, { quality: 'high' });
            const data = this.props.data;
            const stringBlob = new Blob([data], { type: 'text/plain' });
            this._stage.loadFile(stringBlob, { ext: 'cube' }).then((o) => {
                o.addRepresentation('surface', {
                    name: 'positive_surface',
                    visible: true,
                    isolevelType: 'value',
                    isolevel: 0.01,
                    color: 'red',
                    opacity: 0.7,
                    opaqueBack: false,
                });
                o.addRepresentation('surface', {
                    name: 'negative_surface',
                    visible: true,
                    isolevelType: 'value',
                    isolevel: -0.01,
                    color: 'blue',
                    opacity: 0.7,
                    opaqueBack: false,
                });
                o.autoView();
            }),
                function (e) {
                    console.log('information:' + e);
                };
        });
    }
    valuetext(value) {
        return String(value) + '%';
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "container" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_Grid__WEBPACK_IMPORTED_MODULE_4__.default, { container: true, spacing: 3, justify: "center", style: { marginTop: '20px' } },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_Grid__WEBPACK_IMPORTED_MODULE_4__.default, { item: true, sm: 8 },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { id: this.uuid, style: {
                            width: '100%',
                            height: '400px',
                            backgroundColor: 'black',
                        } })),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_Grid__WEBPACK_IMPORTED_MODULE_4__.default, { item: true, sm: 1 },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_Slider__WEBPACK_IMPORTED_MODULE_5__.default, { orientation: "vertical", getAriaValueText: this.valuetext, valueLabelDisplay: "auto", defaultValue: 70, "aria-labelledby": "vertical-slider", min: 0, max: 100, marks: marks1, onChange: this.handleOpacityChange, color: 'primary' })),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_Grid__WEBPACK_IMPORTED_MODULE_4__.default, { item: true, sm: 1 },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_Slider__WEBPACK_IMPORTED_MODULE_5__.default, { orientation: "vertical", defaultValue: [0.01, -0.01], "aria-labelledby": "vertical-slider", getAriaValueText: this.valuetext, valueLabelDisplay: "on", marks: marks2, min: -0.02, max: 0.02, step: 0.001, onChange: this.handleIsovalueChange, color: 'secondary' }))),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_Grid__WEBPACK_IMPORTED_MODULE_4__.default, { container: true, direction: "row", justify: "center", alignItems: "center", style: { marginTop: '20px' } },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(material_ui_color__WEBPACK_IMPORTED_MODULE_3__.ColorPalette, { palette: palette, onSelect: this.handlePaletteSelection }),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_uploadbuttons__WEBPACK_IMPORTED_MODULE_6__.default, { onChange: this.loadStructure }),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_Switch__WEBPACK_IMPORTED_MODULE_7__.default, { checked: this.state.spin, onChange: this.toggleSpin, name: "spin", color: "secondary" }))));
    }
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js.ee010f861204eab6d677.js.map