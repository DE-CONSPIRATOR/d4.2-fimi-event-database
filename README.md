# D4.2 FIMI Event Database

**The DE-CONSPIRATOR FIMI Attribution Event Dataset**

| Item | Value |
|---|---|
| Deliverable | D4.2 FIMI Event Database |
| Work package | WP4 FIMI 'Major Events' Repository |
| Issued by | Özyeğin University |
| Dissemination level | PU (Public) |
| Dataset release | v2.4.3 |
| Project | DE-CONSPIRATOR, Horizon Europe Grant Agreement No. 101132671 |

## The dataset

The dataset records the attributions of foreign information manipulation and interference (FIMI) that European and allied institutions have published. We compiled it from 534 documents issued by 97 institutions and organised it into 3,029 distinct incidents. Each row carries the institution, the source document, the page and a verbatim quotation, so that a reader can check it against its source.

We record what institutions have said, and we do not establish what took place. The dataset supports claims about how European institutions attribute FIMI. It does not support claims about the incidence, distribution or trend of FIMI itself.

The D4.2 report sets out the design, the validation and the findings. The codebook documents the 81 variables of the data file.

## Repository layout

```
data/        DCFIMIEvent_v2_4_3.csv, DCFIMIEvent_v2_4_3_registries.xlsx
docs/        D4.2 report and codebook
scripts/     reproduce_figures.py, make_figures.py
portal/      build scripts of the interactive portal
index.html   interactive portal, served with GitHub Pages
```

We will add these files when D4.2 is submitted.

## Interactive portal

The portal is a single web page that carries its own data. A user can filter the incidents, explore the attribution patterns and download the filtered records. We will publish it with GitHub Pages from this repository.

## Reading the data

The file holds one row for each description of an incident in a document. Count incidents by filtering on `is_primary`.

```python
import pandas as pd
d = pd.read_csv("data/DCFIMIEvent_v2_4_3.csv", dtype=str, keep_default_na=False)
incidents = d[d.is_primary == "1"]   # 3,029 rows
```

The script `reproduce_figures.py` checks every published figure against the released file.

## How to cite

DE-CONSPIRATOR Consortium (2026). The DE-CONSPIRATOR FIMI Attribution Event Dataset, release v2.4.3. Deliverable D4.2, Horizon Europe Grant Agreement 101132671.

We will add a DOI for the dataset with the first public release.

## Licence

We release the data and the codebook under the Creative Commons Attribution 4.0 International licence (CC BY 4.0). Third-party material quoted from source documents remains subject to the rights of its original publishers.

## Corrections

Any institution or individual named in the dataset may contest a row. We record every correction in the correction register. Write to info@deconspirator-project.eu.

## Funding

Funded by the European Union under Grant Agreement No. 101132671. Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union or the European Research Executive Agency. Neither the European Union nor the granting authority can be held responsible for them.
