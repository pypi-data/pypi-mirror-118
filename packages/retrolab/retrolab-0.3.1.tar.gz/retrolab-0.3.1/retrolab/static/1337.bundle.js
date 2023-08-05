(self.webpackChunk_JUPYTERLAB_CORE_OUTPUT=self.webpackChunk_JUPYTERLAB_CORE_OUTPUT||[]).push([[1337,1809],{1809:(n,e,t)=>{"use strict";t.r(e),t.d(e,{IRunningSessionManagers:()=>u,RunningSessionManagers:()=>m,RunningSessions:()=>b});var a=t(96667),s=t(807),l=t(48423),r=t(76943),o=t(78429),i=t(72245);const u=new r.Token("@jupyterlab/running:IRunningSessionManagers");class m{constructor(){this._managers=[]}add(n){return this._managers.push(n),new o.DisposableDelegate((()=>{const e=this._managers.indexOf(n);e>-1&&this._managers.splice(e,1)}))}items(){return this._managers}}function c(n){var e;const{runningItem:t}=n,r=t.icon(),o=null===(e=t.detail)||void 0===e?void 0:e.call(t),u=(n.translator||s.nullTranslator).load("jupyterlab"),m=n.shutdownLabel||u.__("Shut Down"),c=n.shutdownItemIcon||l.closeIcon;return i.createElement("li",{className:"jp-RunningSessions-item"},i.createElement(r.react,{tag:"span",stylesheet:"runningItem"}),i.createElement("span",{className:"jp-RunningSessions-itemLabel",title:t.labelTitle?t.labelTitle():"",onClick:()=>t.open()},t.label()),o&&i.createElement("span",{className:"jp-RunningSessions-itemDetail"},o),i.createElement(a.ToolbarButtonComponent,{className:"jp-RunningSessions-itemShutdown",icon:c,onClick:()=>t.shutdown(),tooltip:m}))}function g(n){return i.createElement("ul",{className:"jp-RunningSessions-sectionList"},n.runningItems.map(((e,t)=>i.createElement(c,{key:t,runningItem:e,shutdownLabel:n.shutdownLabel,shutdownItemIcon:n.shutdownItemIcon,translator:n.translator}))))}function d(n){return i.createElement(a.UseSignal,{signal:n.manager.runningChanged},(()=>i.createElement(g,{runningItems:n.manager.running(),shutdownLabel:n.shutdownLabel,shutdownAllLabel:n.shutdownAllLabel,shutdownItemIcon:n.manager.shutdownItemIcon,translator:n.translator})))}function h(n){const e=(n.translator||s.nullTranslator).load("jupyterlab"),t=n.manager.shutdownAllLabel||e.__("Shut Down All"),l=`${t}?`,r=n.manager.shutdownAllConfirmationText||`${t} ${n.manager.name}`;function o(){(0,a.showDialog)({title:l,body:r,buttons:[a.Dialog.cancelButton({label:e.__("Cancel")}),a.Dialog.warnButton({label:t})]}).then((e=>{e.button.accept&&n.manager.shutdownAll()}))}return i.createElement("div",{className:"jp-RunningSessions-section"},i.createElement(i.Fragment,null,i.createElement("div",{className:"jp-RunningSessions-sectionHeader jp-stack-panel-header"},i.createElement("h2",null,n.manager.name),i.createElement(a.UseSignal,{signal:n.manager.runningChanged},(()=>{const e=0===n.manager.running().length;return i.createElement("button",{className:`jp-RunningSessions-shutdownAll jp-mod-styled ${e&&"jp-mod-disabled"}`,disabled:e,onClick:o},t)}))),i.createElement("div",{className:"jp-RunningSessions-sectionContainer"},i.createElement(d,{manager:n.manager,shutdownLabel:n.manager.shutdownLabel,shutdownAllLabel:t,translator:n.translator}))))}function p(n){const e=(n.translator||s.nullTranslator).load("jupyterlab");return i.createElement(i.Fragment,null,i.createElement("div",{className:"jp-RunningSessions-header"},i.createElement(a.ToolbarButtonComponent,{tooltip:e.__("Refresh List"),icon:l.refreshIcon,onClick:()=>n.managers.items().forEach((n=>n.refreshRunning()))})),n.managers.items().map((e=>i.createElement(h,{key:e.name,manager:e,translator:n.translator}))))}class b extends a.ReactWidget{constructor(n,e){super(),this.managers=n,this.translator=e||s.nullTranslator,this.addClass("jp-RunningSessions")}render(){return i.createElement(p,{managers:this.managers,translator:this.translator})}}}}]);