(self.webpackChunk_JUPYTERLAB_CORE_OUTPUT=self.webpackChunk_JUPYTERLAB_CORE_OUTPUT||[]).push([[2604],{56738:(r,t,e)=>{"use strict";e.r(t),e.d(t,{default:()=>n});var o=e(93476),i=e.n(o)()((function(r){return r[1]}));i.push([r.id,".cm-s-liquibyte.CodeMirror {\n\tbackground-color: #000;\n\tcolor: #fff;\n\tline-height: 1.2em;\n\tfont-size: 1em;\n}\n.cm-s-liquibyte .CodeMirror-focused .cm-matchhighlight {\n\ttext-decoration: underline;\n\ttext-decoration-color: #0f0;\n\ttext-decoration-style: wavy;\n}\n.cm-s-liquibyte .cm-trailingspace {\n\ttext-decoration: line-through;\n\ttext-decoration-color: #f00;\n\ttext-decoration-style: dotted;\n}\n.cm-s-liquibyte .cm-tab {\n\ttext-decoration: line-through;\n\ttext-decoration-color: #404040;\n\ttext-decoration-style: dotted;\n}\n.cm-s-liquibyte .CodeMirror-gutters { background-color: #262626; border-right: 1px solid #505050; padding-right: 0.8em; }\n.cm-s-liquibyte .CodeMirror-gutter-elt div { font-size: 1.2em; }\n.cm-s-liquibyte .CodeMirror-guttermarker {  }\n.cm-s-liquibyte .CodeMirror-guttermarker-subtle {  }\n.cm-s-liquibyte .CodeMirror-linenumber { color: #606060; padding-left: 0; }\n.cm-s-liquibyte .CodeMirror-cursor { border-left: 1px solid #eee; }\n\n.cm-s-liquibyte span.cm-comment     { color: #008000; }\n.cm-s-liquibyte span.cm-def         { color: #ffaf40; font-weight: bold; }\n.cm-s-liquibyte span.cm-keyword     { color: #c080ff; font-weight: bold; }\n.cm-s-liquibyte span.cm-builtin     { color: #ffaf40; font-weight: bold; }\n.cm-s-liquibyte span.cm-variable    { color: #5967ff; font-weight: bold; }\n.cm-s-liquibyte span.cm-string      { color: #ff8000; }\n.cm-s-liquibyte span.cm-number      { color: #0f0; font-weight: bold; }\n.cm-s-liquibyte span.cm-atom        { color: #bf3030; font-weight: bold; }\n\n.cm-s-liquibyte span.cm-variable-2  { color: #007f7f; font-weight: bold; }\n.cm-s-liquibyte span.cm-variable-3, .cm-s-liquibyte span.cm-type { color: #c080ff; font-weight: bold; }\n.cm-s-liquibyte span.cm-property    { color: #999; font-weight: bold; }\n.cm-s-liquibyte span.cm-operator    { color: #fff; }\n\n.cm-s-liquibyte span.cm-meta        { color: #0f0; }\n.cm-s-liquibyte span.cm-qualifier   { color: #fff700; font-weight: bold; }\n.cm-s-liquibyte span.cm-bracket     { color: #cc7; }\n.cm-s-liquibyte span.cm-tag         { color: #ff0; font-weight: bold; }\n.cm-s-liquibyte span.cm-attribute   { color: #c080ff; font-weight: bold; }\n.cm-s-liquibyte span.cm-error       { color: #f00; }\n\n.cm-s-liquibyte div.CodeMirror-selected { background-color: rgba(255, 0, 0, 0.25); }\n\n.cm-s-liquibyte span.cm-compilation { background-color: rgba(255, 255, 255, 0.12); }\n\n.cm-s-liquibyte .CodeMirror-activeline-background { background-color: rgba(0, 255, 0, 0.15); }\n\n/* Default styles for common addons */\n.cm-s-liquibyte .CodeMirror span.CodeMirror-matchingbracket { color: #0f0; font-weight: bold; }\n.cm-s-liquibyte .CodeMirror span.CodeMirror-nonmatchingbracket { color: #f00; font-weight: bold; }\n.CodeMirror-matchingtag { background-color: rgba(150, 255, 0, .3); }\n/* Scrollbars */\n/* Simple */\n.cm-s-liquibyte div.CodeMirror-simplescroll-horizontal div:hover, .cm-s-liquibyte div.CodeMirror-simplescroll-vertical div:hover {\n\tbackground-color: rgba(80, 80, 80, .7);\n}\n.cm-s-liquibyte div.CodeMirror-simplescroll-horizontal div, .cm-s-liquibyte div.CodeMirror-simplescroll-vertical div {\n\tbackground-color: rgba(80, 80, 80, .3);\n\tborder: 1px solid #404040;\n\tborder-radius: 5px;\n}\n.cm-s-liquibyte div.CodeMirror-simplescroll-vertical div {\n\tborder-top: 1px solid #404040;\n\tborder-bottom: 1px solid #404040;\n}\n.cm-s-liquibyte div.CodeMirror-simplescroll-horizontal div {\n\tborder-left: 1px solid #404040;\n\tborder-right: 1px solid #404040;\n}\n.cm-s-liquibyte div.CodeMirror-simplescroll-vertical {\n\tbackground-color: #262626;\n}\n.cm-s-liquibyte div.CodeMirror-simplescroll-horizontal {\n\tbackground-color: #262626;\n\tborder-top: 1px solid #404040;\n}\n/* Overlay */\n.cm-s-liquibyte div.CodeMirror-overlayscroll-horizontal div, div.CodeMirror-overlayscroll-vertical div {\n\tbackground-color: #404040;\n\tborder-radius: 5px;\n}\n.cm-s-liquibyte div.CodeMirror-overlayscroll-vertical div {\n\tborder: 1px solid #404040;\n}\n.cm-s-liquibyte div.CodeMirror-overlayscroll-horizontal div {\n\tborder: 1px solid #404040;\n}\n",""]);const n=i},93476:r=>{"use strict";r.exports=function(r){var t=[];return t.toString=function(){return this.map((function(t){var e=r(t);return t[2]?"@media ".concat(t[2]," {").concat(e,"}"):e})).join("")},t.i=function(r,e,o){"string"==typeof r&&(r=[[null,r,""]]);var i={};if(o)for(var n=0;n<this.length;n++){var l=this[n][0];null!=l&&(i[l]=!0)}for(var c=0;c<r.length;c++){var s=[].concat(r[c]);o&&i[s[0]]||(e&&(s[2]?s[2]="".concat(e," and ").concat(s[2]):s[2]=e),t.push(s))}},t}},2604:(r,t,e)=>{var o=e(56738);"string"==typeof(o=o.__esModule?o.default:o)&&(o=[[r.id,o,""]]);e(1892)(o,{insert:"head",singleton:!1}),o.locals&&(r.exports=o.locals)},1892:(r,t,e)=>{"use strict";var o,i={},n=function(){var r={};return function(t){if(void 0===r[t]){var e=document.querySelector(t);if(window.HTMLIFrameElement&&e instanceof window.HTMLIFrameElement)try{e=e.contentDocument.head}catch(r){e=null}r[t]=e}return r[t]}}();function l(r,t){for(var e=[],o={},i=0;i<r.length;i++){var n=r[i],l=t.base?n[0]+t.base:n[0],c={css:n[1],media:n[2],sourceMap:n[3]};o[l]?o[l].parts.push(c):e.push(o[l]={id:l,parts:[c]})}return e}function c(r,t){for(var e=0;e<r.length;e++){var o=r[e],n=i[o.id],l=0;if(n){for(n.refs++;l<n.parts.length;l++)n.parts[l](o.parts[l]);for(;l<o.parts.length;l++)n.parts.push(p(o.parts[l],t))}else{for(var c=[];l<o.parts.length;l++)c.push(p(o.parts[l],t));i[o.id]={id:o.id,refs:1,parts:c}}}}function s(r){var t=document.createElement("style");if(void 0===r.attributes.nonce){var o=e.nc;o&&(r.attributes.nonce=o)}if(Object.keys(r.attributes).forEach((function(e){t.setAttribute(e,r.attributes[e])})),"function"==typeof r.insert)r.insert(t);else{var i=n(r.insert||"head");if(!i)throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");i.appendChild(t)}return t}var a,d=(a=[],function(r,t){return a[r]=t,a.filter(Boolean).join("\n")});function u(r,t,e,o){var i=e?"":o.css;if(r.styleSheet)r.styleSheet.cssText=d(t,i);else{var n=document.createTextNode(i),l=r.childNodes;l[t]&&r.removeChild(l[t]),l.length?r.insertBefore(n,l[t]):r.appendChild(n)}}function b(r,t,e){var o=e.css,i=e.media,n=e.sourceMap;if(i&&r.setAttribute("media",i),n&&btoa&&(o+="\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(n))))," */")),r.styleSheet)r.styleSheet.cssText=o;else{for(;r.firstChild;)r.removeChild(r.firstChild);r.appendChild(document.createTextNode(o))}}var f=null,m=0;function p(r,t){var e,o,i;if(t.singleton){var n=m++;e=f||(f=s(t)),o=u.bind(null,e,n,!1),i=u.bind(null,e,n,!0)}else e=s(t),o=b.bind(null,e,t),i=function(){!function(r){if(null===r.parentNode)return!1;r.parentNode.removeChild(r)}(e)};return o(r),function(t){if(t){if(t.css===r.css&&t.media===r.media&&t.sourceMap===r.sourceMap)return;o(r=t)}else i()}}r.exports=function(r,t){(t=t||{}).attributes="object"==typeof t.attributes?t.attributes:{},t.singleton||"boolean"==typeof t.singleton||(t.singleton=(void 0===o&&(o=Boolean(window&&document&&document.all&&!window.atob)),o));var e=l(r,t);return c(e,t),function(r){for(var o=[],n=0;n<e.length;n++){var s=e[n],a=i[s.id];a&&(a.refs--,o.push(a))}r&&c(l(r,t),t);for(var d=0;d<o.length;d++){var u=o[d];if(0===u.refs){for(var b=0;b<u.parts.length;b++)u.parts[b]();delete i[u.id]}}}}}}]);