(self.webpackChunk_JUPYTERLAB_CORE_OUTPUT=self.webpackChunk_JUPYTERLAB_CORE_OUTPUT||[]).push([[8579,3694],{3694:(e,t,n)=>{"use strict";n.r(t),n.d(t,{default:()=>k});var o=n(65579),a=n(96667),r=n(49839),i=n(79870),l=n(30084),s=n(2952),d=n(807),c=n(53190),p=n(14472),u=n(36735);const m=new RegExp("/(notebooks|edit)/(.*)");var g;!function(e){e.toggleTop="application:toggle-top",e.toggleZen="application:toggle-zen",e.openLab="application:open-lab",e.openTree="application:open-tree"}(g||(g={}));const b={id:"@retrolab/application-extension:dirty",autoStart:!0,requires:[o.ILabStatus,d.ITranslator],activate:(e,t,n)=>{if(!(e instanceof c.RetroApp))throw new Error(`${b.id} must be activated in RetroLab.`);const o=n.load("jupyterlab").__("Are you sure you want to exit RetroLab?\n\nAny unsaved changes will be lost.");window.addEventListener("beforeunload",(t=>{if(e.status.isDirty)return t.returnValue=o}))}},h={id:"@retrolab/application-extension:logo",autoStart:!0,activate:e=>{const t=r.PageConfig.getBaseUrl(),n=document.createElement("a");n.href=`${t}retro/tree`,n.target="_blank",n.rel="noopener noreferrer";const o=new u.Widget({node:n});("true"===r.PageConfig.getOption("retroLogo")?p.retroInlineIcon:p.jupyterIcon).element({container:n,elementPosition:"center",padding:"2px 2px 2px 8px",height:"28px",width:"auto"}),o.id="jp-RetroLogo",e.shell.add(o,"top",{rank:0})}},x={id:"@retrolab/application-extension:opener",autoStart:!0,requires:[o.IRouter,i.IDocumentManager],activate:(e,t,n)=>{const{commands:o}=e,a="router:tree";o.addCommand(a,{execute:t=>{var o;const a=null!==(o=t.path.match(m))&&void 0!==o?o:[],[,,i]=a;if(!i)return;const l=decodeURIComponent(i),s=r.PathExt.extname(l);e.restored.then((()=>{".ipynb"===s?n.open(l,"Notebook",void 0,{ref:"_noref"}):n.open(l,"Editor",void 0,{ref:"_noref"})}))}}),t.register({command:a,pattern:m})}},v={id:"@retrolab/application-extension:no-tabs-menu",requires:[s.IMainMenu],autoStart:!0,activate:(e,t)=>{t.tabsMenu.dispose()}},f={id:"@retrolab/application-extension:pages",autoStart:!0,optional:[a.ICommandPalette,s.IMainMenu],activate:(e,t,n)=>{const o=r.PageConfig.getBaseUrl();e.commands.addCommand(g.openLab,{label:"Open JupyterLab",execute:()=>{window.open(`${o}lab`)}}),e.commands.addCommand(g.openTree,{label:"Open Files",execute:()=>{window.open(`${o}retro/tree`)}}),t&&[g.openLab,g.openTree].forEach((e=>{t.addItem({command:e,category:"View"})})),n&&n.viewMenu.addGroup([{command:g.openLab},{command:g.openTree}],0)}},w={id:"@retrolab/application-extension:paths",autoStart:!0,provides:o.JupyterFrontEnd.IPaths,activate:e=>{if(!(e instanceof c.RetroApp))throw new Error(`${w.id} must be activated in RetroLab.`);return e.paths}},I={id:"@retrolab/application-extension:router",autoStart:!0,provides:o.IRouter,requires:[o.JupyterFrontEnd.IPaths],activate:(e,t)=>{const{commands:n}=e,a=t.urls.base,r=new o.Router({base:a,commands:n});return e.started.then((()=>{r.route(),window.addEventListener("popstate",(()=>{r.route()}))})),r}},R={id:"@retrolab/application-extension:session-dialogs",provides:a.ISessionContextDialogs,autoStart:!0,activate:()=>a.sessionContextDialogs},S={id:"@retrolab/application-extension:shell",activate:e=>{if(!(e.shell instanceof c.RetroShell))throw new Error(`${S.id} did not find a RetroShell instance.`);return e.shell},autoStart:!0,provides:c.IRetroShell},C={id:"@retrolab/application-extension:spacer",autoStart:!0,activate:e=>{const t=new u.Widget;t.id=a.DOMUtils.createDomID(),t.addClass("jp-RetroSpacer"),e.shell.add(t,"top",{rank:1e4});const n=new u.Widget;n.id=a.DOMUtils.createDomID(),n.addClass("jp-RetroSpacer"),e.shell.add(n,"menu",{rank:1e4})}},E={id:"@retrolab/application-extension:status",autoStart:!0,provides:o.ILabStatus,activate:e=>{if(!(e instanceof c.RetroApp))throw new Error(`${E.id} must be activated in RetroLab.`);return e.status}},T={id:"@retrolab/application-extension:tab-title",autoStart:!0,requires:[c.IRetroShell],activate:(e,t)=>{const n=()=>{const e=t.currentWidget;if(!(e instanceof l.DocumentWidget))return;const n=()=>{const t=r.PathExt.basename(e.context.path);document.title=t};e.context.pathChanged.connect(n),n()};t.currentChanged.connect(n),n()}},L={id:"@retrolab/application-extension:title",autoStart:!0,requires:[c.IRetroShell],optional:[i.IDocumentManager,o.IRouter],activate:(e,t,n,o)=>{const a=new u.Widget;a.id="jp-title",e.shell.add(a,"top",{rank:10});const s=async()=>{const e=t.currentWidget;if(!(e&&e instanceof l.DocumentWidget))return;if(a.node.children.length>0)return;const s=document.createElement("h1");s.textContent=e.title.label,a.node.appendChild(s),a.node.style.marginLeft="10px",n&&(a.node.onclick=async()=>{var t,a;const l=await(0,i.renameDialog)(n,e.context.path);if(e&&e.activate(),null===l)return;const d=null!==(t=e.context.path)&&void 0!==t?t:l.path,c=r.PathExt.basename(d);if(s.textContent=c,!o)return;const p=null!==(a=o.current.path.match(m))&&void 0!==a?a:[],[,u,g]=p;if(!u||!g)return;const b=encodeURIComponent(d);o.navigate(`/retro/${u}/${b}`,{skipRouting:!0})})};t.currentChanged.connect(s),s()}},M={id:"@retrolab/application-extension:top",requires:[c.IRetroShell],optional:[s.IMainMenu],activate:(e,t,n)=>{const o=t.top;e.commands.addCommand(g.toggleTop,{label:"Show Header",execute:()=>{o.setHidden(o.isVisible)},isToggled:()=>o.isVisible}),n&&n.viewMenu.addGroup([{command:g.toggleTop}],2);const a=()=>{"desktop"===e.format?t.expandTop():t.collapseTop()};e.formatChanged.connect(a),a()},autoStart:!0},y={id:"@retrolab/application-extension:translator",activate:e=>new d.TranslationManager,autoStart:!0,provides:d.ITranslator},P={id:"@retrolab/application-extension:zen",autoStart:!0,optional:[a.ICommandPalette,c.IRetroShell,s.IMainMenu],activate:(e,t,n,o)=>{const{commands:a}=e,r=document.documentElement,i=()=>{null==n||n.expandTop(),null==n||n.menu.setHidden(!1),l=!1};let l=!1;a.addCommand(g.toggleZen,{label:"Toggle Zen Mode",execute:()=>{l?(document.exitFullscreen(),i()):(r.requestFullscreen(),null==n||n.collapseTop(),null==n||n.menu.setHidden(!0),l=!0)}}),document.addEventListener("fullscreenchange",(()=>{document.fullscreenElement||i()})),t&&t.addItem({command:g.toggleZen,category:"Mode"}),o&&o.viewMenu.addGroup([{command:g.toggleZen}],3)}},k=[b,h,v,x,f,w,I,R,S,C,E,T,L,M,y,P]}}]);