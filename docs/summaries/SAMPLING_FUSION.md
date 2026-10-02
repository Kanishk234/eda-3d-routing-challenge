# Sampling and iterative fusion checkpoint

Goal: improve legal sink-delay scores through alternative neighborhood selection and candidate geometry.

Hard neutral pilot18legal,10M expansions each:5wins/4losses; geometric delay ratio1.0001062995. Added full9case fixedseed1 continuation improves7/unchanged2,1101neutral moves,20.242s wrapper. Hard score1.258790632279399. This mixed pilot supports optional use only.

Weighted sampling pilot18legal,10M each,44.347s wrapper: designs modes1/2 each lose3/3; congested mode1 loses3/3,mode2 wins1/loses2. Defaults stay shuffled. Iterative fusion compares the same7designs/8congested frozen archive pools over two sweeps,42.819s selection excluding rescorers and historical generation. Strict fusion gains10delay on congested03; donor-preferring ties add no scored benefit. Designs has no fusion gain.

Added fixedseed1 neutral10M designs/congested continuation costs22.282s wrapper;all7 improve. New scores designs1.2361933015773814,congested1.1021197794267317. Gains come from retained neutral adaptive repair/polish plus strict congested fusion, not weighted sampling or donor tie preference.

Pinned CLI coverage tier-sampling-fusion-followup-coverage.json independently confirms45/45legal. Unchanged tiers intro1.098317782147403,scale1.0479000969718766,stress1.02137484120527. Three new archives retain exact source/routes/manifests;all45restored hashes verified.39focused engine checks and3closure checks (340random exhaustive oracles plus explicit cases) pass;warning-free build. No upstream full-test rerun claimed.

Reference warm-start attribution and missing older ancestors/reference-generation cost remain disclosed. Added pilot/fusion/continuation costs are separate from historical search; expansion equality does not imply CPU equality. No final freeze, end-to-end regeneration, unseen-case or global-best claim.

Next: measure eligibility and repair cost before further sampling bias; compare bounded fresh candidate generation against continued incumbent search to seek useful alternative basins.
