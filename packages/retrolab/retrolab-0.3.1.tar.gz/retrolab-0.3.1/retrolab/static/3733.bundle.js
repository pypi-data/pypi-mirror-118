(self.webpackChunk_JUPYTERLAB_CORE_OUTPUT=self.webpackChunk_JUPYTERLAB_CORE_OUTPUT||[]).push([[3733],{13733:(e,t,r)=>{"use strict";r.r(t),r.d(t,{AttachedProperty:()=>a});var i,a=function(){function e(e){this._pid=i.nextPID(),this.name=e.name,this._create=e.create,this._coerce=e.coerce||null,this._compare=e.compare||null,this._changed=e.changed||null}return e.prototype.get=function(e){var t=i.ensureMap(e);return this._pid in t?t[this._pid]:t[this._pid]=this._createValue(e)},e.prototype.set=function(e,t){var r,a=i.ensureMap(e);r=this._pid in a?a[this._pid]:a[this._pid]=this._createValue(e);var n=this._coerceValue(e,t);this._maybeNotify(e,r,a[this._pid]=n)},e.prototype.coerce=function(e){var t,r=i.ensureMap(e);t=this._pid in r?r[this._pid]:r[this._pid]=this._createValue(e);var a=this._coerceValue(e,t);this._maybeNotify(e,t,r[this._pid]=a)},e.prototype._createValue=function(e){return(0,this._create)(e)},e.prototype._coerceValue=function(e,t){var r=this._coerce;return r?r(e,t):t},e.prototype._compareValue=function(e,t){var r=this._compare;return r?r(e,t):e===t},e.prototype._maybeNotify=function(e,t,r){var i=this._changed;i&&!this._compareValue(t,r)&&i(e,t,r)},e}();!function(e){e.clearData=function(e){i.ownerData.delete(e)}}(a||(a={})),function(e){var t;e.ownerData=new WeakMap,e.nextPID=(t=0,function(){return"pid-"+(""+Math.random()).slice(2)+"-"+t++}),e.ensureMap=function(t){var r=e.ownerData.get(t);return r||(r=Object.create(null),e.ownerData.set(t,r),r)}}(i||(i={}))}}]);