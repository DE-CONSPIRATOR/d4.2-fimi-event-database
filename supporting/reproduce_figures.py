"""Reproduce every quantity in codebook Section 8 (Table 19) from DCFIMIEvent_v2_4_3.csv.

Run:  python reproduce_figures.py [path to CSV]
Each line prints the quantity, the value the codebook states, the value computed
from the file, and OK or MISMATCH. The script exits with status 1 on any mismatch.

Conventions: read every column as text with keep_default_na=False, so that an empty
cell stays an empty string and the value "None recorded" is never mistaken for a
missing value; split multi-valued fields on ";" and strip each item.
"""
import sys, hashlib, collections
import pandas as pd

path = sys.argv[1] if len(sys.argv) > 1 else 'DCFIMIEvent_v2_4_3.csv'
d = pd.read_csv(path, dtype=str, keep_default_na=False)
u = d[d.is_primary == '1']
lat = u[u.analysis_include_latency == '1']
lag = pd.to_numeric(lat.entry_lag_years)

def split(s):
    return [x.strip() for x in s.split(';') if x.strip()]

def recorded(col):
    """A response or evidence field counts as recorded when it is neither empty nor 'None recorded'."""
    return ~u[col].isin(['', 'None recorded'])

named = u[u.parent_institutions != '']
parent_counts = collections.Counter()
for s in named.parent_institutions:
    for p in set(split(s)):
        parent_counts[p] += 1
def n_for_share(counter, total, share):
    cum = 0
    for i, v in enumerate(sorted(counter.values(), reverse=True), 1):
        cum += v
        if cum >= total * share:
            return i
identity_counts = collections.Counter()
for s in named.source_identity:
    for p in set(split(s)):
        identity_counts[p] += 1

checks = [
    ('Rows', 3131, len(d)),
    ('Incidents', 3029, int((d.is_primary == '1').sum())),
    ('Corroborated, strict', 30, int((u.corroborated_independent == '1').sum())),
    ('Corroborated, broad', 61, int((u.corroborated == '1').sum())),
    ('Latency population', 2708, len(lat)),
    ('Median delay, years', 1.0, float(lag.median())),
    ('Mean delay, years', 2.13, round(float(lag.mean()), 2)),
    ('Reported in year of occurrence', 646, int((lag == 0).sum())),
    ('Reported 3 or more years later, %', 26.2, round(float((lag >= 3).mean() * 100), 1)),
    ('Target analysis population', 2912, int((u.analysis_include_target == '1').sum())),
    ('Target assignments excluded', 117, int((u.target_field_status == 'review_required').sum())),
    ('Latency anomalies quarantined', 5, int((u.latency_status == 'excluded_negative_lag').sum())),
    ('Official response recorded, %', 24.8, round(float(recorded('official_response').mean() * 100), 1)),
    ('Official response explicitly none', 2097, int((u.official_response == 'None recorded').sum())),
    ('International response recorded, %', 7.6, round(float(recorded('international_response').mean() * 100), 1)),
    ('Evidence of impact recorded, %', 35.6, round(float(recorded('evidence_of_impact').mean() * 100), 1)),
    ('Platform identified', 1975, int((u.primary_platform != 'Unknown').sum())),
    ('Weak, none, unknown or unrecorded coordination evidence', 1133,
     int(u.evidence_of_coordination.isin(['Weak', 'None recorded', 'Unknown', '']).sum())),
    ('Incidents with a named institution', 2797, len(named)),
    ('Incidents without a named institution', 232, len(u) - len(named)),
    ('Parent institutions observed', 96, len(parent_counts)),
    ('Parent institutions for half the named record', 8, n_for_share(parent_counts, len(named), 0.5)),
    ('Parent institutions for 80% of the named record', 21, n_for_share(parent_counts, len(named), 0.8)),
    ('Source identities for half the named record', 10, n_for_share(identity_counts, len(named), 0.5)),
    ('Source identities for 80% of the named record', 23, n_for_share(identity_counts, len(named), 0.8)),
    ('NATO StratCom incidents', 515, parent_counts['NATO Strategic Communications Centre of Excellence']),
    ('State actors', 1685, int((u.actor_named == 'state_actor').sum())),
    ('Non-state actors', 918, int((~u.actor_named.isin(['state_actor', 'unspecified'])).sum())),
    ('Incidents with a characterised actor', 2603, int((u.actor_named != 'unspecified').sum())),
    ('Russia attributed', 1443, int((u.actor_state == 'Russia').sum())),
    ('China attributed', 223, int((u.actor_state == 'China').sum())),
    ('DISARM techniques used', 77, u.disarm_ttps[u.disarm_ttps != ''].str.split(';').explode().str.strip().nunique()),
    ('DISARM technique mentions', 12518, int(u.disarm_ttps[u.disarm_ttps != ''].str.split(';').explode().shape[0])),
    ('Target information spaces, incidents', 113, u.target_information_space[u.target_information_space != ''].str.split(';').explode().str.strip().nunique()),
    ('Target information spaces, all rows', 114, d.target_information_space[d.target_information_space != ''].str.split(';').explode().str.strip().nunique()),
    ('Institution jurisdiction known, % of named', 97.2, round(float((named.institution_country != '').mean() * 100), 1)),
    ('Institution jurisdiction known, % of all incidents', 89.7, round(float((u.institution_country != '').mean() * 100), 1)),
    ('Rows flagged in institution_resolution', 246, int((d.institution_resolution != '').sum())),
]
bad = 0
for name, stated, got in checks:
    ok = (abs(stated - got) < 1e-9) if isinstance(stated, float) else (stated == got)
    bad += (not ok)
    print(f'{name:60s} stated {stated!s:>8} computed {got!s:>8}  {"OK" if ok else "MISMATCH"}')
print('SHA-256', hashlib.sha256(open(path, 'rb').read()).hexdigest())
sys.exit(1 if bad else 0)
