(self.webpackChunk_JUPYTERLAB_CORE_OUTPUT=self.webpackChunk_JUPYTERLAB_CORE_OUTPUT||[]).push([[8875,1650],{71650:(e,t,n)=>{"use strict";n.r(t),n.d(t,{default:()=>a});var o=n(49839);const a=[{id:"@retrolab/docmanager-extension:opener",requires:[n(79870).IDocumentManager],autoStart:!0,activate:(e,t)=>{const n=o.PageConfig.getBaseUrl(),a=t.open;t.open=(e,r="default",i,s)=>{if("_noref"===(null==s?void 0:s.ref))return void a.call(t,e,r,i,s);const u=".ipynb"===o.PathExt.extname(e)?"notebooks":"edit";window.open(`${n}retro/${u}/${e}`)}}}]}}]);