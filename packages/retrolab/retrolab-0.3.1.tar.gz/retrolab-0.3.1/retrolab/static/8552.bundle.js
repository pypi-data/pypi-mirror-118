(self.webpackChunk_JUPYTERLAB_CORE_OUTPUT=self.webpackChunk_JUPYTERLAB_CORE_OUTPUT||[]).push([[8552],{78552:(t,e,o)=>{"use strict";o.r(e),o.d(e,{default:()=>i});var s=o(75581),n=o(807),r=o(76943),a=o(78429);const c={id:"@jupyterlab/shortcuts-extension:shortcuts",requires:[s.ISettingRegistry,n.ITranslator],activate:async(t,e,o)=>{const n=o.load("jupyterlab"),{commands:a}=t;let i,u={};function l(o){const s=t.commands.listCommands().join("\n");u={},o.properties.shortcuts.default=Object.keys(e.plugins).map((t=>{const o=e.plugins[t].schema["jupyter.lab.shortcuts"]||[];return u[t]=o,o})).concat([o.properties.shortcuts.default]).reduce(((t,e)=>t.concat(e)),[]).sort(((t,e)=>t.command.localeCompare(e.command))),o.properties.shortcuts.description=n.__('Note: To disable a system default shortcut,\ncopy it to User Preferences and add the\n"disabled" key, for example:\n{\n    "command": "application:activate-next-tab",\n    "keys": [\n        "Ctrl Shift ]"\n    ],\n    "selector": "body",\n    "disabled": true\n}\n\nList of commands followed by keyboard shortcuts:\n%1\n\nList of keyboard shortcuts:',s)}e.pluginChanged.connect((async(t,o)=>{if(o!==c.id){const t=u[o],s=e.plugins[o].schema["jupyter.lab.shortcuts"]||[];void 0!==t&&r.JSONExt.deepEqual(t,s)||(i=null,await e.reload(c.id))}})),e.transform(c.id,{compose:t=>{var e,o,n,a;i||(i=r.JSONExt.deepCopy(t.schema),l(i));const c=null!==(n=null===(o=null===(e=i.properties)||void 0===e?void 0:e.shortcuts)||void 0===o?void 0:o.default)&&void 0!==n?n:[],d={shortcuts:null!==(a=t.data.user.shortcuts)&&void 0!==a?a:[]},u={shortcuts:s.SettingRegistry.reconcileShortcuts(c,d.shortcuts)};return t.data={composite:u,user:d},t},fetch:t=>(i||(i=r.JSONExt.deepCopy(t.schema),l(i)),{data:t.data,id:t.id,raw:t.raw,schema:i,version:t.version})});try{i=null;const t=await e.load(c.id);d.loadShortcuts(a,t.composite),t.changed.connect((()=>{d.loadShortcuts(a,t.composite)}))}catch(t){console.error(`Loading ${c.id} failed.`,t)}},autoStart:!0},i=c;var d;!function(t){let e;t.loadShortcuts=function(t,o){var s;const n=null!==(s=null==o?void 0:o.shortcuts)&&void 0!==s?s:[];e&&e.dispose(),e=n.reduce(((e,o)=>{const s=function(t){if(!t||"object"!=typeof t)return;const{isArray:e}=Array;return"command"in t&&"keys"in t&&"selector"in t&&e(t.keys)?t:void 0}(o);return s&&e.add(t.addKeyBinding(s)),e}),new a.DisposableSet)}}(d||(d={}))}}]);