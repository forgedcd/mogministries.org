/* Public Shopify photos. Back/color associations were visually checked against the real mockups. */
(()=>{
 'use strict';
 const $=s=>document.querySelector(s);
 const node=(tag,text,cls)=>{const n=document.createElement(tag);if(text)n.textContent=text;if(cls)n.className=cls;return n};
 const BACKS={
  '54024933343383':'Black','54024938029207':'Black','54024938913943':'Black',
  '54024939896983':'Light Gray','54024939962519':'Flower Gray',
  '54024942092439':'Black','54024942157975':'Deep Teal','54024942223511':'Pink',
  '54024942813335':'Black with Gray','54024942878871':'White with Navy Blue',
  '54024942944407':'Light Blue with White','54024943894679':'Black','54024945205399':'Black'
 };
 const image=$('#dialog-image'),stage=image.parentElement,media=node('div',null,'dialog-media');
 stage.replaceWith(media);media.append(stage);
 const controls=node('div',null,'gallery-controls'),previous=node('button','←'),next=node('button','→');
 previous.type=next.type='button';previous.setAttribute('aria-label','Previous product photo');next.setAttribute('aria-label','Next product photo');
 const caption=node('span',null,'gallery-caption');caption.setAttribute('aria-live','polite');
 controls.append(previous,caption,next);
 const thumbs=node('div',null,'gallery-thumbs');thumbs.setAttribute('role','group');thumbs.setAttribute('aria-label','Product photos');
 const note=node('p',null,'gallery-note');
 media.append(controls,thumbs,note);
 let photos=[],index=0,title='';
 function show(i){
  if(!photos.length)return;
  index=(i+photos.length)%photos.length;
  const photo=photos[index],label=[photo.side,photo.color].filter(Boolean).join(' · ');
  image.src=photo.url;image.alt=`${title} · ${label}`;
  caption.textContent=`${label} · ${index+1} / ${photos.length}`;
  [...thumbs.children].forEach((b,n)=>b.setAttribute('aria-pressed',String(n===index)));
  previous.disabled=next.disabled=photos.length<2;
 }
 previous.onclick=()=>show(index-1);next.onclick=()=>show(index+1);
 thumbs.addEventListener('keydown',e=>{
  if(e.key!=='ArrowLeft'&&e.key!=='ArrowRight')return;
  const focused=[...thumbs.children].indexOf(e.target.closest('button'));
  e.preventDefault();show((focused<0?index:focused)+(e.key==='ArrowRight'?1:-1));thumbs.children[index]?.focus();
 });
 let pointer=null;
 stage.addEventListener('pointerdown',e=>{pointer={x:e.clientX,y:e.clientY}});
 stage.addEventListener('pointerup',e=>{
  if(!pointer)return;
  const dx=e.clientX-pointer.x,dy=e.clientY-pointer.y;pointer=null;
  if(Math.abs(dx)>45&&Math.abs(dx)>Math.abs(dy)*1.5)show(index+(dx<0?1:-1));
 });
 stage.addEventListener('pointercancel',()=>{pointer=null});
 function set(items,preferred,productTitle){
  photos=items;title=productTitle;thumbs.replaceChildren();
  for(const [n,photo] of photos.entries()){
   const label=[photo.side,photo.color].filter(Boolean).join(' · '),button=node('button',null,'gallery-thumb');
   button.type='button';button.setAttribute('aria-label',`View ${label}`);
   const thumb=node('img');let thumbnail=photo.url;
   if(photo.url.startsWith('https://cdn.shopify.com/')){
    const url=new URL(photo.url);url.searchParams.set('width','160');thumbnail=url.href;
   }
   thumb.src=thumbnail;thumb.alt='';thumb.width=68;thumb.height=68;thumb.loading='lazy';
   button.append(thumb,node('span',photo.side));button.onclick=()=>show(n);thumbs.append(button);
  }
  thumbs.hidden=photos.length<2;
  note.textContent=photos.length===1?'Only one photo is currently available for this selection.':'View each angle using the thumbnails or arrows.';
  note.hidden=!photos.length;
  controls.hidden=!photos.length;
  show(Math.max(0,photos.findIndex(p=>p.url===preferred)));
 }
 window.MOGGallery={
  reset(snapshot){
   photos=[];index=0;thumbs.replaceChildren();thumbs.hidden=controls.hidden=note.hidden=true;
   image.src=snapshot.image;image.alt=snapshot.title;
  },
  forProduct(product,snapshot,variants){
   const frontColors=new Map();
   for(const v of product.variants.nodes){
    if(v.image?.id)frontColors.set(v.image.id,v.selectedOptions.find(o=>/colou?r/i.test(o.name))?.value||'');
   }
   const all=(product.images?.nodes||[]).map((p,i)=>{
    const back=BACKS[p.id?.split('/').pop()];
    const color=back||frontColors.get(p.id)||'';
    return {...p,color,side:back?'Back':frontColors.has(p.id)?'Front':/\bback\b/i.test(p.altText||'')?'Back':`Photo ${i+1}`};
   }).filter(p=>!(snapshot.handle==='mog-golf-polo'&&p.color==='White with Navy Blue'));
   let lastColor=null;
   return (color,preferred)=>{
    if(lastColor===color)return; // A size change must not reset the chosen back view.
    lastColor=color;
    const filtered=all.filter(p=>!color||!p.color||p.color===color);
    const fallback=variants.find(v=>v.image?.url&&(!color||v.selectedOptions.some(o=>/colou?r/i.test(o.name)&&o.value===color)))?.image;
    set(filtered.length?filtered:[{url:fallback?.url||snapshot.image,side:'Product photo',color}],preferred,product.title);
   };
  }
 };
})();
