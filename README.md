# taboown
A collection of offensive terms (mainly in Japanese) linked to wordnets


## Taboo Domains

This is a list of synsets considered potentially offensive.

There are six possible categorizations, and a synset can belong to more than one.

| Category  | Type     | Synset (PWN3.0) |   ILI   |
| --------  | -----    | ----------------| --------|
| sexual    | category | 00844254-n      | i39841  |
| LGBTQ+    | category | new             |         |
| excrement | category | 14853947-n      | i115114 |
| offensive | usage    | 06717170-n	 | i71809  |
| vulgar    | usage    | 07124340-n	 | i74099  |
| slur      | usage    | 06718862-n	 | i71813  |

[`data/taboo_domains.tsv`](data/taboo_domains.tsv) has 4 columns


| category | synset     | name.pos     | evidence |
| -------- | ---------- | ------------ | -------- |
| sexual   | 02133431-a	| lecherous.s  | insult05;insult09;sex10 |

See the paper at GWC2021 for more details

This is used to make a wordnet formatted using the GWA LMF, which can
be loaded by the python WN library or OMW.

[`data/taboown-dmn.xml`](data/taboown-dmn.xml)