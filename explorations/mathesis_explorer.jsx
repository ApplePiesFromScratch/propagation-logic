import { useState, useRef, useEffect, useCallback } from "react";

// ── Dual number arithmetic for forward-mode AD ──────────────────────────────
class Dual {
  constructor(v, e = 0) { this.v = +v; this.e = +e; }
  add(o) { const b = o instanceof Dual ? o : new Dual(o); return new Dual(this.v+b.v, this.e+b.e); }
  sub(o) { const b = o instanceof Dual ? o : new Dual(o); return new Dual(this.v-b.v, this.e-b.e); }
  mul(o) { const b = o instanceof Dual ? o : new Dual(o); return new Dual(this.v*b.v, this.e*b.v+this.v*b.e); }
  div(o) { const b = o instanceof Dual ? o : new Dual(o); return new Dual(this.v/b.v, (this.e*b.v-this.v*b.e)/(b.v*b.v)); }
  pow(n) { return new Dual(Math.pow(this.v,n), this.e*n*Math.pow(this.v,n-1)); }
  sin()  { return new Dual(Math.sin(this.v),  this.e*Math.cos(this.v)); }
  cos()  { return new Dual(Math.cos(this.v), -this.e*Math.sin(this.v)); }
  exp()  { const ev=Math.exp(this.v); return new Dual(ev, this.e*ev); }
  log()  { return new Dual(Math.log(this.v), this.e/this.v); }
  neg()  { return new Dual(-this.v, -this.e); }
  abs()  { return new Dual(Math.abs(this.v), this.v>=0?this.e:-this.e); }
}

// ── Shared SVG function plotter ─────────────────────────────────────────────
function Plot({ funcs, xMin, xMax, yMin, yMax, W=380, H=220, title }) {
  const N = 600;
  const xs = Array.from({length:N}, (_,i) => xMin + (xMax-xMin)*i/(N-1));
  const sx = x => ((x-xMin)/(xMax-xMin))*W;
  const sy = y => H - ((y-yMin)/(yMax-yMin))*H;

  const pathD = fn => {
    let d='', on=false;
    for (const x of xs) {
      const y=fn(x);
      if (!isFinite(y)||y<yMin*5||y>yMax*5) { on=false; continue; }
      d += on ? ` L ${sx(x).toFixed(1)} ${sy(y).toFixed(1)}`
               : `M ${sx(x).toFixed(1)} ${sy(y).toFixed(1)}`;
      on=true;
    }
    return d;
  };

  const xTicks = Array.from({length: Math.round(xMax)-Math.round(xMin)+1},
    (_,i)=>Math.round(xMin)+i);
  const yTicks = Array.from({length: Math.round(yMax)-Math.round(yMin)+1},
    (_,i)=>Math.round(yMin)+i);
  const ox=sx(0), oy=sy(0);

  return (
    <div>
      {title && <div style={{fontSize:12,color:'#505080',marginBottom:5,fontStyle:'italic'}}>{title}</div>}
      <svg width={W} height={H} style={{display:'block',background:'#0c0c1a',borderRadius:6,border:'1px solid #1a1a38'}}>
        {xTicks.map(x=><line key={x} x1={sx(x)} y1={0} x2={sx(x)} y2={H} stroke="#10102a" strokeWidth={1}/>)}
        {yTicks.map(y=><line key={y} x1={0} y1={sy(y)} x2={W} y2={sy(y)} stroke="#10102a" strokeWidth={1}/>)}
        {oy>0&&oy<H&&<line x1={0} y1={oy} x2={W} y2={oy} stroke="#22224a" strokeWidth={1}/>}
        {ox>0&&ox<W&&<line x1={ox} y1={0} x2={ox} y2={H} stroke="#22224a" strokeWidth={1}/>}
        {funcs.map(({fn,color,width=2,dash},i)=>(
          <path key={i} d={pathD(fn)} fill="none" stroke={color} strokeWidth={width}
            strokeDasharray={dash||'none'} strokeLinecap="round"/>
        ))}
      </svg>
    </div>
  );
}

// ── SECTION 1: G_diff^n fixed points ────────────────────────────────────────
function GdiffOrbits() {
  const [n, setN] = useState(4);

  const configs = {
    1: {
      funcs: [{fn: x=>Math.exp(x), color:'#5ac8fa', label:'eˣ', star:false}],
      yRange: [-1.5, 5],
      insight: 'One root: λ=1. The differential operator has exactly one fixed function — eˣ. d/dx[eˣ] = eˣ.',
      roots: [{re:1,im:0}], rootLabels:['+1'], colors:['#5ac8fa'],
    },
    2: {
      funcs: [
        {fn: x=>Math.cosh(x), color:'#5ac8fa', label:'cosh(x)', star:false},
        {fn: x=>Math.sinh(x), color:'#ff6060', label:'sinh(x)', star:false},
      ],
      yRange: [-3, 5],
      insight: 'Two roots: λ=±1. Two fixed functions: cosh (even) and sinh (odd). d²/dx²[cosh]=cosh, d²/dx²[sinh]=sinh.',
      roots: [{re:1,im:0},{re:-1,im:0}], rootLabels:['+1','−1'], colors:['#5ac8fa','#ff6060'],
    },
    3: {
      funcs: [
        {fn: x=>Math.exp(x), color:'#5ac8fa', label:'eˣ', star:false},
        {fn: x=>Math.exp(-x/2)*Math.cos(Math.sqrt(3)/2*x), color:'#ffcc44', label:'Re(e^ωx)', star:false},
        {fn: x=>Math.exp(-x/2)*Math.sin(Math.sqrt(3)/2*x), color:'#ff7760', label:'Im(e^ωx)', star:false},
      ],
      yRange: [-2, 4],
      insight: 'Three roots: one real (λ=1), two complex conjugates (ω,ω²). The complex pair produces oscillating exponential decay.',
      roots: Array.from({length:3},(_,k)=>({re:Math.cos(2*Math.PI*k/3),im:Math.sin(2*Math.PI*k/3)})),
      rootLabels:['1','ω','ω²'], colors:['#5ac8fa','#ffcc44','#ff7760'],
    },
    4: {
      funcs: [
        {fn: x=>Math.exp(x),   color:'#5ac8fa', label:'eˣ',     star:false},
        {fn: x=>Math.exp(-x),  color:'#8888ff', label:'e⁻ˣ',    star:false},
        {fn: x=>Math.cos(x),   color:'#ff9f0a', label:'cos(x)', star:true},
        {fn: x=>Math.sin(x),   color:'#ff3b6a', label:'sin(x)', star:true},
      ],
      yRange: [-1.6, 2],
      insight: '★ Four roots: +1, −1, +i, −i. The imaginary pair forces e^(ix) = cos(x)+i·sin(x) into existence. sin and cos are NOT primitive — they are the real and imaginary projections of the rotation gradient\'s 4-step orbit in ℂ.',
      roots: Array.from({length:4},(_,k)=>({re:Math.cos(2*Math.PI*k/4),im:Math.sin(2*Math.PI*k/4)})),
      rootLabels:['+1','−1','+i','−i'], colors:['#5ac8fa','#8888ff','#ff9f0a','#ff3b6a'],
    },
  };

  const cfg = configs[n];
  const cW=170, cH=170, cr=60, cx=85, cy=85;

  return (
    <div>
      <h2 style={{color:'#c0c0ff',fontSize:18,margin:'0 0 6px'}}>
        Fixed Points of G_diff^n — How sin and cos Emerge
      </h2>
      <p style={{color:'#7070aa',fontSize:13,margin:'0 0 16px',lineHeight:1.65}}>
        f^(n) = f means the function equals its own n-th derivative. Solutions: exp(λx) where λ^n = 1.
        Each n-th root of unity contributes one basis function. For n=4, the roots ±i force complex exponentials —
        and their real/imaginary parts are exactly sin and cos.
      </p>

      <div style={{display:'flex',gap:8,marginBottom:18}}>
        {[1,2,3,4].map(v=>(
          <button key={v} onClick={()=>setN(v)} style={{
            padding:'8px 22px', fontSize:17,
            background: n===v?'#1a1a40':'#0e0e1e',
            border:`1px solid ${n===v?'#5050bb':'#222240'}`,
            color: n===v?'#d0d0ff':'#484880',
            borderRadius:5, cursor:'pointer', fontWeight: n===v?'bold':'normal',
          }}>n = {v}</button>
        ))}
        <span style={{alignSelf:'center',fontSize:13,color:'#404068',marginLeft:8}}>
          f^({n}) = f &nbsp;→&nbsp; λ^{n} = 1
        </span>
      </div>

      <div style={{display:'flex',gap:22,flexWrap:'wrap',alignItems:'flex-start'}}>
        {/* Unit circle */}
        <div>
          <div style={{fontSize:11,color:'#404068',marginBottom:6}}>{n}-th roots of unity (eigenvalues)</div>
          <svg width={cW} height={cH} style={{display:'block',background:'#0c0c1a',borderRadius:6,border:'1px solid #1a1a38'}}>
            <circle cx={cx} cy={cy} r={cr} fill="none" stroke="#18183a" strokeWidth={1}/>
            <line x1={cx-cr-10} y1={cy} x2={cx+cr+10} y2={cy} stroke="#202048" strokeWidth={1}/>
            <line x1={cx} y1={cy-cr-10} x2={cx} y2={cy+cr+10} stroke="#202048" strokeWidth={1}/>
            {cfg.roots.map((r,i)=>{
              const px=cx+r.re*cr, py=cy-r.im*cr;
              const col=cfg.colors[i];
              const lx=px+(r.re>0.1?9:r.re<-0.1?-32:-8);
              const ly=py+(r.im>0.1?-9:r.im<-0.1?16:4);
              return (
                <g key={i}>
                  <circle cx={px} cy={py} r={6} fill={col} opacity={0.9}/>
                  <text x={lx} y={ly} fill={col} fontSize={11}>{cfg.rootLabels[i]}</text>
                </g>
              );
            })}
            <text x={cx+cr+2} y={cy+12} fill="#282860" fontSize={9}>Re</text>
            <text x={cx-5} y={cy-cr-4} fill="#282860" fontSize={9}>Im</text>
          </svg>
        </div>

        {/* Function plot */}
        <div>
          <Plot
            funcs={cfg.funcs.map(f=>({fn:f.fn,color:f.color,width:f.star?2.5:1.5}))}
            xMin={-Math.PI} xMax={Math.PI}
            yMin={cfg.yRange[0]} yMax={cfg.yRange[1]}
            W={330} H={200}
            title={`Basis functions of f^(${n}) = f`}
          />
          <div style={{marginTop:8,display:'flex',flexWrap:'wrap',gap:12}}>
            {cfg.funcs.map((f,i)=>(
              <div key={i} style={{display:'flex',alignItems:'center',gap:7,fontSize:12}}>
                <svg width={22} height={10}><line x1={0} y1={5} x2={22} y2={5} stroke={f.color} strokeWidth={f.star?2.5:1.5}/></svg>
                <span style={{color:f.color}}>{f.label}</span>
                {f.star&&<span style={{color:'#ff9f0a',fontSize:10,marginLeft:-4}}>★</span>}
              </div>
            ))}
          </div>
        </div>
      </div>

      <div style={{
        marginTop:18,padding:'12px 16px',
        background: n===4?'#14140a':'#0c0c1a',
        border:`1px solid ${n===4?'#5a5014':'#1a1a38'}`,
        borderRadius:6,fontSize:13,
        color: n===4?'#ddc880':'#7070aa',
        lineHeight:1.7,
      }}>
        {cfg.insight}
      </div>

      {n===4&&(
        <div style={{marginTop:10,padding:'10px 16px',background:'#120a1a',border:'1px solid #3a1a4a',borderRadius:6,fontSize:13,color:'#cc88ff',lineHeight:1.7}}>
          <strong>Euler's identity as coda:</strong> e^(iπ)+1=0. Three structurally different fixed-point types —
          e (G_diff fixed point), i (G²=G_neg carrier extension), π (G_rot coherence cycle) —
          co-propagated in ℂ, meeting at the additive identity. <em>Beautiful because forced, not chosen.</em>
        </div>
      )}
    </div>
  );
}

// ── SECTION 2: Three Constants ───────────────────────────────────────────────
function ThreeConstants() {
  const [which, setWhich] = useState('e');
  const [steps, setSteps] = useState(8);

  const PHI = (1+Math.sqrt(5))/2;

  const seqs = {
    e: {
      target: Math.E,
      color: '#5ac8fa',
      label: 'e',
      formula: 'e = Σ 1/k! = 1 + 1 + ½ + ⅙ + ...',
      type: 'G_diff fixed point',
      desc: 'd/dx[eˣ]=eˣ. The exp function is its own derivative. Error at step n ≈ e/(n+1)! — superexponential decay. Factorial growth kills each term.',
      maxN: 15,
      chartShape: 'Accelerating curve — superexponential (each step kills more than the last)',
      compute: (n) => { let s=0,f=1; for(let k=0;k<=n;k++){if(k>0)f*=k;s+=1/f;} return s; },
    },
    pi: {
      target: Math.PI,
      color: '#ff9f0a',
      label: 'π',
      formula: 'π/4 = 1 − 1/3 + 1/5 − 1/7 + ... (Leibniz–Gregory)',
      type: 'G_rot coherence cycle',
      desc: 'Error ≈ 1/(2n+3) — algebraic O(1/n). The rotation orbit never closes exactly; each term contributes a fixed fraction of the remaining gap.',
      maxN: 500,
      chartShape: 'Near-flat line — O(1/n) decay, log error ≈ −log(n)',
      compute: (n) => { let s=0; for(let k=0;k<=n;k++) s+=(k%2===0?1:-1)/(2*k+1); return 4*s; },
    },
    phi: {
      target: PHI,
      color: '#30d158',
      label: 'φ',
      formula: 'φ = fixed point of x → 1+1/x, starting x₀=1',
      type: 'Ratio reconfiguration fixed point',
      desc: 'f\'(φ)=−1/φ². Each step multiplies error by 1/φ²≈0.382. Geometric convergence — log error is a perfect straight line with slope −log₁₀(φ²)≈−0.418.',
      maxN: 25,
      chartShape: 'Perfect straight line — geometric convergence, rate = 1/φ² (the fixed point encodes its own approach rate)',
      compute: (n) => { let x=1; for(let k=0;k<n;k++) x=1+1/x; return x; },
    },
  };

  const s = seqs[which];
  const cur = Math.min(steps, s.maxN);
  const val = s.compute(cur);
  const err = Math.abs(val - s.target);

  // Use exactly min(maxN, 80) distinct data points — no duplicates
  const nPoints = Math.min(s.maxN, 80);
  // Build data: n goes from 1 to maxN, distributed across nPoints samples
  const data = Array.from({length: nPoints}, (_,i) => {
    const n = Math.max(1, Math.round(1 + i*(s.maxN-1)/(nPoints-1)));
    const e = Math.abs(s.compute(n) - s.target);
    return {n, e: isFinite(e) && e > 0 ? e : 1e-16};
  });

  const svgW=460, svgH=130;
  const pad = {l:10, r:10, t:12, b:12};
  const chartW = svgW - pad.l - pad.r;
  const chartH = svgH - pad.t - pad.b;

  // Log scale: map log10(e) from [lo, hi] → [0,1], 1=high error (top), 0=low error (bottom)
  const logErrors = data.map(d => Math.log10(d.e));
  const hiLog = Math.max(...logErrors);
  const loLog = Math.min(...logErrors, -15);
  const logToY = le => {
    const frac = (le - loLog) / (hiLog - loLog); // 0=bottom, 1=top
    return pad.t + chartH * (1 - frac);           // small y = top
  };
  const nToX = n => pad.l + (n - 1) / (s.maxN - 1) * chartW;
  const curX = nToX(cur);

  // For φ: theoretical straight line y = log10(|x0-φ|) + n*log10(1/φ²)
  const phiLine = which==='phi' ? (() => {
    const slope = Math.log10(1/PHI/PHI); // ≈ -0.418 per step
    const intercept = Math.log10(Math.abs(1 - PHI)); // at n=0
    return {slope, intercept};
  })() : null;

  // Fibonacci ratio at step cur (correct: after cur steps of x→1+1/x from x=1)
  // Step k gives F(k+2)/F(k+1) where F is 1,1,2,3,5,8,...
  const fibRatio = (() => {
    let a=1, b=1;
    for(let k=1; k<=Math.min(cur,40); k++) { const t=a+b; a=b; b=t; }
    // now b=F(cur+2), a=F(cur+1)
    return {num: b, den: a};
  })();

  return (
    <div>
      <h2 style={{color:'#c0c0ff',fontSize:18,margin:'0 0 6px'}}>
        e, π, φ — Three Structurally Distinct Fixed Points
      </h2>
      <p style={{color:'#7070aa',fontSize:13,margin:'0 0 16px',lineHeight:1.65}}>
        The mechanism distinguishes them by convergence type. Each chart shape IS the
        structural signature — not decoration.
      </p>

      <div style={{display:'flex',gap:10,marginBottom:18,flexWrap:'wrap'}}>
        {Object.entries(seqs).map(([k,v])=>(
          <button key={k} onClick={()=>{setWhich(k);setSteps(k==='pi'?80:k==='phi'?5:5);}} style={{
            padding:'10px 22px',fontSize:22,fontWeight:'bold',
            background: which===k?'#101030':'#0c0c1a',
            border:`2px solid ${which===k?v.color:'#222240'}`,
            color: which===k?v.color:'#363660',
            borderRadius:6,cursor:'pointer',
          }}>{v.label}</button>
        ))}
      </div>

      <div style={{padding:'10px 16px',background:'#0c0c1a',
        border:`1px solid ${s.color}44`,borderLeft:`3px solid ${s.color}`,
        borderRadius:6,marginBottom:14}}>
        <div style={{fontSize:13,color:s.color,fontFamily:'monospace',marginBottom:4}}>{s.formula}</div>
        <div style={{fontSize:12,color:'#6060aa'}}>
          <strong style={{color:'#8888bb'}}>{s.type}</strong> — {s.desc}
        </div>
      </div>

      {/* Convergence chart */}
      <div style={{marginBottom:6}}>
        <div style={{fontSize:11,color:'#404068',marginBottom:5}}>
          log₁₀(|error|) vs steps — <span style={{color:s.color}}>{s.chartShape}</span>
        </div>
        <svg width={svgW} height={svgH}
          style={{display:'block',background:'#0c0c1a',borderRadius:6,border:'1px solid #1a1a38'}}>
          {/* Grid lines */}
          {[-2,-4,-6,-8,-10,-12,-14].map(le=>{
            if(le<loLog||le>hiLog) return null;
            const y=logToY(le);
            return <g key={le}>
              <line x1={pad.l} y1={y} x2={svgW-pad.r} y2={y} stroke="#10102a" strokeWidth={1}/>
              <text x={pad.l+2} y={y-2} fill="#222248" fontSize={8}>{le}</text>
            </g>;
          })}

          {/* φ theoretical straight line */}
          {phiLine && (()=>{
            const {slope, intercept} = phiLine;
            const x1=nToX(1), y1=logToY(intercept+slope);
            const x2=nToX(s.maxN), y2=logToY(intercept+s.maxN*slope);
            return <line x1={x1} y1={y1} x2={x2} y2={y2}
              stroke="#30d15840" strokeWidth={8} strokeLinecap="round"/>;
          })()}

          {/* Data line */}
          <polyline
            points={data.map((d,i)=>`${nToX(d.n).toFixed(1)},${logToY(Math.log10(d.e)).toFixed(1)}`).join(' ')}
            fill="none" stroke={s.color} strokeWidth={2} strokeLinejoin="round"/>

          {/* Current step marker */}
          {cur >= 1 && cur <= s.maxN && (()=>{
            const x = curX;
            const le = Math.log10(Math.max(err, 1e-16));
            const y = logToY(Math.max(loLog, Math.min(hiLog, le)));
            return <>
              <line x1={x} y1={pad.t} x2={x} y2={svgH-pad.b}
                stroke={s.color} strokeWidth={1} opacity={0.35} strokeDasharray="3,3"/>
              <circle cx={x} cy={y} r={4} fill={s.color} opacity={0.9}/>
            </>;
          })()}

          <text x={pad.l+2} y={pad.t+10} fill="#282858" fontSize={9}>log error</text>
          <text x={svgW-pad.r-38} y={svgH-pad.b+10} fill="#282858" fontSize={9}>steps →</text>
        </svg>
      </div>

      {/* Slider */}
      <div style={{display:'flex',alignItems:'center',gap:12,marginBottom:16,marginTop:8}}>
        <span style={{fontSize:12,color:'#606080',minWidth:76}}>step: {cur}</span>
        <input type="range" min={1} max={s.maxN} value={cur}
          onChange={e=>setSteps(+e.target.value)}
          style={{flex:1,accentColor:s.color}}/>
        <span style={{fontSize:11,color:'#303056',minWidth:70,textAlign:'right'}}>
          max: {s.maxN}
        </span>
      </div>

      {/* Values */}
      <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:12,marginBottom:18}}>
        <div style={{padding:'12px 16px',background:'#0c0c1a',border:`1px solid ${s.color}33`,borderRadius:6}}>
          <div style={{fontSize:11,color:'#404068',marginBottom:8}}>At step {cur}</div>
          <div style={{fontFamily:'monospace',fontSize:13,color:s.color,marginBottom:4}}>
            approx: {val.toFixed(10)}
          </div>
          <div style={{fontFamily:'monospace',fontSize:13,color:'#505080',marginBottom:6}}>
            target: {s.target.toFixed(10)}
          </div>
          <div style={{fontFamily:'monospace',fontSize:11,
            color:err<1e-12?'#30d158':err<1e-5?'#ffcc44':'#ff6060'}}>
            |error|: {err > 0 ? err.toExponential(3) : '< 1e-16'}
            {err<1e-12?' ✓ converged':''}
          </div>
        </div>
        <div style={{padding:'12px 16px',background:'#0c0c1a',border:'1px solid #1a1a38',
          borderRadius:6,fontSize:12,color:'#6060aa',lineHeight:1.75}}>
          {which==='e' && <>
            <strong style={{color:'#8888bb'}}>Term {cur}: </strong>
            1/{cur}! ≈ {(1/Array.from({length:cur},(_,i)=>i+1).reduce((a,b)=>a*b,1)).toExponential(2)}<br/>
            Factorial growth kills each term. The curve accelerates downward — each step removes more than the last.
          </>}
          {which==='pi' && <>
            <strong style={{color:'#8888bb'}}>Term {cur}: </strong>
            ±1/{2*cur+1} ≈ {(1/(2*cur+1)).toExponential(2)}<br/>
            The rotation orbit never closes. Each new term only nudges the sum — O(1/n) is the structural cost of an irrational cycle.
          </>}
          {which==='phi' && (()=>{
            const prevErr = cur > 1 ? Math.abs(s.compute(cur-1) - PHI) : null;
            const scaledErr = err * PHI * PHI;
            const match = prevErr ? Math.abs(scaledErr - prevErr) / prevErr < 0.001 : false;
            return <>
              <strong style={{color:'#8888bb'}}>Step {cur}:</strong>{' '}
              F({cur+2})/F({cur+1}) = {fibRatio.num}/{fibRatio.den}<br/>
              <br/>
              <span style={{color:'#30d158'}}>error_{cur}</span>{' '}
              = {err.toExponential(3)}<br/>
              <span style={{color:'#30d158'}}>error_{cur} × φ²</span>{' '}
              = {scaledErr.toExponential(3)}<br/>
              <span style={{color:'#aaaacc'}}>error_{cur-1}</span>{' '}
              = {prevErr ? prevErr.toExponential(3) : '—'}{' '}
              {match
                ? <span style={{color:'#30d158'}}>✓ equal</span>
                : <span style={{color:'#ff6060'}}>≠</span>}
            </>;
          })()}
        </div>
      </div>

      {/* Three-way structural summary */}
      <div style={{display:'grid',gridTemplateColumns:'repeat(3,1fr)',gap:10}}>
        {Object.entries(seqs).map(([k,v])=>(
          <div key={k} style={{
            padding:'12px',background:'#0c0c1a',
            border:`1px solid ${v.color}${which===k?'55':'22'}`,
            borderTop:`2px solid ${v.color}`,
            borderRadius:6,opacity:which===k?1:0.5,transition:'opacity 0.2s',
          }}>
            <div style={{fontSize:24,color:v.color,fontWeight:'bold',marginBottom:4}}>{v.label}</div>
            <div style={{fontSize:10,color:v.color,marginBottom:6,opacity:0.8}}>{v.type}</div>
            <div style={{fontSize:10,color:'#505078',lineHeight:1.5}}>
              {k==='e'  && 'Superexponential — 1/n! collapse'}
              {k==='pi' && 'Algebraic O(1/n) — orbit never closes'}
              {k==='phi'&& 'Geometric 1/φ² — fixed point encodes its own convergence rate'}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ── SECTION 3: Logistic Map / Chaos ─────────────────────────────────────────
function LogisticMap() {
  const bifRef = useRef();
  const [rVal, setRVal] = useState(3.5);
  const [drew, setDrew] = useState(false);

  useEffect(()=>{
    const canvas = bifRef.current;
    if(!canvas) return;
    const ctx = canvas.getContext('2d');
    const W=canvas.width, H=canvas.height;
    ctx.fillStyle='#09090f';
    ctx.fillRect(0,0,W,H);

    const rMin=2.5, rMax=4.0;
    for (let px=0;px<W;px++) {
      const r = rMin+(px/W)*(rMax-rMin);
      let x=0.5;
      for (let i=0;i<500;i++) x=r*x*(1-x);
      for (let i=0;i<300;i++) {
        x=r*x*(1-x);
        const py=Math.round((1-x)*H);
        ctx.fillStyle='rgba(60,110,255,0.22)';
        ctx.fillRect(px,py,1,1);
      }
    }

    // Bifurcation markers
    ctx.strokeStyle='rgba(255,80,80,0.35)';
    ctx.setLineDash([3,3]);
    [3.0, 3.449, 3.544, 3.5688, 3.5699].forEach(rb=>{
      const px=((rb-rMin)/(rMax-rMin))*W;
      ctx.beginPath(); ctx.moveTo(px,0); ctx.lineTo(px,H); ctx.stroke();
    });
    ctx.setLineDash([]);
    setDrew(true);
  }, []);

  const orbit = (()=>{
    let x=0.5;
    for (let i=0;i<400;i++) x=rVal*x*(1-x);
    return Array.from({length:100}, ()=>{ x=rVal*x*(1-x); return x; });
  })();

  const status =
    rVal<3 ?     {t:'Stable fixed point — one attractor', c:'#30d158'} :
    rVal<3.449 ? {t:'Period-2 orbit — first bifurcation at r≈3', c:'#5ac8fa'} :
    rVal<3.544 ? {t:'Period-4 — second bifurcation at r≈3.449', c:'#5ac8fa'} :
    rVal<3.57 ?  {t:'Period-8, 16, 32... Feigenbaum cascade', c:'#ff9f0a'} :
    rVal<3.83 ?  {t:'Chaos — Observation 2.2: demand → ∞, no finite threshold contains it', c:'#ff453a'} :
    {t:'Periodic window — simpler patterns propagating outward from the chaotic core', c:'#bf5af2'};

  const rMin=2.5, rMax=4.0;
  const indX=((rVal-rMin)/(rMax-rMin))*490;

  return (
    <div>
      <h2 style={{color:'#c0c0ff',fontSize:18,margin:'0 0 6px'}}>
        Logistic Map — Observation 2.2 Made Visible
      </h2>
      <p style={{color:'#7070aa',fontSize:13,margin:'0 0 14px',lineHeight:1.65}}>
        x → r·x·(1−x). As r grows, gradient demand exceeds the coherence threshold
        and the pattern reconfigures: period-2, then 4, then 8, then chaos at r≈3.570.
        The periodic windows inside chaos are simpler patterns propagating outward
        from the complex core — exactly Observation 2.2's second clause.
      </p>

      <div style={{position:'relative',marginBottom:10}}>
        <canvas ref={bifRef} width={490} height={290}
          style={{display:'block',borderRadius:6,border:'1px solid #1a1a38'}}/>
        <div style={{position:'absolute',top:0,left:indX,
          width:1,height:290,background:'rgba(255,210,60,0.75)',pointerEvents:'none'}}/>
        {drew&&<>
          <div style={{position:'absolute',top:7,left:10,fontSize:10,color:'#2a2a60'}}>
            bifurcation diagram (r: 2.5 → 4.0)
          </div>
          <div style={{position:'absolute',top:7,right:10,fontSize:10,color:'#502020'}}>
            red dashes: bifurcation points
          </div>
        </>}
      </div>

      <div style={{display:'flex',alignItems:'center',gap:12,marginBottom:10}}>
        <span style={{fontSize:13,color:'#606080',minWidth:76}}>r = {rVal.toFixed(3)}</span>
        <input type="range" min={2.5} max={4.0} step={0.001} value={rVal}
          onChange={e=>setRVal(+e.target.value)}
          style={{flex:1,accentColor:'#ffcc44'}}/>
      </div>

      <div style={{
        padding:'8px 14px',borderRadius:5,marginBottom:12,
        background:'#0c0c1a',border:`1px solid ${status.c}44`,
        fontSize:12,color:status.c,
      }}>
        r = {rVal.toFixed(3)}: {status.t}
      </div>

      <div style={{marginBottom:12}}>
        <div style={{fontSize:11,color:'#404068',marginBottom:5}}>Orbit after 400 transients</div>
        <svg width={490} height={70} style={{display:'block',background:'#0c0c1a',borderRadius:6,border:'1px solid #1a1a38'}}>
          {orbit.map((x,i)=>(
            <circle key={i} cx={(i/orbit.length)*488+1} cy={x*70} r={1.5} fill="#4080ff" opacity={0.5}/>
          ))}
        </svg>
      </div>

      <div style={{padding:'10px 16px',background:'#0c0c1a',border:'1px solid #1a1a38',borderRadius:6,fontSize:12,color:'#6060aa',lineHeight:1.7}}>
        <strong style={{color:'#9090cc'}}>Feigenbaum constant δ ≈ 4.6692:</strong>{' '}
        The ratio of successive bifurcation interval widths converges to δ universally —
        for ANY smooth unimodal map. This is itself a fixed point: of the renormalization
        operator T[f] = α·f(f(x/α)) in function space. A fixed point of a gradient on an
        infinite-dimensional carrier.
      </div>
    </div>
  );
}

// ── SECTION 4: Mandelbrot Set ────────────────────────────────────────────────
function MandelbrotSet() {
  const canvasRef = useRef();
  const [view, setView] = useState({cx:-0.5, cy:0, zoom:1.5});
  const [rendering, setRendering] = useState(false);

  useEffect(()=>{
    const canvas = canvasRef.current;
    if(!canvas) return;
    setRendering(true);
    const ctx=canvas.getContext('2d');
    const W=canvas.width, H=canvas.height;
    const img=ctx.createImageData(W,H);
    const d=img.data;
    const maxIter=90;
    const {cx,cy,zoom}=view;

    for (let py=0;py<H;py++) {
      for (let px=0;px<W;px++) {
        const cr=cx+(px/W-0.5)*2*zoom*(W/H);
        const ci=cy+(py/H-0.5)*2*zoom;
        let zr=0, zi=0, iter=0;
        while (zr*zr+zi*zi<=4&&iter<maxIter) {
          const tr=zr*zr-zi*zi+cr;
          zi=2*zr*zi+ci; zr=tr; iter++;
        }
        const idx=(py*W+px)*4;
        if (iter===maxIter) {
          d[idx]=8; d[idx+1]=8; d[idx+2]=28; d[idx+3]=255;
        } else {
          const t=iter/maxIter;
          d[idx]   = Math.min(255,15+230*Math.pow(t,0.5)+20*Math.sin(t*20));
          d[idx+1] = Math.min(255,8+90*t*t);
          d[idx+2] = Math.min(255,40+160*Math.pow(1-t,0.7)+40*Math.cos(t*10));
          d[idx+3] = 255;
        }
      }
    }
    ctx.putImageData(img,0,0);
    setRendering(false);
  }, [view]);

  const handleClick = e=>{
    const canvas=canvasRef.current;
    const rect=canvas.getBoundingClientRect();
    const px=(e.clientX-rect.left)*(canvas.width/rect.width);
    const py=(e.clientY-rect.top)*(canvas.height/rect.height);
    const W=canvas.width, H=canvas.height;
    setView({
      cx: view.cx+(px/W-0.5)*2*view.zoom*(W/H),
      cy: view.cy+(py/H-0.5)*2*view.zoom,
      zoom: view.zoom*0.35,
    });
  };

  return (
    <div>
      <h2 style={{color:'#c0c0ff',fontSize:18,margin:'0 0 6px'}}>
        Mandelbrot Set — Coherence Boundary of Complex Propagation
      </h2>
      <p style={{color:'#7070aa',fontSize:13,margin:'0 0 14px',lineHeight:1.65}}>
        z → z²+c is propagation under G_c in ℂ.{' '}
        <strong style={{color:'#2a3a80'}}>Dark blue = coherent</strong>{' '}
        (orbit stays bounded; c ∈ M).{' '}
        <strong style={{color:'#aa6025'}}>Colors = escaped</strong>,{' '}
        colored by propagation depth before incoherence.
        The boundary ∂M has infinite complexity — it is the exact coherence threshold,
        where Observation 2.2 is instantaneously active. <em style={{color:'#505080'}}>Click to zoom.</em>
      </p>

      <div style={{position:'relative',marginBottom:10}}>
        <canvas ref={canvasRef} width={490} height={340}
          style={{display:'block',borderRadius:6,border:'1px solid #1a1a38',cursor:'crosshair'}}
          onClick={handleClick}/>
        {rendering&&(
          <div style={{position:'absolute',top:'50%',left:'50%',
            transform:'translate(-50%,-50%)',color:'#5050aa',fontSize:13}}>
            rendering...
          </div>
        )}
      </div>

      <div style={{display:'flex',gap:10,alignItems:'center',marginBottom:14,flexWrap:'wrap'}}>
        <button onClick={()=>setView({cx:-0.5,cy:0,zoom:1.5})} style={{
          padding:'6px 14px',background:'#0e0e1e',border:'1px solid #222240',
          color:'#6060aa',borderRadius:4,cursor:'pointer',fontSize:12,
        }}>Reset</button>
        <button onClick={()=>setView({cx:-0.7269,cy:0.1889,zoom:0.003})} style={{
          padding:'6px 14px',background:'#0e0e1e',border:'1px solid #222240',
          color:'#6060aa',borderRadius:4,cursor:'pointer',fontSize:12,
        }}>Seahorse Valley</button>
        <button onClick={()=>setView({cx:-0.235,cy:0.827,zoom:0.02})} style={{
          padding:'6px 14px',background:'#0e0e1e',border:'1px solid #222240',
          color:'#6060aa',borderRadius:4,cursor:'pointer',fontSize:12,
        }}>Elephant Valley</button>
        <span style={{fontSize:11,color:'#303060'}}>
          center ({view.cx.toFixed(5)}, {view.cy.toFixed(5)}i) ·{' '}
          zoom ×{(1.5/view.zoom).toFixed(1)}
        </span>
      </div>

      <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:10}}>
        <div style={{padding:'10px 14px',background:'#0c0c1a',border:'1px solid #1a1a38',borderRadius:6,fontSize:12,color:'#6060aa',lineHeight:1.65}}>
          <strong style={{color:'#8888bb'}}>Main cardioid & bulbs:</strong>{' '}
          The cardioid is the set of c with a stable fixed point.
          The period-2 bulb is the first bifurcation.
          Each bulb is a period-doubling — the same cascade as the logistic map,
          now drawn in parameter space.
        </div>
        <div style={{padding:'10px 14px',background:'#0c0c1a',border:'1px solid #1a1a38',borderRadius:6,fontSize:12,color:'#6060aa',lineHeight:1.65}}>
          <strong style={{color:'#8888bb'}}>Self-similarity:</strong>{' '}
          Miniature copies of the whole set appear near the boundary.
          Simpler patterns propagating outward from complex cores —
          Observation 2.2's second clause, drawn as a picture.
        </div>
      </div>
    </div>
  );
}

// ── SECTION 5: Dual Numbers ──────────────────────────────────────────────────
const PRESETS = [
  {label:'x³',         fn: x=>x.pow(3)},
  {label:'x²·sin(x)',  fn: x=>x.pow(2).mul(x.sin())},
  {label:'sin(x²)',    fn: x=>x.mul(x).sin()},
  {label:'eˣ / x',    fn: x=>x.exp().div(x)},
  {label:'cos(eˣ)',    fn: x=>x.exp().cos()},
  {label:'ln(x²+1)',  fn: x=>x.mul(x).add(1).log()},
];

function DualNumbers() {
  const [pi, setPi] = useState(1);
  const [xv, setXv] = useState(1.3);

  const pr = PRESETS[pi];
  const safeCall = fn => { try { return fn(); } catch { return null; } };

  const res   = safeCall(()=>pr.fn(new Dual(xv,1)));
  const eps   = 1e-7;
  const numD  = safeCall(()=>(pr.fn(new Dual(xv+eps)).v - pr.fn(new Dual(xv-eps)).v)/(2*eps));
  const err   = res&&numD!=null ? Math.abs(res.e-numD) : null;

  const fnV = t => { const r=safeCall(()=>pr.fn(new Dual(t)).v); return r??NaN; };
  const fnE = t => { const r=safeCall(()=>pr.fn(new Dual(t,1)).e); return r??NaN; };

  return (
    <div>
      <h2 style={{color:'#c0c0ff',fontSize:18,margin:'0 0 6px'}}>
        Dual Numbers — Derivative via Loaded History
      </h2>
      <p style={{color:'#7070aa',fontSize:13,margin:'0 0 16px',lineHeight:1.65}}>
        P = (v, e): value and first-order loaded history. The Leibniz product rule
        (v₁,e₁)·(v₂,e₂) = (v₁v₂, e₁v₂+v₁e₂) follows from zero-drag co-propagation,
        with ε₁·ε₂ = 0 as the boundary condition of the first-order propagation regime.
        The derivative propagates WITH the computation — exact, at the cost of one extra float.
      </p>

      <div style={{display:'flex',gap:8,flexWrap:'wrap',marginBottom:16}}>
        {PRESETS.map((p,i)=>(
          <button key={i} onClick={()=>setPi(i)} style={{
            padding:'6px 14px',fontFamily:'monospace',fontSize:13,
            background: pi===i?'#121230':'#0c0c1a',
            border:`1px solid ${pi===i?'#4040bb':'#1e1e40'}`,
            color: pi===i?'#a0a0ff':'#404068',
            borderRadius:4,cursor:'pointer',
          }}>f(x)={p.label}</button>
        ))}
      </div>

      <div style={{display:'flex',alignItems:'center',gap:12,marginBottom:16}}>
        <span style={{fontSize:12,color:'#606080',minWidth:70}}>x = {xv.toFixed(2)}</span>
        <input type="range" min={0.2} max={3.0} step={0.01} value={xv}
          onChange={e=>setXv(+e.target.value)}
          style={{flex:1,accentColor:'#8060ff'}}/>
      </div>

      <div style={{display:'flex',gap:14,flexWrap:'wrap',marginBottom:16}}>
        {/* Results panel */}
        <div style={{padding:'14px 18px',background:'#0c0c1a',border:'1px solid #1a1a38',borderRadius:6,minWidth:280}}>
          <div style={{fontSize:11,color:'#404068',marginBottom:10}}>
            Dual number propagation from ({xv.toFixed(3)}, <span style={{color:'#ff9f0a'}}>1</span>)
          </div>
          <div style={{fontFamily:'monospace',fontSize:13,color:'#5ac8fa',marginBottom:5}}>
            f({xv.toFixed(3)}) = {res?isFinite(res.v)?res.v.toFixed(8):'∞':'—'}
          </div>
          <div style={{fontFamily:'monospace',fontSize:13,color:'#ff9f0a',marginBottom:10}}>
            f′({xv.toFixed(3)}) = {res?isFinite(res.e)?res.e.toFixed(8):'∞':'—'}
          </div>
          <div style={{fontFamily:'monospace',fontSize:11,color:'#606080',marginBottom:3}}>
            numerical: {numD!=null?numD.toFixed(8):'—'}
          </div>
          <div style={{fontFamily:'monospace',fontSize:11,
            color:err!=null&&err<1e-10?'#30d158':'#ff9f0a'}}>
            |error|: {err!=null?err.toExponential(2):'—'}
            {err!=null&&err<1e-10?' ✓ machine precision':''}
          </div>
        </div>

        {/* Arithmetic rules */}
        <div style={{flex:1,minWidth:200,padding:'12px 16px',background:'#0c0c1a',border:'1px solid #1a1a38',borderRadius:6,fontSize:12,color:'#6060aa',lineHeight:2}}>
          <strong style={{color:'#8888bb',lineHeight:1.5,display:'block',marginBottom:4}}>
            Arithmetic rules (derived from zero-drag)
          </strong>
          <code style={{fontSize:11,color:'#c0c0ff',display:'block'}}>add:  (v₁+v₂,  e₁+e₂)</code>
          <code style={{fontSize:11,color:'#c0c0ff',display:'block'}}>
            mul:  (v₁v₂, <span style={{color:'#ff9f0a'}}>e₁v₂+v₁e₂</span>) ← Leibniz
          </code>
          <code style={{fontSize:11,color:'#c0c0ff',display:'block'}}>
            exp:  (eᵛ,   <span style={{color:'#ff9f0a'}}>e·eᵛ</span>) ← G_diff fixed point
          </code>
          <code style={{fontSize:11,color:'#c0c0ff',display:'block'}}>
            sin:  (sin v, <span style={{color:'#ff9f0a'}}>e·cos v</span>) ← chain rule
          </code>
          <div style={{fontSize:11,color:'#404070',marginTop:4}}>
            ε₁·ε₂ = 0 — boundary condition of first-order propagation (Theorem 4.1)
          </div>
        </div>
      </div>

      <Plot
        funcs={[
          {fn:fnV, color:'#5ac8fa', width:2},
          {fn:fnE, color:'#ff9f0a', width:2},
        ]}
        xMin={0.2} xMax={3.0} yMin={-5} yMax={8}
        W={480} H={200}
        title={`f(x) = ${pr.label} (blue) and f′(x) computed via dual numbers (orange)`}
      />

      <div style={{marginTop:14,padding:'10px 14px',background:'#0c0c1a',border:'1px solid #1a1a38',borderRadius:6,fontSize:12,color:'#6060aa',lineHeight:1.65}}>
        <strong style={{color:'#8888bb'}}>Flux propagation (Section 8):</strong>{' '}
        In iterative solvers, the same principle applies across fixed-point iterations:
        seed the parameter with flux 1.0, iterate until convergence, and the flux at the
        fixed point is exactly the implicit derivative — computed in constant 48 bytes,
        regardless of iteration depth. No computation graph. No Jacobian inversion.
      </div>
    </div>
  );
}

// ── SECTION 6: Propagation Hierarchy ────────────────────────────────────────
function PropagationHierarchy() {
  const [hovRow, setHovRow] = useState(null);

  const rows = [
    {carrier:'{0,1}',         gamma:'Full Boolean',               system:'Classical logic',       forced:'LNC, LEM, Modus Ponens as coherence conditions',               type:'A'},
    {carrier:'ℕ',             gamma:'Successor + add',            system:'Arithmetic',            forced:'Peano axioms as propagation step counts',                       type:'A'},
    {carrier:'ℤ',             gamma:'ℕ + reconfiguration dir.',  system:'Integers',              forced:'Additive inverses as signed reconfiguration steps',             type:'A'},
    {carrier:'ℚ',             gamma:'ℤ + ratio (Stern-Brocot)',  system:'Rationals',             forced:'Density; mediant = minimum-load fraction between two rationals', type:'A'},
    {carrier:'ℝ',             gamma:'ℚ + coherence pressure',    system:'Reals',                 forced:'Cauchy completion: √2 generates Cauchy seq converging outside ℚ',type:'B'},
    {carrier:'ℂ',             gamma:'ℝ + G²=G_neg demand',       system:'Complex numbers',       forced:'G_rot forced; sin/cos emerge as G_diff⁴ fixed points in ℂ→ℝ',   type:'D'},
    {carrier:'Dual(ℝ)',       gamma:'ℝ + ε, ε²=0',               system:'Calculus (1st order)',  forced:'Leibniz rule; FTC as G_diff∘G_int=G_id (≡ ¬¬P=P in logic)',      type:'A'},
    {carrier:'n-Dual(ℝ)',     gamma:'ℝ + n commuting dirs',      system:'Taylor series',         forced:'1/k! from commutativity; if drag≠0 → 1/[k]_q! instead',         type:'A'},
    {carrier:'Prob. carrier', gamma:'Convolution',                system:'Probability',           forced:'Gaussian = max-entropy coherence attractor (CLT is 2nd Law)',    type:'C'},
    {carrier:'Partial-drag',  gamma:'ℝ + q-deformed step',       system:'q-Calculus',            forced:'[n]_q=(qⁿ−1)/(q−1); at q→1 recovers standard counting',          type:'B'},
    {carrier:'{0,1}+state',   gamma:'Linear gradient family',    system:'Linear logic',          forced:'Consumption state: each pattern available exactly once',          type:'A'},
    {carrier:'{0,1}+tags',    gamma:'Relevance gradient',        system:'Relevance logic',       forced:'history(P)∩history(Q)≠∅ required for co-propagation',            type:'A'},
    {carrier:'Solvable group',gamma:'Abelian quotient chain',    system:'Radical solutions',     forced:'Zero drag at each quotient level → solvable by radicals (deg≤4)',  type:'A'},
    {carrier:'A₅ carrier',    gamma:'Non-abelian (A₅ simple)',   system:'Quintic',               forced:'Irreducible non-commutative drag → no radical chain exists',       type:'C'},
    {carrier:'TM states',     gamma:'Execution history G_step',  system:'Computation / Halting', forced:'Halting=fixed point; H(H)⊇H(H) → L_d=2^d→∞ (Observation 2.2)',   type:'C'},
    {carrier:'Function space',gamma:'Euler-Lagrange δS=0',      system:'Physics (mechanics)',   forced:'Noether: gradient families fixing S ↔ conserved quantities',       type:'C'},
    {carrier:'Mult. carrier', gamma:'G_× (primes as seeds)',     system:'Number theory',         forced:'FTA = unique seed decomposition; PNT via ζ coherence structure',   type:'C'},
  ];

  const typeInfo = {
    A:{color:'#5ac8fa',label:'Derives',    desc:'Mechanism independently generates the structure — no import'},
    B:{color:'#ff9f0a',label:'Motivates', desc:'Explains why structure is needed; natural construction follows'},
    C:{color:'#30d158',label:'Reveals',   desc:'Reframes a known result to make structural role visible'},
    D:{color:'#bf5af2',label:'Questions', desc:'Asks the right question, forcing carrier extension'},
  };

  return (
    <div>
      <h2 style={{color:'#c0c0ff',fontSize:18,margin:'0 0 6px'}}>The Propagation Hierarchy</h2>
      <p style={{color:'#7070aa',fontSize:13,margin:'0 0 14px',lineHeight:1.65}}>
        Each level of mathematics is forced by demands of the previous.
        The single operator P/G→Q acts across every carrier.
        Every axiom is the boundary condition of a specific propagation regime.
      </p>

      <div style={{display:'flex',gap:8,flexWrap:'wrap',marginBottom:14}}>
        {Object.entries(typeInfo).map(([t,v])=>(
          <div key={t} style={{
            padding:'5px 12px',background:'#0c0c1a',
            border:`1px solid ${v.color}44`,borderLeft:`3px solid ${v.color}`,
            borderRadius:4,fontSize:11,
          }}>
            <span style={{color:v.color,fontWeight:'bold'}}>Type {t}: {v.label}</span>
            <span style={{color:'#404068'}}> — {v.desc}</span>
          </div>
        ))}
      </div>

      <div style={{overflowX:'auto'}}>
        <table style={{width:'100%',borderCollapse:'collapse',fontSize:12}}>
          <thead>
            <tr>
              {['Carrier V','Gradient Family Γ','System','What is Forced','Type'].map(h=>(
                <th key={h} style={{padding:'8px 10px',color:'#404068',textAlign:'left',
                  fontWeight:'normal',borderBottom:'1px solid #1a1a38',whiteSpace:'nowrap'}}>
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row,i)=>{
              const ti=typeInfo[row.type];
              return (
                <tr key={i}
                  onMouseEnter={()=>setHovRow(i)}
                  onMouseLeave={()=>setHovRow(null)}
                  style={{
                    borderBottom:'1px solid #10102a',
                    background: hovRow===i?'#0e0e28':'transparent',
                    transition:'background 0.1s',cursor:'default',
                  }}>
                  <td style={{padding:'7px 10px',color:'#c0c0ff',fontFamily:'monospace',whiteSpace:'nowrap'}}>{row.carrier}</td>
                  <td style={{padding:'7px 10px',color:'#6060aa',whiteSpace:'nowrap'}}>{row.gamma}</td>
                  <td style={{padding:'7px 10px',color:'#8888cc',whiteSpace:'nowrap'}}>{row.system}</td>
                  <td style={{padding:'7px 10px',color:'#555585',fontSize:11,lineHeight:1.5}}>{row.forced}</td>
                  <td style={{padding:'7px 10px'}}>
                    <span style={{
                      padding:'2px 8px',
                      background:ti.color+'20',border:`1px solid ${ti.color}44`,
                      color:ti.color,borderRadius:3,fontWeight:'bold',fontSize:11,
                    }}>{row.type}</span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <div style={{marginTop:16,padding:'14px 18px',background:'#0c0c1a',border:'1px solid #1a1a38',borderRadius:6}}>
        <div style={{fontSize:13,color:'#7070aa',lineHeight:1.75}}>
          <strong style={{color:'#c0c0ff'}}>Mathematical truth as carrier-relative coherence.</strong>{' '}
          A theorem is a pattern that propagation cannot destroy within its carrier.
          The constants e, π, φ are the least unstable structures.
          Impossibility results (Halting, Gödel, quintic) are coherence failures — demand exceeds what the carrier provides.
          Incompleteness is not defeat: it is the same pressure that generates ℝ from ℚ, or ℂ from ℝ.
          The Gödel sentence G is not coherent in C, but is coherent in the meta-carrier that reasons about C.
          Every sufficiently expressive system generates patterns whose coherence demands a larger carrier.{' '}
          <strong style={{color:'#9090cc'}}>P/G → Q.</strong>
        </div>
      </div>
    </div>
  );
}

// ── Main shell ───────────────────────────────────────────────────────────────
const TABS = [
  {label:'G_diff^n Orbits',   C: GdiffOrbits},
  {label:'Three Constants',   C: ThreeConstants},
  {label:'Logistic Map',      C: LogisticMap},
  {label:'Mandelbrot',        C: MandelbrotSet},
  {label:'Dual Numbers',      C: DualNumbers},
  {label:'Hierarchy',         C: PropagationHierarchy},
];

export default function MathesisExplorer() {
  const [tab, setTab] = useState(0);
  const {C:Tab} = TABS[tab];

  return (
    <div style={{
      background:'#09090f', color:'#e0e0ff',
      minHeight:'100vh', fontFamily:'Georgia, serif',
    }}>
      {/* Header */}
      <div style={{padding:'14px 20px 0',borderBottom:'1px solid #141430'}}>
        <div style={{
          fontSize:10,letterSpacing:'0.22em',color:'#2a2a60',
          marginBottom:4,textTransform:'uppercase',
        }}>
          Mathesis Universalis — Differential Propagation · Interactive Exploration
        </div>
        <div style={{display:'flex',gap:2,flexWrap:'wrap',marginTop:10}}>
          {TABS.map(({label},i)=>(
            <button key={i} onClick={()=>setTab(i)} style={{
              padding:'7px 14px', fontSize:12,
              background: tab===i?'#0f0f2a':'transparent',
              border:`1px solid ${tab===i?'#252550':'transparent'}`,
              borderBottom:`1px solid ${tab===i?'#09090f':'#141430'}`,
              color: tab===i?'#9898ee':'#38385a',
              cursor:'pointer', borderRadius:'4px 4px 0 0',
              marginBottom:'-1px', fontFamily:'Georgia, serif',
              transition:'color 0.15s',
            }}>
              {label}
            </button>
          ))}
        </div>
      </div>

      {/* Content */}
      <div style={{padding:'24px 20px', maxWidth:780}}>
        <Tab/>
      </div>
    </div>
  );
}
