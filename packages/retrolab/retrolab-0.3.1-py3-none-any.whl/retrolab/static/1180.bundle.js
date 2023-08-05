(self.webpackChunk_JUPYTERLAB_CORE_OUTPUT=self.webpackChunk_JUPYTERLAB_CORE_OUTPUT||[]).push([[1180,9068],{41180:(t,e,s)=>{"use strict";s.r(e),s.d(e,{YBaseCell:()=>g,YCodeCell:()=>y,YDocument:()=>i,YFile:()=>c,YMarkdownCell:()=>m,YNotebook:()=>h,YRawCell:()=>p,convertYMapEventToMapChange:()=>_,createCellFromType:()=>u,createMutex:()=>M,createStandaloneCell:()=>d});var n=s(76943),a=s(12291),r=s(90157),o=s(28306);const l=t=>JSON.parse(JSON.stringify(t));class i{constructor(){this.isDisposed=!1,this.ydoc=new o.Doc,this.source=this.ydoc.getText("source"),this.ystate=this.ydoc.getMap("state"),this.undoManager=new o.UndoManager([this.source],{trackedOrigins:new Set([this])}),this.awareness=new r.GL(this.ydoc),this._changed=new a.Signal(this)}transact(t,e=!0){this.ydoc.transact(t,e?this:null)}dispose(){this.isDisposed=!0,this.ydoc.destroy()}canUndo(){return this.undoManager.undoStack.length>0}canRedo(){return this.undoManager.redoStack.length>0}undo(){this.undoManager.undo()}redo(){this.undoManager.redo()}clearUndoHistory(){this.undoManager.clear()}get changed(){return this._changed}}class c extends i{constructor(){super(),this._modelObserver=t=>{const e={};e.sourceChange=t.changes.delta,this._changed.emit(e)},this._onStateChanged=t=>{const e=[];t.keysChanged.forEach((s=>{const n=t.changes.keys.get(s);e.push({name:s,oldValue:(null==n?void 0:n.oldValue)?n.oldValue:0,newValue:this.ystate.get(s)})})),this._changed.emit({stateChange:e})},this.ysource=this.ydoc.getText("source"),this.ysource.observe(this._modelObserver),this.ystate.observe(this._onStateChanged)}dispose(){this.ysource.unobserve(this._modelObserver),this.ystate.unobserve(this._onStateChanged)}static create(){return new c}getSource(){return this.ysource.toString()}setSource(t){this.transact((()=>{const e=this.ysource;e.delete(0,e.length),e.insert(0,t)}))}updateSource(t,e,s=""){this.transact((()=>{const n=this.ysource;n.insert(t,s),n.delete(t+s.length,e-t)}))}}class h extends i{constructor(){super(),this._onYCellsChanged=t=>{t.changes.added.forEach((t=>{const e=t.content.type;this._ycellMapping.has(e)||this._ycellMapping.set(e,u(e));const s=this._ycellMapping.get(e);s._notebook=this,s._undoManager=this.undoManager})),t.changes.deleted.forEach((t=>{const e=t.content.type,s=this._ycellMapping.get(e);s&&(s.dispose(),this._ycellMapping.delete(e))}));let e=0;const s=[];t.changes.delta.forEach((t=>{if(null!=t.insert){const n=t.insert.map((t=>this._ycellMapping.get(t)));s.push({insert:n}),this.cells.splice(e,0,...n),e+=t.insert.length}else null!=t.delete?(s.push(t),this.cells.splice(e,t.delete)):null!=t.retain&&(s.push(t),e+=t.retain)})),this._changed.emit({cellsChange:s})},this._onStateChanged=t=>{const e=[];t.keysChanged.forEach((s=>{const n=t.changes.keys.get(s);e.push({name:s,oldValue:(null==n?void 0:n.oldValue)?n.oldValue:0,newValue:this.ystate.get(s)})})),this._changed.emit({stateChange:e})},this.ycells=this.ydoc.getArray("cells"),this.ymeta=this.ydoc.getMap("meta"),this.ymodel=this.ydoc.getMap("model"),this.undoManager=new o.UndoManager([this.ycells],{trackedOrigins:new Set([this])}),this._ycellMapping=new Map,this.ycells.observe(this._onYCellsChanged),this.cells=this.ycells.toArray().map((t=>(this._ycellMapping.has(t)||this._ycellMapping.set(t,u(t)),this._ycellMapping.get(t)))),this.ystate.observe(this._onStateChanged)}get nbformat(){return this.ystate.get("nbformat")}set nbformat(t){this.transact((()=>{this.ystate.set("nbformat",t)}),!1)}get nbformat_minor(){return this.ystate.get("nbformatMinor")}set nbformat_minor(t){this.transact((()=>{this.ystate.set("nbformatMinor",t)}),!1)}dispose(){this.ycells.unobserve(this._onYCellsChanged),this.ystate.unobserve(this._onStateChanged)}getCell(t){return this.cells[t]}insertCell(t,e){this.insertCells(t,[e])}insertCells(t,e){e.forEach((t=>{this._ycellMapping.set(t.ymodel,t)})),this.transact((()=>{this.ycells.insert(t,e.map((t=>t.ymodel)))}))}moveCell(t,e){this.transact((()=>{const s=this.getCell(t).clone();this.deleteCell(t),this.insertCell(e,s)}))}deleteCell(t){this.deleteCellRange(t,t+1)}deleteCellRange(t,e){this.transact((()=>{this.ycells.delete(t,e-t)}))}getMetadata(){const t=this.ymeta.get("metadata");return t?l(t):{orig_nbformat:1}}setMetadata(t){this.ymeta.set("metadata",l(t))}updateMetadata(t){this.ymeta.set("metadata",Object.assign({},this.getMetadata(),t))}static create(){return new h}}const u=t=>{switch(t.get("cell_type")){case"code":return new y(t);case"markdown":return new m(t);case"raw":return new p(t);default:throw new Error("Found unknown cell type")}},d=(t,e)=>{switch(t){case"markdown":return m.createStandalone(e);case"code":return y.createStandalone(e);default:return p.createStandalone(e)}};class g{constructor(t){this._notebook=null,this.isStandalone=!1,this._modelObserver=t=>{const e={},s=t.find((t=>t.target===this.ymodel.get("source")));s&&(e.sourceChange=s.changes.delta);const n=t.find((t=>t.target===this.ymodel.get("outputs")));n&&(e.outputsChange=n.changes.delta);const a=t.find((t=>t.target===this.ymodel));if(a&&a.keysChanged.has("metadata")){const t=a.changes.keys.get("metadata");e.metadataChange={oldValue:(null==t?void 0:t.oldValue)?t.oldValue:void 0,newValue:this.getMetadata()}}if(a&&a.keysChanged.has("execution_count")){const t=a.changes.keys.get("execution_count");e.executionCountChange={oldValue:t.oldValue,newValue:this.ymodel.get("execution_count")}}const r=this.ymodel.get("source");a&&a.keysChanged.has("source")&&(e.sourceChange=[{delete:this._prevSourceLength},{insert:r.toString()}]),this._prevSourceLength=r.length,this._changed.emit(e)},this.isDisposed=!1,this._undoManager=null,this._changed=new a.Signal(this),this.ymodel=t;const e=t.get("source");this._prevSourceLength=e?e.length:0,this.ymodel.observeDeep(this._modelObserver)}get ysource(){return this.ymodel.get("source")}get awareness(){var t;return(null===(t=this.notebook)||void 0===t?void 0:t.awareness)||null}transact(t,e=!0){this.notebook&&e?this.notebook.transact(t):this.ymodel.doc.transact(t,this)}get undoManager(){return this.notebook?this.notebook.undoManager:this._undoManager}undo(){var t;null===(t=this.undoManager)||void 0===t||t.undo()}redo(){var t;null===(t=this.undoManager)||void 0===t||t.redo()}canUndo(){return!!this.undoManager&&this.undoManager.undoStack.length>0}canRedo(){return!!this.undoManager&&this.undoManager.redoStack.length>0}clearUndoHistory(){var t;null===(t=this.undoManager)||void 0===t||t.clear()}get notebook(){return this._notebook}static create(t=n.UUID.uuid4()){const e=new o.Map,s=new o.Text;return e.set("source",s),e.set("metadata",{}),e.set("cell_type",this.prototype.cell_type),e.set("id",t),new this(e)}static createStandalone(t){const e=this.create(t);return e.isStandalone=!0,(new o.Doc).getArray().insert(0,[e.ymodel]),e._undoManager=new o.UndoManager([e.ymodel],{trackedOrigins:new Set([e])}),e}clone(){const t=new o.Map,e=new o.Text(this.getSource());return t.set("source",e),t.set("metadata",this.getMetadata()),t.set("cell_type",this.cell_type),t.set("id",this.getId()),new(0,this.constructor)(t)}get changed(){return this._changed}dispose(){this.ymodel.unobserveDeep(this._modelObserver)}getAttachments(){return this.ymodel.get("attachments")}setAttachments(t){this.transact((()=>{null==t?this.ymodel.set("attachments",t):this.ymodel.delete("attachments")}))}getId(){return this.ymodel.get("id")}getSource(){return this.ymodel.get("source").toString()}setSource(t){const e=this.ymodel.get("source");this.transact((()=>{e.delete(0,e.length),e.insert(0,t)}))}updateSource(t,e,s=""){this.transact((()=>{const n=this.ysource;n.insert(t,s),n.delete(t+s.length,e-t)}))}get cell_type(){throw new Error("A YBaseCell must not be constructed")}getMetadata(){return l(this.ymodel.get("metadata"))}setMetadata(t){this.transact((()=>{this.ymodel.set("metadata",l(t))}))}toJSON(){return{id:this.getId(),cell_type:this.cell_type,source:this.getSource(),metadata:this.getMetadata()}}}class y extends g{get cell_type(){return"code"}get execution_count(){return this.ymodel.get("execution_count")}set execution_count(t){this.transact((()=>{this.ymodel.set("execution_count",t)}))}getOutputs(){return l(this.ymodel.get("outputs").toArray())}setOutputs(t){const e=this.ymodel.get("outputs");this.transact((()=>{e.delete(0,e.length),e.insert(0,t)}),!1)}updateOutputs(t,e,s=[]){const n=this.ymodel.get("outputs"),a=e<n.length?e-t:n.length-t;this.transact((()=>{n.delete(t,a),n.insert(t,s)}),!1)}static create(t){const e=super.create(t);return e.ymodel.set("execution_count",0),e.ymodel.set("outputs",new o.Array),e}static createStandalone(t){const e=super.createStandalone(t);return e.ymodel.set("execution_count",null),e.ymodel.set("outputs",new o.Array),e}clone(){const t=super.clone(),e=new o.Array;return e.insert(0,this.getOutputs()),t.ymodel.set("execution_count",this.execution_count),t.ymodel.set("outputs",e),t}toJSON(){return{id:this.getId(),cell_type:"code",source:this.getSource(),metadata:this.getMetadata(),outputs:this.getOutputs(),execution_count:this.execution_count}}}class p extends g{static create(t){return super.create(t)}static createStandalone(t){return super.createStandalone(t)}get cell_type(){return"raw"}toJSON(){return{id:this.getId(),cell_type:"raw",source:this.getSource(),metadata:this.getMetadata(),attachments:this.getAttachments()}}}class m extends g{static create(t){return super.create(t)}static createStandalone(t){return super.createStandalone(t)}get cell_type(){return"markdown"}toJSON(){return{id:this.getId(),cell_type:"markdown",source:this.getSource(),metadata:this.getMetadata(),attachments:this.getAttachments()}}}function _(t){let e=new Map;return t.changes.keys.forEach(((t,s)=>{e.set(s,{action:t.action,oldValue:t.oldValue,newValue:this.ymeta.get(s)})})),e}const M=()=>{let t=!0;return e=>{if(t){t=!1;try{e()}finally{t=!0}}}}},79504:(t,e,s)=>{"use strict";s.d(e,{Z$:()=>n,s7:()=>a,Dp:()=>r,$m:()=>o});const n=t=>t[t.length-1],a=(t,e)=>{for(let s=0;s<e.length;s++)t.push(e[s])},r=Array.from,o=(t,e)=>{return t.length===e.length&&(s=(t,s)=>t===e[s],t.every(s));var s}},38828:(t,e,s)=>{"use strict";s.d(e,{PP:()=>r,UV:()=>o,Hi:()=>l});var n=s(79504),a=s(36498);const r=(t,e,s=0)=>{try{for(;s<t.length;s++)t[s](...e)}finally{s<t.length&&r(t,e,s+1)}},o=(t,e)=>t===e||null!=t&&null!=e&&t.constructor===e.constructor&&(t instanceof Array&&n.$m(t,e)||"object"==typeof t&&a.$m(t,e)),l=(t,e)=>{if(null==t||null==e)return((t,e)=>t===e)(t,e);if(t.constructor!==e.constructor)return!1;if(t===e)return!0;switch(t.constructor){case ArrayBuffer:t=new Uint8Array(t),e=new Uint8Array(e);case Uint8Array:if(t.byteLength!==e.byteLength)return!1;for(let s=0;s<t.length;s++)if(t[s]!==e[s])return!1;break;case Set:if(t.size!==e.size)return!1;for(const s of t)if(!e.has(s))return!1;break;case Map:if(t.size!==e.size)return!1;for(const s of t.keys())if(!e.has(s)||!l(t.get(s),e.get(s)))return!1;break;case Object:if(a.kE(t)!==a.kE(e))return!1;for(const s in t)if(!a.l$(t,s)||!l(t[s],e[s]))return!1;break;case Array:if(t.length!==e.length)return!1;for(let s=0;s<t.length;s++)if(!l(t[s],e[s]))return!1;break;default:return!1}return!0}},11182:(t,e,s)=>{"use strict";s.d(e,{GW:()=>n,Wn:()=>a,mv:()=>r,IH:()=>o,VV:()=>l,Fp:()=>i,GR:()=>c});const n=Math.floor,a=(Math.ceil,Math.abs),r=(Math.imul,Math.round,Math.log10),o=(Math.log2,Math.log,Math.sqrt,(t,e)=>t+e),l=(t,e)=>t<e?t:e,i=(t,e)=>t>e?t:e,c=(Number.isNaN,Math.pow,Math.sign,t=>0!==t?t<0:1/t<0)},36498:(t,e,s)=>{"use strict";s.d(e,{UI:()=>a,kE:()=>r,l$:()=>o,$m:()=>l}),Object.assign;const n=Object.keys,a=(t,e)=>{const s=[];for(const n in t)s.push(e(t[n],n));return s},r=t=>n(t).length,o=(t,e)=>Object.prototype.hasOwnProperty.call(t,e),l=(t,e)=>t===e||r(t)===r(e)&&((t,e)=>{for(const s in t)if(!e(t[s],s))return!1;return!0})(t,((t,s)=>(void 0!==t||o(e,s))&&e[s]===t))},90157:(t,e,s)=>{"use strict";s.d(e,{GL:()=>c,Ag:()=>h,xq:()=>u,oy:()=>d});var n=s(76615),a=s(66962),r=s(2431),o=s(11182),l=s(12330),i=s(38828);s(28306);class c extends l.y{constructor(t){super(),this.doc=t,this.clientID=t.clientID,this.states=new Map,this.meta=new Map,this._checkInterval=setInterval((()=>{const t=r.ZG();null!==this.getLocalState()&&15e3<=t-this.meta.get(this.clientID).lastUpdated&&this.setLocalState(this.getLocalState());const e=[];this.meta.forEach(((s,n)=>{n!==this.clientID&&3e4<=t-s.lastUpdated&&this.states.has(n)&&e.push(n)})),e.length>0&&h(this,e,"timeout")}),o.GW(3e3)),t.on("destroy",(()=>{this.destroy()})),this.setLocalState({})}destroy(){this.emit("destroy",[this]),this.setLocalState(null),super.destroy(),clearInterval(this._checkInterval)}getLocalState(){return this.states.get(this.clientID)||null}setLocalState(t){const e=this.clientID,s=this.meta.get(e),n=void 0===s?0:s.clock+1,a=this.states.get(e);null===t?this.states.delete(e):this.states.set(e,t),this.meta.set(e,{clock:n,lastUpdated:r.ZG()});const o=[],l=[],c=[],h=[];null===t?h.push(e):null==a?null!=t&&o.push(e):(l.push(e),i.Hi(a,t)||c.push(e)),(o.length>0||c.length>0||h.length>0)&&this.emit("change",[{added:o,updated:c,removed:h},"local"]),this.emit("update",[{added:o,updated:l,removed:h},"local"])}setLocalStateField(t,e){const s=this.getLocalState();null!==s&&this.setLocalState({...s,[t]:e})}getStates(){return this.states}}const h=(t,e,s)=>{const n=[];for(let s=0;s<e.length;s++){const a=e[s];if(t.states.has(a)){if(t.states.delete(a),a===t.clientID){const e=t.meta.get(a);t.meta.set(a,{clock:e.clock+1,lastUpdated:r.ZG()})}n.push(a)}}n.length>0&&(t.emit("change",[{added:[],updated:[],removed:n},s]),t.emit("update",[{added:[],updated:[],removed:n},s]))},u=(t,e,s=t.states)=>{const a=e.length,r=n.Mf();n.uE(r,a);for(let o=0;o<a;o++){const a=e[o],l=s.get(a)||null,i=t.meta.get(a).clock;n.uE(r,a),n.uE(r,i),n.uw(r,JSON.stringify(l))}return n._f(r)},d=(t,e,s)=>{const n=a.l1(e),o=r.ZG(),l=[],c=[],h=[],u=[],d=a.yg(n);for(let e=0;e<d;e++){const e=a.yg(n);let s=a.yg(n);const r=JSON.parse(a.kf(n)),d=t.meta.get(e),g=t.states.get(e),y=void 0===d?0:d.clock;(y<s||y===s&&null===r&&t.states.has(e))&&(null===r?e===t.clientID&&null!=t.getLocalState()?s++:t.states.delete(e):t.states.set(e,r),t.meta.set(e,{clock:s,lastUpdated:o}),void 0===d&&null!==r?l.push(e):void 0!==d&&null===r?u.push(e):null!==r&&(i.Hi(r,g)||h.push(e),c.push(e)))}(l.length>0||h.length>0||u.length>0)&&t.emit("change",[{added:l,updated:h,removed:u},s]),(l.length>0||c.length>0||u.length>0)&&t.emit("update",[{added:l,updated:c,removed:u},s])}}}]);