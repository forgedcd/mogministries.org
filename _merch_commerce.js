/* MOG's Shopify storefront and cart. No Admin API credentials or customer payment data. */
(()=>{
 'use strict';
 const SHOP='wvw0rw-p5.myshopify.com',API=`https://${SHOP}/api/2026-10/graphql.json`;
 const qs=s=>document.querySelector(s), money=(n,c='USD')=>new Intl.NumberFormat('en-US',{style:'currency',currency:c}).format(Number(n));
 const el=(tag,text,cls)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=text;if(cls)n.className=cls;return n};
 const status=qs('#product-status'),cartStatus=qs('#cart-status'),purchase=qs('#product-purchase'),dialog=qs('#product-dialog'),cartDialog=qs('#cart-dialog'),cartContent=qs('#cart-content');
 const CART_FIELDS=`id totalQuantity checkoutUrl cost { subtotalAmount { amount currencyCode } } lines(first:100) { nodes { id quantity cost { totalAmount { amount currencyCode } } merchandise { ... on ProductVariant { id title availableForSale product { handle title } image { url altText } price { amount currencyCode } } } } pageInfo { hasNextPage } }`;
 const PRODUCT_QUERY=`query Product($handle:String!) { product(handle:$handle) { id title description availableForSale options { name values } variants(first:100) { nodes { id title availableForSale selectedOptions {name value} image {url altText} price {amount currencyCode} } pageInfo {hasNextPage} } } }`;
 let cart=null,cartId=null,cartBusy=false,productRequest=0,activeProduct=null,activeSnapshot=null,openFrom=null,cartFrom=null;
 // Store only the cart reference, never customer or payment information.
 const CART_KEY='mog-shopify-cart-v1',CART_AGE=7*24*60*60*1000;
 let cartStorageAvailable=true;
 try{
  const saved=JSON.parse(localStorage.getItem(CART_KEY)||'null');
  if(saved&&typeof saved.id==='string'&&saved.id.startsWith('gid://shopify/Cart/')&&Number.isFinite(saved.savedAt)&&Date.now()-saved.savedAt<CART_AGE)cartId=saved.id;
  else localStorage.removeItem(CART_KEY);
 }catch{cartStorageAvailable=false}
 function storeCartId(id){
  cartId=id;
  try{
   if(id)localStorage.setItem(CART_KEY,JSON.stringify({id,savedAt:Date.now()}));
   else localStorage.removeItem(CART_KEY);
   cartStorageAvailable=true;
  }catch{cartStorageAvailable=false}
 }
 function renderDescription(handle){
  const description=qs('#dialog-description');
  const fitNotes={
   'mog-golf-polo':'Runs small. Size up one size: if you normally wear an L, order an XL.',
   'mog-golf-jersey':'This jersey has a cropped cut. Keep the shorter length in mind when ordering.'
  };
  description.replaceChildren();
  if(fitNotes[handle]){
   const note=el('span',undefined,'fit-note');
   note.append(el('strong','Fit note: '),document.createTextNode(fitNotes[handle]));
   description.append(note);
  }
  description.append(document.createTextNode("Thank you for supporting the ministry and the mission. More anointed? Ask the Holy Spirit. More of a savage animal for the Kingdom? That's the look."));
 }
 async function gql(query,variables={}){
  let response,data;
  try{
   response=await fetch(API,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({query,variables}),signal:AbortSignal.timeout(15000)});
   if(!response.ok)throw Error();
   data=await response.json();
  }catch{throw Error('Shopify could not be reached. Your card has not been charged. Please try again.')}
  if(data.errors?.length||!data.data)throw Error('The store could not complete that request. Please try again.');
  return data.data;
 }
 function acceptCart(value){
  if(value?.lines?.pageInfo?.hasNextPage)throw Error('This cart has too many items for this page. Please contact MOG for help.');
  cart=value;storeCartId(value?.id||null);qs('#cart-count').textContent=String(value?.totalQuantity||0);
  return value;
 }
 function selectedLines(){return cart?.lines?.nodes||[]}
 async function refreshCart(){
  if(!cartId)return acceptCart(null);
  const data=await gql(`query Cart($id:ID!){cart(id:$id){${CART_FIELDS}}}`,{id:cartId});
  return acceptCart(data.cart);
 }
 async function mutation(name,decl,args,variables){
  const data=await gql(`mutation ${name}(${decl}) { ${name}(${args}) { cart {${CART_FIELDS}} userErrors {message} warnings {message} } }`,variables);
  const result=data[name];
  if(result.userErrors?.length)throw Error(result.userErrors.map(e=>e.message).join(' '));
  if(!result.cart)throw Error('Your cart could not be updated. Please try again.');
  acceptCart(result.cart);
  return result.warnings?.map(w=>w.message).join(' ')||'';
 }
 function openModal(which,from){
  if(which===dialog){openFrom=from;cartDialog.close()}else{cartFrom=from;dialog.close()}
  which.showModal();document.body.style.overflow='hidden';
 }
 for(const modal of [dialog,cartDialog]){
  modal.querySelector('.dialog-close').addEventListener('click',()=>modal.close());
  modal.addEventListener('close',()=>{
   if(!dialog.open&&!cartDialog.open)document.body.style.overflow='';
   const from=modal===dialog?openFrom:cartFrom;
   if(from?.isConnected)from.focus();
  });
  modal.addEventListener('click',e=>{if(e.target===modal){const r=modal.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)modal.close()}});
  modal.addEventListener('keydown',e=>{
   if(e.key!=='Tab')return;
   const focusable=[...modal.querySelectorAll('button:not(:disabled),select:not(:disabled),input:not(:disabled),a[href]')].filter(x=>x.getClientRects().length);
   const first=focusable[0],last=focusable.at(-1);
   if(e.shiftKey&&document.activeElement===first){e.preventDefault();last?.focus()}
   else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first?.focus()}
  });
 }
 async function showProduct(handle,from){
  const snapshot=window.MOGCatalog.products.find(p=>p.handle===handle);if(!snapshot)return;
  activeSnapshot=snapshot;activeProduct=null;
  const ticket=++productRequest;
  qs('#dialog-title').textContent=snapshot.title;qs('#dialog-category').textContent=`MOG / ${snapshot.category}`;
  qs('#dialog-price').textContent='Checking price…';renderDescription(handle);
  const image=qs('#dialog-image');image.src=snapshot.image;image.alt=snapshot.title;
  purchase.replaceChildren();status.textContent='Checking live options and availability…';
  openModal(dialog,from);
  try{
   const {product}=await gql(PRODUCT_QUERY,{handle});
   if(ticket!==productRequest||!dialog.open)return;
   if(!product)throw Error('This product is not currently available to purchase.');
   if(product.variants.pageInfo.hasNextPage)throw Error('This product has more options than this page supports. Please contact MOG for help.');
   activeProduct=product;qs('#dialog-title').textContent=product.title;
   renderOptions(product,snapshot);
  }catch(e){
   if(ticket!==productRequest||!dialog.open)return;
   status.textContent=e.message;qs('#dialog-price').textContent='Live price unavailable';
   const retry=el('button','Try again','btn outline retry-product');retry.onclick=()=>showProduct(handle,from);purchase.replaceChildren(retry);
  }
 }
 function renderOptions(product,snapshot){
  // Merch-page merchandising only; Shopify's underlying variants are not deleted.
  const variants=product.variants.nodes.filter(v=>!(
   snapshot.handle==='mog-golf-polo'&&v.selectedOptions.some(o=>/colou?r/i.test(o.name)&&o.value==='White with Navy Blue')
  ));
  if(!variants.length||!product.availableForSale){
   purchase.replaceChildren();status.textContent='This product is currently sold out.';qs('#dialog-price').textContent='Unavailable';return;
  }
  const form=el('form',undefined,'purchase-form'),selects=[];
  for(const option of product.options){
   const values=[...new Set(variants.flatMap(v=>v.selectedOptions.filter(o=>o.name===option.name).map(o=>o.value)))];
   const label=el('label',option.name),select=el('select');select.name=option.name;select.setAttribute('aria-label',option.name);
   if(values.length>1){const placeholder=el('option',`Choose ${option.name.toLowerCase()}`);placeholder.value='';select.append(placeholder)}
   for(const value of values){const o=el('option',value);o.value=value;select.append(o)}
   if(values.length===1)select.disabled=true;
   label.append(select);form.append(label);selects.push(select);
  }
  const qtyLabel=el('label','Quantity','quantity-field'),qty=el('input');qty.type='number';qty.min='1';qty.max='20';qty.step='1';qty.value='1';qty.required=true;qty.setAttribute('aria-label','Product quantity');qtyLabel.append(qty);form.append(qtyLabel);
  const add=el('button','Choose your options','btn gold');add.type='submit';add.disabled=true;form.append(add);purchase.replaceChildren(form);
  function selection(){return variants.find(v=>selects.every(s=>s.value&&v.selectedOptions.some(o=>o.name===s.name&&o.value===s.value)))}
  function update(){
   const variant=selection();
   const allChosen=selects.every(s=>s.value);
   const canBuy=variant?.availableForSale&&!cartBusy;
   add.disabled=!canBuy;add.textContent=canBuy?'Add to cart':allChosen?'Unavailable in this option':'Choose your options';
   status.textContent=allChosen&&!variant?.availableForSale?'This combination is unavailable. Please choose another.':'';
   const color=selects.find(s=>/colou?r/i.test(s.name));
   const sameColorImage=color?.value?variants.find(v=>v.image?.url&&v.selectedOptions.some(o=>o.name===color.name&&o.value===color.value)):null;
   const visualVariant=variant?.image?.url?variant:sameColorImage;
   if(visualVariant){
    qs('#dialog-image').src=visualVariant.image.url;
    qs('#dialog-image').alt=visualVariant.image.altText||`${product.title}${color?.value?` in ${color.value}`:''}`;
   }else{
    qs('#dialog-image').src=snapshot.image;qs('#dialog-image').alt=`${product.title} general product image`;
    if(color?.value&&!sameColorImage)status.textContent=allChosen&&!variant?.availableForSale?'This combination is unavailable. Please choose another.':'A separate mockup is not available for this color. The selected option is shown below.';
   }
   if(variant){
    qs('#dialog-price').textContent=`${money(variant.price.amount,variant.price.currencyCode)} ${variant.price.currencyCode}`;
   }else{
    const min=variants.reduce((a,b)=>Number(a.price.amount)<Number(b.price.amount)?a:b);
    qs('#dialog-price').textContent=`From ${money(min.price.amount,min.price.currencyCode)} ${min.price.currencyCode}`;
   }
  }
  selects.forEach(s=>s.addEventListener('change',update));update();
  form.addEventListener('submit',async e=>{
   e.preventDefault();if(cartBusy)return;
   const variant=selection(),quantity=Number(qty.value);
   if(!variant?.availableForSale||!Number.isInteger(quantity)||quantity<1||quantity>20){status.textContent='Choose an available option and a quantity from 1 to 20.';return}
   cartBusy=true;add.disabled=true;add.textContent='Adding…';status.textContent='';let addError='';
   try{
    if(cartId)await refreshCart();
    const current=selectedLines().find(l=>l.merchandise.id===variant.id);
    if((current?.quantity||0)+quantity>20)throw Error('A maximum of 20 per option can be added.');
    if(!current&&selectedLines().length>=30)throw Error('A maximum of 30 different options can be added.');
    let warning;
    if(!cartId)warning=await mutation('cartCreate','$input:CartInput','input:$input',{input:{lines:[{merchandiseId:variant.id,quantity}]}});
    else warning=await mutation('cartLinesAdd','$cartId:ID!,$lines:[CartLineInput!]!','cartId:$cartId,lines:$lines',{cartId,lines:[{merchandiseId:variant.id,quantity}]});
    const line=selectedLines().find(l=>l.merchandise.id===variant.id);
    if(!line||line.quantity!==(current?.quantity||0)+quantity)warning=warning||'Shopify adjusted the quantity to available stock. Please review your cart.';
    openModal(cartDialog,qs('.cart-trigger'));renderCart(warning);
   }catch(e){addError=e.message;status.textContent=addError}
   finally{cartBusy=false;if(dialog.open){update();if(addError)status.textContent=addError}setCartBusy(false)}
  });
 }
 function setCartBusy(value){cartDialog.querySelectorAll('[data-cart-action]').forEach(b=>b.disabled=value)}
 function renderCart(warning=''){
  cartContent.replaceChildren();cartStatus.textContent='';
  const lines=selectedLines();
  if(!lines.length){
   const empty=el('div',undefined,'cart-empty');empty.append(el('p','Your cart is empty. Find a piece that speaks to you.'));
   const browse=el('button','Explore the collection','btn gold');browse.onclick=()=>{cartDialog.close();qs('#collection').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'})};empty.append(browse);cartContent.append(empty);return;
  }
  const list=el('div',undefined,'cart-lines');
  for(const line of lines){
   const variant=line.merchandise,product=variant.product,row=el('section',undefined,'cart-line');
   const snapshot=window.MOGCatalog.products.find(p=>p.handle===product.handle),img=el('img');
   img.src=variant.image?.url||snapshot?.image||'';img.alt=`${product.title} ${variant.title}`;img.width=95;img.height=115;row.append(img);
   const detail=el('div');detail.append(el('h3',product.title),el('p',variant.title==='Default Title'?'Standard':variant.title,'cart-variant'));
   const controls=el('div',undefined,'cart-controls');
   function action(text,label,fn,cls){const b=el('button',text,cls);b.type='button';b.setAttribute('aria-label',label);b.dataset.cartAction='1';b.onclick=()=>performCart(fn);return b}
   controls.append(action('−',`Decrease quantity for ${product.title}`,()=>changeQuantity(line,line.quantity-1)),el('output',String(line.quantity)),action('+',`Increase quantity for ${product.title}`,()=>changeQuantity(line,line.quantity+1)),action('Remove',`Remove ${product.title}`,()=>removeLine(line.id),'remove'));
   detail.append(controls,el('div',money(line.cost.totalAmount.amount,line.cost.totalAmount.currencyCode),'cart-line-price'));row.append(detail);list.append(row);
  }
  cartContent.append(list);
  if(warning)cartContent.append(el('p',warning,'cart-warning'));
  const summary=el('div',undefined,'cart-summary'),total=el('div',undefined,'cart-total');
  total.append(el('span','Subtotal'),el('span',money(cart.cost.subtotalAmount.amount,cart.cost.subtotalAmount.currencyCode)));
  summary.append(total,el('p','Shipping and taxes are calculated at secure Shopify checkout. You will leave this page only for the final payment step.','cart-note'));
  const checkout=el('button','Continue to secure checkout ↗','btn gold');checkout.type='button';checkout.dataset.cartAction='1';checkout.id='checkout-button';
  checkout.onclick=()=>{
   if(cartBusy)return;
   // A sandboxed design preview cannot display Shopify's payment page in its iframe.
   // Reserve a tab during the click gesture; the real top-level MOG page navigates normally.
   let previewTab=null;
   if(window.top!==window){previewTab=window.open('about:blank','_blank');if(previewTab){try{previewTab.opener=null}catch{/* Opaque preview origins may forbid changing opener; location.replace remains allowed. */}}}
   performCart(()=>checkoutNow(previewTab));
  };summary.append(checkout);
  summary.append(el('p',cartStorageAvailable?'Your cart is saved in this browser. Adding an item does not charge your card or place an order.':'Your browser is blocking cart storage. Keep this page open until checkout; refreshing may reset your cart.','cart-note'));
  cartContent.append(summary);setCartBusy(cartBusy);
 }
 async function performCart(fn){
  if(cartBusy)return;cartBusy=true;setCartBusy(true);cartStatus.textContent='Updating…';
  try{await fn()}catch(e){cartStatus.textContent=e.message}
  finally{cartBusy=false;setCartBusy(false)}
 }
 async function removeLine(id){
  const warning=await mutation('cartLinesRemove','$cartId:ID!,$lineIds:[ID!]!','cartId:$cartId,lineIds:$lineIds',{cartId,lineIds:[id]});
  renderCart(warning);
 }
 async function changeQuantity(line,quantity){
  if(quantity<1)return removeLine(line.id);
  if(quantity>20)throw Error('A maximum of 20 per option can be added.');
  const warning=await mutation('cartLinesUpdate','$cartId:ID!,$lines:[CartLineUpdateInput!]!','cartId:$cartId,lines:$lines',{cartId,lines:[{id:line.id,quantity}]});
  const result=selectedLines().find(l=>l.id===line.id);
  renderCart(warning||(result?.quantity!==quantity?'Shopify adjusted the quantity to available stock. Please review it.':''));
 }
 async function checkoutNow(previewTab=null){
  let handedOff=false;
  try{
  const before=selectedLines().map(l=>({id:l.merchandise.id,quantity:l.quantity,amount:l.cost.totalAmount.amount}));
  cartStatus.textContent='Checking your cart with Shopify…';
  await refreshCart();
  if(!selectedLines().length){renderCart();throw Error('Your cart is empty. Add an item before checkout.')}
  const after=selectedLines();
  if(before.length!==after.length||before.some(l=>!after.some(n=>n.merchandise.id===l.id&&n.quantity===l.quantity&&n.cost.totalAmount.amount===l.amount))){
   renderCart('Your cart changed during the live stock/price check. Review it, then continue again.');return;
  }
  if(after.some(l=>!l.merchandise.availableForSale))throw Error('An option in your cart is unavailable. Remove it or choose another.');
  const url=new URL(cart.checkoutUrl);
  if(url.protocol!=='https:'||![SHOP,'checkout.shopify.com'].includes(url.hostname))throw Error('Checkout address could not be verified. Please contact MOG.');
  cartStatus.textContent='Opening secure Shopify checkout…';
  // Same final handoff as GOG. No payment details are handled by this page.
  if(window.top!==window){
   if(!previewTab||previewTab.closed)throw Error('Allow a new tab to open secure checkout from this preview, then try again.');
   previewTab.location.replace(url.href);
  }else window.location.assign(url.href);
  handedOff=true;
  }finally{if(!handedOff&&previewTab&&!previewTab.closed)previewTab.close()}
 }
 async function showCart(from){
  openModal(cartDialog,from);cartContent.replaceChildren(el('p','Checking your cart…','cart-note'));cartStatus.textContent='';
  if(cartBusy){renderCart();return}
  cartBusy=true;
  try{await refreshCart();renderCart()}
  catch(e){
   renderCart();cartStatus.textContent=e.message;
   const retry=el('button','Retry cart','btn outline');retry.onclick=()=>showCart(from);cartContent.append(retry);
  }finally{cartBusy=false;setCartBusy(false)}
 }
 async function updateCatalog(){
  const node=qs('#catalog-status');
  try{
   const data=await gql('query Catalog { products(first:100) { nodes {handle availableForSale priceRange {minVariantPrice {amount currencyCode}}} pageInfo {hasNextPage}}}');
   if(data.products.pageInfo.hasNextPage)throw Error('Catalog pagination needs review.');
   let changed=0;
   for(const p of window.MOGCatalog.products){
    const live=data.products.nodes.find(n=>n.handle===p.handle);
    if(live&&live.priceRange.minVariantPrice.currencyCode==='USD'){p.price=Number(live.priceRange.minVariantPrice.amount);p.liveAvailable=live.availableForSale;changed++}
   }
   window.MOGCatalog.render();
   const hero=window.MOGCatalog.products.find(p=>p.handle==='prophet-t-shirt');
   const feature=window.MOGCatalog.products.find(p=>p.handle==='mog-fur-jacket');
   if(hero)qs('.product-caption button').textContent=`New release / Prophet T-Shirt · ${money(hero.price)} ↗`;
   if(feature)qs('.feature-price').textContent=`From ${money(feature.price)} USD`;
   node.textContent=changed===window.MOGCatalog.products.length?'Live Shopify prices checked. Select a piece to check options and add to your cart.':'Some catalog prices are saved estimates. Live prices and availability are checked when you select a piece.';
  }catch{
   node.textContent='Live catalog check unavailable. Saved prices are estimates; options must load from Shopify before you can add to cart.';node.classList.add('catalog-offline');
  }
 }
 document.addEventListener('click',e=>{
  const product=e.target.closest('[data-product]');
  if(product){showProduct(product.dataset.product,product);return}
  const trigger=e.target.closest('.cart-trigger');if(trigger)showCart(trigger);
 });
 updateCatalog();
 if(cartId)refreshCart().catch(()=>{qs('#cart-count').textContent='—'});
})();
