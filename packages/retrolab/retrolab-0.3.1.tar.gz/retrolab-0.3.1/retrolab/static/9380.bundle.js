(self.webpackChunk_JUPYTERLAB_CORE_OUTPUT=self.webpackChunk_JUPYTERLAB_CORE_OUTPUT||[]).push([[9380],{19380:(e,t,a)=>{"use strict";a.r(t),a.d(t,{default:()=>c});var o=a(96667),n=a(2952),l=a(14472),r=a(72245);const u=[{text:"About Jupyter",url:"https://jupyter.org"},{text:"Markdown Reference",url:"https://commonmark.org/help/"}];var s;!function(e){e.open="help:open",e.shortcuts="help:shortcuts",e.about="help:about"}(s||(s={}));const c={id:"@retrolab/help-extension:plugin",autoStart:!0,optional:[n.IMainMenu],activate:(e,t)=>{const{commands:a}=e;a.addCommand(s.open,{label:e=>e.text,execute:e=>{const t=e.url;window.open(t)}}),a.addCommand(s.shortcuts,{label:"Keyboard Shortcuts",execute:()=>{const e=r.createElement("span",{className:"jp-AboutRetro-about-header"},r.createElement("div",{className:"jp-AboutRetro-about-header-info"},"Keyboard Shortcuts")),t=r.createElement("table",{className:"jp-AboutRetro-shortcuts"},r.createElement("thead",null,r.createElement("tr",null,r.createElement("th",null,"Name"),r.createElement("th",null,"Shortcut"))),r.createElement("tbody",null,a.keyBindings.filter((e=>a.isEnabled(e.command))).map(((e,t)=>r.createElement("tr",{key:t},r.createElement("td",null,a.label(e.command)),r.createElement("td",null,r.createElement("pre",null,e.keys.join(", "))))))));return(0,o.showDialog)({title:e,body:t,buttons:[o.Dialog.createButton({label:"Dismiss",className:"jp-AboutRetro-about-button jp-mod-reject jp-mod-styled"})]})}}),a.addCommand(s.about,{label:`About ${e.name}`,execute:()=>{const t=r.createElement(r.Fragment,null,r.createElement("span",{className:"jp-AboutRetro-header"},r.createElement(l.retroIcon.react,{height:"256px",width:"auto"}))),a=r.createElement("span",null,r.createElement("a",{href:"https://github.com/jupyterlab/retrolab",target:"_blank",rel:"noopener noreferrer",className:"jp-Button-flat jp-AboutRetro-about-externalLinks"},"RETROLAB ON GITHUB")),n=r.createElement(r.Fragment,null,r.createElement("span",{className:"jp-AboutRetro-body"},"Version: ",e.version),r.createElement("div",null,a)),u=new o.Dialog({title:t,body:n,buttons:[o.Dialog.createButton({label:"Dismiss",className:"jp-AboutRetro-about-button jp-mod-reject jp-mod-styled"})]});u.addClass("jp-AboutRetro"),u.launch()}});const n=u.map((e=>({args:e,command:s.open})));t.helpMenu.addGroup([{command:s.about}]),t.helpMenu.addGroup([{command:s.shortcuts}]),t.helpMenu.addGroup(n)}}}}]);