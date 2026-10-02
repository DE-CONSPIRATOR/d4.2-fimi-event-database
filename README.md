# DE-CONSPIRATOR Deliverable D4.2: The FIMI Attribution Event Dataset

Submission package, 30 September 2026. Report v1.2, dataset release v2.4.3, codebook v2.4.5, portal v2.4.3.
Horizon Europe Grant Agreement 101132671. Licence: CC BY 4.0 for the data and the codebook; quoted source material remains the right of its publishers.

## What to open

| File | Open it when you want to |
|---|---|
| DECONSPIRATOR_D4.2.docx | Read the design, the findings and the policy implications (report, 11 sections) |
| DECONSPIRATOR_D4.2_Codebook.docx | Work with the data: every variable, every rule, and the expressions that reproduce the published figures |
| DCFIMIEvent_v2_4_3.csv | The dataset: 3,131 rows, 3,029 distinct incidents (is_primary == 1), 81 variables |
| DCFIMIEvent_v2_4_3_registries.xlsx | The registers behind the dataset, one sheet each: institutions, source identities, documents, aliases, corrections |
| fimi_portal_v2_4_3.html | Explore the incidents in a browser; its links point to the files in this folder |
| supporting/reproduce_figures.py | Check the dataset: runs every line of codebook Table 19 and fails on any mismatch |
| supporting/make_figures.py | Regenerate report Figures 3, 5, 9, 10 and 13 from the dataset |

## Reading the dataset

Read every column as text and keep empty cells empty: `pd.read_csv(path, dtype=str, keep_default_na=False)`.
Count incidents with `is_primary == "1"`. Split multi-valued fields on ";" and strip each item; do not split `cited_sources`.
In the 4 response and evidence fields, `None recorded` means the source was read and describes none, and an empty cell means the field was not populated.

## SHA-256

    cc3adab3af3994ae7bb5a770e806579b20cb66487333bbb4c8c824a6aa939a5a  DECONSPIRATOR_D4.2.docx
    aac0c8af37894bf7e448232bb2f5e7b1fca6600c82fc96ec870319183689b8e0  DECONSPIRATOR_D4.2_Codebook.docx
    737f23bea8fabfd312c5903730d2b9022be7e6cd9eaeb09a5ae30bcaa26fa649  DCFIMIEvent_v2_4_3.csv
    8a61538f3e93b24a7220bc331570a2baa662d3f34c3b63b5e433a7ee6f5439e2  DCFIMIEvent_v2_4_3_registries.xlsx
    c23b9fc0755e86f44eb9f23c5c20b20416e7e91c591f2790c21d8107a739b9dc  fimi_portal_v2_4_3.html
    52a64cb906ad883fa9c2238cfa1b8c4cc67652d0eb8be6bf664e1d1e321a080b  supporting/reproduce_figures.py
    635962084e82a128840304d42e4dba07b4f58693fb9d687088def3f1b22b9d29  supporting/make_figures.py
