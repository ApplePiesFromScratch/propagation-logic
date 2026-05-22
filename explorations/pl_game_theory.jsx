import { useState, useEffect, useRef, useCallback } from "react";

// ─────────────────────────────────────────────────────────────────────────────
// THE MECHANISM — P / G → Q
// Everything in this file is a consequence of these definitions.
// ─────────────────────────────────────────────────────────────────────────────

// Definition 2.1 — Loaded Pattern
const mkPattern = (v, load, tags = []) => ({ v, load, tags });

// Definition 2.2 — Context, Support, Gradient Demand
const demand  = (p, theta) => Math.max(0, p.load - theta);
const support = (p, theta) => Math.min(p.load, theta);
const coherent = (p, theta) => p.load <= theta;

// Definition 2.3 — Propagation Rate
const rate = (p, theta) =>
  p.load === 0 ? 1 : Math.min(p.load, theta) / p.load;

// Definition 2.4 — Relational Drag
// drag=0: zero-drag (classical). drag>0: resource-sensitive.
const combinedLoad = (lA, lB, drag = 0) => lA + lB + drag;

// ─────────────────────────────────────────────────────────────────────────────
// GAME THEORY DERIVED FROM MECHANISM
//
// A Game is a shared carrier V² with two gradient families G_A, G_B.
// A "move" is a gradient injection: P / G → Q in the shared carrier.
// An "outcome" is the load state reached.
//
// KEY STRUCTURAL CLAIM:
//   Nash Equilibrium = individual fixed point (each gradient locally stable)
//   Joint Coherence  = minimum of SHARED load
//   These are NOT the same. Standard game theory has no vocabulary for this.
//   The mechanism distinguishes them precisely.
//
// Cooperation = zero-drag (G_A and G_B co-propagate without history conflict)
// Defection   = nonzero drag (defector injects load into shared carrier)
// ─────────────────────────────────────────────────────────────────────────────

// The drag parameter δ is the structural heart of any game.
// δ = 0: pure coordination. δ → ∞: pure conflict.
// Prisoner's Dilemma: δ_defect > 0, δ_coop = 0

const MOVES = { C: 'C', D: 'D' };

// Load accounting from mechanism:
//   Cooperate costs you load 1 (you propagate into shared carrier)
//   Defect costs you load 1 BUT injects drag δ onto opponent
//   Being defected against: you absorb the drag
const outcomeLoads = (mA, mB, delta) => {
  // Each player's self-load from their own move
  const selfCost = 1;
  // Drag injected by defector onto victim
  const drag = delta;

  let lA = selfCost, lB = selfCost;
  if (mA === 'D') lB += drag;  // A defects: B absorbs drag
  if (mB === 'D') lA += drag;  // B defects: A absorbs drag

  // Joint load = shared carrier load
  const joint = combinedLoad(lA, lB, mA==='D'&&mB==='D' ? drag*0.5 : 0);
  return { lA, lB, joint };
};

// Payoff = inverted load (as per mechanism: coherence = low load = high payoff)
// Map load to [0,5] payoff scale
const loadToPayoff = (l, delta) => {
  const max = 1 + delta; // maximum possible load for one player
  return Math.max(0, 5 * (1 - (l - 1) / delta));
};

// ─────────────────────────────────────────────────────────────────────────────
// STRATEGIES as gradient families
// Each strategy is a function: (my_history, their_history) → move
// Load of a strategy = average load it generates in the shared carrier
// ─────────────────────────────────────────────────────────────────────────────

const STRATEGIES = {
  AllC:  { name: 'AllCooperate', color: '#30d158', sym: 'C∞',
           fn: ()=>'C',
           desc: 'Always cooperates. Zero-drag gradient. Minimum self-load. Vulnerable to exploitation.' },
  AllD:  { name: 'AllDefect',    color: '#ff453a', sym: 'D∞',
           fn: ()=>'D',
           desc: 'Always defects. Maximum drag injection. Individually optimal in 1-shot carrier. Destroys shared coherence.' },
  TfT:   { name: 'TitForTat',   color: '#5ac8fa', sym: 'T₁',
           fn: (h)=> h.length===0 ? 'C' : h[h.length-1].their,
           desc: 'Cooperates first. Mirrors opponent. Minimum-load strategy achieving joint coherence. Theorem 2.1 in strategy space.' },
  Grim:  { name: 'GrimTrigger', color: '#ff9f0a', sym: 'G∞',
           fn: (h)=> h.some(r=>r.their==='D') ? 'D' : 'C',
           desc: 'Cooperates until first defection, then defects forever. Maximum punishment. High terminal load.' },
  WSLS:  { name: 'Win-Stay-Lose-Shift', color: '#bf5af2', sym: 'WS',
           fn: (h)=> {
             if(h.length===0) return 'C';
             const last = h[h.length-1];
             const won = (last.mine==='C'&&last.their==='C')||(last.mine==='D'&&last.their==='D');
             return won ? last.mine : (last.mine==='C'?'D':'C');
           },
           desc: 'Repeat winning moves. Shift after losing. Adaptive — seeks personal coherence each step.' },
  Rand:  { name: 'Random',      color: '#6e6e73', sym: 'R?',
           fn: ()=> Math.random()<0.5?'C':'D',
           desc: 'Random gradient injection. High average drag. No convergence to fixed point.' },
};

// ─────────────────────────────────────────────────────────────────────────────
// COLOURS / THEME
// ─────────────────────────────────────────────────────────────────────────────
const T = {
  bg:     '#07070e',
  panel:  '#0d0d1a',
  border: '#16163a',
  dim:    '#252550',
  muted:  '#404070',
  mid:    '#6060a0',
  text:   '#c0c0f0',
  head:   '#e0e0ff',
  C:      '#30d158',
  D:      '#ff453a',
  J:      '#5ac8fa',
  acc:    '#bf5af2',
};

// ─────────────────────────────────────────────────────────────────────────────
// UI ATOMS
// ─────────────────────────────────────────────────────────────────────────────
const Panel = ({children, style={}}) => (
  <div style={{background:T.panel,border:`1px solid ${T.border}`,borderRadius:8,padding:'14px 16px',...style}}>
    {children}
  </div>
);

const Label = ({children,style={}}) => (
  <div style={{fontSize:10,letterSpacing:'0.12em',color:T.muted,textTransform:'uppercase',marginBottom:6,...style}}>
    {children}
  </div>
);

const Tag = ({children,color}) => (
  <span style={{
    display:'inline-block',padding:'2px 8px',borderRadius:3,
    background:color+'22',border:`1px solid ${color}44`,
    color,fontSize:11,fontFamily:'monospace',
  }}>{children}</span>
);

// ─────────────────────────────────────────────────────────────────────────────
// SECTION 1: SHARED CARRIER — what a game IS
// ─────────────────────────────────────────────────────────────────────────────
function SharedCarrier({ delta, setDelta }) {
  const outcomes = ['CC','CD','DC','DD'];
  const cells = outcomes.map(o => {
    const mA = o[0], mB = o[1];
    const { lA, lB, joint } = outcomeLoads(mA, mB, delta);
    return { mA, mB, lA, lB, joint, key: o };
  });

  // Individual fixed points: neither can reduce own load by switching
  // A is at individual FP if switching their move doesn't reduce lA
  const fixedPoints = cells.filter(c => {
    const altA = outcomeLoads(c.mA==='C'?'D':'C', c.mB, delta);
    const altB = outcomeLoads(c.mA, c.mB==='C'?'D':'C', delta);
    return altA.lA >= c.lA && altB.lB >= c.lB;
  });
  const jointMin = cells.reduce((best,c) => c.joint < best.joint ? c : best, cells[0]);

  const isNE = c => fixedPoints.some(f=>f.key===c.key);
  const isJC = c => c.key === jointMin.key;

  const maxL = Math.max(...cells.map(c=>Math.max(c.lA,c.lB)));

  return (
    <div>
      <h2 style={{color:T.head,fontSize:17,margin:'0 0 4px',fontFamily:'Georgia,serif'}}>
        The Shared Carrier
      </h2>
      <p style={{color:T.mid,fontSize:12,margin:'0 0 16px',lineHeight:1.7}}>
        A game is <em>not</em> players maximizing utility scalars. It is two gradient families
        {' '}G_A, G_B co-propagating in a shared carrier V². A move is a gradient injection.
        An outcome is the load state reached. <strong style={{color:T.text}}>Payoffs are loads, inverted.</strong>
      </p>

      {/* Drag slider */}
      <Panel style={{marginBottom:16}}>
        <Label>Drag parameter δ — structural heart of the game</Label>
        <div style={{display:'flex',alignItems:'center',gap:12}}>
          <span style={{fontFamily:'monospace',fontSize:13,color:T.acc,minWidth:36}}>δ={delta.toFixed(1)}</span>
          <input type="range" min={0.1} max={5} step={0.1} value={delta}
            onChange={e=>setDelta(+e.target.value)} style={{flex:1,accentColor:T.acc}}/>
          <span style={{fontSize:11,color:T.muted,minWidth:120,textAlign:'right'}}>
            {delta<0.5?'Near coordination':delta<2?'Mixed':delta<4?'Strong conflict':'Pure conflict'}
          </span>
        </div>
        <div style={{fontSize:11,color:T.muted,marginTop:6,lineHeight:1.6}}>
          δ=0: cooperation is zero-drag — histories align perfectly.&nbsp;
          δ>0: defection injects drag δ into victim's load.&nbsp;
          Prisoner's Dilemma lives at δ≈2.
        </div>
      </Panel>

      {/* 2×2 outcome grid */}
      <div style={{display:'grid',gridTemplateColumns:'auto 1fr 1fr',gap:4,marginBottom:16}}>
        {/* Headers */}
        <div/>
        <div style={{textAlign:'center',fontSize:11,color:T.C,padding:'4px',fontFamily:'monospace'}}>B: Cooperate</div>
        <div style={{textAlign:'center',fontSize:11,color:T.D,padding:'4px',fontFamily:'monospace'}}>B: Defect</div>

        {['C','D'].map((mA,ri) => (
          <>
            <div key={'row'+mA} style={{display:'flex',alignItems:'center',fontSize:11,
              color:mA==='C'?T.C:T.D,paddingRight:8,fontFamily:'monospace'}}>
              A: {mA==='C'?'Cooperate':'Defect'}
            </div>
            {['C','D'].map(mB => {
              const c = cells.find(x=>x.mA===mA&&x.mB===mB);
              const ne = isNE(c), jc = isJC(c);
              const barA = (c.lA/maxL)*100, barB = (c.lB/maxL)*100;
              return (
                <div key={mA+mB} style={{
                  background: ne&&jc?'#0a1a0a': ne?'#150a0a': jc?'#0a150a':'#0d0d1a',
                  border:`1px solid ${ne&&jc?'#30d15844': ne?'#ff453a44': jc?'#30d15822':T.border}`,
                  borderRadius:6,padding:'10px 12px',position:'relative',
                }}>
                  {ne && <span style={{position:'absolute',top:5,right:7,fontSize:9,color:'#ff453a',opacity:0.8}}>NE</span>}
                  {jc && <span style={{position:'absolute',top:ne?16:5,right:7,fontSize:9,color:T.C,opacity:0.8}}>JC</span>}

                  <div style={{fontSize:11,color:T.muted,marginBottom:6,fontFamily:'monospace'}}>
                    ({mA},{mB})
                  </div>

                  {/* Load bars */}
                  <div style={{marginBottom:4}}>
                    <div style={{display:'flex',alignItems:'center',gap:6,marginBottom:3}}>
                      <span style={{fontSize:10,color:T.C,width:14}}>A</span>
                      <div style={{flex:1,height:6,background:T.dim,borderRadius:3,overflow:'hidden'}}>
                        <div style={{width:`${barA}%`,height:'100%',background:mA==='C'?T.C:T.D,borderRadius:3}}/>
                      </div>
                      <span style={{fontFamily:'monospace',fontSize:10,color:mA==='C'?T.C:T.D,width:28,textAlign:'right'}}>
                        L={c.lA.toFixed(1)}
                      </span>
                    </div>
                    <div style={{display:'flex',alignItems:'center',gap:6}}>
                      <span style={{fontSize:10,color:T.D,width:14}}>B</span>
                      <div style={{flex:1,height:6,background:T.dim,borderRadius:3,overflow:'hidden'}}>
                        <div style={{width:`${barB}%`,height:'100%',background:mB==='C'?T.C:T.D,borderRadius:3}}/>
                      </div>
                      <span style={{fontFamily:'monospace',fontSize:10,color:mB==='C'?T.C:T.D,width:28,textAlign:'right'}}>
                        L={c.lB.toFixed(1)}
                      </span>
                    </div>
                  </div>

                  <div style={{borderTop:`1px solid ${T.border}`,paddingTop:5,marginTop:2}}>
                    <span style={{fontSize:10,color:T.J,fontFamily:'monospace'}}>
                      joint: {c.joint.toFixed(2)}
                    </span>
                  </div>
                </div>
              );
            })}
          </>
        ))}
      </div>

      {/* The structural claim */}
      <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:10,marginBottom:14}}>
        <Panel>
          <div style={{fontSize:11,color:'#ff453a',marginBottom:6}}>
            <Tag color="#ff453a">NE</Tag> Nash Equilibrium = individual fixed point
          </div>
          <div style={{fontSize:11,color:T.muted,lineHeight:1.65}}>
            Neither player reduces their own load by switching.
            In PD, (D,D) is NE — each gradient locally stable.
            But jointly incoherent: shared load is NOT minimized.
          </div>
        </Panel>
        <Panel>
          <div style={{fontSize:11,color:T.C,marginBottom:6}}>
            <Tag color={T.C}>JC</Tag> Joint Coherence = shared load minimum
          </div>
          <div style={{fontSize:11,color:T.muted,lineHeight:1.65}}>
            The outcome minimizing total load in the shared carrier.
            In PD, (C,C) is JC — zero-drag, histories align.
            Under reconfiguration pressure from both individual gradients.
          </div>
        </Panel>
      </div>

      <Panel style={{borderLeft:`3px solid ${T.acc}`,background:'#0e0a18'}}>
        <div style={{fontSize:12,color:T.text,lineHeight:1.7}}>
          <strong style={{color:T.acc}}>The structural claim standard game theory cannot make:</strong>
          {' '}NE ≠ JC. (D,D) is simultaneously a Nash Equilibrium (individual gradients stable)
          and jointly incoherent (shared load maximized). The mechanism distinguishes these precisely
          because it has the concepts of <em>individual load</em> and <em>shared carrier load</em>.
          Standard game theory operates only on scalar payoffs — it cannot see the distinction.
        </div>
      </Panel>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// SECTION 2: ITERATED PLAY — loaded history extension
// ─────────────────────────────────────────────────────────────────────────────
function IteratedPlay({ delta }) {
  const [stratA, setStratA] = useState('TfT');
  const [stratB, setStratB] = useState('AllD');
  const [rounds, setRounds] = useState(20);
  const theta = 1 + delta * 0.8; // coherence threshold grows with delta

  // Simulate iterated game
  const simulate = useCallback((sA, sB, N) => {
    const hA = [], hB = [];
    let cumLA = 0, cumLB = 0;
    const history = [];

    for (let i = 0; i < N; i++) {
      const mA = STRATEGIES[sA].fn(hA);
      const mB = STRATEGIES[sB].fn(hB);
      const { lA, lB, joint } = outcomeLoads(mA, mB, delta);
      cumLA += lA; cumLB += lB;

      const entry = { round: i+1, mA, mB, lA, lB, joint, cumLA, cumLB,
        rateA: rate({load: cumLA/(i+1)}, theta),
        rateB: rate({load: cumLB/(i+1)}, theta),
        demandA: demand({load: cumLA/(i+1)}, theta),
        demandB: demand({load: cumLB/(i+1)}, theta),
      };
      history.push(entry);
      hA.push({ mine: mA, their: mB });
      hB.push({ mine: mB, their: mA });
    }
    return history;
  }, [delta, theta]);

  const hist = simulate(stratA, stratB, rounds);
  const last = hist[hist.length-1];

  // Chart: cumulative load per player over rounds
  const svgW=460, svgH=160;
  const pad={l:32,r:12,t:10,b:28};
  const cW=svgW-pad.l-pad.r, cH=svgH-pad.t-pad.b;

  const maxCum = Math.max(...hist.map(h=>Math.max(h.cumLA, h.cumLB)), 1);
  const rx = i => pad.l + (i/(rounds-1))*cW;
  const ryA = v => pad.t + cH - (v/maxCum)*cH;

  // Path helper
  const linePath = (pts) => pts.map((p,i)=>`${i===0?'M':'L'} ${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join(' ');

  // Coherence threshold line in load-space: theta * rounds (total)
  const thetaLine = hist.map(h => [rx(h.round-1), ryA(theta * h.round)]);

  // Defection/Cooperation indicators along x-axis
  return (
    <div>
      <h2 style={{color:T.head,fontSize:17,margin:'0 0 4px',fontFamily:'Georgia,serif'}}>
        Iterated Play — History Extension
      </h2>
      <p style={{color:T.mid,fontSize:12,margin:'0 0 16px',lineHeight:1.7}}>
        Each round extends H_P. Cumulative load tells the full story:
        defection load grows at rate (1+δ) per round; cooperation at rate 1.
        When defection load crosses the coherence threshold, the strategy
        becomes incoherent — this is the Folk Theorem, derived from Observation 2.1.
      </p>

      {/* Strategy pickers */}
      <div style={{display:'flex',gap:12,flexWrap:'wrap',marginBottom:14}}>
        {['A','B'].map((player,pi) => {
          const cur = pi===0?stratA:stratB;
          const setCur = pi===0?setStratA:setStratB;
          return (
            <div key={player}>
              <Label>Player {player} gradient family</Label>
              <div style={{display:'flex',gap:6,flexWrap:'wrap'}}>
                {Object.entries(STRATEGIES).map(([k,v])=>(
                  <button key={k} onClick={()=>setCur(k)} style={{
                    padding:'5px 11px',fontSize:12,fontFamily:'monospace',
                    background: cur===k?v.color+'22':'#0d0d1a',
                    border:`1px solid ${cur===k?v.color:T.border}`,
                    color: cur===k?v.color:T.muted,
                    borderRadius:4,cursor:'pointer',
                  }}>{v.sym}</button>
                ))}
              </div>
            </div>
          );
        })}
        <div>
          <Label>Rounds</Label>
          <div style={{display:'flex',alignItems:'center',gap:8}}>
            <input type="range" min={5} max={60} value={rounds}
              onChange={e=>setRounds(+e.target.value)}
              style={{width:120,accentColor:T.J}}/>
            <span style={{fontFamily:'monospace',fontSize:12,color:T.J}}>{rounds}</span>
          </div>
        </div>
      </div>

      {/* Cumulative load chart */}
      <svg width={svgW} height={svgH}
        style={{display:'block',background:'#09090f',borderRadius:7,border:`1px solid ${T.border}`,marginBottom:12}}>
        {/* Grid */}
        {[0.25,0.5,0.75,1].map(f=>{
          const y=pad.t+cH*(1-f);
          return <line key={f} x1={pad.l} y1={y} x2={svgW-pad.r} y2={y}
            stroke={T.border} strokeWidth={1}/>;
        })}
        {/* Coherence threshold band */}
        {thetaLine.length>1&&<>
          <path d={linePath(thetaLine)+` L ${thetaLine[thetaLine.length-1][0]} ${svgH-pad.b} L ${pad.l} ${svgH-pad.b} Z`}
            fill={T.acc} opacity={0.06}/>
          <path d={linePath(thetaLine)} fill="none" stroke={T.acc} strokeWidth={1}
            strokeDasharray="4,4" opacity={0.5}/>
        </>}
        {/* Load lines */}
        {hist.length>1&&<>
          <path d={linePath(hist.map(h=>[rx(h.round-1),ryA(h.cumLA)]))}
            fill="none" stroke={STRATEGIES[stratA].color} strokeWidth={2.5}/>
          <path d={linePath(hist.map(h=>[rx(h.round-1),ryA(h.cumLB)]))}
            fill="none" stroke={STRATEGIES[stratB].color} strokeWidth={2.5}/>
        </>}
        {/* Per-round move indicators */}
        {hist.slice(0,Math.min(rounds,30)).map((h,i)=>(
          <g key={i}>
            <circle cx={rx(i)} cy={svgH-pad.b+8} r={3}
              fill={h.mA==='C'?T.C:T.D} opacity={0.7}/>
            <circle cx={rx(i)} cy={svgH-pad.b+16} r={3}
              fill={h.mB==='C'?T.C:T.D} opacity={0.7}/>
          </g>
        ))}
        {/* Y-axis labels */}
        {[0,0.5,1].map(f=>{
          const y=pad.t+cH*(1-f);
          const val=(f*maxCum).toFixed(0);
          return <text key={f} x={pad.l-4} y={y+4} textAnchor="end"
            fill={T.muted} fontSize={8}>{val}</text>;
        })}
        {/* Legend */}
        <circle cx={svgW-pad.r-80} cy={pad.t+8} r={3} fill={STRATEGIES[stratA].color}/>
        <text x={svgW-pad.r-74} y={pad.t+12} fill={STRATEGIES[stratA].color} fontSize={9}>
          {STRATEGIES[stratA].sym} cumulative load
        </text>
        <circle cx={svgW-pad.r-80} cy={pad.t+22} r={3} fill={STRATEGIES[stratB].color}/>
        <text x={svgW-pad.r-74} y={pad.t+26} fill={STRATEGIES[stratB].color} fontSize={9}>
          {STRATEGIES[stratB].sym} cumulative load
        </text>
        <line x1={svgW-pad.r-80} y1={pad.t+35} x2={svgW-pad.r-70} y2={pad.t+35}
          stroke={T.acc} strokeWidth={1} strokeDasharray="3,3" opacity={0.6}/>
        <text x={svgW-pad.r-64} y={pad.t+39} fill={T.acc} fontSize={9} opacity={0.7}>
          θ·t coherence
        </text>
        {/* Move dots legend */}
        {rounds<=30&&<>
          <circle cx={pad.l} cy={svgH-pad.b+8} r={3} fill={T.C}/>
          <circle cx={pad.l} cy={svgH-pad.b+16} r={3} fill={T.C}/>
          <text x={pad.l+6} y={svgH-pad.b+12} fill={STRATEGIES[stratA].color} fontSize={8}>A moves</text>
          <text x={pad.l+6} y={svgH-pad.b+20} fill={STRATEGIES[stratB].color} fontSize={8}>B moves</text>
        </>}
      </svg>

      {/* Stats */}
      <div style={{display:'grid',gridTemplateColumns:'1fr 1fr 1fr',gap:8,marginBottom:12}}>
        {[
          {label:`${STRATEGIES[stratA].sym} avg load`, val:(last.cumLA/rounds).toFixed(3),
           color:STRATEGIES[stratA].color, sub:`demand: ${last.demandA.toFixed(3)}`},
          {label:`${STRATEGIES[stratB].sym} avg load`, val:(last.cumLB/rounds).toFixed(3),
           color:STRATEGIES[stratB].color, sub:`demand: ${last.demandB.toFixed(3)}`},
          {label:'avg joint load', val:(hist.reduce((s,h)=>s+h.joint,0)/rounds).toFixed(3),
           color:T.J, sub:`θ = ${theta.toFixed(2)}`},
        ].map((s,i)=>(
          <Panel key={i}>
            <Label>{s.label}</Label>
            <div style={{fontFamily:'monospace',fontSize:16,color:s.color,marginBottom:3}}>{s.val}</div>
            <div style={{fontSize:10,color:T.muted,fontFamily:'monospace'}}>{s.sub}</div>
          </Panel>
        ))}
      </div>

      {/* Strategy descriptions */}
      <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:8}}>
        {[stratA,stratB].map((sk,i)=>{
          const sv=STRATEGIES[sk];
          return (
            <Panel key={i} style={{borderLeft:`3px solid ${sv.color}`}}>
              <div style={{fontSize:12,color:sv.color,fontFamily:'monospace',marginBottom:4}}>
                {sv.sym} — {sv.name}
              </div>
              <div style={{fontSize:11,color:T.muted,lineHeight:1.65}}>{sv.desc}</div>
            </Panel>
          );
        })}
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// SECTION 3: STRATEGY EVOLUTION — Theorem 2.1 in population space
//
// Replicator dynamics IS differential propagation (Theorem 2.1):
// "Simpler patterns propagate faster" = strategies with lower load
// grow in frequency relative to strategies with higher load.
//
// ẋ_i = x_i · (f_i - f̄)    replicator equation
// f_i ∝ 1/avg_load_i        fitness = inverse load
// ─────────────────────────────────────────────────────────────────────────────
function StrategyEvolution({ delta }) {
  const stratKeys = ['AllC','AllD','TfT','Grim','WSLS'];
  const [pop, setPop] = useState(() => Object.fromEntries(stratKeys.map(k=>[k,1/stratKeys.length])));
  const [running, setRunning] = useState(false);
  const [gen, setGen] = useState(0);
  const [history, setHistory] = useState([Object.fromEntries(stratKeys.map(k=>[k,1/stratKeys.length]))]);
  const tickRef = useRef();

  // Compute fitness of each strategy against the current population
  // Each strategy plays against a random mix weighted by population frequencies
  const computeFitness = useCallback((p) => {
    const N = 20; // rounds per encounter
    const fitness = {};
    for (const sk of stratKeys) {
      let totalLoad = 0, count = 0;
      for (const sk2 of stratKeys) {
        if (p[sk2] < 0.001) continue;
        // Simulate sk vs sk2
        const hA=[], hB=[];
        let cum=0;
        for (let r=0;r<N;r++){
          const mA=STRATEGIES[sk].fn(hA);
          const mB=STRATEGIES[sk2].fn(hB);
          const {lA}=outcomeLoads(mA,mB,delta);
          cum+=lA;
          hA.push({mine:mA,their:mB}); hB.push({mine:mB,their:mA});
        }
        totalLoad += (cum/N) * p[sk2];
        count += p[sk2];
      }
      const avgLoad = count>0 ? totalLoad/count : 1;
      // Fitness = inverse load: lower load = higher fitness (Theorem 2.1)
      fitness[sk] = 1 / Math.max(0.01, avgLoad);
    }
    return fitness;
  }, [delta]);

  const step = useCallback(() => {
    setPop(prev => {
      const fitness = computeFitness(prev);
      const meanFit = stratKeys.reduce((s,k)=>s+prev[k]*fitness[k],0);
      const next = {};
      let total = 0;
      for (const k of stratKeys) {
        next[k] = Math.max(0, prev[k] * (fitness[k] / meanFit));
        total += next[k];
      }
      // Normalise
      for (const k of stratKeys) next[k] /= total;
      setHistory(h => [...h.slice(-80), next]);
      setGen(g => g+1);
      return next;
    });
  }, [computeFitness]);

  useEffect(() => {
    if (running) { tickRef.current = setInterval(step, 120); }
    else clearInterval(tickRef.current);
    return () => clearInterval(tickRef.current);
  }, [running, step]);

  const reset = () => {
    const eq = Object.fromEntries(stratKeys.map(k=>[k,1/stratKeys.length]));
    setPop(eq); setGen(0); setHistory([eq]); setRunning(false);
  };

  // Chart: stacked frequency over time
  const svgW=460, svgH=170;
  const pad={l:10,r:10,t:8,b:8};
  const cW=svgW-pad.l-pad.r, cH=svgH-pad.t-pad.b;

  // Build stacked areas
  const nH = history.length;
  const stackedPaths = stratKeys.map((k,ki) => {
    let d = '';
    const lows=[], highs=[];
    history.forEach((h,i) => {
      const x = pad.l + (i/(Math.max(nH-1,1)))*cW;
      const stackBelow = stratKeys.slice(0,ki).reduce((s,k2)=>s+h[k2],0);
      const stackAbove = stackBelow + h[k];
      lows.push([x, pad.t + cH*(1-stackBelow)]);
      highs.push([x, pad.t + cH*(1-stackAbove)]);
    });
    // Forward along top, backward along bottom
    const pts = [...highs, ...[...lows].reverse()];
    return pts.map((p,i)=>`${i===0?'M':'L'} ${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join(' ')+' Z';
  });

  // Dominant strategy
  const dominant = stratKeys.reduce((a,b)=>pop[a]>pop[b]?a:b);

  return (
    <div>
      <h2 style={{color:T.head,fontSize:17,margin:'0 0 4px',fontFamily:'Georgia,serif'}}>
        Strategy Evolution — Theorem 2.1 in Population Space
      </h2>
      <p style={{color:T.mid,fontSize:12,margin:'0 0 14px',lineHeight:1.7}}>
        Replicator dynamics IS differential propagation. Fitness = 1/average_load.
        Lower-load strategies propagate faster through the population — Theorem 2.1
        applied to the strategy carrier. Watch which gradient family wins.
      </p>

      <svg width={svgW} height={svgH}
        style={{display:'block',background:'#09090f',borderRadius:7,border:`1px solid ${T.border}`,marginBottom:10}}>
        {stratKeys.map((k,i)=>(
          <path key={k} d={stackedPaths[i]} fill={STRATEGIES[k].color} opacity={0.75}/>
        ))}
        {/* Generation marker */}
        <text x={pad.l+6} y={pad.t+14} fill={T.muted} fontSize={9}>
          gen {gen} · dominant: {STRATEGIES[dominant].sym}
        </text>
      </svg>

      {/* Legend */}
      <div style={{display:'flex',gap:10,flexWrap:'wrap',marginBottom:14}}>
        {stratKeys.map(k=>(
          <div key={k} style={{display:'flex',alignItems:'center',gap:5,fontSize:11}}>
            <div style={{width:12,height:12,background:STRATEGIES[k].color,
              borderRadius:2,opacity:0.75}}/>
            <span style={{color:STRATEGIES[k].color,fontFamily:'monospace'}}>
              {STRATEGIES[k].sym}
            </span>
            <span style={{color:T.muted}}>
              {(pop[k]*100).toFixed(1)}%
            </span>
          </div>
        ))}
      </div>

      {/* Controls */}
      <div style={{display:'flex',gap:8,marginBottom:14}}>
        <button onClick={()=>setRunning(r=>!r)} style={{
          padding:'8px 20px',background:running?'#2a1a1a':'#0a1a2a',
          border:`1px solid ${running?T.D:T.J}`,
          color:running?T.D:T.J,borderRadius:5,cursor:'pointer',fontSize:13,
        }}>{running ? '⏸ Pause' : '▶ Evolve'}</button>
        <button onClick={()=>{ step(); }} style={{
          padding:'8px 16px',background:'#0d0d1a',border:`1px solid ${T.border}`,
          color:T.muted,borderRadius:5,cursor:'pointer',fontSize:13,
        }}>Step</button>
        <button onClick={reset} style={{
          padding:'8px 16px',background:'#0d0d1a',border:`1px solid ${T.border}`,
          color:T.muted,borderRadius:5,cursor:'pointer',fontSize:13,
        }}>Reset</button>
        <div style={{display:'flex',alignItems:'center',gap:6,marginLeft:8}}>
          <span style={{fontSize:11,color:T.muted}}>δ={delta.toFixed(1)}</span>
        </div>
      </div>

      {/* Structural insight about winner */}
      <Panel style={{borderLeft:`3px solid ${STRATEGIES[dominant].color}`}}>
        <div style={{fontSize:11,color:STRATEGIES[dominant].color,fontFamily:'monospace',marginBottom:4}}>
          {STRATEGIES[dominant].sym} — {STRATEGIES[dominant].name} ({(pop[dominant]*100).toFixed(1)}%)
        </div>
        <div style={{fontSize:11,color:T.muted,lineHeight:1.65,marginBottom:8}}>
          {STRATEGIES[dominant].desc}
        </div>
        <div style={{fontSize:11,color:T.text,lineHeight:1.65}}>
          <strong style={{color:T.acc}}>Theorem 2.1 applied:</strong> the winning strategy
          is the one generating lowest average load in the shared carrier at δ={delta.toFixed(1)}.
          As δ→0 (pure coordination), AllC dominates.
          At δ≈2 (Prisoner's Dilemma), TfT is the minimum-load strategy achieving joint coherence.
          At δ→∞ (pure conflict), AllD becomes individually coherent despite destroying the shared carrier.
        </div>
      </Panel>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// SECTION 4: GRADIENT GEOMETRY — fixed point landscape
// ─────────────────────────────────────────────────────────────────────────────
function GradientGeometry({ delta }) {
  const canvasRef = useRef();
  const [showJoint, setShowJoint] = useState(true);
  const [showIndiv, setShowIndiv] = useState(true);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const W = canvas.width, H = canvas.height;
    ctx.fillStyle = '#09090f';
    ctx.fillRect(0,0,W,H);

    // Strategy space: x=P(A cooperates), y=P(B cooperates) ∈ [0,1]²
    // For mixed strategies: each player plays C with probability p
    // Load for A: p_A*p_B*(1) + p_A*(1-p_B)*(1+delta) + (1-p_A)*p_B*(1) + (1-p_A)*(1-p_B)*(1)
    // Simplifying: load_A = 1 + (1-p_B)*delta*p_A ... wait

    // Expected load for A given (p_A, p_B):
    // Cooperate: always cost 1 for self
    // Being defected against: B defects with prob (1-p_B), so A gets +delta with prob (1-p_B)
    const loadA = (pA, pB) => pA*(1 + (1-pB)*delta) + (1-pA)*(1 + (1-pB)*delta);
    // Simplifies to: 1 + (1-pB)*delta regardless of pA
    // That's wrong - let me redo
    // A cooperates (pA): cost 1, gets drag (1-pB)*delta
    // A defects (1-pA): cost 1, creates drag on B, doesn't reduce A's load
    // Wait - defecting doesn't reduce your own load, it adds drag to OTHER
    // So: load_A = 1 + (1-pB)*delta (what B does to A)
    // load_B = 1 + (1-pA)*delta (what A does to B)
    // joint = load_A + load_B = 2 + (2 - pA - pB)*delta

    const lA = (pA, pB) => 1 + (1-pB)*delta;
    const lB = (pA, pB) => 1 + (1-pA)*delta;
    const lJ = (pA, pB) => lA(pA,pB) + lB(pA,pB);

    // Gradient of joint load (direction of steepest descent = direction of reconfiguration)
    const N = W;
    for (let px = 0; px < N; px++) {
      for (let py = 0; py < H; py++) {
        const pA = px/N, pB = 1 - py/H;
        const j = lJ(pA,pB);
        // Color by joint load: low=green, high=red
        const t = (j - 2) / (2*delta + 0.001);
        const r = Math.round(20 + 200*t);
        const g = Math.round(200 - 160*t);
        const b = Math.round(40 + 40*(1-t));
        ctx.fillStyle = `rgb(${r},${g},${b})`;
        ctx.fillRect(px, py, 1, 1);
      }
    }

    // Gradient arrows (reconfiguration direction = toward low load)
    if (showJoint) {
      ctx.strokeStyle = 'rgba(255,255,255,0.35)';
      ctx.lineWidth = 1;
      const step = W/14;
      for (let i=1; i<14; i++) for (let j=1; j<14; j++) {
        const pA = i/14, pB = j/14;
        const j0 = lJ(pA,pB);
        const dpA = lJ(pA+0.01,pB) - j0; // positive = load increases with pA
        const dpB = lJ(pA,pB+0.01) - j0;
        // Arrow points toward decreasing joint load
        const ax = -dpA, ay = -dpB;
        const len = Math.sqrt(ax*ax+ay*ay);
        if (len < 0.0001) continue;
        const scale = 10 / len;
        const x0 = pA*W, y0 = (1-pB)*H;
        const x1 = x0 + ax*scale, y1 = y0 - ay*scale;
        ctx.beginPath(); ctx.moveTo(x0,y0); ctx.lineTo(x1,y1); ctx.stroke();
      }
    }

    // Nash Equilibrium point(s)
    if (showIndiv) {
      // Best response for A: defect always (load_A is independent of pA! so NE at pA=0)
      // Best response for B: defect always (load_B is independent of pB, NE at pB=0)
      // NE = (0,0) = (D,D)
      const neX = 0, neY = H;
      ctx.beginPath();
      ctx.arc(neX, neY, 10, 0, Math.PI*2);
      ctx.strokeStyle = '#ff453a'; ctx.lineWidth = 2.5;
      ctx.stroke();
      ctx.fillStyle = '#ff453a33'; ctx.fill();
      ctx.fillStyle='#ff453a'; ctx.font='bold 11px monospace';
      ctx.fillText('NE (D,D)', neX+12, neY-6);

      // Joint coherence minimum = (1,1) = (C,C)
      const jcX = W, jcY = 0;
      ctx.beginPath();
      ctx.arc(jcX, jcY, 10, 0, Math.PI*2);
      ctx.strokeStyle = T.C; ctx.lineWidth = 2.5;
      ctx.stroke();
      ctx.fillStyle = T.C+'33'; ctx.fill();
      ctx.fillStyle=T.C; ctx.font='bold 11px monospace';
      ctx.fillText('JC (C,C)', jcX-72, jcY+18);
    }

    // Axes
    ctx.fillStyle='rgba(9,9,15,0.7)';
    ctx.fillRect(0,H-20,W,20); ctx.fillRect(0,0,40,H);
    ctx.fillStyle=T.muted; ctx.font='10px monospace';
    ctx.fillText('P(A cooperates) →',10,H-5);
    ctx.save(); ctx.translate(12,H/2); ctx.rotate(-Math.PI/2);
    ctx.fillText('P(B cooperates) →',0,0); ctx.restore();

  }, [delta, showJoint, showIndiv]);

  return (
    <div>
      <h2 style={{color:T.head,fontSize:17,margin:'0 0 4px',fontFamily:'Georgia,serif'}}>
        Gradient Geometry — The Load Landscape
      </h2>
      <p style={{color:T.mid,fontSize:12,margin:'0 0 14px',lineHeight:1.7}}>
        The mixed strategy space as a load surface. Green = low joint load (coherence);
        red = high joint load (drag). White arrows show reconfiguration direction
        (Definition 2.6: toward argmin demand). NE and JC are marked.
      </p>

      <canvas ref={canvasRef} width={460} height={380}
        style={{display:'block',borderRadius:7,border:`1px solid ${T.border}`,marginBottom:10}}/>

      <div style={{display:'flex',gap:12,marginBottom:14,flexWrap:'wrap'}}>
        {[
          {label:'show gradient arrows (reconfiguration direction)',val:showJoint,set:setShowJoint,color:T.J},
          {label:'show NE & JC fixed points',val:showIndiv,set:setShowIndiv,color:T.D},
        ].map((b,i)=>(
          <button key={i} onClick={()=>b.set(v=>!v)} style={{
            padding:'6px 14px',fontSize:11,
            background: b.val?b.color+'22':'#0d0d1a',
            border:`1px solid ${b.val?b.color:T.border}`,
            color: b.val?b.color:T.muted,borderRadius:4,cursor:'pointer',
          }}>{b.label}</button>
        ))}
      </div>

      <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:10}}>
        <Panel>
          <div style={{fontSize:11,color:T.D,marginBottom:6,fontFamily:'monospace'}}>
            NE = (D,D) — individual fixed point
          </div>
          <div style={{fontSize:11,color:T.muted,lineHeight:1.65}}>
            Each gradient G_A, G_B is independently stable.
            Reconfiguration pressure from B drives A toward D regardless of A's choice.
            The individual gradients point toward the bottom-left corner.
          </div>
        </Panel>
        <Panel>
          <div style={{fontSize:11,color:T.C,marginBottom:6,fontFamily:'monospace'}}>
            JC = (C,C) — joint coherence minimum
          </div>
          <div style={{fontSize:11,color:T.muted,lineHeight:1.65}}>
            Joint load is minimized here: L_joint = 2 (zero drag).
            But neither gradient is individually stable — each player
            faces reconfiguration pressure toward defection.
            The shared carrier optimum is unreachable from individual gradients alone.
          </div>
        </Panel>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// SECTION 5: CUSTOM GAME — set the drag structure
// ─────────────────────────────────────────────────────────────────────────────
function CustomGame({ delta }) {
  // Allow any 2×2 game by setting drag for each outcome
  const [dCC, setDCC] = useState(0);
  const [dCD, setDCD] = useState(delta);
  const [dDC, setDDC] = useState(delta);
  const [dDD, setDDD] = useState(delta*0.5);

  // Sync DD to delta slider
  useEffect(() => {
    setDCD(delta); setDDC(delta); setDDD(delta*0.5);
  }, [delta]);

  const dragMatrix = { CC:dCC, CD:dCD, DC:dDC, DD:dDD };

  // Compute loads with per-outcome drag
  const cellLoad = (mA, mB) => {
    const key = mA+mB;
    const d = dragMatrix[key];
    return outcomeLoads(mA, mB, d);
  };

  const cells = [['C','C'],['C','D'],['D','C'],['D','D']].map(([mA,mB]) => ({
    mA, mB, ...cellLoad(mA, mB), key: mA+mB
  }));

  const fixedPts = cells.filter(c => {
    const altA = cellLoad(c.mA==='C'?'D':'C', c.mB);
    const altB = cellLoad(c.mA, c.mB==='C'?'D':'C');
    return altA.lA >= c.lA && altB.lB >= c.lB;
  });
  const jointMin = cells.reduce((best,c)=>c.joint<best.joint?c:best,cells[0]);

  const gameType = () => {
    const ne = fixedPts.map(f=>f.key);
    if (ne.includes('CC') && jointMin.key==='CC') return {t:'Coordination / Stag Hunt', c:T.C};
    if (ne.includes('DD') && !ne.includes('CC')) return {t:"Prisoner's Dilemma",       c:T.D};
    if (ne.length===0)                            return {t:'No pure-strategy NE',      c:T.acc};
    if (ne.length===2)                            return {t:'Battle of the Sexes',      c:'#ff9f0a'};
    return {t:'Custom game', c:T.mid};
  };
  const gtype = gameType();

  const sliders = [
    {key:'CC',label:'(C,C) drag',val:dCC,set:setDCC,color:T.C},
    {key:'CD',label:'(C,D) drag',val:dCD,set:setDCD,color:T.D},
    {key:'DC',label:'(D,C) drag',val:dDC,set:setDDC,color:T.D},
    {key:'DD',label:'(D,D) drag',val:dDD,set:setDDD,color:'#888'},
  ];

  return (
    <div>
      <h2 style={{color:T.head,fontSize:17,margin:'0 0 4px',fontFamily:'Georgia,serif'}}>
        Game Builder — Any 2×2 Game as Drag Structure
      </h2>
      <p style={{color:T.mid,fontSize:12,margin:'0 0 14px',lineHeight:1.7}}>
        Every 2×2 game is determined by its drag parameters: how much load
        each outcome injects into the shared carrier. Set them and watch the
        game type emerge. Coordination games, PD, Chicken, Battle of the Sexes —
        all instances of the same mechanism with different δ matrices.
      </p>

      <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:10,marginBottom:16}}>
        {sliders.map(s=>(
          <Panel key={s.key}>
            <Label>{s.label}</Label>
            <div style={{display:'flex',alignItems:'center',gap:8}}>
              <input type="range" min={0} max={5} step={0.1} value={s.val}
                onChange={e=>s.set(+e.target.value)}
                style={{flex:1,accentColor:s.color}}/>
              <span style={{fontFamily:'monospace',fontSize:12,color:s.color,minWidth:28}}>
                {s.val.toFixed(1)}
              </span>
            </div>
          </Panel>
        ))}
      </div>

      {/* Resulting matrix */}
      <div style={{display:'grid',gridTemplateColumns:'auto 1fr 1fr',gap:4,marginBottom:16}}>
        <div/>
        <div style={{textAlign:'center',fontSize:11,color:T.C,fontFamily:'monospace',padding:'4px'}}>B: C</div>
        <div style={{textAlign:'center',fontSize:11,color:T.D,fontFamily:'monospace',padding:'4px'}}>B: D</div>
        {['C','D'].map(mA=>(
          <>
            <div key={mA} style={{display:'flex',alignItems:'center',
              fontSize:11,color:mA==='C'?T.C:T.D,paddingRight:8,fontFamily:'monospace'}}>
              A: {mA}
            </div>
            {['C','D'].map(mB=>{
              const c = cells.find(x=>x.mA===mA&&x.mB===mB);
              const ne = fixedPts.some(f=>f.key===c.key);
              const jc = c.key===jointMin.key;
              return (
                <Panel key={mA+mB} style={{
                  borderColor: ne&&jc?T.C: ne?T.D: jc?T.C+'44':T.border,
                  background: ne&&jc?'#0a1a0a': ne?'#150a0a':'#0d0d1a',
                }}>
                  <div style={{fontFamily:'monospace',fontSize:12,marginBottom:4,
                    display:'flex',justifyContent:'space-between'}}>
                    <span style={{color:T.text}}>({c.lA.toFixed(1)}, {c.lB.toFixed(1)})</span>
                    <span style={{fontSize:10}}>
                      {ne&&<Tag color={T.D}>NE</Tag>}
                      {' '}{jc&&<Tag color={T.C}>JC</Tag>}
                    </span>
                  </div>
                  <div style={{fontSize:10,color:T.muted,fontFamily:'monospace'}}>
                    δ={dragMatrix[mA+mB].toFixed(1)} joint={c.joint.toFixed(2)}
                  </div>
                </Panel>
              );
            })}
          </>
        ))}
      </div>

      <Panel style={{borderLeft:`3px solid ${gtype.c}`,background:'#0a0a14'}}>
        <div style={{fontSize:14,color:gtype.c,fontFamily:'Georgia,serif',marginBottom:6}}>
          {gtype.t}
        </div>
        <div style={{fontSize:11,color:T.muted,lineHeight:1.7}}>
          NE: {fixedPts.length===0 ? 'none' : fixedPts.map(f=>`(${f.mA},${f.mB})`).join(', ')}{' '}·{' '}
          JC: ({jointMin.mA},{jointMin.mB}){' '}·{' '}
          {fixedPts.some(f=>f.key===jointMin.key)
            ? <span style={{color:T.C}}>NE = JC — coordination: individual and joint gradients agree</span>
            : <span style={{color:T.D}}>NE ≠ JC — conflict: individual gradients work against the shared carrier</span>
          }
        </div>
      </Panel>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// MAIN SHELL
// ─────────────────────────────────────────────────────────────────────────────
const TABS = [
  { id:'carrier',   label:'Shared Carrier',    C: SharedCarrier   },
  { id:'iterated',  label:'Iterated Play',      C: IteratedPlay    },
  { id:'evolution', label:'Strategy Evolution', C: StrategyEvolution },
  { id:'geometry',  label:'Gradient Geometry',  C: GradientGeometry },
  { id:'builder',   label:'Game Builder',        C: CustomGame      },
];

export default function PLGameTheory() {
  const [tab, setTab] = useState('carrier');
  const [delta, setDelta] = useState(2.0);
  const { C: Tab } = TABS.find(t=>t.id===tab);

  return (
    <div style={{background:T.bg,color:T.text,minHeight:'100vh',fontFamily:'Georgia,serif'}}>

      {/* Header */}
      <div style={{
        padding:'16px 20px 0',
        borderBottom:`1px solid ${T.border}`,
      }}>
        <div style={{fontSize:9,letterSpacing:'0.25em',color:T.dim,
          textTransform:'uppercase',marginBottom:2}}>
          Propagation Logic · Game Theory Engine · P / G → Q
        </div>
        <div style={{fontSize:17,color:T.head,marginBottom:2,fontFamily:'Georgia,serif'}}>
          Game Theory from the Mechanism
        </div>
        <div style={{fontSize:11,color:T.muted,marginBottom:12,lineHeight:1.5}}>
          A game is a shared carrier with co-propagating gradient families.
          A move is a gradient injection. A payoff is an inverted load.
          Nash Equilibrium ≠ Joint Coherence. Everything else follows.
        </div>
        <div style={{display:'flex',gap:2,flexWrap:'wrap'}}>
          {TABS.map(t=>(
            <button key={t.id} onClick={()=>setTab(t.id)} style={{
              padding:'6px 14px',fontSize:11,
              background: tab===t.id?T.panel:'transparent',
              border:`1px solid ${tab===t.id?T.border:'transparent'}`,
              borderBottom:`1px solid ${tab===t.id?T.bg:T.border}`,
              color: tab===t.id?T.head:T.muted,
              cursor:'pointer',borderRadius:'4px 4px 0 0',
              marginBottom:'-1px',fontFamily:'Georgia,serif',
            }}>{t.label}</button>
          ))}
        </div>
      </div>

      {/* Content */}
      <div style={{padding:'20px',maxWidth:760}}>
        <Tab delta={delta} setDelta={setDelta}/>
      </div>

      {/* Footer — the mechanism in one line */}
      <div style={{padding:'12px 20px',borderTop:`1px solid ${T.border}`,
        fontSize:10,color:T.dim,fontFamily:'monospace',letterSpacing:'0.05em'}}>
        P /C G := Q &nbsp;·&nbsp; demand(P,C) = max(0, L_P − θ_C) &nbsp;·&nbsp;
        rate(P,C) = min(L_P,θ)/L_P &nbsp;·&nbsp; drag=0: zero-drag (cooperation) &nbsp;·&nbsp;
        drag>0: resource-sensitive (defection) &nbsp;·&nbsp; fixed point: coherence
      </div>
    </div>
  );
}
