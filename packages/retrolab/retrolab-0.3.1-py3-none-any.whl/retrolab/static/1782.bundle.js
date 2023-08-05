(self.webpackChunk_JUPYTERLAB_CORE_OUTPUT=self.webpackChunk_JUPYTERLAB_CORE_OUTPUT||[]).push([[1782],{67991:(n,e,r)=>{"use strict";r.r(e),r.d(e,{default:()=>c});var t=r(93476),o=r.n(t)()((function(n){return n[1]}));o.push([n.id,'/**\n * "\n *  Using Zenburn color palette from the Emacs Zenburn Theme\n *  https://github.com/bbatsov/zenburn-emacs/blob/master/zenburn-theme.el\n *\n *  Also using parts of https://github.com/xavi/coderay-lighttable-theme\n * "\n * From: https://github.com/wisenomad/zenburn-lighttable-theme/blob/master/zenburn.css\n */\n\n.cm-s-zenburn .CodeMirror-gutters { background: #3f3f3f !important; }\n.cm-s-zenburn .CodeMirror-foldgutter-open, .CodeMirror-foldgutter-folded { color: #999; }\n.cm-s-zenburn .CodeMirror-cursor { border-left: 1px solid white; }\n.cm-s-zenburn.CodeMirror { background-color: #3f3f3f; color: #dcdccc; }\n.cm-s-zenburn span.cm-builtin { color: #dcdccc; font-weight: bold; }\n.cm-s-zenburn span.cm-comment { color: #7f9f7f; }\n.cm-s-zenburn span.cm-keyword { color: #f0dfaf; font-weight: bold; }\n.cm-s-zenburn span.cm-atom { color: #bfebbf; }\n.cm-s-zenburn span.cm-def { color: #dcdccc; }\n.cm-s-zenburn span.cm-variable { color: #dfaf8f; }\n.cm-s-zenburn span.cm-variable-2 { color: #dcdccc; }\n.cm-s-zenburn span.cm-string { color: #cc9393; }\n.cm-s-zenburn span.cm-string-2 { color: #cc9393; }\n.cm-s-zenburn span.cm-number { color: #dcdccc; }\n.cm-s-zenburn span.cm-tag { color: #93e0e3; }\n.cm-s-zenburn span.cm-property { color: #dfaf8f; }\n.cm-s-zenburn span.cm-attribute { color: #dfaf8f; }\n.cm-s-zenburn span.cm-qualifier { color: #7cb8bb; }\n.cm-s-zenburn span.cm-meta { color: #f0dfaf; }\n.cm-s-zenburn span.cm-header { color: #f0efd0; }\n.cm-s-zenburn span.cm-operator { color: #f0efd0; }\n.cm-s-zenburn span.CodeMirror-matchingbracket { box-sizing: border-box; background: transparent; border-bottom: 1px solid; }\n.cm-s-zenburn span.CodeMirror-nonmatchingbracket { border-bottom: 1px solid; background: none; }\n.cm-s-zenburn .CodeMirror-activeline { background: #000000; }\n.cm-s-zenburn .CodeMirror-activeline-background { background: #000000; }\n.cm-s-zenburn div.CodeMirror-selected { background: #545454; }\n.cm-s-zenburn .CodeMirror-focused div.CodeMirror-selected { background: #4f4f4f; }\n',""]);const c=o},93476:n=>{"use strict";n.exports=function(n){var e=[];return e.toString=function(){return this.map((function(e){var r=n(e);return e[2]?"@media ".concat(e[2]," {").concat(r,"}"):r})).join("")},e.i=function(n,r,t){"string"==typeof n&&(n=[[null,n,""]]);var o={};if(t)for(var c=0;c<this.length;c++){var a=this[c][0];null!=a&&(o[a]=!0)}for(var s=0;s<n.length;s++){var i=[].concat(n[s]);t&&o[i[0]]||(r&&(i[2]?i[2]="".concat(r," and ").concat(i[2]):i[2]=r),e.push(i))}},e}},31782:(n,e,r)=>{var t=r(67991);"string"==typeof(t=t.__esModule?t.default:t)&&(t=[[n.id,t,""]]);r(1892)(t,{insert:"head",singleton:!1}),t.locals&&(n.exports=t.locals)},1892:(n,e,r)=>{"use strict";var t,o={},c=function(){var n={};return function(e){if(void 0===n[e]){var r=document.querySelector(e);if(window.HTMLIFrameElement&&r instanceof window.HTMLIFrameElement)try{r=r.contentDocument.head}catch(n){r=null}n[e]=r}return n[e]}}();function a(n,e){for(var r=[],t={},o=0;o<n.length;o++){var c=n[o],a=e.base?c[0]+e.base:c[0],s={css:c[1],media:c[2],sourceMap:c[3]};t[a]?t[a].parts.push(s):r.push(t[a]={id:a,parts:[s]})}return r}function s(n,e){for(var r=0;r<n.length;r++){var t=n[r],c=o[t.id],a=0;if(c){for(c.refs++;a<c.parts.length;a++)c.parts[a](t.parts[a]);for(;a<t.parts.length;a++)c.parts.push(p(t.parts[a],e))}else{for(var s=[];a<t.parts.length;a++)s.push(p(t.parts[a],e));o[t.id]={id:t.id,refs:1,parts:s}}}}function i(n){var e=document.createElement("style");if(void 0===n.attributes.nonce){var t=r.nc;t&&(n.attributes.nonce=t)}if(Object.keys(n.attributes).forEach((function(r){e.setAttribute(r,n.attributes[r])})),"function"==typeof n.insert)n.insert(e);else{var o=c(n.insert||"head");if(!o)throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");o.appendChild(e)}return e}var u,l=(u=[],function(n,e){return u[n]=e,u.filter(Boolean).join("\n")});function d(n,e,r,t){var o=r?"":t.css;if(n.styleSheet)n.styleSheet.cssText=l(e,o);else{var c=document.createTextNode(o),a=n.childNodes;a[e]&&n.removeChild(a[e]),a.length?n.insertBefore(c,a[e]):n.appendChild(c)}}function f(n,e,r){var t=r.css,o=r.media,c=r.sourceMap;if(o&&n.setAttribute("media",o),c&&btoa&&(t+="\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(c))))," */")),n.styleSheet)n.styleSheet.cssText=t;else{for(;n.firstChild;)n.removeChild(n.firstChild);n.appendChild(document.createTextNode(t))}}var b=null,m=0;function p(n,e){var r,t,o;if(e.singleton){var c=m++;r=b||(b=i(e)),t=d.bind(null,r,c,!1),o=d.bind(null,r,c,!0)}else r=i(e),t=f.bind(null,r,e),o=function(){!function(n){if(null===n.parentNode)return!1;n.parentNode.removeChild(n)}(r)};return t(n),function(e){if(e){if(e.css===n.css&&e.media===n.media&&e.sourceMap===n.sourceMap)return;t(n=e)}else o()}}n.exports=function(n,e){(e=e||{}).attributes="object"==typeof e.attributes?e.attributes:{},e.singleton||"boolean"==typeof e.singleton||(e.singleton=(void 0===t&&(t=Boolean(window&&document&&document.all&&!window.atob)),t));var r=a(n,e);return s(r,e),function(n){for(var t=[],c=0;c<r.length;c++){var i=r[c],u=o[i.id];u&&(u.refs--,t.push(u))}n&&s(a(n,e),e);for(var l=0;l<t.length;l++){var d=t[l];if(0===d.refs){for(var f=0;f<d.parts.length;f++)d.parts[f]();delete o[d.id]}}}}}}]);