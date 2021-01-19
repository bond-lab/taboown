from lxml import etree
from collections import defaultdict as dd

tsv = "data/taboo_domains.tsv"
xml = "data/taboown-dmn.xml"
ili = 'data/ili-map.tab'
nsmap = { 'dc':"http://purl.org/dc/elements/1.1/" }


root = etree.Element("LexicalResource", nsmap=nsmap)

lexicon = etree.SubElement(root, "Lexicon")
#print(lexicon)
lexicon.set('id', 'taboown-dmn')
lexicon.set('label', 'Taboo Wordnet Domains')
lexicon.set('language', 'en') 
lexicon.set('email', 'bond@ieee.org')
lexicon.set('license', 'https://creativecommons.org/licenses/by/4.0/')
lexicon.set('version', '1.0')
lexicon.set('citation', 'Merrick Choo Yeu Herng and Francis Bond (2021), Taboo Wordnet, GWC 2021')
lexicon.set('url', 'https://github.com/bond-lab/taboown')
lexicon.set('confidenceScore', '1.0') 

### Add a lexical entry for LGBTQ+
lexentry = etree.SubElement(lexicon, "LexicalEntry")
lexentry.set('id', 'lgbtq')

lemma = etree.SubElement(lexentry, "Lemma")
lemma.set('writtenForm', "LGBTQ+")
lemma.set('partOfSpeech', "n")
sense = etree.SubElement(lexentry, "Sense")
sense.set('id', "lgbtq-sns")
sense.set('synset', "taboown-lgbtq")

label = dict()
label['sexual'] = ('category', '00844254-n', 'i39841')
label['LGBTQ+'] = ('category', 'lgbtq', '')
label['excrement'] = ('category', '14853947-n', 'i115114')
label['offensive'] = ('usage', '06717170-n', 'i71809')
label['vulgar'] = ('usage', '07124340-n', 'i74099')
label['slur'] = ('usage', '06718862-n', 'i71813')


### get the ili mapping
ilimap = dd(str)
map_file = open(ili,'r')
for l in map_file:
    row = l.strip().split()
    ilimap[row[1]] = row[0]
    if row[1].endswith('-s'):
        ### map as either -s or -a
        ilimap[row[1].replace('-s','-a')] = row[0]


def addSynset(pwnid,pos):
    """Add a synset if it does not exist"""
    results = lexicon.xpath(f"//Synset[@id = 'taboown-{pwnid}']")
    if results:
        return results[0]
    else:
        synset = etree.SubElement(lexicon, 'Synset')
        synset.set('id', f'taboown-{pwnid}')
        if ilimap[pwnid]:
            synset.set('ili', f'ilimap[pwnid]')
        else:
            synset.set('ili','')
        synset.set('partOfSpeech', pos)
        return synset
        
### Add the synsets for the labels
for l in label:
    synset = etree.SubElement(lexicon, 'Synset')
    synset.set('id', f'taboown-{label[l][1]}')
    if label[l][2]:
        synset.set('ili', f'{label[l][2]}')
    else:
         synset.set('ili','')
    synset.set('partOfSpeech', 'n')
    if l == 'LGBTQ+':
        dfn = etree.SubElement(synset, 'Definition')
        dfn.text = 'an umbrella term for those who have a non-normative gender and/or sexual identity, including lesbian, gay, bisexual, transgender, intersex, or asexual'

        
### Add the synsets that are labelled
df = open(tsv)

for l in df:
    (cat, ss, name, evidence) = l.strip().split()
    synset = addSynset(ss, ss[-1])
    link = etree.SubElement(synset, 'SynsetRelation')
    ### Is it ok to label a thing with itself?   I think so
    if label[cat][0] == 'category':
        link.set('relType', 'domain_topic')
    elif label[cat][0] == 'usage':
        link.set('relType', 'exemplifies')
    else:
        link.set('relType', 'also')
        print('WARNING unknown topic:',  cat, ss, name, evidence)
    link.set('target', f'taboown-{label[cat][1]}')

        
### write
wndtd="""<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE LexicalResource SYSTEM "http://globalwordnet.github.io/schemas/WN-LMF-1.0.dtd">"""
tree = etree.ElementTree(root)
f = open(xml, 'wb')
f.write(etree.tostring(tree, pretty_print=True,
#                       xml_declaration=True, encoding='UTF-8',
                       doctype=wndtd))
f.close()
