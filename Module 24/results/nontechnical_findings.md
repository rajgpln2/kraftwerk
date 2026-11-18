# Synthetic capstone findings

### Later-period results

The selected **Random forest** model flagged **8 of 12** out-of-spec lots and missed **4**. It also flagged **20 of 108** acceptable lots. That gives **66.7% recall**, **18.5% false-positive rate**, and **28.6% precision**. The stated success criterion was **not met** on this synthetic test.

### Operational meaning

Reviewing all **28** alerts would identify **8** out-of-spec lots in the 120-lot test period. **20** alerts would consume review capacity on acceptable lots. Each lot contains 50 units, but this lot-mean target does not support counting all units in a flagged lot as defective or rescued.

The largest importance scores belonged to **incoming oca delta um, precheck pressure mpa, precheck vacuum pa abs**. Those rankings reflect the simulator and this fitted model. Correlated settings and the small test sample limit how precisely the signals can be ranked.

### Limits and next steps

The test contains only **12** positive lots. The five-day block-bootstrap recall interval is **40.0%–90.0%**. Longer production histories and repeated runs under different process assumptions are needed to assess stability.

Before operational use, collect timestamped pre-lot checks, incoming material measurements, metrology release times, and the actual disposition rule. Confirm measurement repeatability and product specifications. Validate on a later real production period, then test inspection prioritization in shadow mode. Maintenance and recipe decisions need engineering approval and controlled experiments. This exercise provides no measured factory savings.

