"""Regenerate Figures 3, 5, 9, 10 and 13 of D4.2 (report v1.2 numbering) from DCFIMIEvent_v2_4_3.csv.

Joint publications are treated as one source identity carrying one jurisdiction and one type
(institution_country, institution_type), as codebook Section 2 states.

Institution type groups (documented in codebook Section 6):
  Intelligence   <- Intelligence
  Government     <- Government; Parliamentary oversight
  NATO           <- NATO
  EU             <- EU; EU/NATO
  Civil society  <- Civil society; EU-based civil society; Civil society consortium;
                    Baltic (EDMO hub); Central Europe (EDMO hub); Commercial research
  Not yet typed  <- Unmapped
Rows with no identified institution carry no type and are excluded.
"""
import json, collections, math
import numpy as np, pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch, Wedge

NAVY = '#1F3A63'; RED = '#C0392B'; MID = '#5B7DB1'; LIGHT = '#9DB4D8'; GREY = '#D9D9D9'; ORANGE = '#F2A44A'
TITLE = dict(color=NAVY, fontsize=15, fontweight='bold')
plt.rcParams.update({'font.family': 'DejaVu Sans', 'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.edgecolor': '#666666', 'xtick.color': '#444444', 'ytick.color': '#444444'})

GROUP = {'Intelligence': 'Intelligence', 'Government': 'Government', 'Parliamentary oversight': 'Government',
         'NATO': 'NATO', 'EU': 'EU', 'EU/NATO': 'EU',
         'Civil society': 'Civil society', 'EU-based civil society': 'Civil society',
         'Civil society consortium': 'Civil society', 'Baltic (EDMO hub)': 'Civil society',
         'Central Europe (EDMO hub)': 'Civil society', 'Commercial research': 'Civil society',
         'Unmapped': 'Not yet typed'}
ORDER = ['Intelligence', 'Government', 'NATO', 'EU', 'Civil society', 'Not yet typed']

d = pd.read_csv('DCFIMIEvent_v2_4_3.csv', dtype=str, keep_default_na=False)
u = d[d.is_primary == '1'].copy()
u['grp'] = u.institution_type.map(GROUP).fillna('')
typed = u[u.grp != '']
out = {}

def note(fig, text):
    fig.text(0.5, 0.01, text, ha='center', va='bottom', fontsize=10, color='#7f7f7f')

# ---------- Figure 3: latency by institution group ----------
lat = typed[typed.analysis_include_latency == '1'].copy()
lat['lag'] = pd.to_numeric(lat.entry_lag_years)
order3 = ['Civil society', 'EU', 'NATO', 'Government', 'Intelligence', 'Not yet typed'][::-1]
fig, ax = plt.subplots(figsize=(10.6, 5.2), dpi=150)
data = [lat[lat.grp == g].lag.values for g in order3]
bp = ax.boxplot(data, vert=False, widths=0.55, patch_artist=True, showfliers=False,
                medianprops=dict(color=RED, linewidth=2.5), boxprops=dict(facecolor=GREY, edgecolor=NAVY),
                whiskerprops=dict(color='black'), capprops=dict(color='black'))
ax.set_yticks(range(1, len(order3) + 1)); ax.set_yticklabels(order3, fontsize=12)
ax.set_xlabel('Years between occurrence and publication', fontsize=12)
ax.set_xlim(-0.5, 16)
out['fig3'] = {}
for i, g in enumerate(order3, 1):
    v = lat[lat.grp == g].lag
    ax.text(12.2, i, f'median {int(v.median())}  n={len(v)}', va='center', fontsize=11, color='#333333')
    out['fig3'][g] = dict(n=int(len(v)), median=float(v.median()), q1=float(v.quantile(.25)), q3=float(v.quantile(.75)))
ax.set_title('How quickly different kinds of institution publish attributions', **TITLE)
note(fig, 'Intelligence services publish closest to the event; government units and NATO bodies carry the longest delays.')
fig.tight_layout(rect=(0, 0.05, 1, 1)); fig.savefig('fig03.png'); plt.close(fig)

# ---------- Figure 5: share attributed to Russia and China by group ----------
fig, ax = plt.subplots(figsize=(9.2, 4.9), dpi=150)
xs = np.arange(len(ORDER)); w = 0.38
ru = [(typed[typed.grp == g].actor_state == 'Russia').mean() * 100 for g in ORDER]
cn = [(typed[typed.grp == g].actor_state == 'China').mean() * 100 for g in ORDER]
ax.bar(xs - w / 2, ru, w, color=NAVY, label='Russia'); ax.bar(xs + w / 2, cn, w, color=RED, label='China')
for x, r, c in zip(xs, ru, cn):
    ax.text(x - w / 2, r + 1, f'{r:.0f}%', ha='center', fontsize=11, color='#333333')
    ax.text(x + w / 2, c + 1, f'{c:.0f}%', ha='center', fontsize=11, color='#333333')
ax.set_xticks(xs); ax.set_xticklabels(ORDER, fontsize=12)
ax.set_ylabel("Share of that institution type's incidents", fontsize=12)
ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(decimals=0)); ax.set_ylim(0, max(ru) + 8)
ax.legend(frameon=False, fontsize=12, loc='upper right')
ax.set_title('Which institutions name Russia, and which name China', **TITLE)
note(fig, 'Every type of institution attributes to Russia several times more often than to China.')
out['fig5'] = {g: dict(n=int((typed.grp == g).sum()), russia=round(r, 1), china=round(c, 1)) for g, r, c in zip(ORDER, ru, cn)}
fig.tight_layout(rect=(0, 0.05, 1, 1)); fig.savefig('fig05.png'); plt.close(fig)

# ---------- Figure 10: share of each publication year's attributions by group ----------
p = typed[typed.first_publication_year != ''].copy()
p['year'] = p.first_publication_year.astype(float).astype(int)
p = p[(p.year >= 2016) & (p.year <= 2025)]
ct = pd.crosstab(p.year, p.grp)[ORDER]
share = ct.div(ct.sum(axis=1), axis=0) * 100
fig, ax = plt.subplots(figsize=(9.2, 5.6), dpi=150)
cols = [NAVY, MID, '#B87333', LIGHT, GREY, '#F0F0F0']
ax.stackplot(share.index, [share[g] for g in ORDER], labels=ORDER, colors=cols, edgecolor='white', linewidth=0.5)
ax.set_xlim(share.index.min(), share.index.max()); ax.set_ylim(0, 100)
ax.set_xticks(share.index); ax.set_ylabel("Share of that year's published attributions", fontsize=12)
ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(decimals=0))
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=6, frameon=False, fontsize=11)
ax.set_title('Who produces the European attribution record, by year of publication', **TITLE)
note(fig, 'Civil society carries a growing share of the published record; the intelligence share has fallen since 2017.')
out['fig10'] = {int(y): {g: round(float(share.loc[y, g]), 1) for g in ORDER} for y in share.index}
out['fig10_n'] = {int(y): int(ct.loc[y].sum()) for y in ct.index}
fig.tight_layout(rect=(0, 0.06, 1, 1)); fig.savefig('fig10.png'); plt.close(fig)

# ---------- Figure 13: stated confidence by group ----------
order20 = ORDER[::-1]
fig, ax = plt.subplots(figsize=(9.2, 5.4), dpi=150)
levels = ['High', 'Medium', 'Low']; lc = [NAVY, MID, GREY]
out['fig13'] = {}
for i, g in enumerate(order20):
    s = typed[typed.grp == g]; s = s[s.source_confidence.isin(levels)]
    tot = len(s); left = 0
    out['fig13'][g] = {'n': tot}
    for lv, c in zip(levels, lc):
        v = (s.source_confidence == lv).sum() / tot * 100
        ax.barh(i, v, left=left, color=c, height=0.6, label=lv if i == 0 else None)
        if v >= 6:
            ax.text(left + v / 2, i, f'{v:.0f}%', ha='center', va='center', fontsize=11, color='white' if lv != 'Low' else '#333333')
        out['fig13'][g][lv] = round(v, 1); left += v
ax.set_yticks(range(len(order20))); ax.set_yticklabels(order20, fontsize=12)
ax.set_xlim(0, 100); ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(decimals=0))
ax.legend(loc='lower right', bbox_to_anchor=(1, -0.22), ncol=3, frameon=False, fontsize=11)
ax.set_title('Confidence the source expressed in its own attribution, by institution type', fontsize=13.5, color=NAVY, fontweight='bold')
note(fig, 'Intelligence services state high confidence most often, while disclosing the least about their evidence.')
fig.tight_layout(rect=(0, 0.06, 1, 1)); fig.savefig('fig13.png'); plt.close(fig)

# ---------- Figure 9: chord diagram of attribution flows between jurisdictions ----------
t = u[(u.analysis_include_target == '1') & (u.institution_country != '')].copy()
t['target'] = t.target_information_space.str.strip()
t = t[t.target != '']
flows = collections.Counter(zip(t.institution_country, t.target))
tgt_counts = collections.Counter(t.target)
targets_ge2 = {k for k, v in tgt_counts.items() if v >= 2}
targets_kept = {k for k, v in tgt_counts.items() if v >= 10}
OTHER = 'Other targets'
t['node_target'] = t.target.where(t.target.isin(targets_kept) | t.target.isin(attributors_tmp := set(t.institution_country)), OTHER)
flows = collections.Counter(zip(t.institution_country, t.node_target))
targets_kept = set(t.node_target)
attributors = set(t.institution_country)
nodes = sorted(attributors | targets_kept, key=lambda k: -(sum(v for (a, b), v in flows.items() if a == k) + sum(v for (a, b), v in flows.items() if b == k)))
# node weight = out + in (flows among kept nodes)
kept = dict(flows)
weight = collections.Counter()
for (a, b), v in kept.items():
    weight[a] += v; weight[b] += v
# order nodes: attributors first by weight, then pure targets by weight
attr_nodes = sorted(attributors, key=lambda k: -weight[k]); tgt_nodes = sorted(targets_kept - attributors, key=lambda k: -weight[k])
nodes = attr_nodes + tgt_nodes
total = sum(weight.values()); gap = math.radians(1.2)
angles = {}; start = math.pi / 2
for n in nodes:
    span = (2 * math.pi - gap * len(nodes)) * weight[n] / total
    angles[n] = (start, start - span); start = start - span - gap
R = 1.0
fig, ax = plt.subplots(figsize=(11, 11), dpi=150); ax.set_aspect('equal'); ax.axis('off')
ax.set_xlim(-1.55, 1.55); ax.set_ylim(-1.55, 1.55)
for n in nodes:
    a0, a1 = angles[n]
    ax.add_patch(Wedge((0, 0), R + 0.06, math.degrees(a1), math.degrees(a0), width=0.06,
                       facecolor=NAVY if n in attributors else '#A6A6A6', edgecolor='white', linewidth=0.8))
    mid = (a0 + a1) / 2; rot = math.degrees(mid)
    ha = 'left' if math.cos(mid) >= 0 else 'right'
    if math.cos(mid) < 0: rot += 180
    ax.text((R + 0.2) * math.cos(mid), (R + 0.2) * math.sin(mid), n, rotation=rot, rotation_mode='anchor',
            ha=ha, va='center', fontsize=9.5, color='#333333')
# allocate sub-arcs: outgoing first, then incoming, within each node
cursor = {n: angles[n][0] for n in nodes}
def take(n, v):
    a0, a1 = angles[n]; span = (a0 - a1) * v / weight[n]
    s = cursor[n]; cursor[n] = s - span; return s, s - span
def chord(s0, e0, s1, e1, color, alpha, z=1):
    p0 = (R * math.cos(s0), R * math.sin(s0)); p1 = (R * math.cos(e0), R * math.sin(e0))
    p2 = (R * math.cos(s1), R * math.sin(s1)); p3 = (R * math.cos(e1), R * math.sin(e1))
    verts = [p0, (0, 0), p2, p3, (0, 0), p1, p0]
    codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3, Path.LINETO, Path.CURVE3, Path.CURVE3, Path.CLOSEPOLY]
    # arc approximation for the ends is fine at these widths
    ax.add_patch(PathPatch(Path(verts, codes), facecolor=color, edgecolor='none', alpha=alpha, zorder=z))
loops = []
for (a, b), v in sorted(kept.items(), key=lambda kv: -kv[1]):
    if a == b:
        loops.append((a, v)); continue
    s0, e0 = take(a, v); s1, e1 = take(b, v)
    chord(s0, e0, s1, e1, LIGHT, 0.45)
for a, v in loops:
    s0, e0 = take(a, v)
    ang2 = np.linspace(s0, e0, 30)
    rr = R + 0.10
    ax.plot(rr * np.cos(ang2), rr * np.sin(ang2), color=ORANGE, linewidth=2 + 200 * v / total, alpha=0.95, zorder=3, solid_capstyle='butt')
selfn = sum(v for a, v in loops)
out['fig9'] = dict(covered=int(len(t)), incidents=3029, pct=round(len(t) / 3029 * 100), self=int(selfn), self_pct=round(selfn / len(t) * 100),
                    attributing_jurisdictions=len(attributors), targets_ge2=len(targets_ge2), shown_targets=len(targets_kept), other_pooled=int(sum(v for (a,b),v in flows.items() if b==OTHER)),
                    loops={a: int(v) for a, v in sorted(loops, key=lambda x: -x[1])},
                    multinational_out=int(sum(v for (a, b), v in flows.items() if a == 'Multinational')),
                    ukraine_in=int(tgt_counts['Ukraine']), ukraine_out=int(sum(v for (a, b), v in flows.items() if a == 'Ukraine')))
fig.savefig('fig09.png', bbox_inches='tight'); plt.close(fig)

json.dump(out, open('figure_numbers.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
