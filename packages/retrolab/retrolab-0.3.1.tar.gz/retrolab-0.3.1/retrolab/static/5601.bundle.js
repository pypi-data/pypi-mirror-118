(self.webpackChunk_JUPYTERLAB_CORE_OUTPUT=self.webpackChunk_JUPYTERLAB_CORE_OUTPUT||[]).push([[5601,1684],{95601:(e,t,n)=>{"use strict";n.r(t),n.d(t,{default:()=>s});var r=n(65579),a=n(49839),i=n(47721),o=n(24318);const s=[{id:"@retrolab/terminal-extension:opener",requires:[r.IRouter],autoStart:!0,activate:(e,t)=>{const{commands:n}=e,r=new RegExp("/terminals/(.*)"),a="router:terminal";n.addCommand(a,{execute:e=>{const t=e.path.match(r);if(!t)return;const[,a]=t;a&&n.execute("terminal:open",{name:a})}}),t.register({command:a,pattern:r})}},{id:"@retrolab/terminal-extension:redirect",requires:[i.ITerminalTracker],autoStart:!0,activate:(e,t)=>{const n=a.PageConfig.getBaseUrl();t.widgetAdded.connect(((t,r)=>{if((0,o.find)(e.shell.widgets("main"),(e=>e.id===r.id)))return;const a=r.content.session.name;window.open(`${n}retro/terminals/${a}`,"_blank"),r.dispose()}))}}]}}]);