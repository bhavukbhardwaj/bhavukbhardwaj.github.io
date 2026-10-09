(function(){
  var root=document.documentElement;
  var tb=document.getElementById('theme');
  if(tb)tb.addEventListener('click',function(){
    var dark=root.getAttribute('data-theme')==='dark'||(!root.getAttribute('data-theme')&&matchMedia('(prefers-color-scheme:dark)').matches);
    var n=dark?'light':'dark';root.setAttribute('data-theme',n);try{localStorage.setItem('theme',n)}catch(e){}
  });
  function pressed(box,key,val){box.querySelectorAll('button').forEach(function(b){b.setAttribute('aria-pressed',b.dataset[key]===val)})}
  // projects
  var pf=document.getElementById('pfilters');
  if(pf){var pg=document.getElementById('pgrid');
    var run=function(c){pressed(pf,'c',c);pg.querySelectorAll('.pcard').forEach(function(e){e.hidden=!(c==='all'||(c==='top'?e.dataset.top==='1':e.dataset.cat===c))})};
    pf.addEventListener('click',function(e){var b=e.target.closest('button');if(b)run(b.dataset.c)});run('top');}
  // blog
  var bf=document.getElementById('bfilters');
  if(bf){var cat='all',q='',qi=document.getElementById('q'),rows=[].slice.call(document.querySelectorAll('#bfeat,#blist .brow')),yrs=[].slice.call(document.querySelectorAll('[data-yr]'));
    var go=function(){pressed(bf,'c',cat);var shown=0;
      rows.forEach(function(r){var ok=(cat==='all'||r.dataset.tags.split('|').indexOf(cat)>-1)&&(!q||r.dataset.q.indexOf(q)>-1);r.hidden=!ok;if(ok)shown++});
      yrs.forEach(function(y){var n=y.nextElementSibling,any=false;while(n&&!n.hasAttribute('data-yr')){if(!n.hidden)any=true;n=n.nextElementSibling}y.hidden=!any});
      document.getElementById('bempty').hidden=shown>0};
    bf.addEventListener('click',function(e){var b=e.target.closest('button');if(b){cat=b.dataset.c;go()}});
    qi.addEventListener('input',function(){q=qi.value.trim().toLowerCase();go()});go();}
  // certificates
  var cf=document.getElementById('cf-filters');
  if(cf){var grid=document.getElementById('certs-grid'),lb=document.getElementById('lb'),lbi=document.getElementById('lbi'),lbc=document.getElementById('lbc');
    var cr=function(g){pressed(cf,'g',g);grid.querySelectorAll('.cert').forEach(function(e){e.hidden=!(g==='all'||(g==='top'?e.dataset.top==='1':e.dataset.g===g))})};
    cf.addEventListener('click',function(e){var b=e.target.closest('button');if(b)cr(b.dataset.g)});cr('top');
    grid.addEventListener('click',function(e){var c=e.target.closest('.cert');if(!c)return;lbi.src=c.dataset.src;lbi.alt=c.dataset.cap;lbc.textContent=c.dataset.cap;lb.hidden=false;document.getElementById('lbx').focus()});
    var close=function(){lb.hidden=true};document.getElementById('lbx').addEventListener('click',close);
    lb.addEventListener('click',function(e){if(e.target===lb)close()});document.addEventListener('keydown',function(e){if(e.key==='Escape')close()});}
})();
