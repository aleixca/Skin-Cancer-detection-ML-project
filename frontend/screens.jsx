// DermaScan ML — refined phone screens.
// All screens render inside an iOS frame at 402×874.
// One shared design language: warm off-white surface, near-black ink, hairline rules,
// sage/amber/clay signal swatches, Inter Tight + JetBrains Mono.

const INK       = '#0E1116';
const INK_60    = 'rgba(14,17,22,0.62)';
const INK_45    = 'rgba(14,17,22,0.45)';
const INK_30    = 'rgba(14,17,22,0.30)';
const HAIR      = 'rgba(14,17,22,0.08)';
const HAIR_BOLD = 'rgba(14,17,22,0.14)';
const SURFACE   = '#FAFAF7';
const PAPER     = '#FFFFFF';
const SAGE      = 'oklch(0.74 0.06 160)';
const SAGE_BG   = 'oklch(0.96 0.025 160)';
const AMBER     = 'oklch(0.74 0.10 70)';
const AMBER_BG  = 'oklch(0.96 0.04 80)';
const CLAY      = 'oklch(0.62 0.14 30)';
const CLAY_BG   = 'oklch(0.96 0.04 30)';

const SANS = '"Inter Tight", "Inter", -apple-system, system-ui, sans-serif';
const MONO = '"JetBrains Mono", ui-monospace, "SF Mono", Menlo, monospace';

// ─── Inline line-icon set (lucide-flavored, hand-drawn) ──────────────────────
const Icon = {
  scan:    (p) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke={p.c||INK} strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round"><path d="M3 7V5a2 2 0 0 1 2-2h2"/><path d="M17 3h2a2 2 0 0 1 2 2v2"/><path d="M21 17v2a2 2 0 0 1-2 2h-2"/><path d="M7 21H5a2 2 0 0 1-2-2v-2"/><circle cx="12" cy="12" r="3.5"/></svg>,
  chat:    (p) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke={p.c||INK} strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round"><path d="M3 11a8 8 0 0 1 16 0v2a3 3 0 0 1-3 3h-1l-3 3v-3H11a8 8 0 0 1-8-5z"/></svg>,
  home:    (p) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke={p.c||INK} strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round"><path d="M4 11l8-7 8 7"/><path d="M6 10v9h12v-9"/></svg>,
  info:    (p) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke={p.c||INK} strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 8.5v-.01M11 12h1v5h1"/></svg>,
  arrow:   (p) => <svg width={p.s||14} height={p.s||14} viewBox="0 0 24 24" fill="none" stroke={p.c||INK} strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>,
  back:    (p) => <svg width={p.s||16} height={p.s||16} viewBox="0 0 24 24" fill="none" stroke={p.c||INK} strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round"><path d="M15 6l-6 6 6 6"/></svg>,
  upload:  (p) => <svg width={p.s||18} height={p.s||18} viewBox="0 0 24 24" fill="none" stroke={p.c||INK} strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round"><path d="M12 16V4M7 9l5-5 5 5"/><path d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2"/></svg>,
  camera:  (p) => <svg width={p.s||18} height={p.s||18} viewBox="0 0 24 24" fill="none" stroke={p.c||INK} strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round"><path d="M3 8a2 2 0 0 1 2-2h2l2-2h6l2 2h2a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><circle cx="12" cy="13" r="3.5"/></svg>,
  check:   (p) => <svg width={p.s||14} height={p.s||14} viewBox="0 0 24 24" fill="none" stroke={p.c||INK} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M5 12l5 5 9-11"/></svg>,
  alert:   (p) => <svg width={p.s||14} height={p.s||14} viewBox="0 0 24 24" fill="none" stroke={p.c||INK} strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M12 4l10 17H2z"/><path d="M12 10v5M12 18v.01"/></svg>,
  send:    (p) => <svg width={p.s||16} height={p.s||16} viewBox="0 0 24 24" fill="none" stroke={p.c||INK} strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round"><path d="M4 12l16-8-6 16-3-7z"/></svg>,
  plus:    (p) => <svg width={p.s||14} height={p.s||14} viewBox="0 0 24 24" fill="none" stroke={p.c||INK} strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M12 5v14M5 12h14"/></svg>,
  more:    (p) => <svg width={p.s||16} height={p.s||16} viewBox="0 0 24 24" fill="none" stroke={p.c||INK} strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round"><circle cx="5" cy="12" r="1"/><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/></svg>,
  flash:   (p) => <svg width={p.s||16} height={p.s||16} viewBox="0 0 24 24" fill="none" stroke={p.c||INK} strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round"><path d="M13 2L4 14h7l-1 8 9-12h-7z"/></svg>,
  flip:    (p) => <svg width={p.s||16} height={p.s||16} viewBox="0 0 24 24" fill="none" stroke={p.c||INK} strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round"><path d="M3 7h13a4 4 0 0 1 4 4v1"/><path d="M6 4L3 7l3 3"/><path d="M21 17H8a4 4 0 0 1-4-4v-1"/><path d="M18 20l3-3-3-3"/></svg>,
};

// ─── Shared chrome ──────────────────────────────────────────────────────────
function Wordmark({ size = 18 }) {
  return (
    <div style={{
      display: 'flex', alignItems: 'baseline', gap: 6,
      fontFamily: SANS, color: INK,
    }}>
      <span style={{
        fontSize: size, fontWeight: 600, letterSpacing: -0.4,
      }}>dermascan</span>
      <span style={{
        fontFamily: MONO, fontSize: size * 0.55, fontWeight: 500,
        color: INK_45, textTransform: 'uppercase', letterSpacing: 1.6,
        transform: 'translateY(-1px)',
      }}>ml</span>
    </div>
  );
}

function StatusBar() {
  return (
    <div style={{
      position: 'absolute', top: 0, left: 0, right: 0, height: 54,
      display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      padding: '20px 32px 0', fontFamily: SANS,
      fontSize: 15, fontWeight: 600, color: INK, zIndex: 30,
      pointerEvents: 'none',
    }}>
      <span style={{ fontFeatureSettings: '"tnum"' }}>9:41</span>
      <span style={{ display: 'flex', gap: 6, alignItems: 'center', opacity: 0.9 }}>
        <svg width="18" height="11" viewBox="0 0 18 11"><rect x="0" y="6" width="3" height="5" rx="0.6" fill={INK}/><rect x="5" y="4" width="3" height="7" rx="0.6" fill={INK}/><rect x="10" y="2" width="3" height="9" rx="0.6" fill={INK}/><rect x="15" y="0" width="3" height="11" rx="0.6" fill={INK}/></svg>
        <svg width="26" height="12" viewBox="0 0 26 12"><rect x="0.5" y="0.5" width="22" height="11" rx="2.5" stroke={INK} fill="none"/><rect x="2" y="2" width="19" height="8" rx="1.5" fill={INK}/><rect x="23" y="4" width="2" height="4" rx="0.7" fill={INK}/></svg>
      </span>
    </div>
  );
}

function TabBar({ active = 'home', onNav = () => {} }) {
  const items = [
    { id: 'home',  label: 'today',   icon: 'home' },
    { id: 'chat',  label: 'assist',  icon: 'chat' },
    { id: 'scan',  label: 'scan',    icon: 'scan' },
    { id: 'info',  label: 'about',   icon: 'info' },
  ];
  return (
    <div style={{
      position: 'absolute', bottom: 0, left: 0, right: 0,
      paddingBottom: 28, paddingTop: 12,
      background: 'rgba(250,250,247,0.88)',
      backdropFilter: 'blur(20px) saturate(180%)',
      WebkitBackdropFilter: 'blur(20px) saturate(180%)',
      borderTop: `1px solid ${HAIR}`,
      display: 'flex', justifyContent: 'space-around', alignItems: 'center',
      zIndex: 20,
    }}>
      {items.map(it => {
        const isActive = it.id === active;
        const I = Icon[it.icon];
        return (
          <div key={it.id} onClick={() => onNav(it.id)}
            style={{
              display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 4,
              cursor: 'pointer', fontFamily: SANS, fontSize: 10, fontWeight: 500,
              letterSpacing: 0.4, color: isActive ? INK : INK_45,
              minWidth: 56, paddingTop: 2,
            }}>
            <I s={22} c={isActive ? INK : INK_45} />
            <span>{it.label}</span>
          </div>
        );
      })}
    </div>
  );
}

function ScreenShell({ children, tab, onNav, surface = SURFACE }) {
  return (
    <div style={{
      position: 'absolute', inset: 0, background: surface,
      fontFamily: SANS, color: INK, overflow: 'hidden',
    }}>
      <StatusBar />
      <div style={{
        position: 'absolute', top: 54, bottom: 84, left: 0, right: 0,
        overflow: 'auto', overscrollBehavior: 'contain',
      }}>
        {children}
      </div>
      {tab && <TabBar active={tab} onNav={onNav} />}
    </div>
  );
}

function Hairline({ style }) {
  return <div style={{ height: 1, background: HAIR, ...style }} />;
}

function StatPill({ tone = 'sage', children }) {
  const map = {
    sage:  { bg: SAGE_BG,  fg: 'oklch(0.42 0.08 160)' },
    amber: { bg: AMBER_BG, fg: 'oklch(0.45 0.12 70)' },
    clay:  { bg: CLAY_BG,  fg: 'oklch(0.40 0.14 30)' },
    ink:   { bg: 'rgba(14,17,22,0.06)', fg: INK },
  };
  const c = map[tone];
  return (
    <span style={{
      display: 'inline-flex', alignItems: 'center', gap: 5,
      padding: '4px 9px', borderRadius: 999, background: c.bg, color: c.fg,
      fontFamily: SANS, fontSize: 11, fontWeight: 500, letterSpacing: -0.1,
    }}>{children}</span>
  );
}

function Dot({ color, size = 6 }) {
  return <span style={{
    width: size, height: size, borderRadius: '50%', background: color,
    display: 'inline-block',
  }} />;
}

// Image placeholder — diagonal hatch, monospace label
function LesionPlaceholder({ h = 180, label = 'lesion ▢ 0428' }) {
  return (
    <div style={{
      height: h, borderRadius: 16, overflow: 'hidden', position: 'relative',
      background:
        'repeating-linear-gradient(135deg, #EFEDE6 0 8px, #E8E6DE 8px 16px)',
      border: `1px solid ${HAIR}`,
    }}>
      <div style={{
        position: 'absolute', left: 0, right: 0, bottom: 0,
        padding: '10px 14px', display: 'flex', justifyContent: 'space-between',
        fontFamily: MONO, fontSize: 10, color: INK_60, letterSpacing: 0.4,
        background: 'linear-gradient(to top, rgba(250,250,247,0.85), transparent)',
      }}>
        <span>{label}</span>
        <span>128 × 128 · rgb</span>
      </div>
      {/* synthetic mole circle */}
      <div style={{
        position: 'absolute', left: '50%', top: '48%',
        transform: 'translate(-50%,-50%)',
        width: h * 0.42, height: h * 0.42 * 0.88, borderRadius: '50%',
        background:
          'radial-gradient(ellipse at 35% 30%, #6b4a32 0%, #4a2f1d 45%, #2a1810 100%)',
        boxShadow:
          '0 0 0 1px rgba(0,0,0,0.05), inset 0 -6px 12px rgba(0,0,0,0.3)',
        filter: 'blur(0.2px)',
      }} />
    </div>
  );
}

// ═════════════════════════════════════════════════════════════════════════════
// SCREEN 1 — HOME / TODAY
// ═════════════════════════════════════════════════════════════════════════════
function ScreenHome({ onNav = () => {} }) {
  return (
    <ScreenShell tab="home" onNav={onNav}>
      <div style={{ padding: '4px 24px 0' }}>
        {/* Header */}
        <div style={{
          display: 'flex', justifyContent: 'space-between', alignItems: 'center',
          paddingTop: 14, paddingBottom: 22,
        }}>
          <Wordmark />
          <div style={{
            width: 34, height: 34, borderRadius: '50%',
            background: 'oklch(0.86 0.04 70)', border: `1px solid ${HAIR_BOLD}`,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontFamily: SANS, fontSize: 12, fontWeight: 600, color: INK,
          }}>EM</div>
        </div>

        {/* Greeting */}
        <div style={{
          fontFamily: MONO, fontSize: 10, letterSpacing: 1.4,
          textTransform: 'uppercase', color: INK_45, marginBottom: 8,
        }}>tuesday · may 12</div>
        <h1 style={{
          margin: 0, fontFamily: SANS, fontSize: 30, fontWeight: 500,
          lineHeight: 1.08, letterSpacing: -0.9, color: INK, textWrap: 'pretty',
        }}>Good morning, Elena.<br/>
          <span style={{ color: INK_45 }}>One lesion is due for a follow-up scan.</span>
        </h1>

        {/* Primary action — large quiet card */}
        <div onClick={() => onNav('scan')} style={{
          marginTop: 22, padding: '20px 22px', borderRadius: 22,
          background: INK, color: PAPER, cursor: 'pointer',
          display: 'flex', alignItems: 'center', gap: 16,
          boxShadow: '0 10px 24px -10px rgba(14,17,22,0.45)',
        }}>
          <div style={{
            width: 46, height: 46, borderRadius: 14,
            background: 'rgba(255,255,255,0.08)',
            border: '1px solid rgba(255,255,255,0.14)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
          }}>
            <Icon.scan s={22} c={PAPER}/>
          </div>
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: 16, fontWeight: 500, letterSpacing: -0.2 }}>
              New dermoscopic scan
            </div>
            <div style={{
              fontSize: 12, color: 'rgba(255,255,255,0.55)', marginTop: 2,
            }}>~12 seconds · model v0.3</div>
          </div>
          <Icon.arrow s={18} c={PAPER}/>
        </div>

        {/* Section: tracked lesions */}
        <div style={{
          display: 'flex', justifyContent: 'space-between', alignItems: 'baseline',
          marginTop: 30, marginBottom: 12,
        }}>
          <div style={{
            fontFamily: MONO, fontSize: 10, letterSpacing: 1.4,
            textTransform: 'uppercase', color: INK_45,
          }}>tracked lesions · 04</div>
          <span style={{
            fontFamily: SANS, fontSize: 12, fontWeight: 500, color: INK,
            textDecoration: 'underline', textUnderlineOffset: 3,
          }}>see all</span>
        </div>

        {/* Lesion list — flat, hairline-separated */}
        <div style={{
          background: PAPER, borderRadius: 18, border: `1px solid ${HAIR}`,
          overflow: 'hidden',
        }}>
          {[
            { id: 'L-08', site: 'Right forearm',  date: 'yesterday · 14:30', tone: 'sage',  state: 'stable',    p: 0.08 },
            { id: 'L-03', site: 'Left shoulder',  date: '12 apr',            tone: 'amber', state: 'watch',     p: 0.24 },
            { id: 'L-01', site: 'Upper back',     date: '03 apr',            tone: 'sage',  state: 'stable',    p: 0.06 },
          ].map((row, i, arr) => (
            <React.Fragment key={row.id}>
              <div style={{
                padding: '14px 16px', display: 'flex', alignItems: 'center', gap: 14,
              }}>
                <div style={{
                  width: 38, height: 38, borderRadius: 10, flexShrink: 0,
                  background: row.tone === 'sage' ? SAGE_BG : AMBER_BG,
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  fontFamily: MONO, fontSize: 10, fontWeight: 500,
                  color: row.tone === 'sage' ? 'oklch(0.42 0.08 160)' : 'oklch(0.45 0.12 70)',
                  letterSpacing: 0.4,
                }}>{row.id}</div>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ fontSize: 14, fontWeight: 500, color: INK, letterSpacing: -0.1 }}>
                    {row.site}
                  </div>
                  <div style={{ fontSize: 11, color: INK_45, marginTop: 2 }}>{row.date}</div>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <div style={{
                    fontFamily: MONO, fontSize: 12, color: INK, fontFeatureSettings: '"tnum"',
                  }}>{(row.p * 100).toFixed(1)}%</div>
                  <div style={{
                    fontSize: 10, color: INK_45, marginTop: 1, letterSpacing: 0.3,
                  }}>{row.state}</div>
                </div>
              </div>
              {i < arr.length - 1 && <Hairline style={{ marginLeft: 68 }}/>}
            </React.Fragment>
          ))}
        </div>

        {/* Tiny stat strip */}
        <div style={{
          marginTop: 18, marginBottom: 30, display: 'grid',
          gridTemplateColumns: '1fr 1fr 1fr', gap: 1, background: HAIR,
          border: `1px solid ${HAIR}`, borderRadius: 14, overflow: 'hidden',
        }}>
          {[
            { k: 'scans',     v: '12', sub: 'this month' },
            { k: 'accuracy',  v: '0.81', sub: 'recall · cancer' },
            { k: 'next',      v: '04', sub: 'days · L-03' },
          ].map(s => (
            <div key={s.k} style={{ background: PAPER, padding: '12px 14px' }}>
              <div style={{
                fontFamily: MONO, fontSize: 9, letterSpacing: 1.2,
                color: INK_45, textTransform: 'uppercase',
              }}>{s.k}</div>
              <div style={{
                fontFamily: MONO, fontSize: 20, fontWeight: 500, color: INK,
                marginTop: 4, letterSpacing: -0.4,
              }}>{s.v}</div>
              <div style={{ fontSize: 10, color: INK_45, marginTop: 1 }}>{s.sub}</div>
            </div>
          ))}
        </div>
      </div>
    </ScreenShell>
  );
}

// ═════════════════════════════════════════════════════════════════════════════
// SCREEN 2 — SCAN (camera framing + patient meta)
// ═════════════════════════════════════════════════════════════════════════════
function ScreenScan({ onNav = () => {} }) {
  return (
    <ScreenShell tab="scan" onNav={onNav} surface={SURFACE}>
      <div style={{ padding: '4px 24px 24px' }}>
        {/* Compact nav */}
        <div style={{
          display: 'flex', justifyContent: 'space-between', alignItems: 'center',
          paddingTop: 14, paddingBottom: 18,
        }}>
          <div onClick={() => onNav('home')} style={{
            display: 'flex', alignItems: 'center', gap: 4, cursor: 'pointer',
            fontSize: 13, color: INK_60, fontWeight: 500,
          }}>
            <Icon.back s={14} c={INK_60}/> back
          </div>
          <span style={{
            fontFamily: MONO, fontSize: 10, letterSpacing: 1.4,
            color: INK_45, textTransform: 'uppercase',
          }}>step 1 / 2</span>
          <Icon.more s={16} c={INK_60}/>
        </div>

        <h1 style={{
          margin: 0, fontSize: 26, fontWeight: 500, letterSpacing: -0.7,
          lineHeight: 1.1, color: INK,
        }}>Capture the lesion</h1>
        <p style={{
          margin: '8px 0 22px', color: INK_60, fontSize: 13, lineHeight: 1.5,
          maxWidth: 320,
        }}>Center the mole inside the reticle. Use steady, even daylight — no flash, no shadows.</p>

        {/* Viewfinder */}
        <div style={{
          position: 'relative', height: 280, borderRadius: 20, overflow: 'hidden',
          background: '#1a1a1a',
        }}>
          {/* dark skin tone backdrop */}
          <div style={{
            position: 'absolute', inset: 0,
            background: 'radial-gradient(circle at 50% 55%, #7a5a44 0%, #4a3424 60%, #1a1208 100%)',
          }} />
          {/* mole */}
          <div style={{
            position: 'absolute', left: '50%', top: '52%',
            transform: 'translate(-50%,-50%)',
            width: 70, height: 62, borderRadius: '50%',
            background:
              'radial-gradient(ellipse at 35% 30%, #5a3a22 0%, #2a1810 70%, #150806 100%)',
          }} />
          {/* reticle */}
          <svg width="160" height="160" style={{
            position: 'absolute', left: '50%', top: '50%',
            transform: 'translate(-50%,-50%)',
          }}>
            <circle cx="80" cy="80" r="60" stroke="rgba(255,255,255,0.6)" strokeWidth="1.2" fill="none" strokeDasharray="3 5"/>
            {[0, 90, 180, 270].map(a => (
              <line key={a} x1="80" y1="80" x2="80" y2="20"
                stroke="rgba(255,255,255,0.85)" strokeWidth="1.4" strokeLinecap="round"
                transform={`rotate(${a} 80 80)`} strokeDasharray="0 50 8 0"/>
            ))}
          </svg>
          {/* corner brackets */}
          <svg width="100%" height="100%" style={{ position: 'absolute', inset: 0 }} pointerEvents="none">
            {[[14,14,0],[266,14,90],[266,250,180],[14,250,270]].map(([x,y,a],i)=>(
              <path key={i} d="M0 16V0h16" stroke="rgba(255,255,255,0.9)" strokeWidth="1.5" fill="none"
                transform={`translate(${x} ${y}) rotate(${a})`}/>
            ))}
          </svg>
          {/* overlay text */}
          <div style={{
            position: 'absolute', top: 14, left: 14, display: 'flex', gap: 6,
            alignItems: 'center', padding: '4px 9px', borderRadius: 999,
            background: 'rgba(0,0,0,0.4)', backdropFilter: 'blur(8px)',
            fontFamily: MONO, fontSize: 9, letterSpacing: 1, color: '#fff',
          }}>
            <Dot color="oklch(0.78 0.16 145)" size={5}/> focus locked
          </div>
          <div style={{
            position: 'absolute', bottom: 14, left: 14, right: 14,
            display: 'flex', justifyContent: 'space-between',
            fontFamily: MONO, fontSize: 10, color: 'rgba(255,255,255,0.85)',
          }}>
            <span>f/1.8 · iso 200</span>
            <span>≈ 9.7 cm</span>
          </div>
        </div>

        {/* Capture controls */}
        <div style={{
          display: 'flex', justifyContent: 'space-between', alignItems: 'center',
          padding: '16px 12px',
        }}>
          <div style={{
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            width: 44, height: 44, borderRadius: '50%',
            background: PAPER, border: `1px solid ${HAIR_BOLD}`,
          }}><Icon.upload s={18}/></div>

          <div style={{
            width: 64, height: 64, borderRadius: '50%',
            background: INK, display: 'flex', alignItems: 'center', justifyContent: 'center',
            boxShadow: '0 8px 20px -6px rgba(14,17,22,0.4)',
            border: '4px solid rgba(255,255,255,0.95)',
            outline: `1px solid ${HAIR_BOLD}`,
          }}/>

          <div style={{
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            width: 44, height: 44, borderRadius: '50%',
            background: PAPER, border: `1px solid ${HAIR_BOLD}`,
          }}><Icon.flash s={18}/></div>
        </div>

        {/* Patient context */}
        <div style={{
          marginTop: 8, padding: 18, borderRadius: 18,
          background: PAPER, border: `1px solid ${HAIR}`,
        }}>
          <div style={{
            display: 'flex', justifyContent: 'space-between', alignItems: 'center',
            marginBottom: 14,
          }}>
            <span style={{
              fontFamily: MONO, fontSize: 10, letterSpacing: 1.4,
              color: INK_45, textTransform: 'uppercase',
            }}>patient context</span>
            <StatPill tone="ink">improves accuracy +4%</StatPill>
          </div>

          {[
            { k: 'age',          v: '42' },
            { k: 'sex',          v: 'female' },
            { k: 'localization', v: 'upper back' },
          ].map((f, i, arr) => (
            <React.Fragment key={f.k}>
              <div style={{
                display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                padding: '12px 0',
              }}>
                <span style={{ fontSize: 13, color: INK_60 }}>{f.k}</span>
                <span style={{
                  fontSize: 14, fontWeight: 500, color: INK,
                  display: 'flex', alignItems: 'center', gap: 8,
                }}>
                  {f.v}
                  <Icon.arrow s={12} c={INK_45}/>
                </span>
              </div>
              {i < arr.length - 1 && <Hairline/>}
            </React.Fragment>
          ))}
        </div>

        {/* CTA */}
        <button onClick={() => onNav('analyzing')} style={{
          marginTop: 16, width: '100%', padding: '16px 20px',
          background: INK, color: PAPER, border: 'none', borderRadius: 16,
          fontFamily: SANS, fontSize: 14, fontWeight: 500, letterSpacing: -0.1,
          display: 'flex', justifyContent: 'space-between', alignItems: 'center',
          cursor: 'pointer',
        }}>
          <span>Analyze</span>
          <Icon.arrow s={16} c={PAPER}/>
        </button>
      </div>
    </ScreenShell>
  );
}

// ═════════════════════════════════════════════════════════════════════════════
// SCREEN 3 — ANALYZING
// ═════════════════════════════════════════════════════════════════════════════
function ScreenAnalyzing({ onNav = () => {} }) {
  return (
    <ScreenShell onNav={onNav} surface={INK}>
      <div style={{
        height: '100%', display: 'flex', flexDirection: 'column',
        padding: '4px 28px 28px', color: PAPER,
      }}>
        {/* top bar */}
        <div style={{
          display: 'flex', justifyContent: 'space-between', alignItems: 'center',
          paddingTop: 14,
        }}>
          <span style={{
            fontFamily: MONO, fontSize: 10, letterSpacing: 1.4,
            color: 'rgba(255,255,255,0.45)', textTransform: 'uppercase',
          }}>inference · in progress</span>
          <span style={{
            fontFamily: MONO, fontSize: 10, letterSpacing: 1.4,
            color: 'rgba(255,255,255,0.45)', textTransform: 'uppercase',
          }}>step 2 / 2</span>
        </div>

        {/* center: lesion + pulsing rings */}
        <div style={{
          flex: 1, display: 'flex', flexDirection: 'column',
          alignItems: 'center', justifyContent: 'center', position: 'relative',
        }}>
          <div style={{
            position: 'relative', width: 220, height: 220,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
          }}>
            {[0,1,2].map(i => (
              <div key={i} style={{
                position: 'absolute', inset: 0, borderRadius: '50%',
                border: `1px solid rgba(255,255,255,${0.22 - i*0.06})`,
                animation: `dsRing 2.4s ease-out ${i*0.6}s infinite`,
              }}/>
            ))}
            <div style={{
              width: 130, height: 130, borderRadius: '50%', overflow: 'hidden',
              border: '1px solid rgba(255,255,255,0.2)', position: 'relative',
            }}>
              <div style={{
                position: 'absolute', inset: 0,
                background: 'radial-gradient(circle at 40% 40%, #5a3a22 0%, #2a1810 60%, #150806 100%)',
              }}/>
              {/* scanning sweep */}
              <div style={{
                position: 'absolute', left: 0, right: 0, top: 0, height: 2,
                background: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.85), transparent)',
                animation: 'dsSweep 1.8s linear infinite',
                boxShadow: '0 0 12px rgba(255,255,255,0.6)',
              }}/>
            </div>
          </div>

          <div style={{ marginTop: 32, textAlign: 'center' }}>
            <div style={{
              fontFamily: SANS, fontSize: 22, fontWeight: 500,
              letterSpacing: -0.4, color: PAPER,
            }}>Analyzing lesion</div>
            <div style={{
              marginTop: 8, fontSize: 13, color: 'rgba(255,255,255,0.55)',
              maxWidth: 280, lineHeight: 1.55,
            }}>Extracting HOG descriptors and aligning with HAM10000 feature space.</div>
          </div>

          <style>{`
            @keyframes dsRing { 0% { transform: scale(0.55); opacity: 1 } 100% { transform: scale(1); opacity: 0 } }
            @keyframes dsSweep { 0% { top: -2px } 100% { top: 130px } }
          `}</style>
        </div>

        {/* stage list */}
        <div style={{
          padding: 16, borderRadius: 16,
          background: 'rgba(255,255,255,0.04)',
          border: '1px solid rgba(255,255,255,0.08)',
        }}>
          {[
            { k: 'preprocess', s: 'done',   t: '0.18s' },
            { k: 'hog features',  s: 'done',   t: '0.42s' },
            { k: 'classifier',    s: 'active', t: '...' },
            { k: 'calibration',   s: 'queued', t: '—'    },
          ].map((row, i, arr) => (
            <React.Fragment key={row.k}>
              <div style={{
                display: 'flex', alignItems: 'center', gap: 12,
                padding: '8px 0', fontFamily: MONO, fontSize: 11,
                color: row.s === 'queued' ? 'rgba(255,255,255,0.35)' : 'rgba(255,255,255,0.85)',
              }}>
                <span style={{
                  width: 10, height: 10, borderRadius: '50%', flexShrink: 0,
                  background: row.s === 'done' ? SAGE
                    : row.s === 'active' ? PAPER : 'rgba(255,255,255,0.2)',
                  animation: row.s === 'active' ? 'dsBlink 1.1s ease-in-out infinite' : 'none',
                }}/>
                <span style={{ flex: 1 }}>{row.k}</span>
                <span style={{ color: 'rgba(255,255,255,0.45)' }}>{row.t}</span>
              </div>
              {i < arr.length - 1 && <div style={{ height: 1, background: 'rgba(255,255,255,0.06)' }}/>}
            </React.Fragment>
          ))}
          <style>{`@keyframes dsBlink { 0%,100% { opacity: 1 } 50% { opacity: 0.3 } }`}</style>
        </div>

        <button onClick={() => onNav('result')} style={{
          marginTop: 16, width: '100%', padding: '14px 20px',
          background: 'transparent', color: 'rgba(255,255,255,0.6)',
          border: '1px solid rgba(255,255,255,0.18)', borderRadius: 14,
          fontFamily: SANS, fontSize: 13, fontWeight: 500,
          cursor: 'pointer',
        }}>view result →</button>
      </div>
    </ScreenShell>
  );
}

// ═════════════════════════════════════════════════════════════════════════════
// SCREEN 4 — RESULT
// ═════════════════════════════════════════════════════════════════════════════
function ScreenResult({ onNav = () => {} }) {
  // Demo: amber/watch case — P(cancer) = 0.34, threshold 0.214 → cancerous
  const pCancer = 0.34;
  const threshold = 0.214;
  const isCancer = pCancer >= threshold;
  const tone = isCancer ? 'amber' : 'sage';

  return (
    <ScreenShell tab="home" onNav={onNav}>
      <div style={{ padding: '4px 24px 24px' }}>
        <div style={{
          display: 'flex', justifyContent: 'space-between', alignItems: 'center',
          paddingTop: 14, paddingBottom: 18,
        }}>
          <div onClick={() => onNav('home')} style={{
            display: 'flex', alignItems: 'center', gap: 4, cursor: 'pointer',
            fontSize: 13, color: INK_60, fontWeight: 500,
          }}>
            <Icon.back s={14} c={INK_60}/> back
          </div>
          <span style={{
            fontFamily: MONO, fontSize: 10, letterSpacing: 1.4,
            color: INK_45, textTransform: 'uppercase',
          }}>scan · l-03</span>
          <Icon.more s={16} c={INK_60}/>
        </div>

        {/* Verdict block */}
        <div style={{
          fontFamily: MONO, fontSize: 10, letterSpacing: 1.4,
          color: INK_45, textTransform: 'uppercase',
        }}>model verdict</div>
        <h1 style={{
          margin: '6px 0 4px', fontSize: 30, fontWeight: 500,
          letterSpacing: -0.8, lineHeight: 1.1, color: INK,
        }}>
          {isCancer ? 'Warrants closer review.' : 'No concerning signals.'}
        </h1>
        <p style={{
          margin: 0, fontSize: 13, color: INK_60, lineHeight: 1.55, maxWidth: 320,
        }}>
          The classifier detected pigment irregularities and border asymmetry consistent with atypical nevi. We recommend booking a dermatologist within two weeks.
        </p>

        {/* Probability gauge */}
        <div style={{
          marginTop: 22, padding: 20, borderRadius: 20,
          background: PAPER, border: `1px solid ${HAIR}`,
        }}>
          <div style={{
            display: 'flex', justifyContent: 'space-between', alignItems: 'baseline',
            marginBottom: 18,
          }}>
            <span style={{
              fontFamily: MONO, fontSize: 10, letterSpacing: 1.4,
              color: INK_45, textTransform: 'uppercase',
            }}>p(malignant)</span>
            <span style={{
              fontFamily: MONO, fontSize: 32, fontWeight: 500, color: INK,
              letterSpacing: -0.8, fontFeatureSettings: '"tnum"',
            }}>0.34</span>
          </div>

          {/* track */}
          <div style={{
            position: 'relative', height: 10, borderRadius: 999,
            background: 'rgba(14,17,22,0.05)', overflow: 'visible',
          }}>
            <div style={{
              position: 'absolute', left: 0, top: 0, bottom: 0,
              width: `${pCancer * 100}%`, borderRadius: 999, background: AMBER,
            }}/>
            {/* threshold marker */}
            <div style={{
              position: 'absolute', left: `${threshold * 100}%`, top: -6, bottom: -6,
              width: 1, background: INK,
            }}/>
            <div style={{
              position: 'absolute', left: `${threshold * 100}%`, top: -22,
              transform: 'translateX(-50%)',
              fontFamily: MONO, fontSize: 9, color: INK, letterSpacing: 0.6,
              whiteSpace: 'nowrap',
            }}>θ 0.214</div>
          </div>

          <div style={{
            display: 'flex', justifyContent: 'space-between',
            marginTop: 8, fontFamily: MONO, fontSize: 10, color: INK_45,
          }}>
            <span>0.0 · benign</span>
            <span>1.0 · malignant</span>
          </div>

          <div style={{
            display: 'flex', alignItems: 'center', gap: 10,
            marginTop: 16, padding: '12px 14px', borderRadius: 12,
            background: AMBER_BG, color: 'oklch(0.38 0.13 60)',
            fontSize: 12, lineHeight: 1.5,
          }}>
            <Icon.alert s={16} c="oklch(0.45 0.13 60)"/>
            <span><strong style={{ fontWeight: 600 }}>Above threshold.</strong> Classifier flags for clinical follow-up. Threshold tuned for high recall (Youden's J).</span>
          </div>
        </div>

        {/* ABCD breakdown */}
        <div style={{
          marginTop: 16, padding: 20, borderRadius: 20,
          background: PAPER, border: `1px solid ${HAIR}`,
        }}>
          <div style={{
            display: 'flex', justifyContent: 'space-between', alignItems: 'baseline',
            marginBottom: 16,
          }}>
            <span style={{
              fontFamily: MONO, fontSize: 10, letterSpacing: 1.4,
              color: INK_45, textTransform: 'uppercase',
            }}>abcd attribution</span>
            <span style={{
              fontFamily: SANS, fontSize: 11, color: INK_45,
            }}>per-feature contribution</span>
          </div>

          {[
            { k: 'A',  l: 'asymmetry',       v: 0.62, tone: 'amber' },
            { k: 'B',  l: 'border',          v: 0.71, tone: 'amber' },
            { k: 'C',  l: 'color variation', v: 0.45, tone: 'sage'  },
            { k: 'D',  l: 'diameter',        v: 0.28, tone: 'sage'  },
          ].map((r, i, arr) => (
            <React.Fragment key={r.k}>
              <div style={{
                padding: '10px 0', display: 'flex', alignItems: 'center', gap: 14,
              }}>
                <span style={{
                  width: 22, height: 22, borderRadius: 7, flexShrink: 0,
                  background: r.tone === 'amber' ? AMBER_BG : SAGE_BG,
                  color: r.tone === 'amber' ? 'oklch(0.42 0.13 60)' : 'oklch(0.38 0.08 160)',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  fontFamily: MONO, fontSize: 11, fontWeight: 600,
                }}>{r.k}</span>
                <span style={{
                  flex: 1, fontSize: 13, color: INK, letterSpacing: -0.1,
                }}>{r.l}</span>
                <div style={{
                  width: 80, height: 4, borderRadius: 999,
                  background: 'rgba(14,17,22,0.06)', position: 'relative',
                }}>
                  <div style={{
                    position: 'absolute', left: 0, top: 0, bottom: 0,
                    width: `${r.v * 100}%`, borderRadius: 999,
                    background: r.tone === 'amber' ? AMBER : SAGE,
                  }}/>
                </div>
                <span style={{
                  fontFamily: MONO, fontSize: 11, color: INK, width: 32,
                  textAlign: 'right', fontFeatureSettings: '"tnum"',
                }}>{r.v.toFixed(2)}</span>
              </div>
              {i < arr.length - 1 && <Hairline/>}
            </React.Fragment>
          ))}
        </div>

        {/* Actions */}
        <div style={{ display: 'flex', gap: 10, marginTop: 16 }}>
          <button style={{
            flex: 1, padding: '14px 16px', background: PAPER, color: INK,
            border: `1px solid ${HAIR_BOLD}`, borderRadius: 14,
            fontFamily: SANS, fontSize: 13, fontWeight: 500, cursor: 'pointer',
          }}>Save & track</button>
          <button style={{
            flex: 1.2, padding: '14px 16px', background: INK, color: PAPER,
            border: 'none', borderRadius: 14, fontFamily: SANS, fontSize: 13,
            fontWeight: 500, cursor: 'pointer',
            display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 8,
          }}>Book dermatologist <Icon.arrow s={14} c={PAPER}/></button>
        </div>

        {/* Disclaimer */}
        <p style={{
          marginTop: 18, fontSize: 11, lineHeight: 1.6,
          color: INK_45, textAlign: 'center', maxWidth: 320, marginInline: 'auto',
        }}>
          DermaScan ML is decision-support only. It is not a substitute for clinical evaluation by a licensed dermatologist.
        </p>
      </div>
    </ScreenShell>
  );
}

// ═════════════════════════════════════════════════════════════════════════════
// SCREEN 5 — AI ASSISTANT
// ═════════════════════════════════════════════════════════════════════════════
function ScreenChat({ onNav = () => {} }) {
  const messages = [
    { role: 'assistant', text: 'Hello Elena. I can help you prepare for a scan or unpack a previous result. What would you like to look at?' },
    { role: 'user',      text: 'How should I read the L-03 result?' },
    { role: 'assistant', text: "L-03 came back at P(malignant) = 0.34 — above your 0.214 threshold, so the model flagged it for follow-up.\n\nThe driver was border irregularity (B = 0.71) and asymmetry (A = 0.62). Color and diameter looked fine." },
    { role: 'assistant', text: "I'd suggest booking a dermatologist in the next two weeks and re-scanning in 30 days to track change.", chips: ['Book appointment', 'Set reminder'] },
  ];
  return (
    <ScreenShell tab="chat" onNav={onNav}>
      <div style={{ padding: '4px 24px 0' }}>
        <div style={{
          display: 'flex', justifyContent: 'space-between', alignItems: 'center',
          paddingTop: 14, paddingBottom: 6,
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <div style={{
              width: 34, height: 34, borderRadius: 10,
              background: INK, color: PAPER, display: 'flex',
              alignItems: 'center', justifyContent: 'center',
              fontFamily: MONO, fontSize: 12, fontWeight: 500,
            }}>ds</div>
            <div>
              <div style={{ fontSize: 14, fontWeight: 500, color: INK, letterSpacing: -0.2 }}>Assistant</div>
              <div style={{
                fontSize: 11, color: INK_45, marginTop: 1,
                display: 'flex', alignItems: 'center', gap: 5,
              }}>
                <Dot color={SAGE} size={5}/> online · grounded on your scans
              </div>
            </div>
          </div>
          <Icon.more s={16} c={INK_60}/>
        </div>

        <div style={{
          marginTop: 14,
          fontFamily: MONO, fontSize: 9, letterSpacing: 1.4,
          color: INK_45, textTransform: 'uppercase', textAlign: 'center',
        }}>today · 9:41</div>

        <div style={{ marginTop: 16, display: 'flex', flexDirection: 'column', gap: 12 }}>
          {messages.map((m, i) => (
            <div key={i} style={{
              display: 'flex', flexDirection: m.role === 'user' ? 'row-reverse' : 'row',
              gap: 8,
            }}>
              <div style={{
                maxWidth: '82%',
                padding: '12px 14px',
                borderRadius: 16,
                background: m.role === 'user' ? INK : PAPER,
                color: m.role === 'user' ? PAPER : INK,
                border: m.role === 'user' ? 'none' : `1px solid ${HAIR}`,
                fontSize: 13, lineHeight: 1.55, whiteSpace: 'pre-wrap',
                borderTopRightRadius: m.role === 'user' ? 4 : 16,
                borderTopLeftRadius: m.role === 'user' ? 16 : 4,
                letterSpacing: -0.1,
              }}>
                {m.text}
                {m.chips && (
                  <div style={{ display: 'flex', gap: 6, marginTop: 10, flexWrap: 'wrap' }}>
                    {m.chips.map(c => (
                      <span key={c} style={{
                        padding: '6px 10px', borderRadius: 999,
                        border: `1px solid ${HAIR_BOLD}`, fontSize: 11,
                        color: INK, fontWeight: 500, background: SURFACE,
                      }}>{c}</span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Suggestion chips */}
        <div style={{
          marginTop: 14, display: 'flex', gap: 8, overflowX: 'auto',
          paddingBottom: 4,
        }}>
          {['Re-scan reminder', 'Photo tips', 'What does Youden mean?'].map(c => (
            <span key={c} style={{
              padding: '8px 12px', borderRadius: 999,
              background: PAPER, border: `1px solid ${HAIR}`,
              fontSize: 12, color: INK_60, whiteSpace: 'nowrap', flexShrink: 0,
            }}>{c}</span>
          ))}
        </div>

        {/* Composer */}
        <div style={{
          marginTop: 14, padding: '6px 6px 6px 16px', borderRadius: 999,
          background: PAPER, border: `1px solid ${HAIR_BOLD}`,
          display: 'flex', alignItems: 'center', gap: 10,
        }}>
          <input placeholder="Ask the assistant…" style={{
            flex: 1, border: 'none', outline: 'none', background: 'transparent',
            fontFamily: SANS, fontSize: 13, color: INK, padding: '8px 0',
          }}/>
          <div style={{
            width: 36, height: 36, borderRadius: '50%', background: INK,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            cursor: 'pointer',
          }}>
            <Icon.send s={16} c={PAPER}/>
          </div>
        </div>
      </div>
    </ScreenShell>
  );
}

// ═════════════════════════════════════════════════════════════════════════════
// SCREEN 6 — ABOUT / PROJECT INFO
// ═════════════════════════════════════════════════════════════════════════════
function ScreenInfo({ onNav = () => {} }) {
  return (
    <ScreenShell tab="info" onNav={onNav}>
      <div style={{ padding: '4px 24px 24px' }}>
        <div style={{
          display: 'flex', justifyContent: 'space-between', alignItems: 'center',
          paddingTop: 14, paddingBottom: 18,
        }}>
          <Wordmark size={16}/>
          <span style={{
            fontFamily: MONO, fontSize: 10, letterSpacing: 1.4,
            color: INK_45, textTransform: 'uppercase',
          }}>v0.3 · build 412</span>
        </div>

        <div style={{
          fontFamily: MONO, fontSize: 10, letterSpacing: 1.4,
          color: INK_45, textTransform: 'uppercase', marginBottom: 6,
        }}>project</div>
        <h1 style={{
          margin: '0 0 8px', fontSize: 26, fontWeight: 500,
          letterSpacing: -0.7, lineHeight: 1.15, color: INK,
        }}>
          A teaching prototype for<br/>dermoscopic triage.
        </h1>
        <p style={{
          margin: 0, fontSize: 13, color: INK_60, lineHeight: 1.6,
        }}>
          Built for an ML coursework delivery. Decision support, not diagnosis. Local inference on a Random Forest over HOG descriptors + structured metadata.
        </p>

        {/* Dataset card */}
        <div style={{
          marginTop: 22, padding: 18, borderRadius: 18,
          background: PAPER, border: `1px solid ${HAIR}`,
        }}>
          <div style={{
            display: 'flex', justifyContent: 'space-between', alignItems: 'center',
            marginBottom: 12,
          }}>
            <span style={{
              fontFamily: MONO, fontSize: 10, letterSpacing: 1.4,
              color: INK_45, textTransform: 'uppercase',
            }}>training set</span>
            <StatPill tone="ink">ham10000</StatPill>
          </div>
          <div style={{
            fontFamily: SANS, fontSize: 16, color: INK, fontWeight: 500,
            letterSpacing: -0.2,
          }}>10,015 dermatoscopic images</div>
          <div style={{ fontSize: 12, color: INK_60, marginTop: 4, lineHeight: 1.55 }}>
            7 lesion categories · binary collapse to benign / malignant for V0.
          </div>

          <div style={{
            display: 'grid', gridTemplateColumns: '1fr 1fr 1fr',
            gap: 1, background: HAIR, marginTop: 14,
            borderRadius: 10, overflow: 'hidden', border: `1px solid ${HAIR}`,
          }}>
            {[
              { k: 'accuracy', v: '0.78' },
              { k: 'recall',   v: '0.81' },
              { k: 'auc',      v: '0.83' },
            ].map(s => (
              <div key={s.k} style={{ background: PAPER, padding: '10px 12px' }}>
                <div style={{
                  fontFamily: MONO, fontSize: 9, letterSpacing: 1.2,
                  color: INK_45, textTransform: 'uppercase',
                }}>{s.k}</div>
                <div style={{
                  fontFamily: MONO, fontSize: 16, fontWeight: 500, color: INK,
                  marginTop: 2, fontFeatureSettings: '"tnum"',
                }}>{s.v}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Roadmap */}
        <div style={{
          marginTop: 16, padding: 18, borderRadius: 18,
          background: PAPER, border: `1px solid ${HAIR}`,
        }}>
          <div style={{
            fontFamily: MONO, fontSize: 10, letterSpacing: 1.4,
            color: INK_45, textTransform: 'uppercase', marginBottom: 14,
          }}>roadmap</div>

          {[
            { v: 'v0', s: 'shipped',  t: 'HOG + random forest baseline', desc: 'UI flow, baseline classifier, threshold tuning.' },
            { v: 'v1', s: 'planned',  t: 'Ensembles · bagging & boosting', desc: 'XGBoost over engineered features; cross-validated.' },
            { v: 'v2', s: 'planned',  t: 'CNN over raw dermoscopy', desc: 'EfficientNet transfer learning; SHAP attribution.' },
          ].map((r, i, arr) => (
            <div key={r.v} style={{
              display: 'flex', gap: 14, paddingBottom: i < arr.length - 1 ? 16 : 0,
              position: 'relative',
            }}>
              <div style={{
                display: 'flex', flexDirection: 'column', alignItems: 'center',
                width: 28, flexShrink: 0, paddingTop: 2,
              }}>
                <div style={{
                  width: 10, height: 10, borderRadius: '50%',
                  background: r.s === 'shipped' ? INK : PAPER,
                  border: r.s === 'shipped' ? 'none' : `1px solid ${HAIR_BOLD}`,
                }}/>
                {i < arr.length - 1 && (
                  <div style={{ width: 1, flex: 1, background: HAIR, marginTop: 4 }}/>
                )}
              </div>
              <div style={{ flex: 1, paddingBottom: i < arr.length - 1 ? 4 : 0 }}>
                <div style={{
                  display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4,
                }}>
                  <span style={{
                    fontFamily: MONO, fontSize: 11, color: INK,
                    letterSpacing: 0.4, fontWeight: 500,
                  }}>{r.v}</span>
                  <StatPill tone={r.s === 'shipped' ? 'sage' : 'ink'}>
                    {r.s}
                  </StatPill>
                </div>
                <div style={{ fontSize: 13, fontWeight: 500, color: INK, letterSpacing: -0.1 }}>{r.t}</div>
                <div style={{ fontSize: 12, color: INK_60, marginTop: 3, lineHeight: 1.5 }}>{r.desc}</div>
              </div>
            </div>
          ))}
        </div>

        {/* Concepts */}
        <div style={{
          marginTop: 16, padding: 18, borderRadius: 18,
          background: PAPER, border: `1px solid ${HAIR}`,
        }}>
          <div style={{
            fontFamily: MONO, fontSize: 10, letterSpacing: 1.4,
            color: INK_45, textTransform: 'uppercase', marginBottom: 12,
          }}>concepts in scope</div>
          {[
            'Supervised classification',
            'HOG feature extraction',
            'Threshold optimization · Youden\'s J',
            'Recall-prioritized evaluation',
            'Ensemble methods (planned)',
          ].map((c, i, arr) => (
            <React.Fragment key={c}>
              <div style={{
                padding: '10px 0', display: 'flex', alignItems: 'center', gap: 10,
                fontSize: 13, color: INK,
              }}>
                <Icon.check s={14} c={INK_60}/>
                <span style={{ letterSpacing: -0.1 }}>{c}</span>
              </div>
              {i < arr.length - 1 && <Hairline/>}
            </React.Fragment>
          ))}
        </div>
      </div>
    </ScreenShell>
  );
}

// Export all six screens
Object.assign(window, {
  ScreenHome, ScreenScan, ScreenAnalyzing, ScreenResult, ScreenChat, ScreenInfo,
});
