(self.webpackChunk_JUPYTERLAB_CORE_OUTPUT=self.webpackChunk_JUPYTERLAB_CORE_OUTPUT||[]).push([[330],{64695:(t,e,n)=>{"use strict";n.r(e),n.d(e,{default:()=>a});var o=n(93476),r=n.n(o)()((function(t){return t[1]}));r.push([t.id,"/*\nName:   DuoTone-Light\nAuthor: by Bram de Haan, adapted from DuoTone themes by Simurai (http://simurai.com/projects/2016/01/01/duotone-themes)\n\nCodeMirror template by Jan T. Sott (https://github.com/idleberg), adapted by Bram de Haan (https://github.com/atelierbram/)\n*/\n\n.cm-s-duotone-light.CodeMirror { background: #faf8f5; color: #b29762; }\n.cm-s-duotone-light div.CodeMirror-selected { background: #e3dcce !important; }\n.cm-s-duotone-light .CodeMirror-gutters { background: #faf8f5; border-right: 0px; }\n.cm-s-duotone-light .CodeMirror-linenumber { color: #cdc4b1; }\n\n/* begin cursor */\n.cm-s-duotone-light .CodeMirror-cursor { border-left: 1px solid #93abdc; /* border-left: 1px solid #93abdc80; */ border-right: .5em solid #93abdc; /* border-right: .5em solid #93abdc80; */ opacity: .5; }\n.cm-s-duotone-light .CodeMirror-activeline-background { background: #e3dcce;  /* background: #e3dcce80; */ opacity: .5; }\n.cm-s-duotone-light .cm-fat-cursor .CodeMirror-cursor { background: #93abdc; /* #93abdc80; */ opacity: .5; }\n/* end cursor */\n\n.cm-s-duotone-light span.cm-atom, .cm-s-duotone-light span.cm-number, .cm-s-duotone-light span.cm-keyword, .cm-s-duotone-light span.cm-variable, .cm-s-duotone-light span.cm-attribute, .cm-s-duotone-light span.cm-quote, .cm-s-duotone-light-light span.cm-hr, .cm-s-duotone-light-light span.cm-link { color: #063289; }\n\n.cm-s-duotone-light span.cm-property { color: #b29762; }\n.cm-s-duotone-light span.cm-punctuation, .cm-s-duotone-light span.cm-unit, .cm-s-duotone-light span.cm-negative { color: #063289; }\n.cm-s-duotone-light span.cm-string, .cm-s-duotone-light span.cm-operator { color: #1659df; }\n.cm-s-duotone-light span.cm-positive { color: #896724; }\n\n.cm-s-duotone-light span.cm-variable-2, .cm-s-duotone-light span.cm-variable-3, .cm-s-duotone-light span.cm-type, .cm-s-duotone-light span.cm-string-2, .cm-s-duotone-light span.cm-url { color: #896724; }\n.cm-s-duotone-light span.cm-def, .cm-s-duotone-light span.cm-tag, .cm-s-duotone-light span.cm-builtin, .cm-s-duotone-light span.cm-qualifier, .cm-s-duotone-light span.cm-header, .cm-s-duotone-light span.cm-em { color: #2d2006; }\n.cm-s-duotone-light span.cm-bracket, .cm-s-duotone-light span.cm-comment { color: #b6ad9a; }\n\n/* using #f00 red for errors, don't think any of the colorscheme variables will stand out enough, ... maybe by giving it a background-color ... */\n/* .cm-s-duotone-light span.cm-error { background: #896724; color: #728fcb; } */\n.cm-s-duotone-light span.cm-error, .cm-s-duotone-light span.cm-invalidchar { color: #f00; }\n\n.cm-s-duotone-light span.cm-header { font-weight: normal; }\n.cm-s-duotone-light .CodeMirror-matchingbracket { text-decoration: underline; color: #faf8f5 !important; }\n\n",""]);const a=r},93476:t=>{"use strict";t.exports=function(t){var e=[];return e.toString=function(){return this.map((function(e){var n=t(e);return e[2]?"@media ".concat(e[2]," {").concat(n,"}"):n})).join("")},e.i=function(t,n,o){"string"==typeof t&&(t=[[null,t,""]]);var r={};if(o)for(var a=0;a<this.length;a++){var i=this[a][0];null!=i&&(r[i]=!0)}for(var c=0;c<t.length;c++){var s=[].concat(t[c]);o&&r[s[0]]||(n&&(s[2]?s[2]="".concat(n," and ").concat(s[2]):s[2]=n),e.push(s))}},e}},50330:(t,e,n)=>{var o=n(64695);"string"==typeof(o=o.__esModule?o.default:o)&&(o=[[t.id,o,""]]);n(1892)(o,{insert:"head",singleton:!1}),o.locals&&(t.exports=o.locals)},1892:(t,e,n)=>{"use strict";var o,r={},a=function(){var t={};return function(e){if(void 0===t[e]){var n=document.querySelector(e);if(window.HTMLIFrameElement&&n instanceof window.HTMLIFrameElement)try{n=n.contentDocument.head}catch(t){n=null}t[e]=n}return t[e]}}();function i(t,e){for(var n=[],o={},r=0;r<t.length;r++){var a=t[r],i=e.base?a[0]+e.base:a[0],c={css:a[1],media:a[2],sourceMap:a[3]};o[i]?o[i].parts.push(c):n.push(o[i]={id:i,parts:[c]})}return n}function c(t,e){for(var n=0;n<t.length;n++){var o=t[n],a=r[o.id],i=0;if(a){for(a.refs++;i<a.parts.length;i++)a.parts[i](o.parts[i]);for(;i<o.parts.length;i++)a.parts.push(g(o.parts[i],e))}else{for(var c=[];i<o.parts.length;i++)c.push(g(o.parts[i],e));r[o.id]={id:o.id,refs:1,parts:c}}}}function s(t){var e=document.createElement("style");if(void 0===t.attributes.nonce){var o=n.nc;o&&(t.attributes.nonce=o)}if(Object.keys(t.attributes).forEach((function(n){e.setAttribute(n,t.attributes[n])})),"function"==typeof t.insert)t.insert(e);else{var r=a(t.insert||"head");if(!r)throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");r.appendChild(e)}return e}var d,l=(d=[],function(t,e){return d[t]=e,d.filter(Boolean).join("\n")});function u(t,e,n,o){var r=n?"":o.css;if(t.styleSheet)t.styleSheet.cssText=l(e,r);else{var a=document.createTextNode(r),i=t.childNodes;i[e]&&t.removeChild(i[e]),i.length?t.insertBefore(a,i[e]):t.appendChild(a)}}function m(t,e,n){var o=n.css,r=n.media,a=n.sourceMap;if(r&&t.setAttribute("media",r),a&&btoa&&(o+="\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(a))))," */")),t.styleSheet)t.styleSheet.cssText=o;else{for(;t.firstChild;)t.removeChild(t.firstChild);t.appendChild(document.createTextNode(o))}}var h=null,p=0;function g(t,e){var n,o,r;if(e.singleton){var a=p++;n=h||(h=s(e)),o=u.bind(null,n,a,!1),r=u.bind(null,n,a,!0)}else n=s(e),o=m.bind(null,n,e),r=function(){!function(t){if(null===t.parentNode)return!1;t.parentNode.removeChild(t)}(n)};return o(t),function(e){if(e){if(e.css===t.css&&e.media===t.media&&e.sourceMap===t.sourceMap)return;o(t=e)}else r()}}t.exports=function(t,e){(e=e||{}).attributes="object"==typeof e.attributes?e.attributes:{},e.singleton||"boolean"==typeof e.singleton||(e.singleton=(void 0===o&&(o=Boolean(window&&document&&document.all&&!window.atob)),o));var n=i(t,e);return c(n,e),function(t){for(var o=[],a=0;a<n.length;a++){var s=n[a],d=r[s.id];d&&(d.refs--,o.push(d))}t&&c(i(t,e),e);for(var l=0;l<o.length;l++){var u=o[l];if(0===u.refs){for(var m=0;m<u.parts.length;m++)u.parts[m]();delete r[u.id]}}}}}}]);