(self.webpackChunk_cylynx_pymotif=self.webpackChunk_cylynx_pymotif||[]).push([[886],{2460:(e,t,i)=>{var n=i(6062),r=i(737);"string"==typeof(r=r.__esModule?r.default:r)&&(r=[[e.id,r,""]]);n(r,{insert:"head",singleton:!1}),e.exports=r.locals||{}},4974:(e,t,i)=>{var n=i(6062),r=i(7672);"string"==typeof(r=r.__esModule?r.default:r)&&(r=[[e.id,r,""]]);n(r,{insert:"head",singleton:!1}),e.exports=r.locals||{}},6062:(e,t,i)=>{"use strict";var n,r=function(){var e={};return function(t){if(void 0===e[t]){var i=document.querySelector(t);if(window.HTMLIFrameElement&&i instanceof window.HTMLIFrameElement)try{i=i.contentDocument.head}catch(e){i=null}e[t]=i}return e[t]}}(),o=[];function s(e){for(var t=-1,i=0;i<o.length;i++)if(o[i].identifier===e){t=i;break}return t}function a(e,t){for(var i={},n=[],r=0;r<e.length;r++){var a=e[r],l=t.base?a[0]+t.base:a[0],c=i[l]||0,u="".concat(l," ").concat(c);i[l]=c+1;var d=s(u),p={css:a[1],media:a[2],sourceMap:a[3]};-1!==d?(o[d].references++,o[d].updater(p)):o.push({identifier:u,updater:m(p,t),references:1}),n.push(u)}return n}function l(e){var t=document.createElement("style"),n=e.attributes||{};if(void 0===n.nonce){var o=i.nc;o&&(n.nonce=o)}if(Object.keys(n).forEach((function(e){t.setAttribute(e,n[e])})),"function"==typeof e.insert)e.insert(t);else{var s=r(e.insert||"head");if(!s)throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");s.appendChild(t)}return t}var c,u=(c=[],function(e,t){return c[e]=t,c.filter(Boolean).join("\n")});function d(e,t,i,n){var r=i?"":n.media?"@media ".concat(n.media," {").concat(n.css,"}"):n.css;if(e.styleSheet)e.styleSheet.cssText=u(t,r);else{var o=document.createTextNode(r),s=e.childNodes;s[t]&&e.removeChild(s[t]),s.length?e.insertBefore(o,s[t]):e.appendChild(o)}}function p(e,t,i){var n=i.css,r=i.media,o=i.sourceMap;if(r?e.setAttribute("media",r):e.removeAttribute("media"),o&&"undefined"!=typeof btoa&&(n+="\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(o))))," */")),e.styleSheet)e.styleSheet.cssText=n;else{for(;e.firstChild;)e.removeChild(e.firstChild);e.appendChild(document.createTextNode(n))}}var f=null,h=0;function m(e,t){var i,n,r;if(t.singleton){var o=h++;i=f||(f=l(t)),n=d.bind(null,i,o,!1),r=d.bind(null,i,o,!0)}else i=l(t),n=p.bind(null,i,t),r=function(){!function(e){if(null===e.parentNode)return!1;e.parentNode.removeChild(e)}(i)};return n(e),function(t){if(t){if(t.css===e.css&&t.media===e.media&&t.sourceMap===e.sourceMap)return;n(e=t)}else r()}}e.exports=function(e,t){(t=t||{}).singleton||"boolean"==typeof t.singleton||(t.singleton=(void 0===n&&(n=Boolean(window&&document&&document.all&&!window.atob)),n));var i=a(e=e||[],t);return function(e){if(e=e||[],"[object Array]"===Object.prototype.toString.call(e)){for(var n=0;n<i.length;n++){var r=s(i[n]);o[r].references--}for(var l=a(e,t),c=0;c<i.length;c++){var u=s(i[c]);0===o[u].references&&(o[u].updater(),o.splice(u,1))}i=l}}}},8886:function(e,t,i){"use strict";var n=this&&this.__importDefault||function(e){return e&&e.__esModule?e:{default:e}};Object.defineProperty(t,"__esModule",{value:!0}),t.MotifView=t.MotifModel=void 0;const r=i(2565),o=i(4603),s=n(i(48)),a=n(i(2752)),l=i(8657);class c extends r.DOMWidgetModel{defaults(){return Object.assign(Object.assign({},super.defaults()),{_model_name:c.model_name,_model_module:c.model_module,_model_module_version:c.model_module_version,_view_name:c.view_name,_view_module:c.view_module,_view_module_version:c.view_module_version,state:{}})}}t.MotifModel=c,c.serializers=Object.assign({},r.DOMWidgetModel.serializers),c.model_name="MotifModel",c.model_module=l.MODULE_NAME,c.model_module_version=l.MODULE_VERSION,c.view_name="MotifView",c.view_module=l.MODULE_NAME,c.view_module_version=l.MODULE_VERSION;let u=0;class d extends r.DOMWidgetView{render(){this.el.classList.add("jupyter-widgets"),this.el.classList.add("motif-jupyter-widgets"),this.div=this.createDiv(),this.btn=this.createBtn(),this.store=a.default(),s.default(this.div,this.store,this.onRefChange),this.updateStore(),this.btn.onclick=this.saveState.bind(this)}onRefChange(e){this.graphRef=e;const t={key:"main",id:"layers"};setTimeout((()=>{this.store.dispatch(o.WidgetSlices.updateWidget(t)),this.store.dispatch(o.WidgetSlices.updateWidget(t)),this.graphRef.graph.fitView(10)}),0)}createDiv(){this.id=`motif-${u}`,u++,this.onRefChange=this.onRefChange.bind(this);const e=document.createElement("div");return e.setAttribute("id",this.id),e.classList.add("motif"),this.el.appendChild(e),e}createBtn(){const e=document.createElement("BUTTON");return e.innerHTML="SAVE DATA AND STYLE",e.setAttribute("style","position: absolute; bottom: 0px; left: 40%; color: white; background-color: #252b35"),this.el.appendChild(e),e}updateStore(){const e=this.model.get("state");if(Array.isArray(e.data)&&e.data.length){const t=o.GraphThunks.importJsonData([e],!0,null,!0);this.store.dispatch(t)}this.store.dispatch(o.WidgetSlices.setWidget([])),this.store.dispatch(o.UISlices.closeModal())}saveState(){const e=this.store.getState(),t=o.GraphSelectors.getGraphList(e),i=o.GraphSelectors.getStyleOptions(e);this.model.set("state",{data:t,style:i}),this.model.save_changes()}}t.MotifView=d},2752:(e,t,i)=>{"use strict";Object.defineProperty(t,"__esModule",{value:!0});const n=i(5878),r=i(4603);t.default=()=>n.configureStore({reducer:n.combineReducers({investigate:r.investigateReducer}),middleware:e=>e({serializableCheck:!1,immutableCheck:!1})})},48:function(e,t,i){"use strict";var n=this&&this.__createBinding||(Object.create?function(e,t,i,n){void 0===n&&(n=i),Object.defineProperty(e,n,{enumerable:!0,get:function(){return t[i]}})}:function(e,t,i,n){void 0===n&&(n=i),e[n]=t[i]}),r=this&&this.__setModuleDefault||(Object.create?function(e,t){Object.defineProperty(e,"default",{enumerable:!0,value:t})}:function(e,t){e.default=t}),o=this&&this.__importStar||function(e){if(e&&e.__esModule)return e;var t={};if(null!=e)for(var i in e)"default"!==i&&Object.prototype.hasOwnProperty.call(e,i)&&n(t,e,i);return r(t,e),t},s=this&&this.__importDefault||function(e){return e&&e.__esModule?e:{default:e}};Object.defineProperty(t,"__esModule",{value:!0});const a=o(i(6271)),l=s(i(4456)),c=i(6170),u=i(2226),d=i(4004),p=o(i(4603)),f=i(5907);i(2460),i(4974);const h=new c.Client({prefix:"m_"});t.default=function(e,t,i){l.default.render(a.default.createElement((()=>{const e=a.useRef(null);return a.useEffect((()=>{e&&e.current&&e.current.graph&&i(e.current)}),[e.current]),a.default.createElement(u.Provider,{value:h},a.default.createElement(d.BaseProvider,{theme:p.MotifLightTheme},a.default.createElement(f.Provider,{store:t},a.default.createElement(p.default,{ref:e,name:"Motif",primaryTheme:p.MotifLightTheme,secondaryTheme:p.MotifDarkTheme}))))}),null),e)}},8657:(e,t,i)=>{"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.MODULE_NAME=t.MODULE_VERSION=void 0;const n=i(306);t.MODULE_VERSION=n.version,t.MODULE_NAME=n.name},737:(e,t,i)=>{(t=i(3645)(!1)).push([e.id,"@import url(https://fonts.googleapis.com/icon?family=Material+Icons);"]),t.push([e.id,"@import url(https://fonts.googleapis.com/css2?family=Poppins:wght@100;200;300;400;500;600;700&display=swap);"]),t.push([e.id,"#graphin-container{height:100%;width:100%;position:relative}.graphin-core{height:100%;width:100%;min-height:500px;background:#fff}#graphin-container{height:100%;width:100%;position:relative}.graphin-core{height:100%;width:100%;min-height:500px}::-webkit-scrollbar{height:5px;width:5px}::-webkit-scrollbar-track{background:#f1f1f1}::-webkit-scrollbar-thumb{background:#595f6d}::-webkit-scrollbar-thumb:hover{background:#595f6d}",""]),e.exports=t},7672:(e,t,i)=>{(t=i(3645)(!1)).push([e.id,"/* To override jupyter lab ui box-sizing */\n*, *::before, *::after {\n  box-sizing: border-box;\n}\n",""]),e.exports=t},3645:e=>{"use strict";e.exports=function(e){var t=[];return t.toString=function(){return this.map((function(t){var i=function(e,t){var i,n,r,o=e[1]||"",s=e[3];if(!s)return o;if(t&&"function"==typeof btoa){var a=(i=s,n=btoa(unescape(encodeURIComponent(JSON.stringify(i)))),r="sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(n),"/*# ".concat(r," */")),l=s.sources.map((function(e){return"/*# sourceURL=".concat(s.sourceRoot||"").concat(e," */")}));return[o].concat(l).concat([a]).join("\n")}return[o].join("\n")}(t,e);return t[2]?"@media ".concat(t[2]," {").concat(i,"}"):i})).join("")},t.i=function(e,i,n){"string"==typeof e&&(e=[[null,e,""]]);var r={};if(n)for(var o=0;o<this.length;o++){var s=this[o][0];null!=s&&(r[s]=!0)}for(var a=0;a<e.length;a++){var l=[].concat(e[a]);n&&r[l[0]]||(i&&(l[2]?l[2]="".concat(i," and ").concat(l[2]):l[2]=i),t.push(l))}},t}},306:e=>{"use strict";e.exports=JSON.parse('{"name":"@cylynx/pymotif","version":"0.0.4","description":"jupyter widget bindings for the motif library","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","css/*.css"],"homepage":"https://github.com/Cylynx/motif.gl","bugs":{"url":"https://github.com/Cylynx/motif.gl/issues"},"license":"BSD-3-Clause","author":{"name":"Cylynx","email":"hello@cylynx.io"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://github.com/Cylynx/motif.gl"},"scripts":{"start":"NODE_ENV=development npm-run-all -p watch:*","build":"npm run build:lib && npm run build:nbextension && npm run build:labextension:dev","build:prod":"npm run build:lib && npm run build:nbextension && npm run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack","clean":"npm run clean:lib && npm run clean:nbextension && npm run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf pymotif/labextension","clean:nbextension":"rimraf pymotif/nbextension/static/index.js","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","prepack":"npm run build:lib","test":"jest","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@cylynx/motif":"^0.0.4","@jupyter-widgets/base":"^1.1.10 || ^2.0.0 || ^3.0.0 || ^4.0.0","@reduxjs/toolkit":"^1.2.3","baseui":"^9.90.0","react":"^16.8.6","react-dom":"^16.8.6","react-hook-form":"^7.3.4","react-redux":"^7.2.3","styletron-engine-atomic":"^1.4.5","styletron-react":"^5.2.7"},"devDependencies":{"@babel/core":"^7.5.0","@babel/preset-env":"^7.5.0","@jupyterlab/builder":"^3.0.0","@phosphor/application":"^1.6.0","@phosphor/widgets":"^1.6.0","@types/jest":"^26.0.0","@types/node":"^10.11.6","@types/webpack-env":"^1.13.6","acorn":"^7.2.0","css-loader":"^3.2.0","fs-extra":"^7.0.0","jest":"^26.0.0","mkdirp":"^0.5.1","npm-run-all":"^4.1.3","prettier":"^2.0.5","rimraf":"^2.6.2","source-map-loader":"^0.2.4","style-loader":"^1.0.0","ts-jest":"^26.0.0","ts-loader":"^8.0.0","typescript":"^4.2.4","webpack":"^5.0.0","webpack-cli":"^4.0.0"},"jupyterlab":{"extension":"lib/plugin","outputDir":"pymotif/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}')}}]);