var _JUPYTERLAB;(()=>{"use strict";var e,r,t,n,a,o,i,f,l,d,c,u,s,p,h,b,y,v,m={5417:(e,r,t)=>{var n={"./index":()=>Promise.all([t.e(271),t.e(456),t.e(226),t.e(886),t.e(568)]).then((()=>()=>t(1568))),"./extension":()=>Promise.all([t.e(271),t.e(456),t.e(226),t.e(886),t.e(480)]).then((()=>()=>t(4480)))},a=(e,r)=>(t.R=r,r=t.o(n,e)?n[e]():Promise.resolve().then((()=>{throw new Error('Module "'+e+'" does not exist in container.')})),t.R=void 0,r),o=(e,r)=>{if(t.S){var n=t.S.default,a="default";if(n&&n!==e)throw new Error("Container initialization failed as it has already been initialized with a different share scope");return t.S[a]=e,t.I(a,r)}};t.d(r,{get:()=>a,init:()=>o})}},g={};function x(e){var r=g[e];if(void 0!==r)return r.exports;var t=g[e]={id:e,loaded:!1,exports:{}};return m[e].call(t.exports,t,t.exports,x),t.loaded=!0,t.exports}x.m=m,x.c=g,x.n=e=>{var r=e&&e.__esModule?()=>e.default:()=>e;return x.d(r,{a:r}),r},x.d=(e,r)=>{for(var t in r)x.o(r,t)&&!x.o(e,t)&&Object.defineProperty(e,t,{enumerable:!0,get:r[t]})},x.f={},x.e=e=>Promise.all(Object.keys(x.f).reduce(((r,t)=>(x.f[t](e,r),r)),[])),x.u=e=>e+"."+{24:"b2600497b020256987ad",92:"02ad62f546a883131d85",123:"3411b80d8df4f69e811d",226:"26cbce4e8e5875f32e24",271:"74121e5b125786e300fb",433:"0f1144affa2664e4f769",456:"e98075daae73f7da5a67",480:"0e4705fcc36a9f970eab",534:"1f766f1523925f7b0a8c",568:"1520a9946baff503a701",606:"07610e057b0e528f6d90",675:"d4f15dbdbf65cd76312e",714:"f5bd9b5230e5434a3013",886:"ede72de84740a977a235",903:"70f853067ed598a65543"}[e]+".js?v="+{24:"b2600497b020256987ad",92:"02ad62f546a883131d85",123:"3411b80d8df4f69e811d",226:"26cbce4e8e5875f32e24",271:"74121e5b125786e300fb",433:"0f1144affa2664e4f769",456:"e98075daae73f7da5a67",480:"0e4705fcc36a9f970eab",534:"1f766f1523925f7b0a8c",568:"1520a9946baff503a701",606:"07610e057b0e528f6d90",675:"d4f15dbdbf65cd76312e",714:"f5bd9b5230e5434a3013",886:"ede72de84740a977a235",903:"70f853067ed598a65543"}[e],x.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"==typeof window)return window}}(),x.hmd=e=>((e=Object.create(e)).children||(e.children=[]),Object.defineProperty(e,"exports",{enumerable:!0,set:()=>{throw new Error("ES Modules may not assign module.exports or exports.*, Use ESM export syntax, instead: "+e.id)}}),e),x.o=(e,r)=>Object.prototype.hasOwnProperty.call(e,r),e={},r="@cylynx/pymotif:",x.l=(t,n,a,o)=>{if(e[t])e[t].push(n);else{var i,f;if(void 0!==a)for(var l=document.getElementsByTagName("script"),d=0;d<l.length;d++){var c=l[d];if(c.getAttribute("src")==t||c.getAttribute("data-webpack")==r+a){i=c;break}}i||(f=!0,(i=document.createElement("script")).charset="utf-8",i.timeout=120,x.nc&&i.setAttribute("nonce",x.nc),i.setAttribute("data-webpack",r+a),i.src=t),e[t]=[n];var u=(r,n)=>{i.onerror=i.onload=null,clearTimeout(s);var a=e[t];if(delete e[t],i.parentNode&&i.parentNode.removeChild(i),a&&a.forEach((e=>e(n))),r)return r(n)},s=setTimeout(u.bind(null,void 0,{type:"timeout",target:i}),12e4);i.onerror=u.bind(null,i.onerror),i.onload=u.bind(null,i.onload),f&&document.head.appendChild(i)}},x.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},(()=>{x.S={};var e={},r={};x.I=(t,n)=>{n||(n=[]);var a=r[t];if(a||(a=r[t]={}),!(n.indexOf(a)>=0)){if(n.push(a),e[t])return e[t];x.o(x.S,t)||(x.S[t]={});var o=x.S[t],i="@cylynx/pymotif",f=(e,r,t,n)=>{var a=o[e]=o[e]||{},f=a[r];(!f||!f.loaded&&(!n!=!f.eager?n:i>f.from))&&(a[r]={get:t,from:i,eager:!!n})},l=[];switch(t){case"default":f("@cylynx/motif","0.0.3",(()=>Promise.all([x.e(271),x.e(456),x.e(226),x.e(606)]).then((()=>()=>x(3606))))),f("@cylynx/pymotif","0.0.3",(()=>Promise.all([x.e(271),x.e(456),x.e(226),x.e(886),x.e(568)]).then((()=>()=>x(1568))))),f("@reduxjs/toolkit","1.6.0",(()=>x.e(675).then((()=>()=>x(3675))))),f("baseui","9.116.1",(()=>Promise.all([x.e(92),x.e(271),x.e(433)]).then((()=>()=>x(92))))),f("react-redux","7.2.4",(()=>Promise.all([x.e(714),x.e(271),x.e(456)]).then((()=>()=>x(4568))))),f("styletron-engine-atomic","1.4.8",(()=>x.e(903).then((()=>()=>x(6903))))),f("styletron-react","5.2.7",(()=>Promise.all([x.e(271),x.e(123)]).then((()=>()=>x(534)))))}return e[t]=l.length?Promise.all(l).then((()=>e[t]=1)):1}}})(),(()=>{var e;x.g.importScripts&&(e=x.g.location+"");var r=x.g.document;if(!e&&r&&(r.currentScript&&(e=r.currentScript.src),!e)){var t=r.getElementsByTagName("script");t.length&&(e=t[t.length-1].src)}if(!e)throw new Error("Automatic publicPath is not supported in this browser");e=e.replace(/#.*$/,"").replace(/\?.*$/,"").replace(/\/[^\/]+$/,"/"),x.p=e})(),t=e=>{var r=e=>e.split(".").map((e=>+e==e?+e:e)),t=/^([^-+]+)?(?:-([^+]+))?(?:\+(.+))?$/.exec(e),n=t[1]?r(t[1]):[];return t[2]&&(n.length++,n.push.apply(n,r(t[2]))),t[3]&&(n.push([]),n.push.apply(n,r(t[3]))),n},n=(e,r)=>{e=t(e),r=t(r);for(var n=0;;){if(n>=e.length)return n<r.length&&"u"!=(typeof r[n])[0];var a=e[n],o=(typeof a)[0];if(n>=r.length)return"u"==o;var i=r[n],f=(typeof i)[0];if(o!=f)return"o"==o&&"n"==f||"s"==f||"u"==o;if("o"!=o&&"u"!=o&&a!=i)return a<i;n++}},a=e=>{var r=e[0],t="";if(1===e.length)return"*";if(r+.5){t+=0==r?">=":-1==r?"<":1==r?"^":2==r?"~":r>0?"=":"!=";for(var n=1,o=1;o<e.length;o++)n--,t+="u"==(typeof(f=e[o]))[0]?"-":(n>0?".":"")+(n=2,f);return t}var i=[];for(o=1;o<e.length;o++){var f=e[o];i.push(0===f?"not("+l()+")":1===f?"("+l()+" || "+l()+")":2===f?i.pop()+" "+i.pop():a(f))}return l();function l(){return i.pop().replace(/^\((.+)\)$/,"$1")}},o=(e,r)=>{if(0 in e){r=t(r);var n=e[0],a=n<0;a&&(n=-n-1);for(var i=0,f=1,l=!0;;f++,i++){var d,c,u=f<e.length?(typeof e[f])[0]:"";if(i>=r.length||"o"==(c=(typeof(d=r[i]))[0]))return!l||("u"==u?f>n&&!a:""==u!=a);if("u"==c){if(!l||"u"!=u)return!1}else if(l)if(u==c)if(f<=n){if(d!=e[f])return!1}else{if(a?d>e[f]:d<e[f])return!1;d!=e[f]&&(l=!1)}else if("s"!=u&&"n"!=u){if(a||f<=n)return!1;l=!1,f--}else{if(f<=n||c<u!=a)return!1;l=!1}else"s"!=u&&"n"!=u&&(l=!1,f--)}}var s=[],p=s.pop.bind(s);for(i=1;i<e.length;i++){var h=e[i];s.push(1==h?p()|p():2==h?p()&p():h?o(h,r):!p())}return!!p()},i=(e,r)=>{var t=x.S[e];if(!t||!x.o(t,r))throw new Error("Shared module "+r+" doesn't exist in shared scope "+e);return t},f=(e,r)=>{var t=e[r];return Object.keys(t).reduce(((e,r)=>!e||!t[e].loaded&&n(e,r)?r:e),0)},l=(e,r,t)=>"Unsatisfied version "+r+" of shared singleton module "+e+" (required "+a(t)+")",d=(e,r,t,n)=>{var a=f(e,t);return o(n,a)||"undefined"!=typeof console&&console.warn&&console.warn(l(t,a,n)),u(e[t][a])},c=(e,r,t)=>{var a=e[r];return(r=Object.keys(a).reduce(((e,r)=>!o(t,r)||e&&!n(e,r)?e:r),0))&&a[r]},u=e=>(e.loaded=1,e.get()),p=(s=e=>function(r,t,n,a){var o=x.I(r);return o&&o.then?o.then(e.bind(e,r,x.S[r],t,n,a)):e(r,x.S[r],t,n,a)})(((e,r,t,n)=>(i(e,t),d(r,0,t,n)))),h=s(((e,r,t,n,a)=>{var o=r&&x.o(r,t)&&c(r,t,n);return o?u(o):a()})),b={},y={6271:()=>p("default","react",[1,17,0,1]),4456:()=>p("default","react-dom",[1,17,0,1]),2226:()=>h("default","styletron-react",[1,5,2,7],(()=>x.e(24).then((()=>()=>x(534))))),2565:()=>p("default","@jupyter-widgets/base",[,[1,4,0,0],[1,3,0,0],[1,2,0,0],[1,1,1,10],1,1,1]),4004:()=>h("default","baseui",[1,9,90,0],(()=>Promise.all([x.e(92),x.e(433)]).then((()=>()=>x(92))))),4553:()=>h("default","@cylynx/motif",[3,0,0,1],(()=>x.e(606).then((()=>()=>x(3606))))),5878:()=>h("default","@reduxjs/toolkit",[1,1,2,3],(()=>x.e(675).then((()=>()=>x(3675))))),5907:()=>h("default","react-redux",[1,7,2,3],(()=>x.e(714).then((()=>()=>x(4568))))),6170:()=>h("default","styletron-engine-atomic",[1,1,4,5],(()=>x.e(903).then((()=>()=>x(6903))))),6471:()=>h("default","@reduxjs/toolkit",[1,1,5,0],(()=>x.e(675).then((()=>()=>x(3675))))),8557:()=>h("default","react-redux",[1,7,1,3],(()=>x.e(714).then((()=>()=>x(4568))))),3433:()=>h("default","styletron-react",[,[1,7],[-1],[0,5,2,2],2,2],(()=>x.e(534).then((()=>()=>x(534)))))},v={226:[2226],271:[6271],433:[3433],456:[4456],606:[6471,8557],886:[2565,4004,4553,5878,5907,6170]},x.f.consumes=(e,r)=>{x.o(v,e)&&v[e].forEach((e=>{if(x.o(b,e))return r.push(b[e]);var t=r=>{b[e]=0,x.m[e]=t=>{delete x.c[e],t.exports=r()}},n=r=>{delete b[e],x.m[e]=t=>{throw delete x.c[e],r}};try{var a=y[e]();a.then?r.push(b[e]=a.then(t).catch(n)):t(a)}catch(e){n(e)}}))},(()=>{var e={772:0};x.f.j=(r,t)=>{var n=x.o(e,r)?e[r]:void 0;if(0!==n)if(n)t.push(n[2]);else if(/^(226|271|433|456)$/.test(r))e[r]=0;else{var a=new Promise(((t,a)=>n=e[r]=[t,a]));t.push(n[2]=a);var o=x.p+x.u(r),i=new Error;x.l(o,(t=>{if(x.o(e,r)&&(0!==(n=e[r])&&(e[r]=void 0),n)){var a=t&&("load"===t.type?"missing":t.type),o=t&&t.target&&t.target.src;i.message="Loading chunk "+r+" failed.\n("+a+": "+o+")",i.name="ChunkLoadError",i.type=a,i.request=o,n[1](i)}}),"chunk-"+r,r)}};var r=(r,t)=>{var n,a,[o,i,f]=t,l=0;for(n in i)x.o(i,n)&&(x.m[n]=i[n]);for(f&&f(x),r&&r(t);l<o.length;l++)a=o[l],x.o(e,a)&&e[a]&&e[a][0](),e[o[l]]=0},t=self.webpackChunk_cylynx_pymotif=self.webpackChunk_cylynx_pymotif||[];t.forEach(r.bind(null,0)),t.push=r.bind(null,t.push.bind(t))})();var w=x(5417);(_JUPYTERLAB=void 0===_JUPYTERLAB?{}:_JUPYTERLAB)["@cylynx/pymotif"]=w})();