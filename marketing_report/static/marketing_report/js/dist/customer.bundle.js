(()=>{"use strict";const e=document.querySelector(".report-button"),t=document.querySelector(".btn-export"),o=document.querySelector(".current-date"),c=document.querySelector(".years"),r=document.querySelector(".cust__content"),n=document.querySelector(".dict-block__form-input");async function a(e,t,r){let n=e.dataset.last;n||(n=0);const a=document.querySelector(".cust__content");let l;delete e.dataset.last;const s=a.querySelector(".dict-block__row_hidden"),d=`/marketing/customers_current/${o.value}/${c.value}/${t}/${r}`,i=await function(e){return fetch(e).then((e=>e.json()))}(d);let f=0;const y=[];for(const e of i)f++,l=s.cloneNode(!0),u(e,l),l.classList.remove("dict-block__row_hidden"),50===f&&(l.dataset.last=Number.parseInt(n)+50),a.appendChild(l),y.push(l);return y}function u(e,t){const o=t.querySelectorAll('div[data-field]:not([data-field = ""])');for(const t of o){const o=t.dataset.field;t.textContent=e[o]}}e.addEventListener("click",(async e=>{e.preventDefault();const t=document.querySelector("#customer-0");r.querySelectorAll(".cust__row").forEach((e=>{e.classList.contains("dict-block__row_hidden")||e.remove()})),await a(t,"default",0)})),r.addEventListener("mouseover",(async e=>{const t=r.querySelector('div[data-last]:not([data-last = ""])');if(t){const o=t.dataset.last;if(e.target===t){let e=function(){let e="";return n&&(e=n.value.replace(" ","_")),""===e&&(e="default"),e}();e||(e=""),await a(t,e,o)}}})),t.addEventListener("click",(()=>function(){const e=document.querySelector("#export-form");e.querySelector("#years").value=c.value,e.querySelector("#date").value=o.value,e.submit()}()))})();