#!/usr/bin/python
from __future__ import with_statement 

# ==============================================================================
# 						plotMyGBK
#
# Author: Sandro Valenzuela (sandrolvalenzuead@gmail.com) 
#
# Please type "python plotMyGBK.py -h" for usage help
#
# ==============================================================================

__author__ = 'Sandro Valenzuela (sandrolvalenzuead@gmail.com)'
__version__ = '1.0'
__date__ = '15 February 2016'

import sys, os, re, multiprocessing, subprocess, pandas as pd
from optparse import OptionParser
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.SeqFeature import SeqFeature, FeatureLocation
from Bio import SeqIO

def printCogMap():
	cogmap=open("cognames2003-2014.tab","w")
	cogmap.write("""
COG	func	name
COG0001	H	Glutamate-1-semialdehyde aminotransferase
COG0002	E	N-acetyl-gamma-glutamylphosphate reductase
COG0003	P	Anion-transporting ATPase, ArsA/GET3 family
COG0004	P	Ammonia channel protein AmtB
COG0005	F	Purine nucleoside phosphorylase
COG0006	E	Xaa-Pro aminopeptidase
COG0007	H	Uroporphyrinogen-III methylase (siroheme synthase)
COG0008	J	Glutamyl- or glutaminyl-tRNA synthetase
COG0009	J	tRNA A37 threonylcarbamoyladenosine synthetase subunit TsaC/SUA5/YrdC
COG0010	E	Arginase family enzyme
COG0011	S	Uncharacterized conserved protein YqgV, UPF0045/DUF77 family
COG0012	J	Ribosome-binding ATPase YchF, GTP1/OBG family
COG0013	J	Alanyl-tRNA synthetase
COG0014	E	Gamma-glutamyl phosphate reductase
COG0015	F	Adenylosuccinate lyase
COG0016	J	Phenylalanyl-tRNA synthetase alpha subunit
COG0017	J	Aspartyl/asparaginyl-tRNA synthetase
COG0018	J	Arginyl-tRNA synthetase
COG0019	E	Diaminopimelate decarboxylase
COG0020	I	Undecaprenyl pyrophosphate synthase
COG0021	G	Transketolase
COG0022	C	Pyruvate/2-oxoglutarate/acetoin dehydrogenase complex, dehydrogenase (E1) component
COG0023	J	Translation initiation factor 1 (eIF-1/SUI1)
COG0024	J	Methionine aminopeptidase
COG0025	P	NhaP-type Na+/H+ or K+/H+ antiporter
COG0026	F	Phosphoribosylaminoimidazole carboxylase (NCAIR synthetase)
COG0027	F	Formate-dependent phosphoribosylglycinamide formyltransferase (GAR transformylase)
COG0028	EH	Acetolactate synthase large subunit or other thiamine pyrophosphate-requiring enzyme
COG0029	H	Aspartate oxidase
COG0030	J	16S rRNA A1518 and A1519 N6-dimethyltransferase RsmA/KsgA/DIM1 (may also have DNA glycosylase/AP lyase activity)
COG0031	E	Cysteine synthase
COG0033	G	Phosphoglucomutase
COG0034	F	Glutamine phosphoribosylpyrophosphate amidotransferase
COG0035	F	Uracil phosphoribosyltransferase
COG0036	G	Pentose-5-phosphate-3-epimerase
COG0037	J	tRNA(Ile)-lysidine synthase TilS/MesJ
COG0038	P	H+/Cl- antiporter ClcA
COG0039	C	Malate/lactate dehydrogenase
COG0040	E	ATP phosphoribosyltransferase
COG0041	F	Phosphoribosylcarboxyaminoimidazole (NCAIR) mutase
COG0042	J	tRNA-dihydrouridine synthase
COG0043	H	3-polyprenyl-4-hydroxybenzoate decarboxylase
COG0044	F	Dihydroorotase or related cyclic amidohydrolase
COG0045	C	Succinyl-CoA synthetase, beta subunit
COG0046	F	Phosphoribosylformylglycinamidine (FGAM) synthase, synthetase domain
COG0047	F	Phosphoribosylformylglycinamidine (FGAM) synthase, glutamine amidotransferase domain
COG0048	J	Ribosomal protein S12
COG0049	J	Ribosomal protein S7
COG0050	J	Translation elongation factor EF-Tu, a GTPase
COG0051	J	Ribosomal protein S10
COG0052	J	Ribosomal protein S2
COG0053	P	Divalent metal cation (Fe/Co/Zn/Cd) transporter
COG0054	H	6,7-dimethyl-8-ribityllumazine synthase (Riboflavin synthase beta chain)
COG0055	C	FoF1-type ATP synthase, beta subunit
COG0056	C	FoF1-type ATP synthase, alpha subunit
COG0057	G	Glyceraldehyde-3-phosphate dehydrogenase/erythrose-4-phosphate dehydrogenase
COG0058	G	Glucan phosphorylase
COG0059	EH	Ketol-acid reductoisomerase
COG0060	J	Isoleucyl-tRNA synthetase
COG0061	F	NAD kinase
COG0062	F	NAD(P)H-hydrate repair enzyme Nnr, NAD(P)H-hydrate epimerase domain
COG0063	F	NAD(P)H-hydrate repair enzyme Nnr, NAD(P)H-hydrate dehydratase domain
COG0064	J	Asp-tRNAAsn/Glu-tRNAGln amidotransferase B subunit
COG0065	E	Homoaconitase/3-isopropylmalate dehydratase large subunit
COG0066	E	3-isopropylmalate dehydratase small subunit
COG0067	E	Glutamate synthase domain 1
COG0068	O	Hydrogenase maturation factor HypF (carbamoyltransferase)
COG0069	E	Glutamate synthase domain 2
COG0070	E	Glutamate synthase domain 3
COG0071	O	Molecular chaperone IbpA, HSP20 family
COG0072	J	Phenylalanyl-tRNA synthetase beta subunit
COG0073	J	tRNA-binding EMAP/Myf domain
COG0074	C	Succinyl-CoA synthetase, alpha subunit
COG0075	EF	Archaeal aspartate aminotransferase or a related aminotransferase, includes purine catabolism protein PucG
COG0076	E	Glutamate or tyrosine decarboxylase or a related PLP-dependent protein
COG0077	E	Prephenate dehydratase
COG0078	E	Ornithine carbamoyltransferase
COG0079	E	Histidinol-phosphate/aromatic aminotransferase or cobyric acid decarboxylase
COG0080	J	Ribosomal protein L11
COG0081	J	Ribosomal protein L1
COG0082	E	Chorismate synthase
COG0083	E	Homoserine kinase
COG0084	N	Tat protein secretion system quality control protein TatD (DNase activity)
COG0085	K	DNA-directed RNA polymerase, beta subunit/140 kD subunit
COG0086	K	DNA-directed RNA polymerase, beta' subunit/160 kD subunit
COG0087	J	Ribosomal protein L3
COG0088	J	Ribosomal protein L4
COG0089	J	Ribosomal protein L23
COG0090	J	Ribosomal protein L2
COG0091	J	Ribosomal protein L22
COG0092	J	Ribosomal protein S3
COG0093	J	Ribosomal protein L14
COG0094	J	Ribosomal protein L5
COG0095	H	Lipoate-protein ligase A
COG0096	J	Ribosomal protein S8
COG0097	J	Ribosomal protein L6P/L9E
COG0098	J	Ribosomal protein S5
COG0099	J	Ribosomal protein S13
COG0100	J	Ribosomal protein S11
COG0101	J	tRNA U38,U39,U40 pseudouridine synthase TruA
COG0102	J	Ribosomal protein L13
COG0103	J	Ribosomal protein S9
COG0104	F	Adenylosuccinate synthase
COG0105	F	Nucleoside diphosphate kinase
COG0106	E	Phosphoribosylformimino-5-aminoimidazole carboxamide ribonucleotide (ProFAR) isomerase
COG0107	E	Imidazole glycerol phosphate synthase subunit HisF
COG0108	H	3,4-dihydroxy-2-butanone 4-phosphate synthase
COG0109	HI	Polyprenyltransferase (heme O synthase)
COG0110	R	Acetyltransferase (isoleucine patch superfamily)
COG0111	HR	Phosphoglycerate dehydrogenase or related dehydrogenase
COG0112	E	Glycine/serine hydroxymethyltransferase
COG0113	H	Delta-aminolevulinic acid dehydratase, porphobilinogen synthase
COG0114	C	Fumarate hydratase class II
COG0115	EH	Branched-chain amino acid aminotransferase/4-amino-4-deoxychorismate lyase
COG0116	J	23S rRNA G2445 N2-methylase RlmL
COG0117	H	Pyrimidine deaminase domain of riboflavin biosynthesis protein RibD
COG0118	E	Imidazoleglycerol phosphate synthase glutamine amidotransferase subunit HisH
COG0119	E	Isopropylmalate/homocitrate/citramalate synthases
COG0120	G	Ribose 5-phosphate isomerase
COG0121	R	Predicted glutamine amidotransferase
COG0122	L	3-methyladenine DNA glycosylase/8-oxoguanine DNA glycosylase
COG0123	BQ	Acetoin utilization deacetylase AcuC or a related deacetylase
COG0124	J	Histidyl-tRNA synthetase
COG0125	F	Thymidylate kinase
COG0126	G	3-phosphoglycerate kinase
COG0127	F	Inosine/xanthosine triphosphate pyrophosphatase, all-alpha NTP-PPase family
COG0128	E	5-enolpyruvylshikimate-3-phosphate synthase
COG0129	EG	Dihydroxyacid dehydratase/phosphogluconate dehydratase
COG0130	J	tRNA U55 pseudouridine synthase TruB, may also work on U342 of tmRNA
COG0131	E	Imidazoleglycerol phosphate dehydratase HisB
COG0132	H	Dethiobiotin synthetase
COG0133	E	Tryptophan synthase beta chain
COG0134	E	Indole-3-glycerol phosphate synthase
COG0135	E	Phosphoribosylanthranilate isomerase
COG0136	E	Aspartate-semialdehyde dehydrogenase
COG0137	E	Argininosuccinate synthase
COG0138	F	AICAR transformylase/IMP cyclohydrolase PurH
COG0139	E	Phosphoribosyl-AMP cyclohydrolase
COG0140	E	Phosphoribosyl-ATP pyrophosphohydrolase
COG0141	E	Histidinol dehydrogenase
COG0142	H	Geranylgeranyl pyrophosphate synthase
COG0143	J	Methionyl-tRNA synthetase
COG0144	J	16S rRNA C967 or C1407 C5-methylase, RsmB/RsmF family
COG0145	EQ	N-methylhydantoinase A/oxoprolinase/acetone carboxylase, beta subunit
COG0146	EQ	N-methylhydantoinase B/oxoprolinase/acetone carboxylase, alpha subunit
COG0147	EH	Anthranilate/para-aminobenzoate synthases component I
COG0148	G	Enolase
COG0149	G	Triosephosphate isomerase
COG0150	F	Phosphoribosylaminoimidazole (AIR) synthetase
COG0151	F	Phosphoribosylamine-glycine ligase
COG0152	F	Phosphoribosylaminoimidazole-succinocarboxamide synthase
COG0153	G	Galactokinase
COG0154	J	Asp-tRNAAsn/Glu-tRNAGln amidotransferase A subunit or related amidase
COG0155	P	Sulfite reductase, beta subunit (hemoprotein)
COG0156	H	7-keto-8-aminopelargonate synthetase or related enzyme
COG0157	H	Nicotinate-nucleotide pyrophosphorylase
COG0158	G	Fructose-1,6-bisphosphatase
COG0159	E	Tryptophan synthase alpha chain
COG0160	E	4-aminobutyrate aminotransferase or related aminotransferase
COG0161	H	Adenosylmethionine-8-amino-7-oxononanoate aminotransferase
COG0162	J	Tyrosyl-tRNA synthetase
COG0163	H	3-polyprenyl-4-hydroxybenzoate decarboxylase
COG0164	L	Ribonuclease HII
COG0165	E	Argininosuccinate lyase
COG0166	G	Glucose-6-phosphate isomerase
COG0167	F	Dihydroorotate dehydrogenase
COG0168	P	Trk-type K+ transport system, membrane component
COG0169	E	Shikimate 5-dehydrogenase
COG0170	O	Dolichol kinase
COG0171	H	NH3-dependent NAD+ synthetase
COG0172	J	Seryl-tRNA synthetase
COG0173	J	Aspartyl-tRNA synthetase
COG0174	E	Glutamine synthetase
COG0175	EH	3'-phosphoadenosine 5'-phosphosulfate sulfotransferase (PAPS reductase)/FAD synthetase or related enzyme
COG0176	G	Transaldolase
COG0177	L	Endonuclease III
COG0178	L	Excinuclease UvrABC ATPase subunit
COG0179	Q	2-keto-4-pentenoate hydratase/2-oxohepta-3-ene-1,7-dioic acid hydratase (catechol pathway)
COG0180	J	Tryptophanyl-tRNA synthetase
COG0181	H	Porphobilinogen deaminase
COG0182	E	Methylthioribose-1-phosphate isomerase (methionine salvage pathway), a paralog of eIF-2B alpha subunit
COG0183	I	Acetyl-CoA acetyltransferase
COG0184	J	Ribosomal protein S15P/S13E
COG0185	J	Ribosomal protein S19
COG0186	J	Ribosomal protein S17
COG0187	L	DNA gyrase/topoisomerase IV, subunit B
COG0188	L	DNA gyrase/topoisomerase IV, subunit A
COG0189	HJ	Glutathione synthase/RimK-type ligase, ATP-grasp superfamily
COG0190	H	5,10-methylene-tetrahydrofolate dehydrogenase/Methenyl tetrahydrofolate cyclohydrolase
COG0191	G	Fructose/tagatose bisphosphate aldolase
COG0192	H	S-adenosylmethionine synthetase
COG0193	J	Peptidyl-tRNA hydrolase
COG0194	F	Guanylate kinase
COG0195	K	Transcription antitermination factor NusA, contains S1 and KH domains
COG0196	H	FAD synthase
COG0197	J	Ribosomal protein L16/L10AE
COG0198	J	Ribosomal protein L24
COG0199	J	Ribosomal protein S14
COG0200	J	Ribosomal protein L15
COG0201	U	Preprotein translocase subunit SecY
COG0202	K	DNA-directed RNA polymerase, alpha subunit/40 kD subunit
COG0203	J	Ribosomal protein L17
COG0204	I	1-acyl-sn-glycerol-3-phosphate acyltransferase
COG0205	G	6-phosphofructokinase
COG0206	D	Cell division GTPase FtsZ
COG0207	F	Thymidylate synthase
COG0208	F	Ribonucleotide reductase beta subunit, ferritin-like domain
COG0209	F	Ribonucleotide reductase alpha subunit
COG0210	L	Superfamily I DNA or RNA helicase
COG0211	J	Ribosomal protein L27
COG0212	H	5-formyltetrahydrofolate cyclo-ligase
COG0213	F	Thymidine phosphorylase
COG0214	H	Pyridoxal biosynthesis lyase PdxS
COG0215	J	Cysteinyl-tRNA synthetase
COG0216	J	Protein chain release factor A
COG0217	KJ	Transcriptional and/or translational regulatory protein YebC/TACO1
COG0218	D	GTP-binding protein EngB required for normal cell division
COG0219	J	tRNA(Leu) C34 or U34 (ribose-2'-O)-methylase TrmL, contains SPOUT domain
COG0220	J	tRNA G46 methylase TrmB
COG0221	CP	Inorganic pyrophosphatase
COG0222	J	Ribosomal protein L7/L12
COG0223	J	Methionyl-tRNA formyltransferase
COG0224	C	FoF1-type ATP synthase, gamma subunit
COG0225	O	Peptide methionine sulfoxide reductase MsrA
COG0226	P	ABC-type phosphate transport system, periplasmic component
COG0227	J	Ribosomal protein L28
COG0228	J	Ribosomal protein S16
COG0229	O	Peptide methionine sulfoxide reductase MsrB
COG0230	J	Ribosomal protein L34
COG0231	J	Translation elongation factor P (EF-P)/translation initiation factor 5A (eIF-5A)
COG0232	F	dGTP triphosphohydrolase
COG0233	J	Ribosome recycling factor
COG0234	O	Co-chaperonin GroES (HSP10)
COG0235	G	Ribulose-5-phosphate 4-epimerase/Fuculose-1-phosphate aldolase
COG0236	IQ	Acyl carrier protein
COG0237	H	Dephospho-CoA kinase
COG0238	J	Ribosomal protein S18
COG0239	DP	Fluoride ion exporter CrcB/FEX, affects chromosome condensation
COG0240	C	Glycerol-3-phosphate dehydrogenase
COG0241	E	Histidinol phosphatase or a related phosphatase
COG0242	J	Peptide deformylase
COG0243	C	Anaerobic selenocysteine-containing dehydrogenase
COG0244	J	Ribosomal protein L10
COG0245	I	2C-methyl-D-erythritol 2,4-cyclodiphosphate synthase
COG0246	G	Mannitol-1-phosphate/altronate dehydrogenases
COG0247	C	Fe-S oxidoreductase
COG0248	FTP	Exopolyphosphatase/pppGpp-phosphohydrolase
COG0249	L	DNA mismatch repair ATPase MutS
COG0250	K	Transcription antitermination factor NusG
COG0251	V	Enamine deaminase RidA, house cleaning of reactive enamine intermediates, YjgF/YER057c/UK114 family
COG0252	JU	L-asparaginase/archaeal Glu-tRNAGln amidotransferase subunit D
COG0253	E	Diaminopimelate epimerase
COG0254	J	Ribosomal protein L31
COG0255	J	Ribosomal protein L29
COG0256	J	Ribosomal protein L18
COG0257	J	Ribosomal protein L36
COG0258	L	5'-3' exonuclease
COG0259	H	Pyridoxine/pyridoxamine 5'-phosphate oxidase
COG0260	E	Leucyl aminopeptidase
COG0261	J	Ribosomal protein L21
COG0262	H	Dihydrofolate reductase
COG0263	E	Glutamate 5-kinase
COG0264	J	Translation elongation factor EF-Ts
COG0265	O	Periplasmic serine protease, S1-C subfamily, contain C-terminal PDZ domain
COG0266	L	Formamidopyrimidine-DNA glycosylase
COG0267	J	Ribosomal protein L33
COG0268	J	Ribosomal protein S20
COG0269	G	3-keto-L-gulonate-6-phosphate decarboxylase
COG0270	L	Site-specific DNA-cytosine methylase
COG0271	T	Stress-induced morphogen (activity unknown)
COG0272	L	NAD-dependent DNA ligase
COG0274	F	Deoxyribose-phosphate aldolase
COG0275	J	16S rRNA C1402 N4-methylase RsmH
COG0276	H	Protoheme ferro-lyase (ferrochelatase)
COG0277	C	FAD/FMN-containing dehydrogenase
COG0278	O	Glutaredoxin-related protein
COG0279	G	Phosphoheptose isomerase
COG0280	C	Phosphotransacetylase
COG0281	C	Malic enzyme
COG0282	C	Acetate kinase
COG0283	F	Cytidylate kinase
COG0284	F	Orotidine-5'-phosphate decarboxylase
COG0285	H	Folylpolyglutamate synthase/Dihydropteroate synthase
COG0286	V	Type I restriction-modification system, DNA methylase subunit
COG0287	E	Prephenate dehydrogenase
COG0288	P	Carbonic anhydrase
COG0289	E	Dihydrodipicolinate reductase
COG0290	J	Translation initiation factor IF-3
COG0291	J	Ribosomal protein L35
COG0292	J	Ribosomal protein L20
COG0293	J	23S rRNA U2552 (ribose-2'-O)-methylase RlmE/FtsJ
COG0294	H	Dihydropteroate synthase
COG0295	F	Cytidine deaminase
COG0296	G	1,4-alpha-glucan branching enzyme
COG0297	G	Glycogen synthase
COG0298	O	Hydrogenase maturation factor
COG0299	F	Folate-dependent phosphoribosylglycinamide formyltransferase PurN
COG0300	R	Short-chain dehydrogenase
COG0301	HJ	Adenylyl- and sulfurtransferase ThiI, participates in tRNA 4-thiouridine and thiamine biosynthesis
COG0302	H	GTP cyclohydrolase I
COG0303	H	Molybdopterin biosynthesis enzyme
COG0304	IQ	3-oxoacyl-(acyl-carrier-protein) synthase
COG0305	L	Replicative DNA helicase
COG0306	P	Phosphate/sulfate permease
COG0307	H	Riboflavin synthase alpha chain
COG0308	E	Aminopeptidase N
COG0309	O	Hydrogenase maturation factor
COG0310	P	ABC-type Co2+ transport system, permease component
COG0311	H	Glutamine amidotransferase PdxT (pyridoxal biosynthesis)
COG0312	R	Predicted Zn-dependent protease or its inactivated homolog
COG0313	J	16S rRNA C1402 (ribose-2'-O) methylase RsmI
COG0314	H	Molybdopterin synthase catalytic subunit
COG0315	H	Molybdenum cofactor biosynthesis enzyme
COG0316	O	Fe-S cluster assembly iron-binding protein IscA
COG0317	TK	(p)ppGpp synthase/hydrolase, HD superfamily
COG0318	IQ	Acyl-CoA synthetase (AMP-forming)/AMP-acid ligase II
COG0319	J	ssRNA-specific RNase YbeY, 16S rRNA maturation enzyme
COG0320	H	Lipoate synthase
COG0321	H	Lipoate-protein ligase B
COG0322	L	Excinuclease UvrABC, nuclease subunit
COG0323	L	DNA mismatch repair ATPase MutL
COG0324	J	tRNA A37 N6-isopentenylltransferase MiaA
COG0325	R	Uncharacterized pyridoxal phosphate-containing protein, affects Ilv metabolism, UPF0001 family
COG0326	O	Molecular chaperone, HSP90 family
COG0327	H	Putative GTP cyclohydrolase 1 type 2, NIF3 family
COG0328	L	Ribonuclease HI
COG0329	EM	Dihydrodipicolinate synthase/N-acetylneuraminate lyase
COG0330	O	Regulator of protease activity HflC, stomatin/prohibitin superfamily
COG0331	I	Malonyl CoA-acyl carrier protein transacylase
COG0332	I	3-oxoacyl-[acyl-carrier-protein] synthase III
COG0333	J	Ribosomal protein L32
COG0334	E	Glutamate dehydrogenase/leucine dehydrogenase
COG0335	J	Ribosomal protein L19
COG0336	J	tRNA G37 N-methylase TrmD
COG0337	E	3-dehydroquinate synthetase
COG0338	L	Site-specific DNA-adenine methylase
COG0339	E	Zn-dependent oligopeptidase
COG0340	H	Biotin-(acetyl-CoA carboxylase) ligase
COG0341	U	Preprotein translocase subunit SecF
COG0342	U	Preprotein translocase subunit SecD
COG0343	J	Queuine/archaeosine tRNA-ribosyltransferase
COG0344	I	Phospholipid biosynthesis protein PlsY, probable glycerol-3-phosphate acyltransferase
COG0345	E	Pyrroline-5-carboxylate reductase
COG0346	Q	Catechol 2,3-dioxygenase or other lactoylglutathione lyase family enzyme
COG0347	TE	Nitrogen regulatory protein PII
COG0348	C	Polyferredoxin
COG0349	J	Ribonuclease D
COG0350	L	O6-methylguanine-DNA--protein-cysteine methyltransferase
COG0351	H	Hydroxymethylpyrimidine/phosphomethylpyrimidine kinase
COG0352	H	Thiamine monophosphate synthase
COG0353	L	Recombinational DNA repair protein RecR
COG0354	O	Folate-binding Fe-S cluster repair protein YgfZ, possible role in tRNA modification
COG0355	C	FoF1-type ATP synthase, epsilon subunit
COG0356	C	FoF1-type ATP synthase, membrane subunit a
COG0357	J	16S rRNA G527 N7-methylase RsmG (former glucose-inhibited division protein B)
COG0358	L	DNA primase (bacterial type)
COG0359	J	Ribosomal protein L9
COG0360	J	Ribosomal protein S6
COG0361	J	Translation initiation factor IF-1
COG0362	G	6-phosphogluconate dehydrogenase
COG0363	G	6-phosphogluconolactonase/Glucosamine-6-phosphate isomerase/deaminase
COG0364	G	Glucose-6-phosphate 1-dehydrogenase
COG0365	I	Acyl-coenzyme A synthetase/AMP-(fatty) acid ligase
COG0366	G	Glycosidase
COG0367	E	Asparagine synthetase B (glutamine-hydrolyzing)
COG0368	H	Cobalamin synthase
COG0369	P	Sulfite reductase, alpha subunit (flavoprotein)
COG0370	P	Fe2+ transport system protein B
COG0371	C	Glycerol dehydrogenase or related enzyme, iron-containing ADH family
COG0372	C	Citrate synthase
COG0373	H	Glutamyl-tRNA reductase
COG0374	C	Ni,Fe-hydrogenase I large subunit
COG0375	R	Zn finger protein HypA/HybF (possibly regulating hydrogenase expression)
COG0376	P	Catalase (peroxidase I)
COG0377	C	NADH:ubiquinone oxidoreductase 20 kD subunit (chhain B) or related Fe-S oxidoreductase
COG0378	O	Ni2+-binding GTPase involved in regulation of expression and maturation of urease and hydrogenase
COG0379	H	Quinolinate synthase
COG0380	G	Trehalose-6-phosphate synthase
COG0381	M	UDP-N-acetylglucosamine 2-epimerase
COG0382	H	4-hydroxybenzoate polyprenyltransferase
COG0383	G	Alpha-mannosidase
COG0384	R	Predicted epimerase YddE/YHI9, PhzF superfamily
COG0385	R	Predicted Na+-dependent transporter
COG0386	VI	Glutathione peroxidase, house-cleaning role in reducing lipid peroxides
COG0387	P	Ca2+/H+ antiporter
COG0388	R	Predicted amidohydrolase
COG0389	L	Nucleotidyltransferase/DNA polymerase involved in DNA repair
COG0390	P	ABC-type iron transport system FetAB, permease component
COG0391	HG	Archaeal 2-phospho-L-lactate transferase/Bacterial gluconeogenesis factor, CofD/UPF0052 family
COG0392	S	Uncharacterized membrane protein YbhN, UPF0104 family
COG0393	S	Uncharacterized conserved protein YbjQ, UPF0145 family
COG0394	T	Protein-tyrosine-phosphatase
COG0395	G	ABC-type glycerol-3-phosphate transport system, permease component
COG0396	O	Fe-S cluster assembly ATPase SufC
COG0397	S	Uncharacterized conserved protein YdiU, UPF0061 family
COG0398	S	Uncharacterized membrane protein YdjX, TVP38/TMEM64 family, SNARE-associated domain
COG0399	M	dTDP-4-amino-4,6-dideoxygalactose transaminase
COG0400	R	Predicted esterase
COG0401	S	Uncharacterized membrane protein YqaE, homolog of Blt101, UPF0057 family
COG0402	FR	Cytosine/adenosine deaminase or related metal-dependent hydrolase
COG0403	E	Glycine cleavage system protein P (pyridoxal-binding), N-terminal domain
COG0404	E	Glycine cleavage system T protein (aminomethyltransferase)
COG0405	E	Gamma-glutamyltranspeptidase
COG0406	G	Broad specificity phosphatase PhoE
COG0407	H	Uroporphyrinogen-III decarboxylase
COG0408	H	Coproporphyrinogen III oxidase
COG0409	O	Hydrogenase maturation factor
COG0410	E	ABC-type branched-chain amino acid transport system, ATPase component
COG0411	E	ABC-type branched-chain amino acid transport system, ATPase component
COG0412	Q	Dienelactone hydrolase
COG0413	H	Ketopantoate hydroxymethyltransferase
COG0414	H	Panthothenate synthetase
COG0415	L	Deoxyribodipyrimidine photolyase
COG0416	I	Fatty acid/phospholipid biosynthesis enzyme
COG0417	L	DNA polymerase elongation subunit (family B)
COG0418	F	Dihydroorotase
COG0419	L	DNA repair exonuclease SbcCD ATPase subunit
COG0420	L	DNA repair exonuclease SbcCD nuclease subunit
COG0421	E	Spermidine synthase
COG0422	H	Thiamine biosynthesis protein ThiC
COG0423	J	Glycyl-tRNA synthetase (class II)
COG0424	Q	Predicted house-cleaning NTP pyrophosphatase, Maf/HAM1 superfamily
COG0425	O	TusA-related sulfurtransferase
COG0426	C	Flavorubredoxin
COG0427	C	Acyl-CoA hydrolase
COG0428	P	Zinc transporter ZupT
COG0429	R	Predicted hydrolase of the alpha/beta-hydrolase fold
COG0430	A	RNA 3'-terminal phosphate cyclase
COG0431	C	NAD(P)H-dependent FMN reductase
COG0432	H	Thiamin phosphate synthase YjbQ, UPF0047 family
COG0433	L	Archaeal DNA helicase HerA or a related bacterial ATPase, contains HAS-barrel and ATPase domains
COG0434	R	Predicted TIM-barrel enzyme
COG0435	C	Glutathionyl-hydroquinone reductase
COG0436	E	Aspartate/methionine/tyrosine aminotransferase
COG0437	C	Fe-S-cluster-containing dehydrogenase component
COG0438	M	Glycosyltransferase involved in cell wall bisynthesis
COG0439	I	Biotin carboxylase
COG0440	E	Acetolactate synthase, small subunit
COG0441	J	Threonyl-tRNA synthetase
COG0442	J	Prolyl-tRNA synthetase
COG0443	O	Molecular chaperone DnaK (HSP70)
COG0444	EP	ABC-type dipeptide/oligopeptide/nickel transport system, ATPase component
COG0445	J	tRNA U34 5-carboxymethylaminomethyl modifying enzyme MnmG/GidA
COG0446	I	NADPH-dependent 2,4-dienoyl-CoA reductase, sulfur reductase, or a related oxidoreductase
COG0447	H	1,4-Dihydroxy-2-naphthoyl-CoA synthase
COG0448	G	ADP-glucose pyrophosphorylase
COG0449	M	Glucosamine 6-phosphate synthetase, contains amidotransferase and phosphosugar isomerase domains
COG0450	V	Alkyl hydroperoxide reductase subunit AhpC (peroxiredoxin)
COG0451	M	Nucleoside-diphosphate-sugar epimerase
COG0452	H	Phosphopantothenoylcysteine synthetase/decarboxylase
COG0454	KR	N-acetyltransferase, GNAT superfamily (includes histone acetyltransferase HPA2)
COG0455	DN	MinD-like ATPase involved in chromosome partitioning or flagellar assembly
COG0456	J	Ribosomal protein S18 acetylase RimI and related acetyltransferases
COG0457	R	Tetratricopeptide (TPR) repeat
COG0458	EF	Carbamoylphosphate synthase large subunit
COG0459	O	Chaperonin GroEL (HSP60 family)
COG0460	E	Homoserine dehydrogenase
COG0461	F	Orotate phosphoribosyltransferase
COG0462	FE	Phosphoribosylpyrophosphate synthetase
COG0463	M	Glycosyltransferase involved in cell wall bisynthesis
COG0464	MDT	AAA+-type ATPase, SpoVK/Ycf46/Vps4 family
COG0465	O	ATP-dependent Zn proteases
COG0466	O	ATP-dependent Lon protease, bacterial type
COG0467	T	RecA-superfamily ATPase, KaiC/GvpD/RAD55 family
COG0468	L	RecA/RadA recombinase
COG0469	G	Pyruvate kinase
COG0470	L	DNA polymerase III, delta prime subunit
COG0471	G	Di- and tricarboxylate transporter
COG0472	M	UDP-N-acetylmuramyl pentapeptide phosphotransferase/UDP-N-acetylglucosamine-1-phosphate transferase
COG0473	CE	Isocitrate/isopropylmalate dehydrogenase
COG0474	P	Magnesium-transporting ATPase (P-type)
COG0475	P	Kef-type K+ transport system, membrane component KefB
COG0476	H	Molybdopterin or thiamine biosynthesis adenylyltransferase
COG0477	GEPR	MFS family permease
COG0478	T	RIO-like serine/threonine protein kinase fused to N-terminal HTH domain
COG0479	C	Succinate dehydrogenase/fumarate reductase, Fe-S protein subunit
COG0480	J	Translation elongation factor EF-G, a GTPase
COG0481	J	Translation elongation factor EF-4, membrane-bound GTPase
COG0482	J	tRNA U34 2-thiouridine synthase MnmA/TrmU, contains the PP-loop ATPase domain
COG0483	G	Archaeal fructose-1,6-bisphosphatase or related enzyme of inositol monophosphatase family
COG0484	O	DnaJ-class molecular chaperone with C-terminal Zn finger domain
COG0486	J	tRNA U34 5-carboxymethylaminomethyl modifying GTPase MnmE/TrmE
COG0488	R	ATPase components of ABC transporters with duplicated ATPase domains
COG0489	D	Chromosome partitioning ATPase, Mrp family, contains Fe-S cluster
COG0490	P	K+/H+ antiporter YhaU, regulatory subunit KhtT
COG0491	R	Glyoxylase or a related metal-dependent hydrolase, beta-lactamase superfamily II
COG0492	O	Thioredoxin reductase
COG0493	ER	NADPH-dependent glutamate synthase beta chain or related oxidoreductase
COG0494	V	8-oxo-dGTP pyrophosphatase MutT and related house-cleaning NTP pyrophosphohydrolases, NUDIX family
COG0495	J	Leucyl-tRNA synthetase
COG0496	L	Broad specificity polyphosphatase and 5'/3'-nucleotidase SurE
COG0497	L	DNA repair ATPase RecN
COG0498	E	Threonine synthase
COG0499	H	S-adenosylhomocysteine hydrolase
COG0500	QR	SAM-dependent methyltransferase
COG0501	O	Zn-dependent protease with chaperone function
COG0502	H	Biotin synthase or related enzyme
COG0503	F	Adenine/guanine phosphoribosyltransferase or related PRPP-binding protein
COG0504	F	CTP synthase (UTP-ammonia lyase)
COG0505	EF	Carbamoylphosphate synthase small subunit
COG0506	E	Proline dehydrogenase
COG0507	L	ATP-dependent exoDNAse (exonuclease V), alpha subunit, helicase superfamily I
COG0508	C	Pyruvate/2-oxoglutarate dehydrogenase complex, dihydrolipoamide acyltransferase (E2) component
COG0509	E	Glycine cleavage system H protein (lipoate-binding)
COG0510	H	Thiamine kinase and related kinases
COG0511	HI	Biotin carboxyl carrier protein
COG0512	EH	Anthranilate/para-aminobenzoate synthase component II
COG0513	L	Superfamily II DNA and RNA helicase
COG0514	L	Superfamily II DNA helicase RecQ
COG0515	T	Serine/threonine protein kinase
COG0516	F	IMP dehydrogenase/GMP reductase
COG0517	T	CBS domain
COG0518	F	GMP synthase - Glutamine amidotransferase domain
COG0519	F	GMP synthase, PP-ATPase domain/subunit
COG0520	E	Selenocysteine lyase/Cysteine desulfurase
COG0521	H	Molybdopterin biosynthesis enzyme MoaB
COG0522	J	Ribosomal protein S4 or related protein
COG0523	R	GTPase, G3E family
COG0524	G	Sugar or nucleoside kinase, ribokinase family
COG0525	J	Valyl-tRNA synthetase
COG0526	O	Thiol-disulfide isomerase or thioredoxin
COG0527	E	Aspartokinase
COG0528	F	Uridylate kinase
COG0529	P	Adenylylsulfate kinase or related kinase
COG0530	P	Ca2+/Na+ antiporter
COG0531	E	Amino acid transporter
COG0532	J	Translation initiation factor IF-2, a GTPase
COG0533	J	tRNA A37 threonylcarbamoyltransferase TsaD
COG0534	V	Na+-driven multidrug efflux pump
COG0535	R	Radical SAM superfamily enzyme, MoaA/NifB/PqqE/SkfB family
COG0536	DL	GTPase involved in cell partioning and DNA repair
COG0537	FGR	Diadenosine tetraphosphate (Ap4A) hydrolase or other HIT family hydrolase
COG0538	C	Isocitrate dehydrogenase
COG0539	J	Ribosomal protein S1
COG0540	F	Aspartate carbamoyltransferase, catalytic chain
COG0541	U	Signal recognition particle GTPase
COG0542	O	ATP-dependent Clp protease ATP-binding subunit ClpA
COG0543	HC	NAD(P)H-flavin reductase
COG0544	O	FKBP-type peptidyl-prolyl cis-trans isomerase (trigger factor)
COG0545	O	FKBP-type peptidyl-prolyl cis-trans isomerase
COG0546	C	Phosphoglycolate phosphatase, HAD superfamily
COG0547	E	Anthranilate phosphoribosyltransferase
COG0548	E	Acetylglutamate kinase
COG0549	E	Carbamate kinase
COG0550	L	DNA topoisomerase IA
COG0551	L	ssDNA-binding Zn-finger and Zn-ribbon domains of topoisomerase 1
COG0552	U	Signal recognition particle GTPase
COG0553	KL	Superfamily II DNA or RNA helicase, SNF2 family
COG0554	C	Glycerol kinase
COG0555	P	ABC-type sulfate transport system, permease component
COG0556	L	Excinuclease UvrABC helicase subunit UvrB
COG0557	K	Exoribonuclease R
COG0558	I	Phosphatidylglycerophosphate synthase
COG0559	E	Branched-chain amino acid ABC-type transport system, permease component
COG0560	E	Phosphoserine phosphatase
COG0561	HR	Hydroxymethylpyrimidine pyrophosphatase and other HAD family phosphatases
COG0562	M	UDP-galactopyranose mutase
COG0563	F	Adenylate kinase or related kinase
COG0564	J	Pseudouridylate synthase, 23S rRNA- or tRNA-specific
COG0565	J	tRNA C32,U32 (ribose-2'-O)-methylase TrmJ or a related methyltransferase
COG0566	J	tRNA G18 (ribose-2'-O)-methylase SpoU
COG0567	C	2-oxoglutarate dehydrogenase complex, dehydrogenase (E1) component, and related enzymes
COG0568	K	DNA-directed RNA polymerase, sigma subunit (sigma70/sigma32)
COG0569	P	Trk K+ transport system, NAD-binding component
COG0571	K	dsRNA-specific ribonuclease
COG0572	F	Uridine kinase
COG0573	P	ABC-type phosphate transport system, permease component
COG0574	G	Phosphoenolpyruvate synthase/pyruvate phosphate dikinase
COG0575	I	CDP-diglyceride synthetase
COG0576	O	Molecular chaperone GrpE (heat shock protein)
COG0577	V	ABC-type antimicrobial peptide transport system, permease component
COG0578	C	Glycerol-3-phosphate dehydrogenase
COG0579	G	L-2-hydroxyglutarate oxidase LhgO
COG0580	G	Glycerol uptake facilitator and related aquaporins (Major Intrinsic Protein Family)
COG0581	P	ABC-type phosphate transport system, permease component
COG0582	LX	Integrase
COG0583	K	DNA-binding transcriptional regulator, LysR family
COG0584	I	Glycerophosphoryl diester phosphodiesterase
COG0585	J	tRNA(Glu) U13 pseudouridine synthase TruD
COG0586	S	Uncharacterized membrane protein DedA, SNARE-associated domain
COG0587	L	DNA polymerase III, alpha subunit
COG0588	G	Phosphoglycerate mutase (BPG-dependent)
COG0589	T	Nucleotide-binding universal stress protein,  UspA family
COG0590	J	tRNA(Arg) A34 adenosine deaminase TadA
COG0591	E	Na+/proline symporter
COG0592	L	DNA polymerase III sliding clamp (beta) subunit, PCNA homolog
COG0593	L	Chromosomal replication initiation ATPase DnaA
COG0594	J	RNase P protein component
COG0595	J	mRNA degradation ribonuclease J1/J2
COG0596	HR	Pimeloyl-ACP methyl ester carboxylesterase
COG0597	MU	Lipoprotein signal peptidase
COG0598	P	Mg2+ and Co2+ transporter CorA
COG0599	R	Uncharacterized conserved protein YurZ, alkylhydroperoxidase/carboxymuconolactone decarboxylase family
COG0600	P	ABC-type nitrate/sulfonate/bicarbonate transport system, permease component
COG0601	EP	ABC-type dipeptide/oligopeptide/nickel transport system, permease component
COG0602	R	Organic radical activating enzyme
COG0603	J	7-cyano-7-deazaguanine synthase (queuosine biosynthesis)
COG0604	CR	NADPH:quinone reductase or related Zn-dependent oxidoreductase
COG0605	P	Superoxide dismutase
COG0606	O	Predicted ATPase with chaperone activity
COG0607	P	Rhodanese-related sulfurtransferase
COG0608	L	Single-stranded DNA-specific exonuclease, DHH superfamily, may be involved in archaeal DNA replication intiation
COG0609	P	ABC-type Fe3+-siderophore transport system, permease component
COG0610	V	Type I site-specific restriction-modification system, R (restriction) subunit and related helicases ...
COG0611	H	Thiamine monophosphate kinase
COG0612	R	Predicted Zn-dependent peptidase
COG0613	R	Predicted metal-dependent phosphoesterase TrpH, contains PHP domain
COG0614	P	ABC-type Fe3+-hydroxamate transport system, periplasmic component
COG0615	M	Glycerol-3-phosphate cytidylyltransferase, cytidylyltransferase family
COG0616	O	Periplasmic serine protease, ClpP class
COG0617	J	tRNA nucleotidyltransferase/poly(A) polymerase
COG0618	F	nanoRNase/pAp phosphatase, hydrolyzes c-di-AMP and oligoRNAs
COG0619	H	Energy-coupling factor transporter transmembrane protein EcfT
COG0620	E	Methionine synthase II (cobalamin-independent)
COG0621	J	tRNA A37 methylthiotransferase MiaB
COG0622	R	Predicted phosphodiesterase
COG0623	I	Enoyl-[acyl-carrier-protein] reductase (NADH)
COG0624	E	Acetylornithine deacetylase/Succinyl-diaminopimelate desuccinylase or related deacylase
COG0625	O	Glutathione S-transferase
COG0626	E	Cystathionine beta-lyase/cystathionine gamma-synthase
COG0627	V	S-formylglutathione hydrolase FrmB
COG0628	R	Predicted PurR-regulated permease PerM
COG0629	L	Single-stranded DNA-binding protein
COG0630	U	Type IV secretory pathway ATPase VirB11/Archaellum biosynthesis ATPase
COG0631	T	Serine/threonine protein phosphatase PrpC
COG0632	L	Holliday junction resolvasome RuvABC DNA-binding subunit
COG0633	C	Ferredoxin
COG0634	F	Hypoxanthine-guanine phosphoribosyltransferase
COG0635	H	Coproporphyrinogen III oxidase or related Fe-S oxidoreductase
COG0636	C	FoF1-type ATP synthase, membrane subunit c/Archaeal/vacuolar-type H+-ATPase, subunit K
COG0637	GR	Beta-phosphoglucomutase or related phosphatase, HAD superfamily
COG0638	O	20S proteasome, alpha and beta subunits
COG0639	T	Diadenosine tetraphosphatase ApaH/serine/threonine protein phosphatase, PP2A family
COG0640	K	DNA-binding transcriptional regulator, ArsR family
COG0641	O	Sulfatase maturation enzyme AslB, radical SAM superfamily
COG0642	T	Signal transduction histidine kinase
COG0643	NT	Chemotaxis protein histidine kinase CheA
COG0644	C	Dehydrogenase (flavoprotein)
COG0645	R	Predicted kinase
COG0646	E	Methionine synthase I (cobalamin-dependent), methyltransferase domain
COG0647	F	Ribonucleotide monophosphatase NagD, HAD superfamily
COG0648	L	Endonuclease IV
COG0649	C	NADH:ubiquinone oxidoreductase 49 kD subunit (chain D)
COG0650	C	Formate hydrogenlyase subunit 4
COG0651	CP	Formate hydrogenlyase subunit 3/Multisubunit Na+/H+ antiporter, MnhD subunit
COG0652	O	Peptidyl-prolyl cis-trans isomerase (rotamase) - cyclophilin family
COG0653	U	Preprotein translocase subunit SecA (ATPase, RNA helicase)
COG0654	HC	2-polyprenyl-6-methoxyphenol hydroxylase and related FAD-dependent oxidoreductases
COG0655	C	Multimeric flavodoxin WrbA
COG0656	Q	Aldo/keto reductase, related to diketogulonate reductase
COG0657	I	Acetyl esterase/lipase
COG0658	R	Predicted membrane metal-binding protein
COG0659	P	Sulfate permease or related transporter, MFS superfamily
COG0661	HT	Predicted unusual protein kinase regulating ubiquinone biosynthesis, AarF/ABC1/UbiB family
COG0662	G	Mannose-6-phosphate isomerase, cupin superfamily
COG0663	R	Carbonic anhydrase or acetyltransferase, isoleucine patch superfamily
COG0664	T	cAMP-binding domain of CRP or a regulatory subunit of cAMP-dependent protein kinases
COG0665	E	Glycine/D-amino acid oxidase (deaminating)
COG0666	T	Ankyrin repeat
COG0667	R	Predicted oxidoreductase (related to aryl-alcohol dehydrogenase)
COG0668	M	Small-conductance mechanosensitive channel
COG0669	H	Phosphopantetheine adenylyltransferase
COG0670	R	Integral membrane protein, interacts with FtsH
COG0671	I	Membrane-associated phospholipid phosphatase
COG0672	P	High-affinity Fe2+/Pb2+ permease
COG0673	R	Predicted dehydrogenase
COG0674	C	Pyruvate:ferredoxin oxidoreductase or related 2-oxoacid:ferredoxin oxidoreductase, alpha subunit
COG0675	X	Transposase
COG0676	G	D-hexose-6-phosphate mutarotase
COG0677	M	UDP-N-acetyl-D-mannosaminuronate dehydrogenase
COG0678	O	Peroxiredoxin
COG0679	R	Predicted permease
COG0680	C	Ni,Fe-hydrogenase maturation factor
COG0681	U	Signal peptidase I
COG0682	M	Prolipoprotein diacylglyceryltransferase
COG0683	E	ABC-type branched-chain amino acid transport system, periplasmic component
COG0684	J	Regulator of RNase E activity RraA
COG0685	E	5,10-methylenetetrahydrofolate reductase
COG0686	E	Alanine dehydrogenase
COG0687	E	Spermidine/putrescine-binding periplasmic protein
COG0688	I	Phosphatidylserine decarboxylase
COG0689	J	Ribonuclease PH
COG0690	U	Preprotein translocase subunit SecE
COG0691	O	tmRNA-binding protein
COG0692	L	Uracil DNA glycosylase
COG0693	R	Putative intracellular protease/amidase
COG0694	O	Fe-S cluster biogenesis protein NfuA, 4Fe-4S-binding domain
COG0695	O	Glutaredoxin
COG0696	G	Phosphoglycerate mutase (BPG-independent, AlkP superfamily)
COG0697	GER	Permease of the drug/metabolite transporter (DMT) superfamily
COG0698	G	Ribose 5-phosphate isomerase RpiB
COG0699	L	Replication fork clamp-binding protein CrfC (dynamin-like GTPase family)
COG0700	S	Spore maturation protein SpmB (function unknown)
COG0701	S	Uncharacterized membrane protein YraQ, UPF0718 family
COG0702	R	Uncharacterized conserved protein YbjT, contains NAD(P)-binding and DUF2867 domains
COG0703	E	Shikimate kinase
COG0704	P	Phosphate uptake regulator
COG0705	O	Membrane associated serine protease, rhomboid family
COG0706	M	Membrane protein insertase Oxa1/YidC/SpoIIIJ, required for the localization of integral membrane proteins
COG0707	M	UDP-N-acetylglucosamine:LPS N-acetylglucosamine transferase
COG0708	L	Exonuclease III
COG0709	E	Selenophosphate synthase
COG0710	E	3-dehydroquinate dehydratase
COG0711	C	FoF1-type ATP synthase, membrane subunit b or b'
COG0712	C	FoF1-type ATP synthase, delta subunit
COG0713	C	NADH:ubiquinone oxidoreductase subunit 11 or 4L (chain K)
COG0714	R	MoxR-like ATPase
COG0715	P	ABC-type nitrate/sulfonate/bicarbonate transport system, periplasmic component
COG0716	C	Flavodoxin
COG0717	F	Deoxycytidine triphosphate deaminase
COG0718	R	Conserved DNA-binding protein YbaB (function unknown)
COG0719	O	Fe-S cluster assembly scaffold protein SufB
COG0720	H	6-pyruvoyl-tetrahydropterin synthase
COG0721	J	Asp-tRNAAsn/Glu-tRNAGln amidotransferase C subunit
COG0722	E	3-deoxy-D-arabino-heptulosonate 7-phosphate (DAHP) synthase
COG0723	C	Rieske Fe-S protein
COG0724	J	 RNA recognition motif (RRM) domain
COG0725	P	ABC-type molybdate transport system, periplasmic component
COG0726	GM	Peptidoglycan/xylan/chitin deacetylase, PgdA/CDA1 family
COG0727	R	Fe-S-cluster containining protein
COG0728	M	Peptidoglycan biosynthesis protein MviN/MurJ, putative lipid II flippase
COG0729	M	Outer membrane translocation and assembly module TamA
COG0730	S	Uncharacterized membrane protein YfcA
COG0731	J	Wyosine [tRNA(Phe)-imidazoG37] synthetase, radical SAM superfamily
COG0732	V	Restriction endonuclease S subunit
COG0733	R	Na+-dependent transporter, SNF family
COG0735	P	Fe2+ or Zn2+ uptake regulation protein
COG0736	I	Phosphopantetheinyl transferase (holo-ACP synthase)
COG0737	FV	2',3'-cyclic-nucleotide 2'-phosphodiesterase/5'- or 3'-nucleotidase, 5'-nucleotidase family
COG0738	G	Fucose permease
COG0739	M	Murein DD-endopeptidase MepM and murein hydrolase activator NlpD, contain LysM domain
COG0740	O	ATP-dependent protease ClpP, protease subunit
COG0741	M	Soluble lytic murein transglycosylase and related regulatory proteins (some contain LysM/invasin domains)
COG0742	J	16S rRNA G966 N2-methylase RsmD
COG0743	I	1-deoxy-D-xylulose 5-phosphate reductoisomerase
COG0744	M	Membrane carboxypeptidase (penicillin-binding protein)
COG0745	TK	DNA-binding response regulator, OmpR family, contains REC and winged-helix (wHTH) domain
COG0746	H	Molybdopterin-guanine dinucleotide biosynthesis protein A
COG0747	E	ABC-type transport system, periplasmic component
COG0748	P	Putative heme iron utilization protein
COG0749	L	DNA polymerase I - 3'-5' exonuclease and polymerase domains
COG0750	OK	Membrane-associated protease RseP, regulator of RpoE activity
COG0751	J	Glycyl-tRNA synthetase, beta subunit
COG0752	J	Glycyl-tRNA synthetase, alpha subunit
COG0753	P	Catalase
COG0754	E	Glutathionylspermidine synthase
COG0755	O	ABC-type transport system involved in cytochrome c biogenesis, permease component
COG0756	FV	dUTPase
COG0757	E	3-dehydroquinate dehydratase
COG0758	L	Predicted Rossmann fold nucleotide-binding protein DprA/Smf involved in DNA uptake
COG0759	M	Membrane-anchored protein YidD, putatitve component of membrane protein insertase Oxa1/YidC/SpoIIIJ
COG0760	O	Parvulin-like peptidyl-prolyl isomerase
COG0761	I	4-Hydroxy-3-methylbut-2-enyl diphosphate reductase IspH
COG0762	S	Uncharacterized conserved protein YggT, Ycf19 family
COG0763	M	Lipid A disaccharide synthetase
COG0764	I	3-hydroxymyristoyl/3-hydroxydecanoyl-(acyl carrier protein) dehydratase
COG0765	E	ABC-type amino acid transport system, permease component
COG0766	M	UDP-N-acetylglucosamine enolpyruvyl transferase
COG0767	M	ABC-type transporter Mla maintaining outer membrane lipid asymmetry, permease component MlaE
COG0768	DM	Cell division protein FtsI/penicillin-binding protein 2
COG0769	M	UDP-N-acetylmuramyl tripeptide synthase
COG0770	M	UDP-N-acetylmuramyl pentapeptide synthase
COG0771	M	UDP-N-acetylmuramoylalanine-D-glutamate ligase
COG0772	D	Bacterial cell division protein FtsW, lipid II flippase
COG0773	M	UDP-N-acetylmuramate-alanine ligase
COG0774	M	UDP-3-O-acyl-N-acetylglucosamine deacetylase
COG0775	F	Nucleoside phosphorylase
COG0776	L	Bacterial nucleoid DNA-binding protein
COG0777	I	Acetyl-CoA carboxylase beta subunit
COG0778	C	Nitroreductase
COG0779	J	Ribosome maturation factor RimP
COG0780	J	NADPH-dependent 7-cyano-7-deazaguanine reductase QueF, C-terminal domain, T-fold superfamily
COG0781	K	Transcription termination factor NusB
COG0782	K	Transcription elongation factor, GreA/GreB family
COG0783	PV	DNA-binding ferritin-like protein (oxidative damage protectant)
COG0784	T	CheY chemotaxis protein or a CheY-like REC (receiver) domain
COG0785	CO	Cytochrome c biogenesis protein CcdA
COG0786	E	Na+/glutamate symporter
COG0787	M	Alanine racemase
COG0788	F	Formyltetrahydrofolate hydrolase
COG0789	K	DNA-binding transcriptional regulator, MerR family
COG0790	T	TPR repeat
COG0791	M	Cell wall-associated hydrolase, NlpC family
COG0792	L	Predicted endonuclease distantly related to archaeal Holliday junction resolvase
COG0793	O	C-terminal processing protease CtpA/Prc, contains a PDZ domain
COG0794	GM	D-arabinose 5-phosphate isomerase GutQ
COG0795	MN	Lipopolysaccharide export LptBFGC system, permease protein LptF
COG0796	M	Glutamate racemase
COG0797	M	Rare lipoprotein A, peptidoglycan hydrolase digesting "naked" glycans, contains C-terminal SPOR domain
COG0798	P	Arsenite efflux pump ArsB, ACR3 family
COG0799	J	Ribosomal silencing factor RsfS, regulates association of 30S and 50S subunits
COG0800	G	2-keto-3-deoxy-6-phosphogluconate aldolase
COG0801	H	7,8-dihydro-6-hydroxymethylpterin-pyrophosphokinase
COG0802	J	tRNA A37 threonylcarbamoyladenosine biosynthesis protein TsaE
COG0803	P	ABC-type Zn uptake system ZnuABC, Zn-binding component ZnuA
COG0804	E	Urease alpha subunit
COG0805	U	Sec-independent protein secretion pathway component TatC
COG0806	J	Ribosomal 30S subunit maturation factor RimM, required for 16S rRNA processing
COG0807	H	GTP cyclohydrolase II
COG0809	J	S-adenosylmethionine:tRNA-ribosyltransferase-isomerase (queuine synthetase)
COG0810	M	Periplasmic protein TonB, links inner and outer membranes
COG0811	U	Biopolymer transport protein ExbB/TolQ
COG0812	M	UDP-N-acetylenolpyruvoylglucosamine reductase
COG0813	F	Purine-nucleoside phosphorylase
COG0814	E	Amino acid permease
COG0815	M	Apolipoprotein N-acyltransferase
COG0816	K	RNase H-fold protein, predicted Holliday junction resolvase in Firmicutes and mycoplasms, involved in anti-termination at Rho-dependent terminators
COG0817	L	Holliday junction resolvasome RuvABC endonuclease subunit
COG0818	I	Diacylglycerol kinase
COG0819	H	Thiaminase
COG0820	J	Adenine C2-methylase RlmN of 23S rRNA A2503 and tRNA A37
COG0821	I	4-hydroxy-3-methylbut-2-en-1-yl diphosphate synthase IspG/GcpE
COG0822	O	NifU homolog involved in Fe-S cluster formation
COG0823	U	Periplasmic component of the Tol biopolymer transport system
COG0824	I	Acyl-CoA thioesterase FadM
COG0825	I	Acetyl-CoA carboxylase alpha subunit
COG0826	O	Collagenase-like protease, PrtC family
COG0827	L	Adenine-specific DNA methylase
COG0828	J	Ribosomal protein S21
COG0829	O	Urease accessory protein UreH
COG0830	O	Urease accessory protein UreF
COG0831	E	Urease gamma subunit
COG0832	E	Urease beta subunit
COG0833	E	Amino acid permease
COG0834	ET	ABC-type amino acid transport/signal transduction system, periplasmic component/domain
COG0835	NT	Chemotaxis signal transduction protein
COG0836	M	Mannose-1-phosphate guanylyltransferase
COG0837	G	Glucokinase
COG0838	C	NADH:ubiquinone oxidoreductase subunit 3 (chain A)
COG0839	C	NADH:ubiquinone oxidoreductase subunit 6 (chain J)
COG0840	NT	Methyl-accepting chemotaxis protein
COG0841	V	Multidrug efflux pump subunit AcrB
COG0842	V	ABC-type multidrug transport system, permease component
COG0843	C	Heme/copper-type cytochrome/quinol oxidase, subunit 1
COG0845	MV	Multidrug efflux pump subunit AcrA (membrane-fusion protein)
COG0846	O	NAD-dependent protein deacetylase, SIR2 family
COG0847	L	DNA polymerase III, epsilon subunit or related 3'-5' exonuclease
COG0848	U	Biopolymer transport protein ExbD
COG0849	D	Cell division ATPase FtsA
COG0850	D	Septum formation inhibitor MinC
COG0851	D	Septum formation topological specificity factor MinE
COG0852	C	NADH:ubiquinone oxidoreductase 27 kD subunit (chain C)
COG0853	H	Aspartate 1-decarboxylase
COG0854	H	Pyridoxine 5'-phosphate synthase PdxJ
COG0855	P	Polyphosphate kinase
COG0856	F	Orotate phosphoribosyltransferase homolog
COG0857	R	BioD-like N-terminal domain of phosphotransacetylase
COG0858	J	Ribosome-binding factor A
COG0859	M	ADP-heptose:LPS heptosyltransferase
COG0860	M	N-acetylmuramoyl-L-alanine amidase
COG0861	P	Membrane protein TerC, possibly involved in tellurium resistance
COG0863	L	DNA modification methylase
COG0864	K	Metal-responsive transcriptional regulator, contains CopG/Arc/MetJ DNA-binding domain
COG1001	F	Adenine deaminase
COG1002	V	Type II restriction/modification system, DNA methylase subunit YeeA
COG1003	E	Glycine cleavage system protein P (pyridoxal-binding), C-terminal domain
COG1004	M	UDP-glucose 6-dehydrogenase
COG1005	C	NADH:ubiquinone oxidoreductase subunit 1 (chain H)
COG1006	P	Multisubunit Na+/H+ antiporter, MnhC subunit
COG1007	C	NADH:ubiquinone oxidoreductase subunit 2 (chain N)
COG1008	C	NADH:ubiquinone oxidoreductase subunit 4 (chain M)
COG1009	CP	NADH:ubiquinone oxidoreductase subunit 5 (chain L)/Multisubunit Na+/H+ antiporter, MnhA subunit
COG1010	H	Precorrin-3B methylase
COG1011	H	FMN phosphatase YigB, HAD superfamily
COG1012	C	Acyl-CoA reductase or other NAD-dependent aldehyde dehydrogenase
COG1013	C	Pyruvate:ferredoxin oxidoreductase or related 2-oxoacid:ferredoxin oxidoreductase, beta subunit
COG1014	C	Pyruvate:ferredoxin oxidoreductase or related 2-oxoacid:ferredoxin oxidoreductase, gamma subunit
COG1015	G	Phosphopentomutase
COG1017	C	Hemoglobin-like flavoprotein
COG1018	C	Ferredoxin-NADP reductase
COG1019	H	Phosphopantetheine adenylyltransferase
COG1020	Q	Non-ribosomal peptide synthetase component F
COG1021	Q	Non-ribosomal peptide synthetase component E (peptide arylation enzyme)
COG1022	I	Long-chain acyl-CoA synthetase (AMP-forming)
COG1023	G	6-phosphogluconate dehydrogenase (decarboxylating)
COG1024	I	Enoyl-CoA hydratase/carnithine racemase
COG1025	O	Secreted/periplasmic Zn-dependent peptidases, insulinase-like
COG1026	O	Zn-dependent peptidase, M16 (insulinase) family
COG1027	E	Aspartate ammonia-lyase
COG1028	IQR	NAD(P)-dependent dehydrogenase, short-chain alcohol dehydrogenase family
COG1029	C	Formylmethanofuran dehydrogenase subunit B
COG1030	O	Membrane-bound serine protease (ClpP class)
COG1031	R	Radical SAM superfamily enzyme with C-terminal helix-hairpin-helix motif
COG1032	R	Radical SAM superfamily enzyme YgiQ, UPF0313 family
COG1033	R	Predicted exporter protein, RND superfamily
COG1034	C	NADH dehydrogenase/NADH:ubiquinone oxidoreductase 75 kD subunit (chain G)
COG1035	C	Coenzyme F420-reducing hydrogenase, beta subunit
COG1036	C	Archaeal flavoprotein
COG1038	C	Pyruvate carboxylase
COG1039	L	Ribonuclease HIII
COG1040	R	Predicted amidophosphoribosyltransferases
COG1041	J	tRNA G10  N-methylase Trm11
COG1042	C	Acyl-CoA synthetase (NDP forming)
COG1043	M	Acyl-[acyl carrier protein]--UDP-N-acetylglucosamine O-acyltransferase
COG1044	M	UDP-3-O-[3-hydroxymyristoyl] glucosamine N-acyltransferase
COG1045	E	Serine acetyltransferase
COG1047	O	FKBP-type peptidyl-prolyl cis-trans isomerase 2
COG1048	C	Aconitase A
COG1049	C	Aconitase B
COG1051	F	ADP-ribose pyrophosphatase YjhB, NUDIX family
COG1052	CHR	Lactate dehydrogenase or related 2-hydroxyacid dehydrogenase
COG1053	C	Succinate dehydrogenase/fumarate reductase, flavoprotein subunit
COG1054	R	Predicted sulfurtransferase
COG1055	P	Na+/H+ antiporter NhaD or related arsenite permease
COG1056	H	Nicotinamide mononucleotide adenylyltransferase
COG1057	H	Nicotinic acid mononucleotide adenylyltransferase
COG1058	R	Predicted nucleotide-utilizing enzyme related to molybdopterin-biosynthesis enzyme MoeA
COG1059	LV	Thermostable 8-oxoguanine DNA glycosylase
COG1060	H	2-iminoacetate synthase ThiH (tyrosine cleavage enzyme, thamine biosynthesis)
COG1061	KL	Superfamily II DNA or RNA helicase
COG1062	R	Zn-dependent alcohol dehydrogenase
COG1063	ER	Threonine dehydrogenase or related Zn-dependent dehydrogenase
COG1064	G	D-arabinose 1-dehydrogenase, Zn-dependent alcohol dehydrogenase family
COG1066	O	Predicted ATP-dependent serine protease
COG1067	O	Predicted ATP-dependent protease
COG1069	G	Ribulose kinase
COG1070	G	Sugar (pentulose or hexulose) kinase
COG1071	C	TPP-dependent pyruvate or acetoin dehydrogenase subunit alpha
COG1072	H	Panthothenate kinase
COG1073	T	Fermentation-respiration switch protein FrsA, has esterase activity, DUF1100 family
COG1074	L	ATP-dependent exoDNAse (exonuclease V) beta subunit (contains helicase and exonuclease domains)
COG1075	I	Triacylglycerol esterase/lipase EstA, alpha/beta hydrolase fold
COG1076	O	DnaJ-domain-containing proteins 1
COG1077	D	Actin-like ATPase involved in cell morphogenesis
COG1078	R	HD superfamily phosphohydrolase
COG1079	R	ABC-type uncharacterized transport system, permease component
COG1080	G	Phosphoenolpyruvate-protein kinase (PTS system EI component in bacteria)
COG1082	G	Sugar phosphate isomerase/epimerase
COG1083	M	CMP-N-acetylneuraminic acid synthetase
COG1084	R	GTP-binding protein, GTP1/Obg family
COG1085	G	Galactose-1-phosphate uridylyltransferase
COG1086	MO	NDP-sugar epimerase, includes UDP-GlcNAc-inverting 4,6-dehydratase FlaA1 and capsular polysaccharide biosynthesis protein EpsC
COG1087	M	UDP-glucose 4-epimerase
COG1088	M	dTDP-D-glucose 4,6-dehydratase
COG1089	M	GDP-D-mannose dehydratase
COG1090	R	NAD dependent epimerase/dehydratase family enzyme
COG1091	M	dTDP-4-dehydrorhamnose reductase
COG1092	J	23S rRNA G2069 N7-methylase RlmK or C1962 C5-methylase RlmI
COG1093	J	Translation initiation factor 2, alpha subunit (eIF-2alpha)
COG1094	J	rRNA processing protein Krr1/Pno1, contains KH domain
COG1095	K	DNA-directed RNA polymerase, subunit E'/Rpb7
COG1096	J	Exosome complex RNA-binding protein Csl4, contains S1 and Zn-ribbon domains
COG1097	J	Exosome complex RNA-binding protein Rrp4, contains S1 and KH domains
COG1098	R	Predicted RNA-binding protein, contains ribosomal protein S1 (RPS1) domain
COG1099	R	Predicted metal-dependent hydrolase, TIM-barrel fold
COG1100	R	GTPase SAR1 family domain
COG1101	R	ABC-type uncharacterized transport system, ATPase component
COG1102	F	Cytidylate kinase
COG1103	J	Archaeal Cys-tRNA synthase (O-phospho-L-seryl-tRNA:Cys-tRNA synthase)
COG1104	E	Cysteine sulfinate desulfinase/cysteine desulfurase or related enzyme
COG1105	G	Fructose-1-phosphate kinase or kinase (PfkB)
COG1106	R	ATPase/GTPase, AAA15 family
COG1107	L	Archaea-specific RecJ-like exonuclease, contains DnaJ-type Zn finger domain
COG1108	P	ABC-type Mn2+/Zn2+ transport system, permease component
COG1109	G	Phosphomannomutase
COG1110	L	Reverse gyrase
COG1111	L	ERCC4-related helicase
COG1112	L	Superfamily I DNA and/or RNA helicase
COG1113	E	L-asparagine transporter and related permeases
COG1114	E	Branched-chain amino acid permeases
COG1115	E	Na+/alanine symporter
COG1116	P	ABC-type nitrate/sulfonate/bicarbonate transport system, ATPase component
COG1117	P	ABC-type phosphate transport system, ATPase component
COG1118	P	ABC-type sulfate/molybdate transport systems, ATPase component
COG1119	P	ABC-type molybdenum transport system, ATPase component/photorepair protein PhrA
COG1120	PH	ABC-type cobalamin/Fe3+-siderophores transport system, ATPase component
COG1121	P	ABC-type Mn2+/Zn2+ transport system, ATPase component
COG1122	PR	Energy-coupling factor transporter ATP-binding protein EcfA2
COG1123	O	ABC-type glutathione transport system ATPase component, contains duplicated ATPase domain
COG1124	EP	ABC-type dipeptide/oligopeptide/nickel transport system, ATPase component
COG1125	E	ABC-type proline/glycine betaine transport system, ATPase component
COG1126	E	ABC-type polar amino acid transport system, ATPase component
COG1127	M	ABC-type transporter Mla maintaining outer membrane lipid asymmetry, ATPase component MlaF
COG1129	G	ABC-type sugar transport system, ATPase component
COG1131	V	ABC-type multidrug transport system, ATPase component
COG1132	V	ABC-type multidrug transport system, ATPase and permease component
COG1133	I	ABC-type long-chain fatty acid transport system, fused permease and ATPase components
COG1134	GM	ABC-type polysaccharide/polyol phosphate transport system, ATPase component
COG1135	E	ABC-type methionine transport system, ATPase component
COG1136	M	ABC-type lipoprotein export system, ATPase component
COG1137	M	ABC-type lipopolysaccharide export system, ATPase component
COG1138	CO	Cytochrome c biogenesis factor
COG1139	C	L-lactate utilization protein LutB, contains a ferredoxin-type domain
COG1140	CP	Nitrate reductase beta subunit
COG1141	C	Ferredoxin
COG1142	C	Fe-S-cluster-containing hydrogenase component 2
COG1143	C	Formate hydrogenlyase subunit 6/NADH:ubiquinone oxidoreductase 23 kD subunit (chain I)
COG1144	C	Pyruvate:ferredoxin oxidoreductase or related 2-oxoacid:ferredoxin oxidoreductase, delta subunit
COG1145	C	Ferredoxin
COG1146	F	NAD-dependent dihydropyrimidine dehydrogenase, PreA subunit
COG1148	C	Heterodisulfide reductase, subunit A (polyferredoxin)
COG1149	R	MinD superfamily P-loop ATPase, contains an inserted ferredoxin domain
COG1150	C	Heterodisulfide reductase, subunit C
COG1151	PC	Hydroxylamine reductase (hybrid-cluster protein)
COG1152	C	CO dehydrogenase/acetyl-CoA synthase alpha subunit
COG1153	C	Formylmethanofuran dehydrogenase subunit D
COG1154	HI	Deoxyxylulose-5-phosphate synthase
COG1155	C	Archaeal/vacuolar-type H+-ATPase catalytic subunit A/Vma1
COG1156	C	Archaeal/vacuolar-type H+-ATPase subunit B/Vma2
COG1157	NU	Flagellar biosynthesis/type III secretory pathway ATPase
COG1158	K	Transcription termination factor Rho
COG1159	J	GTPase Era, involved in 16S rRNA processing
COG1160	R	Predicted GTPases
COG1161	J	Ribosome biogenesis GTPase A
COG1162	J	Putative ribosome biogenesis GTPase RsgA
COG1163	J	Ribosome-interacting GTPase 1
COG1164	E	Oligoendopeptidase F
COG1165	H	2-succinyl-5-enolpyruvyl-6-hydroxy-3-cyclohexene-1-carboxylate synthase
COG1166	E	Arginine decarboxylase (spermidine biosynthesis)
COG1167	KE	DNA-binding transcriptional regulator, MocR family, contains an aminotransferase domain
COG1168	ER	Bifunctional PLP-dependent enzyme with beta-cystathionase and maltose regulon repressor activities
COG1169	HQ	Isochorismate synthase EntC
COG1171	E	Threonine dehydratase
COG1172	G	Ribose/xylose/arabinose/galactoside ABC-type transport system, permease component
COG1173	EP	ABC-type dipeptide/oligopeptide/nickel transport system, permease component
COG1174	E	ABC-type proline/glycine betaine transport system, permease component
COG1175	G	ABC-type sugar transport system, permease component
COG1176	E	ABC-type spermidine/putrescine transport system, permease component I
COG1177	E	ABC-type spermidine/putrescine transport system, permease component II
COG1178	P	ABC-type Fe3+ transport system, permease component
COG1179	J	tRNA A37 threonylcarbamoyladenosine dehydratase
COG1180	O	Pyruvate-formate lyase-activating enzyme
COG1181	MR	D-alanine-D-alanine ligase and related ATP-grasp enzymes
COG1182	C	FMN-dependent NADH-azoreductase
COG1183	I	Phosphatidylserine synthase
COG1184	J	Translation initiation factor 2B subunit, eIF-2B alpha/beta/delta family
COG1185	J	Polyribonucleotide nucleotidyltransferase (polynucleotide phosphorylase)
COG1186	J	Protein chain release factor B
COG1187	J	16S rRNA U516 pseudouridylate synthase RsuA and related 23S rRNA U2605, pseudouridylate synthases
COG1188	J	Ribosomal 50S subunit-recycling heat shock protein, contains S4 domain
COG1189	J	Predicted rRNA methylase YqxC, contains S4 and FtsJ domains
COG1190	J	Lysyl-tRNA synthetase (class II)
COG1191	K	DNA-directed RNA polymerase specialized sigma subunit
COG1192	N	Cellulose biosynthesis protein BcsQ
COG1193	L	dsDNA-specific endonuclease/ATPase MutS2
COG1194	L	Adenine-specific DNA glycosylase, acts on AG and A-oxoG pairs
COG1195	L	Recombinational DNA repair ATPase RecF
COG1196	D	Chromosome segregation ATPase
COG1197	LK	Transcription-repair coupling factor (superfamily II helicase)
COG1198	L	Primosomal protein N' (replication factor Y) - superfamily II helicase
COG1199	L	Rad3-related DNA helicase
COG1200	L	RecG-like helicase
COG1201	L	Lhr-like helicase
COG1202	L	Superfamily II helicase, archaea-specific
COG1203	V	CRISPR/Cas system-associated endonuclease/helicase Cas3
COG1204	L	Replicative superfamily II helicase
COG1205	L	ATP-dependent helicase YprA,  contains C-terminal metal-binding DUF1998 domain
COG1206	J	Folate-dependent tRNA-U54 methylase TrmFO/GidA
COG1207	M	Bifunctional protein GlmU, N-acetylglucosamine-1-phosphate-uridyltransferase/glucosamine-1-phosphate-acetyltransferase
COG1208	JM	NDP-sugar pyrophosphorylase, includes eIF-2Bgamma, eIF-2Bepsilon, and LPS biosynthesis proteins
COG1209	M	dTDP-glucose pyrophosphorylase
COG1210	M	UTP-glucose-1-phosphate uridylyltransferase
COG1211	I	2-C-methyl-D-erythritol 4-phosphate cytidylyltransferase
COG1212	M	CMP-2-keto-3-deoxyoctulosonic acid synthetase
COG1213	I	Choline kinase
COG1214	J	tRNA A37 threonylcarbamoyladenosine modification protein TsaB
COG1215	N	Glycosyltransferase, catalytic subunit of cellulose synthase and poly-beta-1,6-N-acetylglucosamine synthase
COG1216	G	Glycosyltransferase, GT2 family
COG1217	T	Predicted membrane GTPase involved in stress response
COG1218	P	3'-Phosphoadenosine 5'-phosphosulfate (PAPS) 3'-phosphatase
COG1219	O	ATP-dependent protease Clp, ATPase subunit
COG1220	O	ATP-dependent protease HslVU (ClpYQ), ATPase subunit
COG1221	KT	Transcriptional regulators containing an AAA-type ATPase domain and a DNA-binding domain
COG1222	O	ATP-dependent 26S proteasome regulatory subunit
COG1223	R	Predicted ATPase, AAA+ superfamily
COG1224	K	DNA helicase TIP49, TBP-interacting protein
COG1225	O	Peroxiredoxin
COG1226	P	Voltage-gated potassium channel Kch
COG1227	CP	Inorganic pyrophosphatase/exopolyphosphatase
COG1228	Q	Imidazolonepropionase or related amidohydrolase
COG1229	C	Formylmethanofuran dehydrogenase subunit A
COG1230	P	Co/Zn/Cd efflux system component
COG1231	E	Monoamine oxidase
COG1232	H	Protoporphyrinogen oxidase
COG1233	Q	Phytoene dehydrogenase-related protein
COG1234	J	Ribonuclease BN, tRNA processing enzyme
COG1235	P	Phosphoribosyl 1,2-cyclic phosphodiesterase
COG1236	J	RNA processing exonuclease, beta-lactamase fold, Cft2 family
COG1237	R	Metal-dependent hydrolase, beta-lactamase superfamily II
COG1238	S	Uncharacterized membrane protein YqaA, SNARE-associated domain
COG1239	H	Mg-chelatase subunit ChlI
COG1240	H	Mg-chelatase subunit ChlD
COG1241	L	DNA replicative helicase MCM subunit Mcm2, Cdc46/Mcm family
COG1242	R	Radical SAM superfamily enzyme
COG1243	KB	Histone acetyltransferase, component of the RNA polymerase elongator complex
COG1244	R	Uncharacterized Fe-S cluster-containing protein. MiaB family
COG1245	J	Translation initiation factor RLI1, contains Fe-S and AAA+ ATPase domains
COG1246	E	N-acetylglutamate synthase or related acetyltransferase, GNAT family
COG1247	E	L-amino acid N-acyltransferase YncA
COG1249	C	Pyruvate/2-oxoglutarate dehydrogenase complex, dihydrolipoamide dehydrogenase (E3) component or related enzyme
COG1250	I	3-hydroxyacyl-CoA dehydrogenase
COG1251	C	NAD(P)H-nitrite reductase, large subunit
COG1252	C	NADH dehydrogenase, FAD-containing subunit
COG1253	R	Hemolysin or related protein, contains CBS domains
COG1254	C	Acylphosphatase
COG1255	S	Uncharacterized protein, UPF0146 family
COG1256	N	Flagellar hook-associated protein FlgK
COG1257	I	Hydroxymethylglutaryl-CoA reductase
COG1258	J	tRNA U54 and U55 pseudouridine synthase Pus10
COG1259	R	Bifunctional DNase/RNase
COG1260	I	Myo-inositol-1-phosphate synthase
COG1261	N	Flagella basal body P-ring formation protein FlgA
COG1262	O	Formylglycine-generating enzyme, required for sulfatase activity, contains SUMF1/FGE domain
COG1263	G	Phosphotransferase system IIC components, glucose/maltose/N-acetylglucosamine-specific
COG1264	G	Phosphotransferase system IIB components
COG1266	O	Membrane protease YdiL, CAAX protease family
COG1267	I	Phosphatidylglycerophosphatase A
COG1268	H	Biotin transporter BioY
COG1269	C	Archaeal/vacuolar-type H+-ATPase subunit I/STV1
COG1270	H	Cobalamin biosynthesis protein CobD/CbiB
COG1271	C	Cytochrome bd-type quinol oxidase, subunit 1
COG1272	U	Predicted membrane channel-forming protein YqfA, hemolysin III family
COG1273	L	Non-homologous end joining protein Ku, dsDNA break repair
COG1274	C	Phosphoenolpyruvate carboxykinase, GTP-dependent
COG1275	V	Tellurite resistance protein TehA and related permeases
COG1276	P	Putative copper export protein
COG1277	O	ABC-type transport system involved in multi-copper enzyme maturation, permease component
COG1278	K	Cold shock protein, CspA family
COG1279	E	Arginine exporter protein ArgO
COG1280	E	Threonine/homoserine/homoserine lactone efflux protein
COG1281	O	Redox-regulated molecular chaperone, HSP33 family
COG1282	C	NAD/NADP transhydrogenase beta subunit
COG1283	P	Na+/phosphate symporter
COG1284	S	Uncharacterized membrane-anchored protein YitT, contains DUF161 and DUF2179 domains
COG1285	S	Uncharacterized membrane protein YhiD, involved in acid resistance
COG1286	S	Uncharacterized membrane protein, required for colicin V production
COG1287	O	Asparagine N-glycosylation enzyme, membrane subunit Stt3
COG1288	R	Uncharacterized membrane protein YfcC, ion transporter superfamily
COG1289	S	Uncharacterized membrane protein YccC
COG1290	C	Cytochrome b subunit of the bc complex
COG1291	N	Flagellar motor component MotA
COG1292	M	Choline-glycine betaine transporter
COG1293	J	Predicted component of the ribosome quality control (RQC) complex, YloA/Tae2 family, contains fibronectin-binding (FbpA) and DUF814 domains
COG1294	C	Cytochrome bd-type quinol oxidase, subunit 2
COG1295	S	Uncharacterized membrane protein, BrkB/YihY/UPF0761 family (not an RNase)
COG1296	E	Predicted branched-chain amino acid permease (azaleucine resistance)
COG1297	S	Uncharacterized membrane protein, oligopeptide transporter (OPT) family
COG1298	N	Flagellar biosynthesis pathway, component FlhA
COG1299	G	Phosphotransferase system, fructose-specific IIC component
COG1300	D	Uncharacterized membrane protein SpoIIM, required for sporulation
COG1301	C	Na+/H+-dicarboxylate symporter
COG1302	S	Uncharacterized conserved protein YloU, alkaline shock protein (Asp23) family
COG1303	R	Predicted rRNA methylase, SpoU family
COG1304	CIR	FMN-dependent dehydrogenase, includes L-lactate dehydrogenase and type II isopentenyl diphosphate isomerase
COG1305	O	Transglutaminase-like enzyme, putative cysteine protease
COG1306	S	Uncharacterized protein
COG1307	I	Fatty acid-binding protein DegV (function unknown)
COG1308	K	Transcription factor homologous to NACalpha-BTF3
COG1309	K	DNA-binding transcriptional regulator, AcrR family
COG1310	O	Proteasome lid subunit RPN8/RPN11, contains Jab1/MPN domain metalloenzyme (JAMM) motif
COG1311	L	Archaeal DNA polymerase II, small subunit/DNA polymerase delta, subunit B
COG1312	G	D-mannonate dehydratase
COG1313	R	Uncharacterized Fe-S protein PflX, radical SAM superfamily
COG1314	U	Preprotein translocase subunit SecG
COG1315	S	Uncharacterized conserved protein, DUF342 family
COG1316	M	Anionic cell wall polymer biosynthesis enzyme,  LytR-Cps2A-Psr (LCP) family
COG1317	NU	Flagellar biosynthesis/type III secretory pathway protein FliH
COG1318	K	Predicted transcriptional regulator
COG1319	C	CO or xanthine dehydrogenase, FAD-binding subunit
COG1320	P	Multisubunit Na+/H+ antiporter, MnhG subunit
COG1321	K	Mn-dependent transcriptional regulator, DtxR family
COG1322	L	DNA anti-recombination protein (rearrangement mutator) RmuC
COG1323	R	Predicted nucleotidyltransferase
COG1324	P	Uncharacterized protein involved in tolerance to divalent cations
COG1325	J	Exosome subunit, RNA binding protein with dsRBD fold
COG1326	R	Uncharacterized archaeal Zn-finger protein
COG1327	K	Transcriptional regulator NrdR, contains Zn-ribbon and ATP-cone domains
COG1328	F	Anaerobic ribonucleoside-triphosphate reductase
COG1329	K	RNA polymerase-interacting regulator, CarD/CdnL/TRCF family
COG1330	L	Exonuclease V gamma subunit
COG1331	R	Uncharacterized conserved protein YyaL, SSP411 family, contains thoiredoxin and six-hairpin glycosidase-like domains
COG1332	V	CRISPR/Cas system CSM-associated protein Csm5, group 7 of RAMP superfamily
COG1333	CO	Cytochrome c biogenesis protein ResB
COG1334	R	Uncharacterized conserved protein, FlaG/YvyC family
COG1335	HR	Nicotinamidase-related amidase
COG1336	V	CRISPR/Cas system CMR subunit Cmr4, Cas7 group, RAMP superfamily
COG1337	V	CRISPR/Cas system CSM-associated protein Csm3, group 7 of RAMP superfamily
COG1338	N	Flagellar biosynthetic protein FliP
COG1339	H	Archaeal CTP-dependent riboflavin kinase
COG1340	S	Uncharacterized coiled-coil protein, contains DUF342 domain
COG1341	J	Polynucleotide 5'-kinase, involved in rRNA processing
COG1342	R	Predicted DNA-binding protein, UPF0251 family
COG1343	V	CRISPR/Cas system-associated endoribonuclease Cas2
COG1344	N	Flagellin and related hook-associated protein FlgL
COG1345	N	Flagellar capping protein FliD
COG1346	M	Putative effector of murein hydrolase
COG1347	C	Na+-transporting NADH:ubiquinone oxidoreductase, subunit NqrD
COG1348	P	Nitrogenase subunit NifH, an ATPase
COG1349	KG	DNA-binding transcriptional regulator of sugar metabolism, DeoR/GlpR family
COG1350	E	Predicted alternative tryptophan synthase beta-subunit (paralog of TrpB)
COG1351	F	Thymidylate synthase ThyX
COG1352	NT	Methylase of chemotaxis methyl-accepting proteins
COG1353	V	CRISPR/Cas system-associated protein Cas10, large subunit of type III CRISPR-Cas systems, contains HD superfamily nuclease domain
COG1354	L	Chromatin segregation and condensation protein Rec8/ScpA/Scc1, kleisin family
COG1355	R	Predicted class III extradiol dioxygenase, MEMO1 family
COG1356	K	Transcriptional regulator
COG1357	S	Uncharacterized protein YjbI, contains pentapeptide repeats
COG1358	J	Ribosomal protein L7Ae or related RNA K-turn-binding protein
COG1359	C	Quinol monooxygenase YgiN
COG1360	N	Flagellar motor protein MotB
COG1361	S	Uncharacterized conserved protein
COG1362	E	Aspartyl aminopeptidase
COG1363	EG	Putative aminopeptidase FrvX
COG1364	E	N-acetylglutamate synthase (N-acetylornithine aminotransferase)
COG1365	R	Predicted ATPase, PP-loop superfamily
COG1366	T	Anti-anti-sigma regulatory factor (antagonist of anti-sigma factor)
COG1367	V	CRISPR/Cas system CMR-associated protein Cmr1, group 7 of RAMP superfamily
COG1368	M	Phosphoglycerol transferase MdoB or a related enzyme of AlkP superfamily
COG1369	J	RNase P/RNase MRP subunit POP5
COG1370	J	tRNA-guanine transglycosylase, archaeosine-15-forming
COG1371	R	SHS2 domain protein implicated in nucleic acid metabolism
COG1372	LX	Intein/homing endonuclease
COG1373	R	Predicted ATPase, AAA+ superfamily
COG1374	J	Rbosome biogenesis protein Nip4, contains PUA domain
COG1376	M	Lipoprotein-anchoring transpeptidase ErfK/SrfK
COG1377	N	Flagellar biosynthesis protein FlhB
COG1378	K	Sugar-specific transcriptional regulator TrmB
COG1379	R	PHP family phosphoesterase with a Zn ribbon
COG1380	R	Putative effector of murein hydrolase LrgA, UPF0299 family
COG1381	L	Recombinational DNA repair protein (RecF pathway)
COG1382	O	Prefoldin, chaperonin cofactor
COG1383	J	Ribosomal protein S17E
COG1384	J	Lysyl-tRNA synthetase, class I
COG1385	J	16S rRNA U1498 N3-methylase RsmE
COG1386	K	Chromosome segregation and condensation protein ScpB
COG1387	ER	Histidinol phosphatase or related hydrolase of the PHP family
COG1388	M	LysM repeat
COG1389	L	DNA topoisomerase VI, subunit B
COG1390	C	Archaeal/vacuolar-type H+-ATPase subunit E/Vma4
COG1391	O	Glutamine synthetase adenylyltransferase
COG1392	S	Uncharacterized conserved protein YkaA, distantly related to PhoU, UPF0111/DUF47 family
COG1393	P	Arsenate reductase and related proteins, glutaredoxin family
COG1394	C	Archaeal/vacuolar-type H+-ATPase subunit D/Vma8
COG1395	K	Predicted transcriptional regulator
COG1396	K	Transcriptional regulator, contains XRE-family HTH domain
COG1397	O	ADP-ribosylglycohydrolase
COG1398	I	Fatty-acid desaturase
COG1399	S	Uncharacterized metal-binding protein YceD, DUF177 family
COG1400	U	Signal recognition particle subunit SEC65
COG1401	V	5-methylcytosine-specific restriction endonuclease McrBC, GTP-binding regulatory subunit McrB
COG1402	HQ	 Creatinine amidohydrolase/Fe(II)-dependent formamide hydrolase involved in riboflavin and F420 biosynthesis
COG1403	V	5-methylcytosine-specific restriction endonuclease McrA
COG1404	O	Serine protease, subtilisin family
COG1405	K	Transcription initiation factor TFIIIB, Brf1 subunit/Transcription initiation factor TFIIB
COG1406	N	Chemotaxis protein CheX, a CheY~P-specific phosphatase
COG1407	R	Metallophosphoesterase superfamily enzyme
COG1408	R	Predicted phosphohydrolase, MPP superfamily
COG1409	T	3',5'-cyclic AMP phosphodiesterase CpdA
COG1410	E	Methionine synthase I, cobalamin-binding domain
COG1411	R	Uncharacterized protein related to proFAR isomerase (HisA)
COG1412	J	rRNA-processing protein FCF1
COG1413	R	HEAT repeat
COG1414	K	DNA-binding transcriptional regulator, IclR family
COG1415	S	Uncharacterized protein
COG1416	P	Intracellular sulfur oxidation protein, DsrE/DsrF family
COG1417	S	Uncharacterized protein
COG1418	JR	HD superfamily phosphodieaserase, includes HD domain of RNase Y
COG1419	N	Flagellar biosynthesis GTPase FlhF
COG1420	K	Transcriptional regulator of heat shock response
COG1421	V	CRISPR/Cas system CSM-associated protein Csm2, small subunit
COG1422	S	Uncharacterized archaeal membrane protein, DUF106 family, distantly related to YidC/Oxa1
COG1423	L	ATP-dependent RNA circularization protein, DNA/RNA ligase (PAB1020)  family
COG1424	H	Pimeloyl-CoA synthetase
COG1426	D	Cytoskeletal protein RodZ, contains Xre-like HTH and DUF4115 domains
COG1427	R	Predicted periplasmic solute-binding protein
COG1428	F	Deoxyadenosine/deoxycytidine kinase
COG1429	H	Cobalamin biosynthesis protein CobN, Mg-chelatase
COG1430	S	Uncharacterized conserved membrane protein, UPF0127 family
COG1431	JV	Argonaute homolog, implicated in RNA metabolism and viral defense
COG1432	S	Uncharacterized conserved protein, LabA/DUF88 family
COG1433	O	Predicted Fe-Mo cluster-binding protein, NifX family
COG1434	R	Uncharacterized SAM-binding protein YcdF, DUF218 family
COG1435	F	Thymidine kinase
COG1436	C	Archaeal/vacuolar-type H+-ATPase subunit F/Vma7
COG1437	TR	Adenylate cyclase class IV, CYTH domain (includes archaeal enzymes of unknown function)
COG1438	K	Arginine repressor
COG1439	J	rRNA maturation endonuclease Nob1
COG1440	G	Phosphotransferase system cellobiose-specific component IIB
COG1441	H	O-succinylbenzoate synthase
COG1442	M	Lipopolysaccharide biosynthesis protein, LPS:glycosyltransferase
COG1443	I	Isopentenyldiphosphate isomerase
COG1444	J	tRNA(Met) C34 N-acetyltransferase TmcA
COG1445	G	Phosphotransferase system fructose-specific component IIB
COG1446	E	Isoaspartyl peptidase or L-asparaginase, Ntn-hydrolase superfamily
COG1447	G	Phosphotransferase system cellobiose-specific component IIA
COG1448	E	Aspartate/tyrosine/aromatic aminotransferase
COG1449	G	Alpha-amylase/alpha-mannosidase, GH57 family
COG1450	U	Type II secretory pathway component GspD/PulD (secretin)
COG1451	R	Predicted metal-dependent hydrolase
COG1452	M	LPS assembly outer membrane protein LptD (organic solvent tolerance protein OstA)
COG1453	R	Predicted oxidoreductase of the aldo/keto reductase family
COG1454	C	Alcohol dehydrogenase, class IV
COG1455	G	Phosphotransferase system cellobiose-specific component IIC
COG1456	C	CO dehydrogenase/acetyl-CoA synthase gamma subunit (corrinoid Fe-S protein)
COG1457	F	Purine-cytosine permease or related protein
COG1458	R	Predicted DNA-binding protein containing PIN domain, UPF0278 family
COG1459	NUW	Type II secretory pathway, component PulF
COG1460	K	DNA-directed RNA polymerase, subunit F
COG1461	R	Predicted kinase related to dihydroxyacetone kinase
COG1462	M	Curli biogenesis system outer membrane secretion channel CsgG
COG1463	M	ABC-type transporter Mla maintaining outer membrane lipid asymmetry, periplasmic component MlaD
COG1464	P	ABC-type metal ion transport system, periplasmic component/surface antigen
COG1465	E	3-dehydroquinate synthase, class II
COG1466	L	DNA polymerase III, delta subunit
COG1467	L	Eukaryotic-type DNA primase, catalytic (small) subunit
COG1468	V	CRISPR/Cas system-associated exonuclease Cas4, RecB family
COG1469	H	GTP cyclohydrolase FolE2
COG1470	S	Uncharacterized membrane protein
COG1471	J	Ribosomal protein S4E
COG1472	G	Periplasmic beta-glucosidase and related glycosidases
COG1473	R	Metal-dependent amidase/aminoacylase/carboxypeptidase
COG1474	L	Cdc6-related protein, AAA superfamily ATPase
COG1475	D	Chromosome segregation protein Spo0J, contains ParB-like nuclease domain
COG1476	K	DNA-binding transcriptional regulator, XRE-family HTH domain
COG1477	H	Thiamine biosynthesis lipoprotein ApbE
COG1478	H	F420-0:Gamma-glutamyl ligase (F420 biosynthesis)
COG1479	S	Uncharacterized conserved protein, contains ParB-like and HNH nuclease domains
COG1480	R	Membrane-associated HD superfamily phosphohydrolase
COG1481	K	DNA-binding transcriptional regulator WhiA, involved in cell division
COG1482	G	Mannose-6-phosphate isomerase, class I
COG1483	R	Predicted ATPase, AAA+ superfamily
COG1484	L	DNA replication protein DnaC
COG1485	R	Predicted ATPase
COG1486	G	Alpha-galactosidase/6-phospho-beta-glucosidase, family 4 of glycosyl hydrolase
COG1487	R	Predicted nucleic acid-binding protein, contains PIN domain
COG1488	H	Nicotinic acid phosphoribosyltransferase
COG1489	GT	DNA-binding protein, stimulates sugar fermentation
COG1490	J	D-Tyr-tRNAtyr deacylase
COG1491	R	Predicted nucleic acid-binding OB-fold protein
COG1492	H	Cobyric acid synthase
COG1493	T	Serine kinase of the HPr protein, regulates carbohydrate metabolism
COG1494	G	Fructose-1,6-bisphosphatase/sedoheptulose 1,7-bisphosphatase or related protein
COG1495	O	Disulfide bond formation protein DsbB
COG1496	P	Copper oxidase (laccase) domain
COG1497	K	Predicted transcriptional regulator
COG1498	J	RNA processing factor Prp31, contains Nop domain
COG1499	J	NMD protein affecting ribosome stability and mRNA decay
COG1500	J	Ribosome maturation protein Sdo1
COG1501	G	Alpha-glucosidase, glycosyl hydrolase family GH31
COG1502	I	Phosphatidylserine/phosphatidylglycerophosphate/cardiolipin synthase or related enzyme
COG1503	J	Peptide chain release factor 1 (eRF1)
COG1504	S	Uncharacterized protein
COG1505	E	Prolyl oligopeptidase PreP, S9A serine peptidase family
COG1506	E	Dipeptidyl aminopeptidase/acylaminoacyl peptidase
COG1507	S	Uncharacterized protein
COG1508	K	DNA-directed RNA polymerase specialized sigma subunit, sigma54 homolog
COG1509	E	L-lysine 2,3-aminomutase (EF-P beta-lysylation pathway)
COG1510	K	DNA-binding transcriptional regulator GbsR, MarR family
COG1511	S	Uncharacterized membrane protein YhgE, phage infection protein (PIP) family
COG1512	S	Uncharacterized membrane protein YgcG, contains a TPM-fold domain
COG1513	P	Cyanate lyase
COG1514	J	2'-5' RNA ligase
COG1515	L	Deoxyinosine 3'endonuclease (endonuclease V)
COG1516	NU	Flagellin-specific chaperone FliS
COG1517	V	CRISPR/Cas system-associated protein Csx1, contains CARF domain
COG1518	V	CRISPR/Cas system-associated endonuclease Cas1
COG1519	M	3-deoxy-D-manno-octulosonic-acid transferase
COG1520	M	Outer membrane protein assembly factor BamB, contains PQQ-like beta-propeller repeat
COG1521	H	Pantothenate kinase type III
COG1522	K	DNA-binding transcriptional regulator, Lrp family
COG1523	G	Pullulanase/glycogen debranching enzyme
COG1524	R	Predicted pyrophosphatase or phosphodiesterase, AlkP superfamily
COG1525	L	Endonuclease YncB, thermonuclease family
COG1526	C	Formate dehydrogenase assembly factor FdhD
COG1527	C	Archaeal/vacuolar-type H+-ATPase subunit C/Vma6
COG1528	P	Ferritin
COG1529	C	CO or xanthine dehydrogenase, Mo-binding subunit
COG1530	J	Ribonuclease G or E
COG1531	S	Uncharacterized protein, UPF0248 family
COG1532	R	Predicted RNA-binding protein
COG1533	L	DNA repair photolyase
COG1534	J	RNA-binding protein YhbY
COG1535	Q	Isochorismate hydrolase
COG1536	N	Flagellar motor switch protein FliG
COG1537	J	Stalled ribosome rescue protein Dom34, pelota family
COG1538	M	Outer membrane protein TolC
COG1539	H	Dihydroneopterin aldolase
COG1540	R	Lactam utilization protein B (function unknown)
COG1541	H	Phenylacetate-coenzyme A ligase PaaK, adenylate-forming domain family
COG1542	S	Uncharacterized protein
COG1543	G	Predicted glycosyl hydrolase, contains GH57 and DUF1957 domains
COG1544	J	Ribosome-associated translation inhibitor RaiA
COG1545	R	Uncharacterized OB-fold protein, contains Zn-ribbon domain
COG1546	H	Nicotinamide mononucleotide (NMN) deamidase PncC
COG1547	S	Predicted metal-dependent hydrolase
COG1548	S	Uncharacterized protein, hydantoinase/oxoprolinase family
COG1549	R	Predicted RNA-binding protein, contains uracil-DNA-glycosylase-like and PUA domains
COG1550	S	Uncharacterized conserved protein YlxP, DUF503 family
COG1551	T	sRNA-binding carbon storage regulator CsrA
COG1552	J	Ribosomal protein L40E
COG1553	P	Sulfur relay (sulfurtransferase) complex TusBCD TusD component, DsrE family
COG1554	G	Trehalose and maltose hydrolase (possible phosphorylase)
COG1555	L	DNA uptake protein ComE and related DNA-binding proteins
COG1556	C	L-lactate utilization protein LutC, contains LUD domain
COG1558	N	Flagellar basal body rod protein FlgC
COG1559	D	Cell division protein YceG, involved in septum cleavage
COG1560	I	Lauroyl/myristoyl acyltransferase
COG1561	S	Uncharacterized conserved protein YicC, UPF0701 family
COG1562	I	Phytoene/squalene synthetase
COG1563	R	Uncharacterized MnhB-related membrane protein
COG1564	H	Thiamine pyrophosphokinase
COG1565	R	SAM-dependent methyltransferase, MidA family
COG1566	V	Multidrug resistance efflux pump
COG1567	V	CRISPR/Cas system CSM-associated protein Csm4, group 5 of RAMP superfamily
COG1568	R	Predicted methyltransferase
COG1569	R	Predicted nucleic acid-binding protein, contains PIN domain
COG1570	L	Exonuclease VII, large subunit
COG1571	J	tRNA(Ile2) C34 agmatinyltransferase TiaS
COG1572	O	Serine protease, subtilase family
COG1573	L	Uracil-DNA glycosylase
COG1574	R	Predicted amidohydrolase YtcJ
COG1575	H	1,4-dihydroxy-2-naphthoate octaprenyltransferase
COG1576	J	23S rRNA pseudoU1915 N3-methylase RlmH
COG1577	I	Mevalonate kinase
COG1578	S	Uncharacterized conserved protein, contains ATP-grasp and redox domains
COG1579	R	Predicted  nucleic acid-binding protein, contains Zn-ribbon domain
COG1580	N	Flagellar basal body-associated protein FliL
COG1581	K	Archaeal DNA-binding protein
COG1582	R	Uncharacterized protein YlzI, FlbEa/FlbD family
COG1583	V	CRISPR/Cas system endoribonuclease Cas6, RAMP superfamily
COG1584	C	Succinate-acetate transporter protein
COG1585	O	Membrane protein implicated in regulation of membrane protease activity
COG1586	E	S-adenosylmethionine decarboxylase or arginine decarboxylase
COG1587	H	Uroporphyrinogen-III synthase
COG1588	J	RNase P/RNase MRP subunit p29
COG1589	D	Cell division septal protein FtsQ
COG1590	J	tRNA(Phe) wybutosine-synthesizing methylase Tyw3
COG1591	L	Holliday junction resolvase, archaeal type
COG1592	C	Rubrerythrin
COG1593	G	TRAP-type C4-dicarboxylate transport system, large permease component
COG1594	K	DNA-directed RNA polymerase, subunit M/Transcription elongation factor TFIIS
COG1595	K	DNA-directed RNA polymerase specialized sigma subunit, sigma24 family
COG1596	M	Periplasmic protein involved in polysaccharide export, contains SLBB domain of the beta-grasp fold
COG1597	IR	Diacylglycerol kinase family enzyme
COG1598	V	Predicted nuclease of the RNAse H fold, HicB family
COG1599	L	ssDNA-binding replication factor A, large subunit
COG1600	J	Epoxyqueuosine reductase  QueG (queuosine biosynthesis)
COG1601	J	Translation initiation factor 2, beta subunit (eIF-2beta)/eIF-5 N-terminal domain
COG1602	S	Uncharacterized protein
COG1603	J	RNase P/RNase MRP subunit p30
COG1604	V	CRISPR/Cas system CMR subunit Cmr6, Cas7 group, RAMP superfamily
COG1605	E	Chorismate mutase
COG1606	R	ATP-utilizing enzyme, PP-loop superfamily
COG1607	I	Acyl-CoA hydrolase
COG1608	I	Isopentenyl phosphate kinase
COG1609	K	DNA-binding transcriptional regulator, LacI/PurR family
COG1610	S	Uncharacterized conserved protein YqeY
COG1611	R	Predicted Rossmann fold nucleotide-binding protein
COG1612	H	Heme A synthase
COG1613	P	ABC-type sulfate transport system, periplasmic component
COG1614	C	CO dehydrogenase/acetyl-CoA synthase beta subunit
COG1615	S	Uncharacterized membrane protein, UPF0182 family
COG1617	J	tRNA threonylcarbamoyladenosine modification (KEOPS) complex,  Cgi121 subunit
COG1618	F	Nucleoside-triphosphatase THEP1
COG1619	M	Muramoyltetrapeptide carboxypeptidase LdcA (peptidoglycan recycling)
COG1620	C	L-lactate permease
COG1621	G	Sucrose-6-phosphate hydrolase SacC, GH32 family
COG1622	C	Heme/copper-type cytochrome/quinol oxidase, subunit 2
COG1623	T	Diadenylate cyclase (c-di-AMP synthetase), DNA integrity scanning protein DisA
COG1624	T	Diadenylate cyclase (c-di-AMP synthetase), DisA_N domain
COG1625	C	Fe-S oxidoreductase, related to NifB/MoaA family
COG1626	G	Neutral trehalase
COG1627	S	Uncharacterized protein
COG1628	R	Endonuclease V homolog, UPF0215 family
COG1629	P	Outer membrane receptor proteins, mostly Fe transport
COG1630	L	NurA 5'-3' nuclease
COG1631	J	Ribosomal protein L44E
COG1632	J	Ribosomal protein L15E
COG1633	P	Rubrerythrin
COG1634	S	Uncharacterized Rossmann fold enzyme
COG1635	H	Archaeal ribulose 1,5-bisphosphate synthetase/yeast thiazole synthase
COG1636	R	Predicted ATPase, Adenine nucleotide alpha hydrolases (AANH) superfamily
COG1637	L	Endonuclease NucS, RecB family
COG1638	G	TRAP-type C4-dicarboxylate transport system, periplasmic component
COG1639	T	HD-like signal output (HDOD) domain, no enzymatic activity
COG1640	G	4-alpha-glucanotransferase
COG1641	S	Uncharacterized conserved protein, DUF111 family
COG1643	J	HrpA-like RNA helicase
COG1644	K	DNA-directed RNA polymerase, subunit N (RpoN/RPB10)
COG1645	R	Uncharacterized Zn-finger containing protein, UPF0148 family
COG1646	I	Heptaprenylglyceryl phosphate synthase
COG1647	Q	Esterase/lipase
COG1648	H	Siroheme synthase (precorrin-2 oxidase/ferrochelatase domain)
COG1649	S	Uncharacterized lipoprotein YddW, UPF0748 family
COG1650	J	D-tyrosyl-tRNA(Tyr) deacylase
COG1651	O	Protein-disulfide isomerase
COG1652	S	Nucleoid-associated protein YgaU, contains BON and LysM domains
COG1653	G	ABC-type glycerol-3-phosphate transport system, periplasmic component
COG1654	K	Biotin operon repressor
COG1655	S	Uncharacterized protein, DUF2225 family
COG1656	S	Uncharacterized conserved protein, contains PIN domain
COG1657	I	Squalene cyclase
COG1658	J	5S rRNA maturation endonuclease (Ribonuclease M5), contains TOPRIM domain
COG1659	S	Uncharacterized protein, linocin/CFP29 family
COG1660	T	RNase adaptor protein for sRNA GlmZ degradation, contains a P-loop ATPase domain
COG1661	R	Predicted DNA-binding protein with PD1-like DNA-binding motif
COG1662	X	Transposase and inactivated derivatives, IS1 family
COG1663	M	Tetraacyldisaccharide-1-P 4'-kinase
COG1664	Z	Cytoskeletal protein CcmA, bactofilin family
COG1665	R	Predicted nucleotidyltransferase
COG1666	S	Uncharacterized conserved protein YajQ, UPF0234 family
COG1667	S	Uncharacterized protein
COG1668	CP	ABC-type Na+ efflux pump, permease component
COG1669	R	Predicted nucleotidyltransferase
COG1670	JO	Protein N-acetyltransferase, RimJ/RimL family
COG1671	S	Uncharacterized conserved protein YaiI, UPF0178 family
COG1672	R	Predicted ATPase, archaeal AAA+ ATPase superfamily
COG1673	R	Predicted RNA-binding protein, contains PUA-like EVE domain
COG1674	D	DNA segregation ATPase FtsK/SpoIIIE and related proteins
COG1675	K	Transcription initiation factor IIE, alpha subunit
COG1676	J	tRNA splicing endonuclease
COG1677	N	Flagellar hook-basal body complex protein FliE
COG1678	K	Putative transcriptional regulator, AlgH/UPF0301 family
COG1679	C	Predicted aconitase
COG1680	V	CubicO group peptidase, beta-lactamase class C family
COG1681	N	Archaellin (archaeal flagellin)
COG1682	GM	ABC-type polysaccharide/polyol phosphate export permease
COG1683	S	Uncharacterized conserved protein YbbK, DUF523 family
COG1684	N	Flagellar biosynthesis protein FliR
COG1685	E	Archaeal shikimate kinase
COG1686	M	D-alanyl-D-alanine carboxypeptidase
COG1687	E	Branched-chain amino acid transport protein AzlD
COG1688	V	CRISPR/Cas system-associated protein Cas5, RAMP superfamily
COG1689	S	Uncharacterized protein
COG1690	J	RNA-splicing ligase RtcB, repairs tRNA damage
COG1691	F	NCAIR mutase (PurE)-related protein
COG1692	R	Calcineurin-like phosphoesterase
COG1693	K	Repressor of nif and glnA expression
COG1694	V	NTP pyrophosphatase, house-cleaning of non-canonical NTPs
COG1695	K	DNA-binding transcriptional regulator, PadR family
COG1696	M	D-alanyl-lipoteichoic acid acyltransferase DltB, MBOAT superfamily
COG1697	L	DNA topoisomerase VI, subunit A
COG1698	S	Uncharacterized protein, UPF0147 family
COG1699	N	Flagellar assembly factor FliW
COG1700	V	Predicted component of virus defense system, contains PD-(D/E)xK nuclease domain, DUF524
COG1701	H	Archaeal phosphopantothenate synthetase
COG1702	T	Phosphate starvation-inducible protein PhoH, predicted ATPase
COG1703	O	Putative periplasmic protein kinase ArgK or related GTPase of G3E family
COG1704	S	Uncharacterized conserved protein
COG1705	MN	Flagellum-specific peptidoglycan hydrolase FlgJ
COG1706	N	Flagellar basal body P-ring protein FlgI
COG1707	R	Uncharacterized protein, contains ACT and thioredoxin-like domains
COG1708	R	Predicted nucleotidyltransferase
COG1709	K	Predicted transcriptional regulator
COG1710	S	Uncharacterized protein
COG1711	L	DNA replication initiation complex subunit, GINS family
COG1712	R	Predicted dinucleotide-utilizing enzyme
COG1713	R	HD superfamily phosphohydrolase YqeK (fused to NMNAT in mycoplasms)
COG1714	S	Uncharacterized membrane protein YckC, RDD family
COG1715	V	Restriction endonuclease Mrr
COG1716	T	Forkhead associated (FHA) domain, binds pSer, pThr, pTyr
COG1717	J	Ribosomal protein L32E
COG1718	T	Serine/threonine-protein kinase RIO1
COG1719	R	Predicted hydrocarbon binding protein, contains 4VR domain
COG1720	J	tRNA (Thr-GGU) A37 N-methylase
COG1721	S	Uncharacterized conserved protein, DUF58 family, contains vWF domain
COG1722	L	Exonuclease VII small subunit
COG1723	S	Uncharacterized protein, Rmd1/YagE family
COG1724	R	Predicted RNA binding protein YcfA, dsRBD-like fold, HicA-like mRNA interferase family
COG1725	K	DNA-binding transcriptional regulator YhcF, GntR family
COG1726	C	Na+-transporting NADH:ubiquinone oxidoreductase, subunit NqrA
COG1727	J	Ribosomal protein L18E
COG1728	S	Uncharacterized protein YaaR, TM1646/DUF327 family
COG1729	R	Periplasmic TolA-binding protein (function unknown)
COG1730	O	Prefoldin subunit 5
COG1731	H	Archaeal riboflavin synthase
COG1732	M	Periplasmic glycine betaine/choline-binding (lipo)protein of an ABC-type transport system (osmoprotectant binding protein)
COG1733	K	DNA-binding transcriptional regulator, HxlR family
COG1734	J	RNA polymerase-binding transcription factor DksA
COG1735	R	Predicted metal-dependent hydrolase, phosphotriesterase family
COG1736	J	Diphthamide synthase subunit DPH2
COG1737	K	DNA-binding transcriptional regulator, MurR/RpiR family, contains HTH and SIS domains
COG1738	S	Uncharacterized PurR-regulated membrane protein YhhQ, DUF165 family
COG1739	R	Putative translation regulator, IMPACT (imprinted ancient) protein family
COG1740	C	Ni,Fe-hydrogenase I small subunit
COG1741	R	Redox-sensitive bicupin YhaK, pirin superfamily
COG1742	R	Uncharacterized inner membrane protein YnfA, drug/metabolite transporter superfamily
COG1743	L	Adenine-specific DNA methylase, contains a Zn-ribbon domain
COG1744	M	Basic membrane lipoprotein Med, periplasmic binding protein (PBP1-ABC) superfamily
COG1745	S	Uncharacterized protein
COG1746	J	tRNA nucleotidyltransferase (CCA-adding enzyme)
COG1747	S	Uncharacterized N-terminal domain of the transcription elongation factor GreA
COG1748	E	Saccharopine dehydrogenase, NADP-dependent
COG1749	N	Flagellar hook protein FlgE
COG1750	R	Predicted archaeal serine protease, S18 family
COG1751	S	Uncharacterized protein
COG1752	R	Predicted acylesterase/phospholipase RssA, containd patatin domain
COG1753	V	Predicted antitoxin, CopG family
COG1754	S	Uncharacterized C-terminal domain of topoisomerase IA
COG1755	S	Uncharacterized protein YpbQ, isoprenylcysteine carboxyl methyltransferase (ICMT) family
COG1756	J	rRNA pseudouridine-1189 N-methylase Emg1, Nep1/Mra1 family
COG1757	C	Na+/H+ antiporter NhaC
COG1758	K	DNA-directed RNA polymerase, subunit K/omega
COG1759	F	5-formaminoimidazole-4-carboxamide-1-beta-D-ribofuranosyl 5'-monophosphate synthetase (purine biosynthesis)
COG1760	E	L-serine deaminase
COG1761	K	DNA-directed RNA polymerase, subunit L
COG1762	GT	Phosphotransferase system mannitol/fructose-specific IIA domain (Ntr-type)
COG1763	H	Molybdopterin-guanine dinucleotide biosynthesis protein
COG1764	V	Organic hydroperoxide reductase OsmC/OhrA
COG1765	R	Uncharacterized OsmC-related protein
COG1766	NU	Flagellar biosynthesis/type III secretory pathway M-ring protein FliF/YscJ
COG1767	H	Triphosphoribosyl-dephospho-CoA synthetase
COG1768	R	Predicted phosphohydrolase
COG1769	V	CRISPR/Cas system CMR-associated protein Cmr3, group 5 of RAMP superfamily
COG1770	E	Protease II
COG1771	S	Uncharacterized protein, contains N-terminal Zn-finger domain
COG1772	S	Uncharacterized protein
COG1773	C	Rubredoxin
COG1774	T	Cell fate regulator YaaT, PSP1 superfamily (controls sporulation, competence, biofilm development)
COG1775	Q	Benzoyl-CoA reductase/2-hydroxyglutaryl-CoA dehydratase subunit, BcrC/BadD/HgdB
COG1776	T	Chemotaxis protein CheY-P-specific phosphatase CheC
COG1777	K	Predicted transcriptional regulator
COG1778	MR	 3-deoxy-D-manno-octulosonate 8-phosphate phosphatase KdsC and related HAD superfamily phosphatases
COG1779	R	C4-type Zn-finger protein
COG1780	F	Protein involved in ribonucleotide reduction
COG1781	F	Aspartate carbamoyltransferase, regulatory subunit
COG1782	R	Predicted metal-dependent RNase, contains metallo-beta-lactamase and KH domains
COG1783	X	Phage terminase large subunit
COG1784	R	TctA family transporter
COG1785	PR	Alkaline phosphatase
COG1786	R	Swiveling domain associated with predicted aconitase
COG1787	V	Endonuclease, HJR/Mrr/RecB family
COG1788	I	Acyl CoA:acetate/3-ketoacid CoA transferase, alpha subunit
COG1790	S	Uncharacterized protein
COG1791	E	Acireductone dioxygenase (methionine salvage), cupin superfamily
COG1792	D	Cell shape-determining protein MreC
COG1793	L	ATP-dependent DNA ligase
COG1794	M	Aspartate/glutamate racemase
COG1795	C	Formaldehyde-activating enzyme nesessary for methanogenesis
COG1796	L	DNA polymerase/3'-5' exonuclease PolX
COG1797	H	Cobyrinic acid a,c-diamide synthase
COG1798	J	Diphthamide biosynthesis methyltransferase
COG1799	D	FtsZ-interacting cell division protein YlmF
COG1800	R	Predicted transglutaminase-like protease
COG1801	S	Uncharacterized conserved protein YecE, DUF72 family
COG1802	K	DNA-binding transcriptional regulator, GntR family
COG1803	G	Methylglyoxal synthase
COG1804	I	Crotonobetainyl-CoA:carnitine CoA-transferase CaiB and related acyl-CoA transferases
COG1805	C	Na+-transporting NADH:ubiquinone oxidoreductase, subunit NqrB
COG1806	T	Regulator of PEP synthase PpsR, kinase-PPPase family (combines ADP:protein kinase and phosphorylase activities)
COG1807	M	4-amino-4-deoxy-L-arabinose transferase or related glycosyltransferase of PMT family
COG1808	S	Uncharacterized membrane protein
COG1809	H	Phosphosulfolactate synthase, CoM biosynthesis protein A
COG1810	S	Uncharacterized protein
COG1811	S	Uncharacterized membrane protein YqgA, affects biofilm formation
COG1812	H	Archaeal S-adenosylmethionine synthetase
COG1813	J	Archaeal ribosome-binding protein aMBF1, putative translation factor, contains Zn-ribbon and HTH domains
COG1814	P	Predicted Fe2+/Mn2+ transporter, VIT1/CCC1 family
COG1815	N	Flagellar basal body rod protein FlgB
COG1816	F	Adenosine deaminase
COG1817	R	Predicted glycosyltransferase
COG1818	J	tRNA(Ser,Leu) C12 N-acetylase TAN1, contains THUMP domain
COG1819	G	UDP:flavonoid glycosyltransferase YjiC, YdhE family
COG1820	G	N-acetylglucosamine-6-phosphate deacetylase
COG1821	R	Predicted ATP-dependent carboligase, ATP-grasp superfamily
COG1822	S	Uncharacterized membrane protein
COG1823	E	L-cystine uptake protein TcyP, sodium:dicarboxylate symporter family
COG1824	P	Permease, similar to cation transporters
COG1825	J	Ribosomal protein L25 (general stress protein Ctc)
COG1826	U	Sec-independent protein translocase protein TatA
COG1827	KH	Transcriptional regulator of NAD metabolism, contains HTH and 3H domains
COG1828	F	Phosphoribosylformylglycinamidine (FGAM) synthase, PurS component
COG1829	H	Archaeal pantoate kinase
COG1830	G	Fructose-bisphosphate aldolase class Ia, DhnA family
COG1831	R	Predicted metal-dependent hydrolase, urease superfamily
COG1832	R	Predicted CoA-binding protein
COG1833	R	Uri superfamily endonuclease
COG1834	E	N-Dimethylarginine dimethylaminohydrolase
COG1835	M	Peptidoglycan/LPS O-acetylase OafA/YrhL, contains acyltransferase and SGNH-hydrolase domains
COG1836	S	Uncharacterized membrane protein
COG1837	R	Predicted RNA-binding protein YlqC, contains KH domain, UPF0109 family
COG1838	C	Tartrate dehydratase beta subunit/Fumarate hydratase class I, C-terminal domain
COG1839	F	Adenosine/AMP kinase
COG1840	P	ABC-type Fe3+ transport system, periplasmic component
COG1841	J	Ribosomal protein L30/L7E
COG1842	KT	Phage shock protein A
COG1843	N	Flagellar hook assembly protein FlgD
COG1844	S	Uncharacterized protein
COG1845	C	Heme/copper-type cytochrome/quinol oxidase, subunit 3
COG1846	K	DNA-binding transcriptional regulator, MarR family
COG1847	R	Predicted RNA-binding protein Jag, conains KH and R3H domains
COG1848	R	Predicted nucleic acid-binding protein, contains PIN domain
COG1849	S	Uncharacterized protein
COG1850	G	Ribulose 1,5-bisphosphate carboxylase, large subunit, or a RuBisCO-like protein
COG1851	S	Uncharacterized protein, UPF0128 family
COG1852	S	Uncharacterized protein
COG1853	C	NADH-FMN oxidoreductase RutF, flavin reductase (DIM6/NTAB) family
COG1854	T	S-ribosylhomocysteine lyase LuxS, autoinducer biosynthesis
COG1855	R	Predicted ATPase, PilT family
COG1856	R	Uncharacterized protein, radical SAM superfamily
COG1857	V	CRISPR/Cas system-associated protein Cas7,  RAMP superfamily
COG1858	O	Cytochrome c peroxidase
COG1859	J	RNA:NAD 2'-phosphotransferase, TPT1/KptA family
COG1860	FL	Uncharacterized conserved protein, UPF0179 family
COG1861	M	Spore coat polysaccharide biosynthesis protein SpsF, cytidylyltransferase family
COG1862	U	Preprotein translocase subunit YajC
COG1863	P	Multisubunit Na+/H+ antiporter, MnhE subunit
COG1864	F	DNA/RNA endonuclease G, NUC1
COG1865	H	Adenosylcobinamide amidohydrolase
COG1866	C	Phosphoenolpyruvate carboxykinase, ATP-dependent
COG1867	J	tRNA G26 N,N-dimethylase Trm1
COG1868	N	Flagellar motor switch protein FliM
COG1869	G	D-ribose pyranose/furanose isomerase RbsD
COG1871	NT	Chemotaxis receptor (MCP) glutamine deamidase CheD
COG1872	S	Uncharacterized conserved protein YggU, UPF0235/DUF167 family
COG1873	R	Sporulation protein YlmC, PRC-barrel domain family
COG1874	G	Beta-galactosidase GanA
COG1875	R	Predicted ribonuclease YlaK, contains NYN-type RNase and PhoH-family ATPase domains
COG1876	M	LD-carboxypeptidase LdcB, LAS superfamily
COG1877	G	Trehalose-6-phosphatase
COG1878	E	Kynurenine formamidase
COG1879	G	ABC-type sugar transport system, periplasmic component, contains N-terminal xre family HTH domain
COG1880	C	CO dehydrogenase/acetyl-CoA synthase epsilon subunit
COG1881	R	Uncharacterized conserved protein, phosphatidylethanolamine-binding protein (PEBP) family
COG1882	C	Pyruvate-formate lyase
COG1883	C	Na+-transporting methylmalonyl-CoA/oxaloacetate decarboxylase, beta subunit
COG1884	I	Methylmalonyl-CoA mutase, N-terminal domain/subunit
COG1885	S	Uncharacterized protein, UPF0212 family
COG1886	NU	Flagellar motor switch/type III secretory pathway protein FliN
COG1887	MI	CDP-glycerol glycerophosphotransferase, TagB/SpsB family
COG1888	S	Uncharacterized protein
COG1889	J	Fibrillarin-like rRNA methylase
COG1890	J	Ribosomal protein S3AE
COG1891	S	Uncharacterized protein, UPF0264 family
COG1892	G	Phosphoenolpyruvate carboxylase
COG1893	H	Ketopantoate reductase
COG1894	C	NADH:ubiquinone oxidoreductase, NADH-binding 51 kD subunit (chain F)
COG1895	S	Uncharacterized protein, contains HEPN domain, UPF0332 family
COG1896	FR	5'-deoxynucleotidase YfbR and related HD superfamily hydrolases
COG1897	E	Homoserine trans-succinylase
COG1898	M	dTDP-4-dehydrorhamnose 3,5-epimerase or related enzyme
COG1899	OJ	Deoxyhypusine synthase
COG1900	S	Uncharacterized conserved protein, DUF39 family
COG1901	J	tRNA pseudouridine-54 N-methylase
COG1902	C	2,4-dienoyl-CoA reductase or related NADH-dependent reductase, Old Yellow Enzyme (OYE) family
COG1903	H	Cobalamin biosynthesis protein CbiD
COG1904	G	Glucuronate isomerase
COG1905	C	NADH:ubiquinone oxidoreductase 24 kD subunit (chain E)
COG1906	S	Uncharacterized protein
COG1907	R	Predicted archaeal sugar kinase
COG1908	C	Coenzyme F420-reducing hydrogenase, delta subunit
COG1909	S	Uncharacterized protein, UPF0218 family
COG1910	P	Periplasmic molybdate-binding protein/domain
COG1911	J	Ribosomal protein L30E
COG1912	H	S-adenosylmethionine hydrolase (SAM-hydroxide adenosyltransferase)
COG1913	R	Predicted Zn-dependent protease
COG1914	P	Mn2+ and Fe2+ transporters of the NRAMP family
COG1915	S	Uncharacterized conserved protein, contains Saccharopine dehydrogenase N-terminal (SDHN) domain
COG1916	S	Pheromone shutdown protein TraB, contains GTxH motif (function unknown)
COG1917	R	Cupin domain protein related to quercetin dioxygenase
COG1918	P	Fe2+ transport system protein FeoA
COG1920	H	2-phospho-L-lactate guanylyltransferase, coenzyme F420 biosynthesis enzyme, CobY/MobA/RfbA family
COG1921	J	Seryl-tRNA(Sec) selenium transferase
COG1922	M	UDP-N-acetyl-D-mannosaminuronic acid transferase, WecB/TagA/CpsF family
COG1923	T	sRNA-binding regulator protein Hfq
COG1924	I	Activator of 2-hydroxyglutaryl-CoA dehydratase (HSP70-class ATPase domain)
COG1925	TG	Phosphotransferase system, HPr and related phosphotransfer proteins
COG1926	R	Predicted phosphoribosyltransferase
COG1927	C	F420-dependent methylenetetrahydromethanopterin dehydrogenase
COG1928	O	Dolichyl-phosphate-mannose--protein O-mannosyl transferase
COG1929	G	Glycerate kinase
COG1930	P	ABC-type cobalt transport system, periplasmic component
COG1931	R	Predicted RNA binding protein with dsRBD fold, UPF0201 family
COG1932	HE	Phosphoserine aminotransferase
COG1933	L	Archaeal DNA polymerase II, large subunit
COG1934	M	Lipopolysaccharide export system protein LptA
COG1935	S	Uncharacterized protein
COG1936	F	Broad-specificity NMP kinase
COG1937	K	DNA-binding transcriptional regulator, FrmR family
COG1938	R	Predicted ATP-dependent carboligase, ATP-grasp superfamily
COG1939	J	23S rRNA maturation mini-RNase III
COG1940	KG	Sugar kinase of the NBD/HSP70 family, may contain an N-terminal HTH domain
COG1941	C	Coenzyme F420-reducing hydrogenase, gamma subunit
COG1942	Q	Phenylpyruvate tautomerase PptA, 4-oxalocrotonate tautomerase family
COG1943	X	REP element-mobilizing transposase RayT
COG1944	J	Ribosomal protein S12 methylthiotransferase accessory factor YcaO
COG1945	E	Pyruvoyl-dependent arginine decarboxylase (PvlArgDC)
COG1946	I	Acyl-CoA thioesterase
COG1947	I	4-diphosphocytidyl-2C-methyl-D-erythritol kinase
COG1948	L	ERCC4-type nuclease
COG1949	A	Oligoribonuclease (3'-5' exoribonuclease)
COG1950	S	Uncharacterized membrane protein YvlD, DUF360 family
COG1951	C	Tartrate dehydratase alpha subunit/Fumarate hydratase class I, N-terminal domain
COG1952	U	Preprotein translocase subunit SecB
COG1953	FH	Cytosine/uracil/thiamine/allantoin permease
COG1954	K	Glycerol-3-phosphate responsive antiterminator (mRNA-binding)
COG1955	N	Archaellum biogenesis protein FlaJ, TadC family
COG1956	VT	GAF domain-containing protein, putative methionine-R-sulfoxide reductase
COG1957	F	Inosine-uridine nucleoside N-ribohydrolase
COG1958	K	Small nuclear ribonucleoprotein (snRNP) homolog
COG1959	K	DNA-binding transcriptional regulator, IscR family
COG1960	I	Acyl-CoA dehydrogenase related to the alkylation response protein AidB
COG1961	L	Site-specific DNA recombinase related to the DNA invertase Pin
COG1962	H	Tetrahydromethanopterin S-methyltransferase, subunit H
COG1963	R	Acid phosphatase family membrane protein YuiD
COG1964	R	Uncharacterized Fe-S cluster-containing enzyme, radical SAM superfamily
COG1965	P	Iron-binding protein CyaY, frataxin homolog
COG1966	T	Carbon starvation protein CstA
COG1967	S	Uncharacterized membrane protein
COG1968	I	Undecaprenyl pyrophosphate phosphatase UppP
COG1969	C	Ni,Fe-hydrogenase I cytochrome b subunit
COG1970	M	Large-conductance mechanosensitive channel
COG1971	P	Putative Mn2+ efflux pump MntP
COG1972	F	Nucleoside permease NupC
COG1973	O	Hydrogenase maturation factor HypE
COG1974	KT	SOS-response transcriptional repressor LexA (RecA-mediated autopeptidase)
COG1975	O	Xanthine and CO dehydrogenase maturation factor, XdhC/CoxF family
COG1976	J	Translation initiation factor 6 (eIF-6)
COG1977	H	Molybdopterin converting factor, small subunit
COG1978	R	Predicted RNase H-related nuclease YkuK, DUF458 family
COG1979	C	Alcohol dehydrogenase YqhD, Fe-dependent ADH family
COG1980	G	Archaeal fructose 1,6-bisphosphatase
COG1981	S	Uncharacterized membrane protein
COG1982	E	Arginine/lysine/ornithine decarboxylase
COG1983	KT	Phage shock protein PspC (stress-responsive transcriptional regulator)
COG1984	E	Allophanate hydrolase subunit 2
COG1985	H	Pyrimidine reductase, riboflavin biosynthesis
COG1986	FV	Non-canonical (house-cleaning) NTP pyrophosphatase, all-alpha NTP-PPase family
COG1987	N	Flagellar biosynthesis protein FliQ
COG1988	R	Membrane-bound metal-dependent hydrolase YbcI, DUF457 family
COG1989	NU	Prepilin signal peptidase PulO (type II secretory pathway) or related peptidase
COG1990	J	Peptidyl-tRNA hydrolase
COG1991	S	Uncharacterized protein, UPF0333 family
COG1992	R	Predicted transcriptional regulator fused phosphomethylpyrimidine kinase (thiamin biosynthesis)
COG1993	T	PII-like signaling protein
COG1994	O	Zn-dependent protease (includes SpoIVFB)
COG1995	H	4-hydroxy-L-threonine phosphate dehydrogenase PdxA
COG1996	K	DNA-directed RNA polymerase, subunit RPC12/RpoP, contains C4-type Zn-finger
COG1997	J	Ribosomal protein L37AE/L43A
COG1998	J	Ribosomal protein S27AE
COG1999	O	Cytochrome oxidase Cu insertion factor, SCO1/SenC/PrrC family
COG2000	R	Uncharacterized Fe-S cluster-containing protein
COG2001	J	MraZ, DNA-binding transcriptional regulator and inhibitor of RsmH methyltransferase activity
COG2002	KV	Bifunctional DNA-binding transcriptional regulator of stationary/sporulation/toxin gene expression and antitoxin component of the YhaV-PrlF toxin-antitoxin module
COG2003	L	DNA repair protein RadC, contains a helix-hairpin-helix DNA-binding motif
COG2004	J	Ribosomal protein S24E
COG2005	K	DNA-binding transcriptional regulator ModE (molybdenum-dependent)
COG2006	S	Uncharacterized conserved protein, DUF362 family
COG2007	J	Ribosomal protein S8E
COG2008	E	Threonine aldolase
COG2009	C	Succinate dehydrogenase/fumarate reductase, cytochrome b subunit
COG2010	C	Cytochrome c, mono- and diheme variants
COG2011	E	ABC-type methionine transport system, permease component
COG2012	K	DNA-directed RNA polymerase, subunit H, RpoH/RPB5
COG2013	S	Uncharacterized conserved protein, AIM24 family
COG2014	S	Uncharacterized conserved protein, contains DUF4213 and DUF364 domains
COG2015	Q	Alkyl sulfatase BDS1 and related hydrolases, metallo-beta-lactamase superfamily
COG2016	J	Predicted ribosome-associated RNA-binding protein Tma20, contains PUA domain
COG2017	G	Galactose mutarotase or related enzyme
COG2018	T	Predicted regulator of Ras-like GTPase activity, Roadblock/LC7/MglB family
COG2019	F	Archaeal adenylate kinase
COG2020	O	Protein-S-isoprenylcysteine O-methyltransferase Ste14
COG2021	E	Homoserine acetyltransferase
COG2022	H	Thiamin biosynthesis thiazole synthase ThiGH, ThiG subunit
COG2023	J	RNase P subunit RPR2
COG2024	J	O-phosphoseryl-tRNA(Cys) synthetase
COG2025	C	Electron transfer flavoprotein, alpha subunit
COG2026	V	mRNA-degrading endonuclease RelE, toxin component of the RelBE toxin-antitoxin system
COG2027	M	D-alanyl-D-alanine carboxypeptidase
COG2028	S	Uncharacterized protein
COG2029	S	Uncharacterized protein
COG2030	I	Acyl dehydratase
COG2031	I	Short chain fatty acids transporter
COG2032	P	Cu/Zn superoxide dismutase
COG2033	C	Desulfoferrodoxin, superoxide reductase-like (SORL) domain
COG2034	S	Uncharacterized membrane protein
COG2035	S	Uncharacterized membrane protein
COG2036	B	Archaeal histone H3/H4
COG2037	C	Formylmethanofuran:tetrahydromethanopterin formyltransferase
COG2038	H	NaMN:DMB phosphoribosyltransferase
COG2039	O	Pyrrolidone-carboxylate peptidase (N-terminal pyroglutamyl peptidase)
COG2040	E	Homocysteine/selenocysteine methylase (S-methylmethionine-dependent)
COG2041	C	Periplasmic DMSO/TMAO reductase YedYZ, molybdopterin-dependent catalytic subunit
COG2042	J	Ribosome biogenesis protein Tsr3 (rRNA maturation)
COG2043	S	Uncharacterized conserved protein, DUF169 family
COG2044	R	Predicted peroxiredoxin
COG2045	HR	Phosphosulfolactate phosphohydrolase or related enzyme
COG2046	P	ATP sulfurylase (sulfate adenylyltransferase)
COG2047	R	Proteasome assembly chaperone (PAC2) family protein
COG2048	C	Heterodisulfide reductase, subunit B
COG2049	E	Allophanate hydrolase subunit 1
COG2050	Q	Acyl-coenzyme A thioesterase PaaI, contains HGG motif
COG2051	J	Ribosomal protein S27E
COG2052	M	Regulator of extracellular matrix RemA, YlzA/DUF370 family
COG2053	J	Ribosomal protein S28E/S33
COG2054	R	Uncharacterized archaeal kinase related to aspartokinase
COG2055	C	Malate/lactate/ureidoglycolate dehydrogenase, LDH2 family
COG2056	E	Predicted histidine transporter YuiF, NhaC family
COG2057	I	Acyl CoA:acetate/3-ketoacid CoA transferase, beta subunit
COG2058	J	Ribosomal protein L12E/L44/L45/RPP1/RPP2
COG2059	P	Chromate transport protein ChrA
COG2060	P	K+-transporting ATPase, A chain
COG2061	R	Uncharacterized conserved protein, contains ACT domain
COG2062	T	Phosphohistidine phosphatase SixA
COG2063	N	Flagellar basal body L-ring protein FlgH
COG2064	W	Pilus assembly protein TadC
COG2065	F	Pyrimidine operon attenuation protein/uracil phosphoribosyltransferase
COG2066	E	Glutaminase
COG2067	I	Long-chain fatty acid transport protein
COG2068	H	CTP:molybdopterin cytidylyltransferase MocA
COG2069	C	CO dehydrogenase/acetyl-CoA synthase delta subunit (corrinoid Fe-S protein)
COG2070	R	NAD(P)H-dependent flavin oxidoreductase YrpB, nitropropane dioxygenase family
COG2071	E	Gamma-glutamyl-gamma-aminobutyrate hydrolase PuuD (putrescine degradation), contains GATase1-like domain
COG2072	P	Predicted flavoprotein CzcO associated with the cation diffusion facilitator CzcD
COG2073	H	Cobalamin biosynthesis protein CbiG
COG2074	G	2-phosphoglycerate kinase
COG2075	J	Ribosomal protein L24E
COG2076	V	Multidrug transporter EmrE and related cation transporters
COG2077	O	Peroxiredoxin
COG2078	S	Uncharacterized conserved protein, AMMECR1 domain
COG2079	G	2-methylcitrate dehydratase PrpD
COG2080	C	Aerobic-type carbon monoxide dehydrogenase, small subunit, CoxS/CutS family
COG2081	R	Predicted flavoprotein YhiN
COG2082	H	Precorrin isomerase
COG2083	S	Uncharacterized protein, UPF0216 family
COG2084	I	3-hydroxyisobutyrate dehydrogenase or related beta-hydroxyacid dehydrogenase
COG2085	R	Predicted dinucleotide-binding enzyme
COG2086	C	Electron transfer flavoprotein, alpha and beta subunits
COG2087	H	Adenosyl cobinamide kinase/adenosyl cobinamide phosphate guanylyltransferase
COG2088	D	DNA-binding protein SpoVG, cell septation regulator
COG2089	M	Sialic acid synthase SpsE, contains C-terminal SAF domain
COG2090	S	Uncharacterized protein
COG2091	H	Phosphopantetheinyl transferase
COG2092	J	Translation elongation factor EF-1beta
COG2093	K	RNA polymerase subunit RPABC4/transcription elongation factor Spt4
COG2094	L	3-methyladenine DNA glycosylase Mpg
COG2095	E	Small neutral amino acid transporter SnatA, MarC family
COG2096	H	Cob(I)alamin adenosyltransferase
COG2097	J	Ribosomal protein L31E
COG2098	S	Uncharacterized protein
COG2099	H	Precorrin-6x reductase
COG2100	R	Uncharacterized Fe-S cluster-containing enzyme, radical SAM superfamily
COG2101	K	TATA-box binding protein (TBP), component of TFIID and TFIIIB
COG2102	J	Diphthamide synthase (EF-2-diphthine--ammonia ligase)
COG2103	M	N-acetylmuramic acid 6-phosphate (MurNAc-6-P) etherase
COG2104	H	Sulfur carrier protein ThiS (thiamine biosynthesis)
COG2105	R	Uncharacterized conserved protein YtfP, gamma-glutamylcyclotransferase (GGCT)/AIG2-like family
COG2106	R	Predicted RNA methylase MTH1, SPOUT superfamily
COG2107	R	Predicted periplasmic solute-binding protein
COG2108	S	Uncharacterized conserved protein related to pyruvate formate-lyase activating enzyme
COG2109	H	ATP:corrinoid adenosyltransferase
COG2110	J	O-acetyl-ADP-ribose deacetylase (regulator of RNase III), contains Macro domain
COG2111	P	Multisubunit Na+/H+ antiporter, MnhB subunit
COG2112	T	Predicted Ser/Thr protein kinase
COG2113	E	ABC-type proline/glycine betaine transport system, periplasmic component
COG2114	T	Adenylate cyclase, class 3
COG2115	G	Xylose isomerase
COG2116	P	Formate/nitrite transporter FocA, FNT family
COG2117	J	Predicted subunit of tRNA(5-methylaminomethyl-2-thiouridylate) methyltransferase, contains the PP-loop ATPase domain
COG2118	R	DNA-binding TFAR19-related protein, PDSD5 family
COG2119	R	Putative Ca2+/H+ antiporter, TMEM165/GDT1 family
COG2120	G	N-acetylglucosaminyl deacetylase, LmbE family
COG2121	S	Uncharacterized conserved protein, lysophospholipid acyltransferase (LPLAT) superfamily
COG2122	S	Uncharacterized protein, UPF0280 family, ApbE superfamily
COG2123	J	Exosome complex RNA-binding protein Rrp42, RNase PH superfamily
COG2124	QV	Cytochrome P450
COG2125	J	Ribosomal protein S6E (S10)
COG2126	J	Ribosomal protein L37E
COG2127	O	ATP-dependent Clp protease adapter protein ClpS
COG2128	P	Alkylhydroperoxidase family enzyme, contains CxxC motif
COG2129	R	Predicted phosphoesterase, related to the Icc protein
COG2130	QR	NADPH-dependent curcumin reductase CurA
COG2131	F	Deoxycytidylate deaminase
COG2132	DPM	Multicopper oxidase with three cupredoxin domains (includes cell division protein FtsP and spore coat protein CotA)
COG2133	G	Glucose/arabinose dehydrogenase, beta-propeller fold
COG2134	I	CDP-diacylglycerol pyrophosphatase
COG2135	O	Putative SOS response-associated peptidase YedK
COG2136	J	rRNA maturation protein Rpf1, contains Brix/IMP4 (anticodon-binding) domain
COG2137	O	SOS response regulatory protein OraA/RecX, interacts with RecA
COG2138	H	Sirohydrochlorin ferrochelatase
COG2139	J	Ribosomal protein L21E
COG2140	G	Oxalate decarboxylase/archaeal phosphoglucose isomerase, cupin superfamily
COG2141	HR	Flavin-dependent oxidoreductase, luciferase family (includes alkanesulfonate monooxygenase SsuD and methylene tetrahydromethanopterin reductase)
COG2142	C	Succinate dehydrogenase, hydrophobic anchor subunit
COG2143	O	Thioredoxin-related protein
COG2144	R	Selenophosphate synthetase-related protein
COG2145	H	Hydroxyethylthiazole kinase, sugar kinase family
COG2146	PQ	Ferredoxin subunit of nitrite reductase or a ring-hydroxylating dioxygenase
COG2147	J	Ribosomal protein L19E
COG2148	M	Sugar transferase involved in LPS biosynthesis (colanic, teichoic acid)
COG2149	S	Uncharacterized membrane protein YidH, DUF202 family
COG2150	R	Predicted regulator of amino acid metabolism, contains ACT domain
COG2151	O	Metal-sulfur cluster biosynthetic enzyme
COG2152	G	Predicted glycosyl hydrolase, GH43/DUF377 family
COG2153	R	Predicted N-acyltransferase, GNAT family
COG2154	H	Pterin-4a-carbinolamine dehydratase
COG2155	S	Uncharacterized membrane protein YuzA, DUF378 family
COG2156	P	K+-transporting ATPase, c chain
COG2157	J	Ribosomal protein L20A (L18A)
COG2158	R	Uncharacterized protein, contains a Zn-finger-like domain
COG2159	R	Predicted metal-dependent hydrolase, TIM-barrel fold
COG2160	G	L-arabinose isomerase
COG2161	V	Antitoxin component YafN of the YafNO toxin-antitoxin module, PHD/YefM family
COG2162	Q	Arylamine N-acetyltransferase
COG2163	J	Ribosomal protein L14E/L6E/L27E
COG2164	S	Uncharacterized protein
COG2165	NUW	Type II secretory pathway, pseudopilin PulG
COG2166	O	Sulfur transfer protein SufE, Fe-S center assembly
COG2167	J	Ribosomal protein L39E
COG2168	O	Sulfur transfer complex TusBCD TusB component, DsrH family
COG2169	L	Methylphosphotriester-DNA--protein-cysteine methyltransferase (N-terminal fragment of Ada), contains Zn-binding and two AraC-type DNA-binding domains
COG2170	O	Gamma-glutamyl:cysteine ligase YbdK, ATP-grasp superfamily
COG2171	E	Tetrahydrodipicolinate N-succinyltransferase
COG2172	T	Anti-sigma regulatory factor (Ser/Thr protein kinase)
COG2173	M	D-alanyl-D-alanine dipeptidase
COG2174	J	Ribosomal protein L34E
COG2175	Q	Taurine dioxygenase, alpha-ketoglutarate-dependent
COG2176	L	DNA polymerase III, alpha subunit (gram-positive type)
COG2177	D	Cell division protein FtsX
COG2178	R	Predicted RNA- or ssDNA-binding protein, translin family
COG2179	R	Predicted phosphohydrolase YqeG, HAD superfamily
COG2180	CPO	Nitrate reductase assembly protein NarJ, required for insertion of molybdenum cofactor
COG2181	CP	Nitrate reductase gamma subunit
COG2182	G	Maltose-binding periplasmic protein MalE
COG2183	K	Transcriptional accessory protein Tex/SPT6
COG2184	T	Fido, protein-threonine AMPylation domain
COG2185	I	Methylmalonyl-CoA mutase, C-terminal domain/subunit (cobalamin-binding)
COG2186	K	DNA-binding transcriptional regulator, FadR family
COG2187	R	Aminoglycoside phosphotransferase family enzyme
COG2188	K	DNA-binding transcriptional regulator, GntR family
COG2189	L	Adenine specific DNA methylase Mod
COG2190	G	Phosphotransferase system IIA component
COG2191	C	Formylmethanofuran dehydrogenase subunit E
COG2192	R	Predicted carbamoyl transferase, NodU family
COG2193	P	Bacterioferritin (cytochrome b1)
COG2194	M	Phosphoethanolamine transferase for periplasmic glucans (OPG), alkaline phosphatase superfamily
COG2195	E	Di- or tripeptidase
COG2197	TK	DNA-binding response regulator, NarL/FixJ family, contains REC and HTH domains
COG2198	T	HPt (histidine-containing phosphotransfer) domain
COG2199	T	GGDEF domain, diguanylate cyclase (c-di-GMP synthetase) or its enzymatically inactive variants
COG2200	T	EAL domain, c-di-GMP-specific phosphodiesterase class I (or its enzymatically inactive variant)
COG2201	NT	Chemotaxis response regulator CheB, contains REC and protein-glutamate methylesterase domains
COG2202	T	PAS domain
COG2203	T	GAF domain
COG2204	T	DNA-binding transcriptional response regulator, NtrC family, contains REC, AAA-type ATPase, and a Fis-type DNA-binding domains
COG2205	T	K+-sensing histidine kinase KdpD
COG2206	T	HD-GYP domain, c-di-GMP phosphodiesterase class II (or its inactivated variant)
COG2207	K	AraC-type DNA-binding domain and AraC-containing proteins
COG2208	TK	Serine phosphatase RsbU, regulator of sigma subunit
COG2209	C	Na+-transporting NADH:ubiquinone oxidoreductase, subunit NqrE
COG2210	C	Peroxiredoxin family protein
COG2211	G	Na+/melibiose symporter or related transporter
COG2212	P	Multisubunit Na+/H+ antiporter, MnhF subunit
COG2213	G	Phosphotransferase system, mannitol-specific IIBC component
COG2214	K	Curved DNA-binding protein CbpA, contains a DnaJ-like domain
COG2215	P	ABC-type nickel/cobalt efflux system, permease component RcnA
COG2216	P	High-affinity K+ transport system, ATPase chain B
COG2217	P	Cation transport ATPase
COG2218	C	Formylmethanofuran dehydrogenase subunit C
COG2219	L	Eukaryotic-type DNA primase, large subunit
COG2220	G	L-ascorbate metabolism protein UlaG, beta-lactamase superfamily
COG2221	P	Dissimilatory sulfite reductase (desulfoviridin), alpha and beta subunits
COG2222	M	Fructoselysine-6-P-deglycase FrlB and related proteins with duplicated sugar isomerase (SIS) domain
COG2223	P	Nitrate/nitrite transporter NarK
COG2224	C	Isocitrate lyase
COG2225	C	Malate synthase
COG2226	H	Ubiquinone/menaquinone biosynthesis C-methylase UbiE
COG2227	H	2-polyprenyl-3-methyl-5-hydroxy-6-metoxy-1,4-benzoquinol methylase
COG2229	U	Signal recognition particle receptor subunit beta, a GTPase
COG2230	I	Cyclopropane fatty-acyl-phospholipid synthase and related methyltransferases
COG2231	R	Uncharacterized protein related to Endonuclease III
COG2232	R	Predicted ATP-dependent carboligase, ATP-grasp superfamily
COG2233	F	Xanthine/uracil permease
COG2234	O	Zn-dependent amino- or carboxypeptidase, M28 family
COG2235	E	Arginine deiminase
COG2236	H	Hypoxanthine phosphoribosyltransferase
COG2237	S	Uncharacterized membrane protein
COG2238	J	Ribosomal protein S19E (S16A)
COG2239	P	Mg/Co/Ni transporter MgtE (contains CBS domain)
COG2240	H	Pyridoxal/pyridoxine/pyridoxamine kinase
COG2241	H	Precorrin-6B methylase 1
COG2242	H	Precorrin-6B methylase 2
COG2243	H	Precorrin-2 methylase
COG2244	M	Membrane protein involved in the export of O-antigen and teichoic acid
COG2245	S	Uncharacterized membrane protein
COG2246	I	Putative flippase GtrA (transmembrane translocase of bactoprenol-linked glucose)
COG2247	M	Putative cell wall-binding domain
COG2248	R	Predicted hydrolase, metallo-beta-lactamase superfamily
COG2249	R	Putative NADPH-quinone reductase (modulator of drug activity B)
COG2250	S	HEPN domain
COG2251	R	Predicted nuclease, RecB family
COG2252	F	Xanthine/uracil/vitamin C permease, AzgA family
COG2253	V	Predicted nucleotidyltransferase component of viral defense system
COG2254	V	CRISPR/Cas system-associated endonuclease Cas3-HD
COG2255	L	Holliday junction resolvasome RuvABC, ATP-dependent DNA helicase subunit
COG2256	L	Replication-associated recombination protein RarA (DNA-dependent ATPase)
COG2257	U	Type III secretion system substrate exporter, FlhB-like
COG2258	S	Uncharacterized conserved protein YiiM, contains MOSC domain
COG2259	S	Uncharacterized membrane protein YphA, DoxX/SURF4 family
COG2260	J	rRNA maturation protein Nop10, contains Zn-ribbon domain
COG2261	R	Uncharacterized membrane protein YeaQ/YmgE, transglycosylase-associated protein family
COG2262	J	50S ribosomal subunit-associated GTPase HflX
COG2263	R	Predicted RNA methylase
COG2264	J	Ribosomal protein L11 methylase PrmA
COG2265	J	tRNA/tmRNA/rRNA uracil-C5-methylase, TrmA/RlmC/RlmD family
COG2266	H	GTP:adenosylcobinamide-phosphate guanylyltransferase
COG2267	I	Lysophospholipase, alpha-beta hydrolase superfamily
COG2268	S	Uncharacterized membrane protein YqiK, contains Band7/PHB/SPFH domain
COG2269	J	Elongation factor P--beta-lysine ligase (EF-P beta-lysylation pathway)
COG2270	R	MFS-type transporter involved in bile tolerance, Atg22 family
COG2271	G	Sugar phosphate permease
COG2272	I	Carboxylesterase type B
COG2273	G	Beta-glucanase, GH16 family
COG2274	V	ABC-type bacteriocin/lantibiotic exporters, contain an N-terminal double-glycine peptidase domain
COG2301	G	Citrate lyase beta subunit
COG2302	R	RNA-binding protein YlmH, contains S4-like domain
COG2303	IR	Choline dehydrogenase or related flavoprotein
COG2304	R	Secreted protein containing bacterial Ig-like domain and vWFA domain
COG2306	R	Predicted RNA-binding protein, associated with RNAse of E/G family
COG2307	S	Uncharacterized conserved protein, Alpha-E superfamily
COG2308	S	Uncharacterized conserved protein, circularly permuted ATPgrasp superfamily
COG2309	E	Leucyl aminopeptidase (aminopeptidase T)
COG2310	T	Stress response protein SCP2
COG2311	S	Uncharacterized membrane protein YeiB
COG2312	Q	Erythromycin esterase homolog
COG2313	F	Pseudouridine-5'-phosphate glycosidase (pseudoU degradation)
COG2314	S	Uncharacterized membrane protein YozV, TM2 domain
COG2315	K	Predicted DNA-binding protein with 'double-wing' structural motif, MmcQ/YjbR family
COG2316	R	Predicted hydrolase, HD superfamily
COG2317	E	Zn-dependent carboxypeptidase, M32 family
COG2318	S	Uncharacterized damage-inducible protein DinB (forms a four-helix bundle)
COG2319	R	WD40 repeat
COG2320	R	GrpB domain, predicted nucleotidyltransferase, UPF0157 family
COG2321	R	Predicted metalloprotease
COG2322	S	Uncharacterized membrane protein YozB, DUF420 family
COG2323	S	Uncharacterized membrane protein YcaP, DUF421 family
COG2324	S	Uncharacterized membrane protein
COG2326	C	Polyphosphate kinase 2, PPK2 family
COG2327	M	Polysaccharide pyruvyl transferase family protein WcaK
COG2329	H	Heme-degrading monooxygenase HmoA and related ABM domain proteins
COG2331	R	Predicted nucleic acid-binding protein, contains Zn-ribbon domain
COG2332	CO	Cytochrome c-type biogenesis protein CcmE
COG2333	R	Metal-dependent hydrolase, beta-lactamase superfamily II
COG2334	T	Ser/Thr protein kinase RdoA involved in Cpx stress response, MazF antagonist
COG2335	R	Uncaracterized surface protein containing fasciclin (FAS1) repeats
COG2336	T	Antitoxin component of the MazEF toxin-antitoxin module
COG2337	V	mRNA-degrading endonuclease, toxin component of the MazEF toxin-antitoxin module
COG2339	T	Membrane proteinase PrsW, cleaves anti-sigma factor RsiW, M82 family
COG2340	S	Uncharacterized conserved protein YkwD, contains CAP (CSP/antigen 5/PR1) domain
COG2342	G	Endo alpha-1,4 polygalactosaminidase, GH114 family (was erroneously annotated as Cys-tRNA synthetase)
COG2343	S	Uncharacterized conserved protein, DUF427 family
COG2344	K	NADH/NAD ratio-sensing transcriptional regulator Rex
COG2345	K	Predicted transcriptional regulator, ArsR family
COG2346	P	Truncated hemoglobin YjbI
COG2348	M	Lipid II:glycine glycyltransferase (Peptidoglycan interpeptide bridge formation enzyme)
COG2350	R	Uncharacterized conserved protein YciI, contains a putative active-site phosphohistidine
COG2351	F	5-hydroxyisourate hydrolase (purine catabolism), transthyretin-related family
COG2352	C	Phosphoenolpyruvate carboxylase
COG2353	R	Polyisoprenoid-binding periplasmic protein YceI
COG2354	S	Uncharacterized membrane protein MutK, may be involved in DNA repair
COG2355	E	Zn-dependent dipeptidase, microsomal dipeptidase homolog
COG2356	L	Endonuclease I
COG2357	FT	ppGpp synthetase catalytic domain (RelA/SpoT-type nucleotidyltranferase)
COG2358	R	TRAP-type uncharacterized transport system, periplasmic component
COG2359	S	Stage V sporulation protein SpoVS  (function unknown)
COG2360	O	Leu/Phe-tRNA-protein transferase
COG2361	S	Uncharacterized conserved protein, contains HEPN domain
COG2362	E	D-aminopeptidase
COG2363	S	Uncharacterized membrane protein YgdD, TMEM256/DUF423 family
COG2364	S	Uncharacterized membrane protein YczE
COG2365	T	Protein tyrosine/serine phosphatase
COG2366	Q	Acyl-homoserine lactone (AHL) acylase PvdQ
COG2367	V	Beta-lactamase class A
COG2368	Q	Aromatic ring hydroxylase
COG2369	S	Uncharacterized conserved protein, contains phage Mu gpF-like domain
COG2370	O	Hydrogenase/urease accessory protein HupE
COG2371	O	Urease accessory protein UreE
COG2372	P	Copper-binding protein CopC (methionine-rich)
COG2373	R	Uncharacterized conserved protein YfaS, alpha-2-macroglobulin family
COG2374	R	Predicted extracellular nuclease
COG2375	P	NADPH-dependent ferric siderophore reductase, contains FAD-binding and SIP domains
COG2376	G	Dihydroxyacetone kinase
COG2377	M	1,6-Anhydro-N-acetylmuramate kinase
COG2378	K	Predicted DNA-binding transcriptional regulator YafY, contains an HTH and WYL domains
COG2379	G	Glycerate-2-kinase
COG2380	S	Uncharacterized protein
COG2382	P	Enterochelin esterase or related enzyme
COG2383	S	Uncharacterized membrane protein, Fun14 family
COG2384	J	tRNA A22 N-methylase
COG2385	M	Peptidoglycan hydrolase (amidase) enhancer domain
COG2386	O	ABC-type transport system involved in cytochrome c biogenesis, permease component
COG2388	R	Predicted acetyltransferase, GNAT superfamily
COG2389	S	Uncharacterized metal-binding protein
COG2390	K	DNA-binding transcriptional regulator LsrR, DeoR family
COG2391	R	Uncharacterized membrane protein YedE/YeeE, contains two sulfur transport domains
COG2401	R	ABC-type ATPase fused to a predicted acetyltransferase domain
COG2402	R	Predicted nucleic acid-binding protein, contains PIN domain
COG2403	R	Predicted GTPase
COG2404	JT	Oligoribonuclease NrnB or cAMP/cGMP phosphodiesterase, DHH superfamily
COG2405	R	Predicted nucleic acid-binding protein, contains PIN domain
COG2406	R	Protein distantly related to bacterial ferritins
COG2407	G	L-fucose isomerase or related protein
COG2409	S	Uncharacterized membrane protein YdfJ, MMPL/SSD domain
COG2410	R	Predicted nuclease (RNAse H fold)
COG2411	S	Uncharacterized protein
COG2412	S	Uncharacterized protein
COG2413	R	Predicted nucleotidyltransferase
COG2414	C	Aldehyde:ferredoxin oxidoreductase
COG2419	J	Trm5-related predicted tRNA methylase
COG2421	C	Acetamidase/formamidase
COG2423	E	Ornithine cyclodeaminase/archaeal alanine dehydrogenase, mu-crystallin family
COG2425	S	Uncharacterized protein, contains a von Willebrand factor type A (vWA) domain
COG2426	S	Uncharacterized membrane protein
COG2427	S	Uncharacterized conserved protein YjgD, DUF1641 family
COG2428	J	Rps3 or RNA methylase involved in ribosome biogenesis, SPOUT family,
COG2429	F	Archaeal GTP cyclohydrolase III
COG2430	S	Uncharacterized protein
COG2431	S	Uncharacterized membrane protein YbjE, DUF340 family
COG2433	R	Possible nuclease of RNase H fold, RuvC/YqgF family
COG2440	C	Ferredoxin-like protein FixX
COG2441	R	Predicted butyrate kinase, DUF1464 family
COG2442	S	Uncharacterized conserved protein, DUF433 family
COG2443	U	Preprotein translocase subunit Sss1
COG2445	S	Uncharacterized conserved protein YutE, UPF0331/DUF86 family
COG2450	D	Predicted archaeal cell division protein, SepF homolog, DUF552 family
COG2451	J	Ribosomal protein L35AE/L33A
COG2452	X	Predicted site-specific integrase-resolvase
COG2453	T	Protein-tyrosine phosphatase
COG2454	S	Uncharacterized protein
COG2456	S	Uncharacterized protein
COG2457	S	Uncharacterized protein
COG2461	S	Uncharacterized conserved protein, DUF438 domain, may contain hemerythrin domain
COG2469	S	Uncharacterized protein, contains HTH domain
COG2501	J	Ribosome-associated protein YbcJ, S4-like RNA binding protein
COG2502	E	Asparagine synthetase A
COG2503	R	Predicted secreted acid phosphatase
COG2508	K	DNA-binding transcriptional regulator, PucR family
COG2509	R	Uncharacterized FAD-dependent dehydrogenase
COG2510	S	Uncharacterized membrane protein
COG2511	J	Archaeal Glu-tRNAGln amidotransferase subunit E, contains GAD domain
COG2512	S	Uncharacterized membrane protein
COG2513	G	2-Methylisocitrate lyase and related enzymes, PEP mutase family
COG2514	Q	Catechol-2,3-dioxygenase
COG2515	E	1-aminocyclopropane-1-carboxylate deaminase/D-cysteine desulfhydrase, PLP-dependent ACC family
COG2516	R	Biotin synthase-related protein, radical SAM superfamily
COG2517	R	Predicted RNA-binding protein, contains C-terminal EMAP domain
COG2518	O	Protein-L-isoaspartate O-methyltransferase
COG2519	J	tRNA A58 N-methylase Trm61
COG2520	J	tRNA G37 N-methylase Trm5
COG2521	R	Predicted archaeal methyltransferase
COG2522	R	Predicted transcriptional regulator
COG2524	K	Predicted transcriptional regulator, contains C-terminal CBS domains
COG2602	V	Beta-lactamase class D
COG2603	J	tRNA 2-selenouridine synthase SelU, contains rhodanese domain
COG2604	S	Uncharacterized conserved protein
COG2605	R	Predicted kinase related to galactokinase and mevalonate kinase
COG2606	J	Cys-tRNA(Pro) deacylase, prolyl-tRNA editing enzyme YbaK/EbsC
COG2607	R	Predicted ATPase, AAA+ superfamily
COG2608	P	Copper chaperone CopZ
COG2609	C	Pyruvate dehydrogenase complex, dehydrogenase (E1) component
COG2610	GR	H+/gluconate symporter or related permease
COG2703	T	Hemerythrin
COG2704	G	Anaerobic C4-dicarboxylate transporter
COG2706	G	6-phosphogluconolactonase, cycloisomerase 2 family
COG2707	S	Uncharacterized membrane protein, DUF441 family
COG2710	P	Nitrogenase molybdenum-iron protein, alpha and beta chains
COG2715	R	Spore maturation protein SpmA (function unknown)
COG2716	E	Glycine cleavage system regulatory protein
COG2717	C	Periplasmic DMSO/TMAO reductase YedYZ, heme-binding membrane subunit
COG2718	R	Uncharacterized conserved protein YeaH/YhbH, required for sporulation, DUF444 family
COG2719	D	Stage V sporulation protein SpoVR/YcgB, involved in spore cortex formation (function unknown)
COG2720	V	Vancomycin resistance protein YoaR (function unknown), contains peptidoglycan-binding and VanW domains
COG2721	G	Altronate dehydratase
COG2723	G	Beta-glucosidase/6-phospho-beta-glucosidase/beta-galactosidase
COG2730	G	Aryl-phospho-beta-D-glucosidase BglC, GH1 family
COG2731	G	Beta-galactosidase, beta subunit
COG2732	K	Barstar, RNAse (barnase) inhibitor
COG2733	S	Uncharacterized membrane-anchored protein YjiN, DUF445 family
COG2738	O	Zn-dependent membrane protease YugP
COG2739	K	Predicted DNA-binding protein YlxM, UPF0122 family
COG2740	R	Predicted RNA-binding protein YlxR, DUF448 family
COG2746	V	Aminoglycoside N3'-acetyltransferase
COG2747	KN	Negative regulator of flagellin synthesis (anti-sigma28 factor)
COG2755	E	Lysophospholipase L1 or related esterase
COG2759	F	Formyltetrahydrofolate synthetase
COG2761	O	Predicted dithiol-disulfide isomerase, DsbA family
COG2764	R	Uncharacterized conserved protein PhnB, glyoxalase superfamily
COG2766	T	Predicted Ser/Thr protein kinase
COG2768	S	Uncharacterized Fe-S center protein
COG2770	T	HAMP domain
COG2771	K	DNA-binding transcriptional regulator, CsgD family
COG2801	X	Transposase InsO and inactivated derivatives
COG2802	S	Uncharacterized protein, similar to the N-terminal domain of Lon protease
COG2804	NUW	Type II secretory pathway ATPase GspE/PulE or T4P pilus assembly pathway ATPase PilB
COG2805	NW	Tfp pilus assembly protein PilT, pilus retraction ATPase
COG2807	P	Cyanate permease
COG2808	T	Predicted FMN-binding regulatory protein PaiB
COG2810	V	Predicted type IV restriction endonuclease
COG2811	C	Archaeal/vacuolar-type H+-ATPase subunit H
COG2812	L	DNA polymerase III, gamma/tau subunits
COG2813	J	16S rRNA G1207 methylase RsmC
COG2814	G	Predicted arabinose efflux permease, MFS family
COG2815	M	PASTA domain, binds beta-lactams
COG2816	F	NADH pyrophosphatase NudC, Nudix superfamily
COG2818	L	3-methyladenine DNA glycosylase Tag
COG2819	R	Predicted hydrolase of the alpha/beta superfamily
COG2820	F	Uridine phosphorylase
COG2821	M	Membrane-bound lytic murein transglycosylase
COG2822	P	Iron uptake system EfeUOB, periplasmic (or lipoprotein) component EfeO/EfeM
COG2823	S	Osmotically-inducible protein OsmY, contains BON domain
COG2824	K	Uncharacterized Zn-ribbon-containing protein
COG2825	MO	Periplasmic chaperone for outer membrane proteins, Skp family
COG2826	X	Transposase and inactivated derivatives, IS30 family
COG2827	L	Predicted endonuclease, GIY-YIG superfamily
COG2828	C	2-Methylaconitate cis-trans-isomerase PrpF (2-methyl citrate pathway)
COG2829	M	Outer membrane phospholipase A
COG2830	S	Uncharacterized protein
COG2831	U	Hemolysin activation/secretion protein
COG2832	S	Uncharacterized membrane protein YbaN, DUF454 family
COG2833	S	Uncharacterized conserved protein, contains ferritin-like DUF455 domain
COG2834	M	Outer membrane lipoprotein-sorting protein
COG2835	S	Uncharacterized conserved protein YbaR, Trm112 family
COG2836	P	Sulfite exporter TauE/SafE
COG2837	P	Periplasmic deferrochelatase/peroxidase EfeB
COG2838	C	Monomeric isocitrate dehydrogenase
COG2839	S	Uncharacterized conserved protein YqgC, DUF456 family
COG2840	L	DNA-nicking endonuclease, Smr domain
COG2841	S	Uncharacterized conserved protein YdcH, DUF465 family
COG2842	X	Bacteriophage DNA transposition protein, AAA+ family ATPase
COG2843	M	Poly-gamma-glutamate biosynthesis protein CapA/YwtB (capsule formation), metallophosphatase superfamily
COG2844	OT	UTP:GlnB (protein PII) uridylyltransferase
COG2845	S	Uncharacterized protein
COG2846	O	Iron-sulfur cluster repair protein YtfE, RIC family, contains ScdAN and hemerythrin domains
COG2847	P	Copper(I)-binding protein
COG2848	D	Uncharacterized conserved protein, UPF0210 family
COG2849	V	Antitoxin component YwqK of the YwqJK toxin-antitoxin module
COG2850	J	Ribosomal protein L16 Arg81 hydroxylase, contains JmjC domain
COG2851	C	Mg2+/citrate symporter
COG2852	L	Very-short-patch-repair endonuclease
COG2853	M	ABC-type transporter Mla maintaining outer membrane lipid asymmetry, lipoprotein component MlaA
COG2854	I	ABC-type transporter Mla maintaining outer membrane lipid asymmetry, periplasmic MlaC component
COG2855	S	Uncharacterized membrane protein YadS
COG2856	E	Zn-dependent peptidase ImmA, M78 family
COG2857	C	Cytochrome c1
COG2859	S	Uncharacterized protein
COG2860	S	Uncharacterized membrane protein YeiH
COG2861	G	Uncharacterized conserved protein YibQ, putative polysaccharide deacetylase 2 family
COG2862	S	Uncharacterized membrane protein YqhA
COG2863	C	Cytochrome c553
COG2864	C	Cytochrome b subunit of formate dehydrogenase
COG2865	K	Predicted transcriptional regulator, contains HTH domain
COG2866	M	Murein tripeptide amidase MpaA
COG2867	J	Ribosome association toxin PasT (RatA) of the RatAB toxin-antitoxin module
COG2868	S	Uncharacterized conserved protein YsxB, DUF464 family
COG2869	C	Na+-transporting NADH:ubiquinone oxidoreductase, subunit NqrC
COG2870	M	ADP-heptose synthase, bifunctional sugar kinase/adenylyltransferase
COG2871	C	Na+-transporting NADH:ubiquinone oxidoreductase, subunit NqrF
COG2872	J	Ser-tRNA(Ala) deacylase AlaX (editing enzyme)
COG2873	E	O-acetylhomoserine/O-acetylserine sulfhydrylase, pyridoxal phosphate-dependent
COG2874	N	Archaellum biogenesis protein FlaH, an ATPase
COG2875	H	Precorrin-4 methylase
COG2876	E	3-deoxy-D-arabino-heptulosonate 7-phosphate (DAHP) synthase
COG2877	M	3-deoxy-D-manno-octulosonic acid (KDO) 8-phosphate synthase
COG2878	C	Na+-translocating ferredoxin:NAD+ oxidoreductase RNF, RnfB subunit
COG2879	S	Uncharacterized short protein YbdD, DUF466 family
COG2880	R	Predicted DNA-binding protein, potential antitoxin AbrB/MazE fold
COG2881	S	Uncharacterized protein
COG2882	N	Flagellar biosynthesis chaperone FliJ
COG2884	D	ABC-type ATPase involved in cell division
COG2885	M	Outer membrane protein OmpA and related peptidoglycan-associated (lipo)proteins
COG2886	R	Predicted antitoxin, contains HTH domain
COG2887	L	RecB family exonuclease
COG2888	R	Predicted RNA-binding protein involved in translation, contains  Zn-ribbon domain, DUF1610 family
COG2890	J	Methylase of polypeptide chain release factors
COG2891	M	Cell shape-determining protein MreD
COG2892	J	tRNA threonylcarbamoyladenosine modification (KEOPS) complex,  Pcc1 subunit
COG2893	G	Phosphotransferase system, mannose/fructose-specific component IIA
COG2894	D	Septum formation inhibitor-activating ATPase MinD
COG2895	P	Sulfate adenylyltransferase subunit 1, EFTu-like GTPase family
COG2896	H	Molybdenum cofactor biosynthesis enzyme MoaA
COG2897	P	3-mercaptopyruvate sulfurtransferase SseA, contains two rhodanese domains
COG2898	S	Lysylphosphatidylglycerol synthetase, C-terminal domain, DUF2156 family
COG2899	S	Uncharacterized protein
COG2900	S	Uncharacterized coiled-coil protein SlyX (sensitive to lysis X)
COG2901	K	DNA-binding protein Fis (factor for inversion stimulation)
COG2902	E	NAD-specific glutamate dehydrogenase
COG2904	J	NADPH-dependent 7-cyano-7-deazaguanine reductase QueF, N-terminal domain
COG2905	T	Signal-transduction protein containing cAMP-binding, CBS, and nucleotidyltransferase domains
COG2906	P	Bacterioferritin-associated ferredoxin
COG2907	R	Predicted NAD/FAD-binding protein
COG2908	M	UDP-2,3-diacylglucosamine pyrophosphatase LpxH
COG2909	K	ATP-, maltotriose- and DNA-dependent transcriptional regulator MalT
COG2910	R	Putative NADH-flavin reductase
COG2911	U	Autotransporter translocation and assembly factor TamB
COG2912	T	Regulator of sirC expression, contains transglutaminase-like and TPR domains
COG2913	M	Outer membrane protein assembly factor BamE, lipoprotein component of the BamABCDE complex
COG2914	V	Putative antitoxin component PasI (RatB) of the RatAB toxin-antitoxin module, ubiquitin-RnfH superfamily
COG2915	XT	Regulator of phage lambda lysogenization HflD, binds to CII and stimulates its degradation
COG2916	K	DNA-binding protein H-NS
COG2917	D	Intracellular septation protein A
COG2918	H	Gamma-glutamylcysteine synthetase
COG2919	D	Cell division protein FtsB
COG2920	P	Sulfur relay (sulfurtransferase) protein, DsrC/TusE family
COG2921	T	Putative lipoic acid-binding regulatory protein
COG2922	S	Uncharacterized conserved protein Smg, DUF494 family
COG2923	P	Sulfur relay (sulfurtransferase) complex TusC component, DsrF/TusC family
COG2924	PO	Fe-S cluster biosynthesis and repair protein YggX
COG2925	L	Exonuclease I
COG2926	S	Uncharacterized conserved protein YeeX, DUF496 family
COG2927	L	DNA polymerase III, chi subunit
COG2928	S	Uncharacterized membrane protein
COG2929	S	Uncharacterized conserved protein, DUF497 family
COG2930	I	Lipid-binding SYLF domain
COG2931	Q	Ca2+-binding protein, RTX toxin-related
COG2932	X	Phage repressor protein C, contains Cro/C1-type HTH and peptisase s24 domains
COG2933	J	23S rRNA C2498 (ribose-2'-O)-methylase RlmM
COG2935	O	Arginyl-tRNA--protein-N-Asp/Glu arginylyltransferase
COG2936	R	Predicted acyl esterase
COG2937	I	Glycerol-3-phosphate O-acyltransferase
COG2938	O	Succinate dehydrogenase flavin-adding protein, antitoxin component of the CptAB toxin-antitoxin module
COG2939	E	Carboxypeptidase C (cathepsin A)
COG2940	R	SET domain-containing protein (function unknown)
COG2941	H	Demethoxyubiquinone hydroxylase, CLK1/Coq7/Cat5 family
COG2942	G	Mannose or cellobiose epimerase, N-acyl-D-glucosamine 2-epimerase family
COG2943	MG	Membrane glycosyltransferase
COG2944	K	DNA-binding transcriptional regulator YiaG, XRE-type HTH domain
COG2945	R	Alpha/beta superfamily hydrolase
COG2946	L	DNA relaxase NicK
COG2947	R	Predicted RNA-binding protein, contains PUA-like domain
COG2948	U	Type IV secretory pathway, VirB10 components
COG2949	M	Uncharacterized periplasmic protein SanA, affects membrane permeability for vancomycin
COG2951	M	Membrane-bound lytic murein transglycosylase B
COG2952	S	Uncharacterized protein
COG2954	R	CYTH domain, found in class IV adenylate cyclase and various triphosphatases
COG2956	M	Lipopolysaccharide biosynthesis regulator YciM, contains six TPR domains and a predicted metal-binding C-terminal domain
COG2957	E	Agmatine/peptidylarginine deiminase
COG2958	S	Uncharacterized protein
COG2959	S	Uncharacterized conserved protein HemX (no evidence of involvement in heme biosynthesis)
COG2960	S	Uncharacterized conserved protein YqiC, BMFP domain
COG2961	J	23S rRNA A2030 N6-methylase RlmJ
COG2962	S	Uncharacterized membrane protein RarD, contains two EamA domains
COG2963	X	Transposase and inactivated derivatives
COG2964	K	Predicted transcriptional regulator YheO, contains PAS and DNA-binding HTH domains
COG2965	L	Primosomal replication protein N
COG2966	S	Uncharacterized membrane protein YjjP, DUF1212 family
COG2967	P	Uncharacterized protein affecting Mg2+/Co2+ transport
COG2968	S	Uncharacterized conserved protein YggE, contains kinase-interacting SIMPL domain
COG2969	R	Stringent starvation protein B
COG2971	G	BadF-type ATPase, related to human N-acetylglucosamine kinase
COG2972	T	Sensor histidine kinase YesM
COG2973	K	Trp operon repressor
COG2974	L	DNA recombination-dependent growth factor C
COG2975	O	Fe-S-cluster formation regulator IscX/YfhJ
COG2976	T	Putative negative regulator of RcsB-dependent stress response
COG2977	Q	4'-phosphopantetheinyl transferase EntD (siderophore biosynthesis)
COG2978	H	p-Aminobenzoyl-glutamate transporter AbgT
COG2979	S	Uncharacterized membrane protein YebE, DUF533 family
COG2980	M	Outer membrane lipoprotein LptE/RlpB (LPS assembly)
COG2981	E	Uncharacterized protein involved in cysteine biosynthesis
COG2982	M	Uncharacterized protein involved in outer membrane biogenesis
COG2983	S	Uncharacterized cysteine cluster protein YcgN, CxxCxxCC family
COG2984	R	ABC-type uncharacterized transport system, periplasmic component
COG2985	R	Uncharacterized membrane protein YbjL, putative transporter
COG2986	E	Histidine ammonia-lyase
COG2987	E	Urocanate hydratase
COG2988	E	Succinylglutamate desuccinylase
COG2989	M	Murein L,D-transpeptidase YcbB/YkuD
COG2990	S	Uncharacterized protein VirK/YbjX
COG2991	S	Uncharacterized protein
COG2992	R	Uncharacterized FlgJ-related protein
COG2993	C	Cbb3-type cytochrome oxidase, cytochrome c subunit
COG2994	O	ACP:hemolysin acyltransferase (hemolysin-activating protein)
COG2995	S	Uncharacterized paraquat-inducible protein A
COG2996	R	Predicted RNA-binding protein, contains S1 domains,  virulence factor B family
COG2998	P	ABC-type tungstate transport system, permease component
COG2999	O	Glutaredoxin 2
COG3000	I	Sterol desaturase/sphingolipid hydroxylase, fatty acid hydroxylase superfamily
COG3001	G	Fructosamine-3-kinase
COG3002	S	Uncharacterized conserved protein YbcC, UPF0753/DUF2309 family
COG3004	CP	Na+/H+ antiporter NhaA
COG3005	C	Tetraheme cytochrome c subunit of nitrate or TMAO reductase
COG3006	D	Chromosome condensin MukBEF complex, kleisin-like MukF subunit
COG3007	I	Trans-2-enoyl-CoA reductase
COG3008	S	Paraquat-inducible protein B
COG3009	S	Uncharacterized lipoprotein YmbA
COG3010	G	Putative N-acetylmannosamine-6-phosphate epimerase
COG3011	R	Predicted thiol-disulfide oxidoreductase YuxK, DCC family
COG3012	S	Uncharacterized conserved protein YchJ, contains N- and C-terminal SEC-C domains
COG3013	S	Uncharacterized protein YfbU, UPF0304 family
COG3014	S	Uncharacterized protein
COG3015	MV	Uncharacterized lipoprotein NlpE involved in copper resistance
COG3016	S	Uncharacterized iron-regulated protein
COG3017	M	Outer membrane lipoprotein LolB, involved in outer membrane biogenesis
COG3018	S	Uncharacterized protein
COG3019	S	Uncharacterized conserved protein
COG3021	R	Uncharacterized conserved protein YafD, endonuclease/exonuclease/phosphatase (EEP) superfamily
COG3022	P	Cytoplasmic iron level regulating protein YaaA, DUF328/UPF0246 family
COG3023	M	N-acetyl-anhydromuramyl-L-alanine amidase AmpD
COG3024	L	Endogenous inhibitor of DNA gyrase, YacG/DUF329 family
COG3025	P	Inorganic triphosphatase YgiF, contains CYTH and CHAD domains
COG3026	T	Negative regulator of sigma E activity
COG3027	D	Cell division protein ZapA, inhibits GTPase activity of FtsZ
COG3028	J	Ribosomal 50S subunit-associated protein YjgA (function unknown), DUF615 family
COG3029	C	Fumarate reductase subunit C
COG3030	R	Protein affecting phage T7 exclusion by the F plasmid, UPF0716 family
COG3031	U	Type II secretory pathway, component PulC
COG3033	E	Tryptophanase
COG3034	M	Murein L,D-transpeptidase YafK
COG3036	J	Stalled ribosome alternative rescue factor ArfA
COG3037	G	Ascorbate-specific PTS system EIIC-type component UlaA
COG3038	C	Cytochrome b561
COG3039	X	Transposase and inactivated derivatives, IS5 family
COG3040	M	Bacterial lipocalin
COG3041	J	mRNA-degrading endonuclease (mRNA interferase) YafQ, toxin component of the YafQ-DinJ toxin-antitoxin module
COG3042	R	Putative hemolysin
COG3043	CP	Nitrate reductase cytochrome c-type subunit
COG3044	R	Predicted ATPase of the ABC class
COG3045	T	Periplasmic catabolite regulation protein CreA (function unknown)
COG3046	R	Uncharacterized protein related to deoxyribodipyrimidine photolyase
COG3047	M	Outer membrane protein W
COG3048	E	D-serine dehydratase
COG3049	MR	Penicillin V acylase or related amidase, Ntn superfamily
COG3050	L	DNA polymerase III, psi subunit
COG3051	C	Citrate lyase, alpha subunit
COG3052	C	Citrate lyase, gamma subunit
COG3053	C	Citrate lyase synthetase
COG3054	R	Predicted transcriptional regulator
COG3055	M	N-acetylneuraminic acid mutarotase
COG3056	S	Uncharacterized lipoprotein YajG
COG3057	L	Negative regulator of replication initiation
COG3058	CO	Formate dehydrogenase maturation protein FdhE
COG3059	S	Uncharacterized membrane protein YkgB
COG3060	KE	Transcriptional regulator of met regulon
COG3061	S	Cell envelope opacity-associated protein A (function unknown)
COG3062	O	Cytoplasmic chaperone NapD for the signal peptide of periplasmic nitrate reductase NapAB
COG3063	NW	Tfp pilus assembly protein PilF
COG3064	M	Membrane protein involved in colicin uptake
COG3065	M	Starvation-inducible outer membrane lipoprotein
COG3066	L	DNA mismatch repair protein MutH
COG3067	CP	Na+/H+ antiporter NhaB
COG3068	S	Uncharacterized protein YjaG, DUF416 family
COG3069	C	C4-dicarboxylate transporter
COG3070	K	Transcriptional regulator of competence genes, TfoX/Sxy family
COG3071	S	Uncharacterized conserved protein HemY, contains two TPR repeats
COG3072	F	Adenylate cyclase
COG3073	T	Negative regulator of sigma E activity
COG3074	D	Cell division protein ZapB, interacts with FtsZ
COG3075	E	Anaerobic glycerol-3-phosphate dehydrogenase
COG3076	J	Regulator of RNase E activity RraB
COG3077	V	Antitoxin component of the RelBE or YafQ-DinJ toxin-antitoxin module
COG3078	J	Ribosome assembly protein YihI, activator of Der GTPase
COG3079	S	Uncharacterized conserved protein YgfB, UPF0149 family
COG3080	C	Fumarate reductase subunit D
COG3081	S	Nucleoid-associated protein YejK (function unknown)
COG3082	S	Uncharacterized conserved protein YejL, UPF0352 family
COG3083	M	Membrane-anchored periplasmic protein YejM, alkaline phosphatase superfamily
COG3084	S	Uncharacterized protein YihD, DUF1040 family
COG3085	S	Uncharacterized conserved protein YifE, UPF0438 family
COG3086	T	Positive regulator of sigma E activity
COG3087	D	Cell division protein FtsN
COG3088	CO	Cytochrome c-type biogenesis protein CcmH/NrfF
COG3089	S	Uncharacterized conserved protein YheU, UPF0270 family
COG3090	G	TRAP-type C4-dicarboxylate transport system, small permease component
COG3091	R	Predicted Zn-dependent metalloprotease, SprT family
COG3092	S	Uncharacterized membrane protein YfbV, UPF0208 family
COG3093	V	Plasmid maintenance system antidote protein VapI, contains XRE-type HTH domain
COG3094	S	Uncharacterized membrane protein SirB2
COG3095	D	Chromosome condensin MukBEF, MukE localization factor
COG3096	D	Chromosome condensin MukBEF, ATPase and DNA-binding subunit MukB [Escherichia coli str. K-12 substr. MG1655
COG3097	S	Uncharacterized protein YqfB, UPF0267 family
COG3098	S	Uncharacterized conserved protein YqcC, DUF446 family
COG3099	S	Uncharacterized conserved protein YciU, UPF0263 family
COG3100	S	Uncharacterized conserved protein YcgL, UPF0745 family
COG3101	J	Elongation factor P hydroxylase (EF-P beta-lysylation pathway)
COG3102	R	Uncharacterized conserved protein YecM, predicted metalloenzyme
COG3103	R	Uncharacterized conserved protein YgiM, contains N-terminal SH3 domain, DUF1202 family
COG3104	E	Dipeptide/tripeptide permease
COG3105	S	Uncharacterized membrane-anchored protein YhcB, DUF1043 family
COG3106	R	Predicted ATPase, YcjX-like family
COG3107	M	Outer membrane lipoprotein LpoA, binds and activates PBP1a
COG3108	S	Uncharacterized conserved protein YcbK, DUF882 family
COG3109	T	sRNA-binding protein
COG3110	S	Uncharacterized conserved protein YccT, UPF0319 family
COG3111	S	Predicted periplasmic protein YdeI with OB-fold, BOF family
COG3112	S	Uncharacterized protein YacL, UPF0231 family
COG3113	M	ABC-type transporter Mla maintaining outer membrane lipid asymmetry, MlaB component, contains STAS domain
COG3114	U	Heme exporter protein D
COG3115	D	Cell division protein ZipA, interacts with FtsZ
COG3116	D	Cell division protein FtsL, interacts with FtsB, FtsL and FtsQ
COG3117	M	Lipopolysaccharide export system protein LptC
COG3118	O	Negative regulator of GroEL, contains thioredoxin-like and TPR-like domains
COG3119	P	Arylsulfatase A or related enzyme
COG3120	L	Macrodomain Ter protein organizer, MatP/YcbG family
COG3121	W	P pilus assembly protein, chaperone PapD
COG3122	S	Uncharacterized conserved protein YaiL, DUF2058 family
COG3123	S	Uncharacterized conserved protein YaiE, UPF0345 family
COG3124	I	Acyl carrier protein phosphodiesterase
COG3125	C	Heme/copper-type cytochrome/quinol oxidase, subunit 4
COG3126	S	Uncharacterized lipoprotein YbaY
COG3127	Q	Predicted ABC-type transport system involved in lysophospholipase L1 biosynthesis, permease component
COG3128	R	Predicted 2-oxoglutarate- and Fe(II)-dependent dioxygenase YbiX
COG3129	J	23S rRNA A1618 N6-methylase RlmF
COG3130	J	Ribosome modulation factor
COG3131	M	Periplasmic glucans biosynthesis protein
COG3132	S	Uncharacterized conserved protein YceH, UPF0502 family
COG3133	M	Outer membrane lipoprotein SlyB
COG3134	S	Uncharacterized conserved protein YcfJ, contains glycine zipper 2TM domain
COG3135	Q	Predicted benzoate:H+ symporter BenE
COG3136	S	Uncharacterized membrane protein, GlpM family
COG3137	M	Putative salt-induced outer membrane protein YdiY
COG3138	E	Arginine/ornithine N-succinyltransferase beta subunit
COG3139	S	Uncharacterized conserved protein YeaC, DUF1315 family
COG3140	S	Uncharacterized conserved protein YoaH, UPF0181 family
COG3141	L	dsDNA-binding SOS-regulon protein, induction by DNA damage requires cAMP
COG3142	P	Copper homeostasis protein CutC
COG3143	NT	Chemotaxis regulator CheZ, phosphatase of CheY~P
COG3144	N	Flagellar hook-length control protein FliK
COG3145	L	Alkylated DNA repair dioxygenase AlkB
COG3146	R	Predicted N-acyltransferase
COG3147	D	Cell division protein DedD (periplasmic protein involved in septation)
COG3148	S	Uncharacterized conserved protein YfiP, DTW domain
COG3149	U	Type II secretory pathway, component PulM
COG3150	R	Predicted esterase YcpF, UPF0227 family
COG3151	S	Uncharacterized protein YqiB, DUF1249 family
COG3152	S	Uncharacterized membrane protein YhaH, DUF805 family
COG3153	R	Predicted N-acetyltransferase YhbS
COG3154	I	Predicted lipid carrier protein YhbT, SCP2 domain
COG3155	Q	Enhancing lycopene biosynthesis protein 2
COG3156	U	Type II secretory pathway, component PulK
COG3157	U	Type VI protein secretion system component Hcp (secreted cytotoxin)
COG3158	P	K+ transporter
COG3159	S	Uncharacterized conserved protein YigA, DUF484 family
COG3160	K	Regulator of sigma D
COG3161	H	4-hydroxybenzoate synthetase (chorismate-pyruvate lyase)
COG3162	S	Uncharacterized membrane protein, DUF485 family
COG3164	S	Uncharacterized conserved protein YhdP, contains DUF3971 and AsmA2 domains
COG3165	H	Ubiquinone biosynthesis protein UbiJ, contains SCP2 domain
COG3166	NW	Tfp pilus assembly protein PilN
COG3167	NW	Tfp pilus assembly protein PilO
COG3168	NW	Tfp pilus assembly protein PilP
COG3169	S	Uncharacterized conserved protein, DUF486 family
COG3170	NW	Tfp pilus assembly protein FimV
COG3171	S	Uncharacterized conserved protein YggL, DUF469 family
COG3172	H	Nicotinamide riboside kinase
COG3173	R	Predicted  kinase, aminoglycoside phosphotransferase (APT) family
COG3174	S	Uncharacterized membrane protein, DUF4010 family
COG3175	CO	Cytochrome c oxidase assembly protein Cox11
COG3176	R	Putative hemolysin
COG3177	K	Fic family protein
COG3178	R	Predicted phosphotransferase, aminoglycoside/choline kinase (APH/ChoK) family
COG3179	R	Predicted chitinase
COG3180	R	Uncharacterized membrane protein AbrB, regulator of aidB expression
COG3181	C	Tripartite-type tricarboxylate transporter, receptor component TctC
COG3182	S	Uncharacterized iron-regulated membrane protein
COG3183	V	Predicted restriction endonuclease, HNH family
COG3184	S	Uncharacterized protein
COG3185	ER	4-hydroxyphenylpyruvate dioxygenase and related hemolysins
COG3186	E	Phenylalanine-4-hydroxylase
COG3187	O	Heat shock protein HslJ
COG3188	NW	Outer membrane usher protein FimD/PapC
COG3189	S	Uncharacterized conserved protein YeaO, DUF488 family
COG3190	N	Flagellar biogenesis protein FliO
COG3191	EQ	L-aminopeptidase/D-esterase
COG3192	E	Ethanolamine transporter EutH, required for ethanolamine utilization at low pH
COG3193	S	Uncharacterized conserved protein GlcG, DUF336 family
COG3194	F	Ureidoglycolate hydrolase (allantoin degradation)
COG3195	F	2-oxo-4-hydroxy-4-carboxy--5-ureidoimidazoline (OHCU) decarboxylase
COG3196	S	Uncharacterized protein CbrC, UPF0167 family
COG3197	P	Uncharacterized protein, possibly involved in nitrogen fixation
COG3198	S	Uncharacterized protein
COG3199	F	Predicted polyphosphate- or ATP-dependent NAD kinase
COG3200	E	3-deoxy-D-arabino-heptulosonate 7-phosphate (DAHP) synthase, class II
COG3201	H	Nicotinamide riboside transporter PnuC
COG3202	C	ATP/ADP translocase
COG3203	M	Outer membrane protein (porin)
COG3204	S	Uncharacterized protein YjiK
COG3205	S	Uncharacterized membrane protein
COG3206	M	Uncharacterized protein involved in exopolysaccharide biosynthesis
COG3207	Q	Pyoverdine/dityrosine biosynthesis protein Dit1
COG3208	Q	Surfactin synthase thioesterase subunit
COG3209	R	Uncharacterized conserved protein RhaS, contains 28 RHS repeats
COG3210	U	Large exoprotein involved in heme utilization or adhesion
COG3211	R	Secreted phosphatase, PhoX family
COG3212	S	Uncharacterized membrane protein YkoI
COG3213	V	Uncharacterized protein involved in response to NO
COG3214	R	Uncharacterized conserved protein YcaQ, contains winged helix DNA-binding domain
COG3215	NW	Tfp pilus assembly protein PilZ
COG3216	S	Uncharacterized conserved protein, DUF2062 family
COG3217	R	Uncharacterized conserved protein YcbX, contains MOSC and Fe-S domains
COG3218	R	ABC-type uncharacterized transport system, auxiliary component
COG3219	S	Uncharacterized protein
COG3220	S	Uncharacterized conserved protein, UPF0276 family
COG3221	P	ABC-type phosphate/phosphonate transport system, periplasmic component
COG3222	S	Uncharacterized conserved protein, glycosyltransferase A (GT-A) superfamily, DUF2064 family
COG3223	R	Phosphate starvation-inducible membrane PsiE (function unknown)
COG3224	R	Antibiotic biosynthesis monooxygenase (ABM) superfamily enzyme
COG3225	N	ABC-type uncharacterized transport system involved in gliding motility, auxiliary component
COG3226	K	DNA-binding transcriptional regulator YbjK
COG3227	O	Zn-dependent metalloprotease
COG3228	T	Mlc titration factor MtfA, regulates ptsG expression
COG3230	P	Heme oxygenase
COG3231	J	Aminoglycoside phosphotransferase
COG3232	E	5-carboxymethyl-2-hydroxymuconate isomerase
COG3233	R	Predicted deacetylase
COG3234	S	Uncharacterized conserved protein YfaT, DUF1175 family
COG3235	S	Uncharacterized membrane protein
COG3236	O	Predicted NAD-dependent protein-ADP-ribosyltransferase YbiA, DUF1768 family
COG3237	S	Uncharacterized conserved protein YjbJ, UPF0337 family
COG3238	S	Uncharacterized membrane protein YdcZ, DUF606 family
COG3239	I	Fatty acid desaturase
COG3240	IR	Phospholipase/lecithinase/hemolysin
COG3241	C	Azurin
COG3242	S	Uncharacterized conserved protein YjeT, DUF2065 family
COG3243	I	Poly(3-hydroxyalkanoate) synthetase
COG3245	C	Cytochrome c5
COG3246	S	Uncharacterized conserved protein, DUF849 family
COG3247	S	Uncharacterized membrane protein HdeD, DUF308 family
COG3248	M	Nucleoside-specific outer membrane channel protein Tsx
COG3249	S	Uncharacterized protein
COG3250	G	Beta-galactosidase/beta-glucuronidase
COG3251	S	Uncharacterized conserved protein YbdZ, MbtH family
COG3252	H	Methenyltetrahydromethanopterin cyclohydrolase
COG3253	P	Chlorite dismutase
COG3254	M	L-rhamnose mutarotase
COG3255	I	Putative sterol carrier protein
COG3256	P	Nitric oxide reductase large subunit
COG3257	S	Uncharacterized protein, possibly involved in glyoxylate utilization
COG3258	C	Cytochrome c
COG3259	C	Coenzyme F420-reducing hydrogenase, alpha subunit
COG3260	C	Ni,Fe-hydrogenase III small subunit
COG3261	C	Ni,Fe-hydrogenase III large subunit
COG3262	C	Ni,Fe-hydrogenase III component G
COG3263	CP	NhaP-type Na+/H+ and K+/H+ antiporter with C-terminal TrkAC and CorC domains
COG3264	M	Small-conductance mechanosensitive channel
COG3265	G	Gluconate kinase
COG3266	D	Cell division protein DamX, binds to the septal ring, contains C-terminal SPOR domain
COG3267	U	Type II secretory pathway, component ExeA (predicted ATPase)
COG3268	S	Uncharacterized conserved protein, related to short-chain dehydrogenases
COG3269	R	Predicted RNA-binding protein, contains TRAM domain
COG3270	J	Ribosome biogenesis protein, NOL1/NOP2/fmu family
COG3271	R	Predicted double-glycine peptidase
COG3272	S	Uncharacterized conserved protein YbgA, DUF1722 family
COG3273	S	Uncharacterized conserved protein, contains PhoU and TrkA_C domains
COG3274	M	Surface polysaccharide O-acyltransferase, integral membrane enzyme
COG3275	T	Sensor histidine kinase, LytS/YehU family
COG3276	J	Selenocysteine-specific translation elongation factor
COG3277	J	rRNA processing protein Gar1
COG3278	C	Cbb3-type cytochrome oxidase, subunit 1
COG3279	KT	DNA-binding response regulator, LytR/AlgR family
COG3280	G	Maltooligosyltrehalose synthase
COG3281	G	Predicted trehalose synthase
COG3283	KE	Transcriptional regulator of aromatic amino acids metabolism
COG3284	K	Transcriptional regulator of acetoin/glycerol metabolism
COG3285	L	Eukaryotic-type DNA primase
COG3286	S	Uncharacterized protein
COG3287	S	Uncharacterized conserved protein, contains FIST_N domain
COG3288	C	NAD/NADP transhydrogenase alpha subunit
COG3290	T	Sensor histidine kinase regulating citrate/malate metabolism
COG3291	S	PKD repeat
COG3292	T	Periplasmic ligand-binding sensor domain
COG3293	X	Transposase
COG3294	R	Metal-dependent phosphatase/phosphodiesterase, HD supefamily
COG3295	S	Uncharacterized protein
COG3296	S	Uncharacterized conserved protein, Tic20 family
COG3297	U	Type II secretory pathway, component PulL
COG3298	L	Predicted 3'-5' exonuclease related to the exonuclease domain of PolB
COG3299	X	Uncharacterized phage protein gp47/JayE
COG3300	T	MHYT domain, NO-binding membrane sensor
COG3301	P	Formate-dependent nitrite reductase, membrane component NrfD
COG3302	C	DMSO reductase anchor subunit
COG3303	P	Formate-dependent nitrite reductase, periplasmic cytochrome c552 subunit
COG3304	S	Uncharacterized membrane protein YccF, DUF307 family
COG3305	S	Uncharacterized membrane protein, DUF2068 family
COG3306	M	Glycosyltransferase involved in LPS biosynthesis, GR25 family
COG3307	M	O-antigen ligase
COG3308	S	Uncharacterized membrane protein
COG3309	S	Virulence-associated protein VapD (function unknown)
COG3310	S	Uncharacterized protein
COG3311	KX	Predicted DNA-binding transcriptional regulator AlpA
COG3312	C	FoF1-type ATP synthase assembly protein I
COG3313	R	Predicted Fe-S protein YdhL, DUF1289 family
COG3314	S	Uncharacterized membrane protein YjiH, contains nucleoside recognition GATE domain
COG3315	Q	O-Methyltransferase involved in polyketide biosynthesis
COG3316	X	Transposase (or an inactivated derivative)
COG3317	S	Uncharacterized lipoprotein
COG3318	S	Uncharacterized conserved protein YecA, UPF0149 family, contains C-terminal Zn-binding SEC-C motif
COG3319	Q	Thioesterase domain of type I polyketide synthase or non-ribosomal peptide synthetase
COG3320	Q	Thioester reductase domain of alpha aminoadipate reductase Lys2 and NRPSs
COG3321	Q	Acyl transferase domain in polyketide synthase (PKS) enzymes
COG3322	T	Extracellular (periplasmic) sensor domain CHASE (specificity unknown)
COG3323	S	Uncharacterized protein
COG3324	R	Predicted enzyme related to lactoylglutathione lyase
COG3325	G	Chitinase, GH18 family
COG3326	S	Uncharacterized membrane protein YsdA, DUF1294 family
COG3327	K	DNA-binding transcriptional regulator PaaX (phenylacetic acid degradation)
COG3328	X	Transposase (or an inactivated derivative)
COG3329	S	Uncharacterized conserved protein
COG3330	S	Uncharacterized conserved protein
COG3331	R	Penicillin-binding protein-related factor A, putative recombinase
COG3332	S	Uncharacterized conserved protein, contains NRDE domain
COG3333	R	TctA family transporter
COG3334	N	Flagellar motility protein MotE, a chaperone for MotC folding
COG3335	X	Transposase
COG3336	CO	Cytochrome c oxidase assembly factor CtaG
COG3337	V	CRISPR/Cas system CMR-associated protein Cmr5, small subunit
COG3338	P	Carbonic anhydrase
COG3339	S	Uncharacterized membrane protein YkvA, DUF1232 family
COG3340	E	Peptidase E
COG3341	R	RNase HI-related protein, contains viroplasmin and RNaseH domains
COG3342	R	Uncharacterized conserved protein, Ntn-hydrolase superfamily
COG3343	K	DNA-directed RNA polymerase, delta subunit
COG3344	X	Retron-type reverse transcriptase
COG3345	G	Alpha-galactosidase
COG3346	O	Cytochrome oxidase assembly protein ShyY1
COG3347	G	Rhamnose utilisation protein RhaD, predicted bifunctional aldolase and dehydrogenase
COG3349	R	Uncharacterized conserved protein, contains NAD-binding domain and a Fe-S cluster
COG3350	S	Uncharacterized conserved protein, YHS domain
COG3351	N	Archaellum component FlaD/FlaE
COG3352	N	Archaellum component FlaC
COG3353	N	Archaellum component FlaF, FlaF/FlaG flagellin family
COG3354	N	Archaellum component FlaG, FlaF/FlaG flagellin family
COG3355	K	Predicted transcriptional regulator
COG3356	I	Predicted membrane-associated lipid hydrolase, neutral ceramidase superfamily
COG3357	K	Predicted transcriptional regulator containing an HTH domain fused to a Zn-ribbon
COG3358	S	Uncharacterized conserved protein, DUF1684 family
COG3359	R	Uncharacterized conserved protein YprB, contains RNaseH-like and TPR domains
COG3360	R	Flavin-binding protein dodecin
COG3361	S	Uncharacterized protein YqjF, DUF2071 family
COG3363	F	Archaeal IMP cyclohydrolase
COG3364	R	Predicted  nucleic acid-binding protein, contains Zn-ribbon domain
COG3365	S	Uncharacterized protein
COG3366	S	Uncharacterized protein
COG3367	R	Uncharacterized conserved protein, NAD-dependent epimerase/dehydratase family
COG3368	R	Predicted permease
COG3369	S	Uncharacterized protein, contains Zn-finger domain of CDGSH type
COG3370	S	Uncharacterized protein
COG3371	S	Uncharacterized membrane protein
COG3372	R	Predicted nuclease of restriction endonuclease-like (RecB) superfamily, implicated in nucleotide excision repair
COG3373	K	Predicted transcriptional regulator, contains HTH domain
COG3374	S	Uncharacterized membrane protein
COG3375	R	Predicted acetyltransferase, GNAT superfamily
COG3376	P	High-affinity nickel permease
COG3377	S	Uncharacterized protein YunC, DUF1805 family
COG3378	X	Phage- or plasmid-associated DNA primase
COG3379	R	Predicted phosphohydrolase or phosphomutase, AlkP superfamily
COG3380	R	Predicted NAD/FAD-dependent oxidoreductase
COG3381	O	Cytoplasmic chaperone TorD involved in molybdoenzyme TorA maturation
COG3382	R	B3/B4 domain (DNA/RNA-binding domain of Phe-tRNA-synthetase)
COG3383	R	Predicted molibdopterin-dependent oxidoreductase YjgC
COG3384	Q	Aromatic ring-opening dioxygenase, catalytic subunit, LigB family
COG3385	X	IS4 transposase
COG3386	G	Sugar lactone lactonase YvrE
COG3387	G	Glucoamylase (glucan-1,4-alpha-glucosidase), GH15 family
COG3388	K	Predicted transcriptional regulator
COG3389	O	Presenilin-like membrane protease, A22 family
COG3390	L	Replication protein A (RPA) family protein
COG3391	R	DNA-binding beta-propeller fold protein YncE
COG3392	L	Adenine-specific DNA methylase
COG3393	R	Predicted acetyltransferase, GNAT family
COG3394	S	Predicted glycoside hydrolase or deacetylase ChbG, UPF0249 family
COG3395	S	Uncharacterized conserved protein YgbK, DUF1537 family
COG3396	Q	1,2-phenylacetyl-CoA epoxidase, catalytic subunit
COG3397	R	Predicted carbohydrate-binding protein, contains CBM5 and CBM33 domains
COG3398	K	Predicted transcriptional regulator, containsd two HTH domains
COG3399	S	Uncharacterized protein
COG3400	S	Uncharacterized protein
COG3401	R	Fibronectin type 3 domain
COG3402	S	Uncharacterized membrane protein YdbS, contains bPH2 (bacterial pleckstrin homology) domain
COG3403	S	Uncharacterized protein YcgG, contains conserved FPC and CPF motifs
COG3404	E	Formiminotetrahydrofolate cyclodeaminase
COG3405	G	Endo-1,4-beta-D-glucanase Y
COG3407	I	Mevalonate pyrophosphate decarboxylase
COG3408	G	Glycogen debranching enzyme (alpha-1,6-glucosidase)
COG3409	M	Peptidoglycan-binding (PGRP) domain of peptidoglycan hydrolases
COG3410	S	Uncharacterized protein, DUF2075 family
COG3411	C	(2Fe-2S) ferredoxin
COG3412	T	PTS-EIIA-like component DhaM of the dihydroxyacetone kinase DhaKLM complex
COG3413	R	Predicted DNA binding protein, contains HTH domain
COG3414	G	Phosphotransferase system, galactitol-specific IIB component
COG3415	X	Transposase
COG3416	S	Uncharacterized protein
COG3417	M	Outer membrane lipoprotein LpoB, binds and activates PBP1b
COG3418	NU	Flagellar biosynthesis/type III secretory pathway chaperone
COG3419	NW	Tfp pilus assembly protein, tip-associated adhesin PilY1
COG3420	P	Nitrous oxidase accessory protein NosD, contains tandem CASH domains
COG3421	S	Uncharacterized protein
COG3422	S	Uncharacterized conserved protein YegP, UPF0339 family
COG3423	K	Predicted transcriptional regulator, lambda repressor-like DNA-binding domain
COG3424	Q	Predicted naringenin-chalcone synthase
COG3425	I	3-hydroxy-3-methylglutaryl CoA synthase
COG3426	C	Butyrate kinase
COG3427	C	Carbon monoxide dehydrogenase subunit G
COG3428	S	Uncharacterized membrane protein YdbT, contains bPH2 (bacterial pleckstrin homology) domain
COG3429	G	Glucose-6-phosphate dehydrogenase assembly protein OpcA, contains a peptidoglycan-binding domain
COG3430	N	Archaeal flagellin (archaellin), FlaG/FlaF family
COG3431	S	Uncharacterized membrane protein, DUF373 family
COG3432	K	Predicted transcriptional regulator
COG3433	Q	Aryl carrier domain
COG3434	T	c-di-GMP-related signal transduction protein, contains EAL and HDOD domains
COG3435	Q	Gentisate 1,2-dioxygenase
COG3436	X	Transposase
COG3437	T	Response regulator c-di-GMP phosphodiesterase, RpfG family, contains REC and HD-GYP domains
COG3439	S	Uncharacterized conserved protein, DUF302 family
COG3440	V	Predicted restriction endonuclease
COG3442	R	Glutamine amidotransferase related to the GATase domain of CobQ
COG3443	P	Periplasmic Zn/Cd-binding protein ZinT
COG3444	G	Phosphotransferase system, mannose/fructose/N-acetylgalactosamine-specific component IIB
COG3445	H	Autonomous glycyl radical cofactor GrcA
COG3447	T	Integral membrane sensor domain MASE1
COG3448	T	CBS-domain-containing membrane protein
COG3449	L	DNA gyrase inhibitor GyrI
COG3450	R	Predicted enzyme of the cupin superfamily
COG3451	U	Type IV secretory pathway, VirB4 component
COG3452	T	Extracellular (periplasmic) sensor domain CHASE (specificity unknown)
COG3453	R	Predicted phosphohydrolase, protein tyrosine phosphatase (PTP) superfamily, DUF442 family
COG3454	P	Alpha-D-ribose 1-methylphosphonate 5-triphosphate diphosphatase PhnM
COG3455	U	Type VI protein secretion system component VasF
COG3456	TU	Predicted component of the type VI protein secretion system, contains a FHA domain
COG3457	E	Predicted amino acid racemase
COG3458	Q	Cephalosporin-C deacetylase or related acetyl esterase
COG3459	G	Cellobiose phosphorylase
COG3460	Q	1,2-phenylacetyl-CoA epoxidase, PaaB subunit
COG3461	S	Uncharacterized protein
COG3462	S	Uncharacterized membrane protein
COG3463	S	Uncharacterized membrane protein
COG3464	X	Transposase
COG3465	S	Uncharacterized protein YwgA
COG3466	X	Putative transposon-encoded protein
COG3467	V	Nitroimidazol reductase NimA or a related FMN-containing flavoprotein, pyridoxamine 5'-phosphate oxidase superfamily
COG3468	MU	Type V secretory pathway, adhesin AidA
COG3469	G	Chitinase
COG3470	MI	Uncharacterized protein probably involved in high-affinity Fe2+ transport
COG3471	S	Predicted secreted (periplasmic) protein
COG3472	S	Uncharacterized protein
COG3473	Q	Maleate cis-trans isomerase
COG3474	C	Cytochrome c2
COG3475	I	Phosphorylcholine metabolism protein LicD
COG3476	T	Tryptophan-rich sensory protein (mitochondrial benzodiazepine receptor homolog)
COG3477	S	Uncharacterized membrane protein YagU, involved in acid resistance, DUF1440 family
COG3478	R	Predicted nucleic-acid-binding protein, contains Zn-ribbon domain
COG3479	Q	Phenolic acid decarboxylase
COG3480	T	Predicted secreted protein containing a PDZ domain
COG3481	J	3'-5' exoribonuclease YhaM, can participate in 23S rRNA maturation,  HD superfamily
COG3482	S	Uncharacterized protein
COG3483	E	Tryptophan 2,3-dioxygenase (vermilion)
COG3484	O	Predicted proteasome-type protease
COG3485	Q	Protocatechuate 3,4-dioxygenase beta subunit
COG3486	Q	Lysine/ornithine N-monooxygenase
COG3487	S	Uncharacterized iron-regulated protein
COG3488	R	Uncharacterized conserved protein with two CxxC motifs, DUF1111 family
COG3489	S	Predicted periplasmic lipoprotein
COG3490	S	Uncharacterized protein
COG3491	Q	Isopenicillin N synthase and related dioxygenases
COG3492	S	Uncharacterized protein
COG3493	C	Na+/citrate or Na+/malate symporter
COG3494	S	Uncharacterized conserved protein, DUF1009 family
COG3495	S	Uncharacterized protein
COG3496	S	Uncharacterized conserved protein, DUF1365 family
COG3497	X	Phage tail sheath protein FI
COG3498	X	Phage tail tube protein FII
COG3499	X	Phage protein U
COG3500	X	Phage protein D
COG3501	UXR	Uncharacterized conserved protein, implicated in type VI secretion and phage assembly
COG3502	S	Uncharacterized conserved protein, DUF952 family
COG3503	S	Uncharacterized membrane protein
COG3504	U	Type IV secretory pathway, VirB9 components
COG3505	U	Type IV secretory pathway, VirD4 component, TraG/TraD family ATPase
COG3506	S	Regulation of enolase protein 1 (function unknown), concanavalin A-like superfamily
COG3507	G	Beta-xylosidase
COG3508	Q	Homogentisate 1,2-dioxygenase
COG3509	Q	Poly(3-hydroxybutyrate) depolymerase
COG3510	V	Cephalosporin hydroxylase
COG3511	M	Phospholipase C
COG3512	V	CRISPR/Cas system-associated protein Cas2, endoribonuclease
COG3513	V	CRISPR/Cas system Type II  associated protein, contains McrA/HNH and RuvC-like nuclease domains
COG3514	S	Uncharacterized conserved protein, DUF4415 family
COG3515	U	Predicted component of the type VI protein secretion system
COG3516	U	Predicted component of the type VI protein secretion system
COG3517	U	Predicted component of the type VI protein secretion system
COG3518	U	Predicted component of the type VI protein secretion system
COG3519	U	Type VI protein secretion system component VasA
COG3520	U	Predicted component of the type VI protein secretion system
COG3521	U	Predicted component of the type VI protein secretion system
COG3522	U	Predicted component of the type VI protein secretion system
COG3523	U	Type VI protein secretion system component VasK
COG3524	M	Capsule polysaccharide export protein KpsE/RkpR
COG3525	G	N-acetyl-beta-hexosaminidase
COG3526	S	Predicted selenoprotein, Rdx family
COG3527	Q	Alpha-acetolactate decarboxylase
COG3528	S	Uncharacterized protein
COG3529	R	Predicted nucleic-acid-binding protein, contains Zn-ribbon domain
COG3530	S	Uncharacterized conserved protein, DUF3820 family
COG3531	O	Predicted protein-disulfide isomerase , contains CxxC motif
COG3533	S	Uncharacterized conserved protein, DUF1680 family
COG3534	G	Alpha-L-arabinofuranosidase
COG3535	S	Uncharacterized conserved protein, DUF917 family
COG3536	S	Uncharacterized conserved protein, DUF971 family
COG3537	G	Putative alpha-1,2-mannosidase
COG3538	S	Meiotically up-regulated gene 157 (Mug157) protein (function unknown)
COG3539	N	Pilin (type 1 fimbria component protein)
COG3540	P	Phosphodiesterase/alkaline phosphatase D
COG3541	R	Predicted nucleotidyltransferase
COG3542	R	Predicted sugar epimerase, cupin superfamily
COG3543	S	Uncharacterized protein
COG3544	S	Uncharacterized conserved protein, DUF305 family
COG3545	R	Predicted esterase of the alpha/beta hydrolase fold
COG3546	P	Mn-containing catalase (includes spore coat protein CotJC)
COG3547	X	Transposase
COG3548	S	Uncharacterized membrane protein
COG3549	V	Plasmid maintenance system killer protein
COG3550	T	Serine/threonine protein kinase HipA, toxin component of the HipAB toxin-antitoxin module
COG3551	S	Uncharacterized protein
COG3552	S	Uncharacterized conserved protein, contains von Willebrand factor type A (vWA) domain
COG3553	S	Uncharacterized protein
COG3554	S	Uncharacterized protein
COG3555	O	Aspartyl/asparaginyl beta-hydroxylase, cupin superfamily
COG3556	S	Uncharacterized membrane protein
COG3557	S	Uncharacterized domain/protein associated with RNAses G and E
COG3558	S	Uncharacterized conserved protein, nuclear transport factor 2 (NTF2) superfamily
COG3559	U	Putative exporter of polyketide antibiotics
COG3560	R	Fatty acid repression mutant protein (predicted oxidoreductase)
COG3561	X	Phage anti-repressor protein
COG3562	M	Capsule polysaccharide modification protein KpsS
COG3563	M	Capsule polysaccharide export protein KpsC/LpsZ
COG3564	S	Uncharacterized conserved protein, DUF779 family
COG3565	R	Predicted dioxygenase of extradiol dioxygenase family
COG3566	S	Uncharacterized protein
COG3567	S	Uncharacterized protein
COG3568	R	Metal-dependent hydrolase, endonuclease/exonuclease/phosphatase family
COG3569	L	DNA topoisomerase IB
COG3570	V	Streptomycin 6-kinase
COG3571	R	Predicted hydrolase of the alpha/beta-hydrolase fold
COG3572	H	Gamma-glutamylcysteine synthetase
COG3573	R	Predicted oxidoreductase
COG3575	S	Uncharacterized protein
COG3576	R	Predicted flavin-nucleotide-binding protein, pyridoxine 5'-phosphate oxidase superfamily
COG3577	R	Predicted aspartyl protease
COG3579	E	Aminopeptidase C
COG3580	R	Predicted nucleotide-binding protein, sugar kinase/HSP70/actin superfamily
COG3581	R	Predicted nucleotide-binding protein, sugar kinase/HSP70/actin superfamily
COG3582	R	Predicted nucleic acid binding protein containing the AN1-type Zn-finger
COG3583	S	Uncharacterized conserved protein YabE, contains G5 and tandem DUF348 domains
COG3584	S	3D (Asp-Asp-Asp) domain
COG3585	H	Molybdopterin-binding protein
COG3586	S	Predicted transport protein
COG3587	V	Restriction endonuclease
COG3588	G	Fructose-bisphosphate aldolase class 1
COG3589	S	Uncharacterized protein
COG3590	O	Predicted metalloendopeptidase
COG3591	E	V8-like Glu-specific endopeptidase
COG3592	S	Uncharacterized Fe-S cluster protein YjdI
COG3593	L	Predicted ATP-dependent endonuclease of the OLD family, contains P-loop ATPase and TOPRIM domains
COG3594	G	Fucose 4-O-acetylase or related acetyltransferase
COG3595	S	Uncharacterized conserved protein YvlB, contains  DUF4097 and DUF4098 domains
COG3596	R	Predicted GTPase
COG3597	S	Uncharacterized conserved protein, DUF697 family
COG3598	L	RecA-family ATPase
COG3599	D	Cell division septum initiation DivIVA, interacts with FtsZ, MinD and other proteins
COG3600	X	Uncharacterized phage-associated protein
COG3601	H	Riboflavin transporter FmnP
COG3602	S	Uncharacterized protein
COG3603	S	Uncharacterized protein
COG3604	KT	Transcriptional regulator containing GAF, AAA-type ATPase, and DNA-binding Fis domains
COG3605	T	Signal transduction protein containing GAF and PtsI domains
COG3607	R	Predicted lactoylglutathione lyase
COG3608	R	Predicted deacylase
COG3609	K	Transcriptional regulator, contains Arc/MetJ-type RHH (ribbon-helix-helix) DNA-binding domain
COG3610	S	Uncharacterized membrane protein YjjB, DUF3815 family
COG3611	L	Replication initiation and membrane attachment protein DnaB
COG3612	S	Uncharacterized protein
COG3613	F	Nucleoside 2-deoxyribosyltransferase
COG3614	T	Extracellular (periplasmic) sensor domain CHASE1 (specificity unknown)
COG3615	S	Uncharacterized protein/domain, possibly involved in tellurite resistance
COG3616	E	D-serine deaminase, pyridoxal phosphate-dependent
COG3617	X	Prophage antirepressor
COG3618	R	Predicted metal-dependent hydrolase, TIM-barrel fold
COG3619	S	Uncharacterized membrane protein YoaK, UPF0700 family
COG3620	K	Predicted transcriptional regulator with C-terminal CBS domains
COG3621	R	Patatin-like phospholipase/acyl hydrolase
COG3622	G	Hydroxypyruvate isomerase
COG3623	G	L-ribulose-5-phosphate 3-epimerase UlaE
COG3624	P	Alpha-D-ribose 1-methylphosphonate 5-triphosphate synthase subunit PhnG
COG3625	P	Alpha-D-ribose 1-methylphosphonate 5-triphosphate synthase subunit PhnH
COG3626	P	Alpha-D-ribose 1-methylphosphonate 5-triphosphate synthase subunit PhnI
COG3627	P	Alpha-D-ribose 1-methylphosphonate 5-phosphate C-P lyase
COG3628	X	Phage baseplate assembly protein W
COG3629	T	DNA-binding transcriptional activator of the SARP family
COG3630	C	Na+-transporting methylmalonyl-CoA/oxaloacetate decarboxylase, gamma subunit
COG3631	R	Ketosteroid isomerase-related protein
COG3633	E	Na+/serine symporter
COG3634	V	Alkyl hydroperoxide reductase subunit AhpF
COG3635	G	2,3-bisphosphoglycerate-independent phosphoglycerate mutase, archeal type
COG3636	X	DNA-binding prophage protein
COG3637	M	Opacity protein and related surface antigens
COG3638	P	ABC-type phosphate/phosphonate transport system, ATPase component
COG3639	P	ABC-type phosphate/phosphonate transport system, permease component
COG3640	O	CO dehydrogenase nickel-insertion accessory protein CooC1
COG3641	S	Uncharacterized membrane protein (does not regulate perfringolysin O expression)
COG3642	J	tRNA A-37 threonylcarbamoyl transferase component Bud32
COG3643	E	Glutamate formiminotransferase
COG3644	S	Uncharacterized protein
COG3645	X	Phage antirepressor protein YoqD, KilAC domain
COG3646	X	Phage regulatory protein Rha
COG3647	S	Uncharacterized membrane protein YjdF
COG3648	Q	Uricase (urate oxidase)
COG3649	V	CRISPR/Cas system type I-B associated protein Csh2, Cas7 group, RAMP superfamily
COG3650	S	Uncharacterized membrane protein
COG3651	S	Uncharacterized conserved protein, DUF2237 family
COG3652	S	Predicted outer membrane protein
COG3653	Q	N-acyl-D-aspartate/D-glutamate deacylase
COG3654	X	Prophage maintenance system killer protein
COG3655	K	DNA-binding transcriptional regulator, XRE family
COG3656	S	Predicted periplasmic protein
COG3657	V	Putative component of the toxin-antitoxin plasmid stabilization module
COG3658	C	Cytochrome b
COG3659	M	Carbohydrate-selective porin OprB
COG3660	D	Mitochondrial fission protein ELM1
COG3661	G	Alpha-glucuronidase
COG3662	S	Uncharacterized conserved protein, DUF2236 family
COG3663	L	G:T/U-mismatch repair DNA glycosylase
COG3664	G	Beta-xylosidase
COG3665	S	Uncharacterized conserved protein YcgI, DUF1989 family
COG3666	X	Transposase
COG3667	P	Uncharacterized protein involved in copper resistance
COG3668	X	Plasmid stabilization system protein ParE
COG3669	G	Alpha-L-fucosidase
COG3670	Q	Carotenoid cleavage dioxygenase or a related enzyme
COG3671	S	Uncharacterized membrane protein
COG3672	O	Predicted transglutaminase-like cysteine proteinase
COG3673	S	Uncharacterized protein, PA2063/DUF2235 family
COG3675	I	Predicted lipase
COG3676	X	Transposase and inactivated derivatives
COG3677	X	Transposase
COG3678	O	Periplasmic protein refolding chaperone Spy/CpxP family
COG3679	T	Cell fate regulator YlbF, YheA/YmcA/DUF963 family (controls sporulation, competence, biofilm development)
COG3680	S	Uncharacterized protein
COG3681	E	L-cysteine desulfidase
COG3682	K	Predicted transcriptional regulator
COG3683	R	ABC-type uncharacterized transport system, periplasmic component
COG3684	G	Tagatose-1,6-bisphosphate aldolase
COG3685	P	Ferritin-like metal-binding protein YciE
COG3686	S	Uncharacterized conserved protein, MAPEG superfamily
COG3687	R	Predicted metal-dependent hydrolase
COG3688	R	Predicted RNA-binding protein containing a PIN domain
COG3689	S	Uncharacterized membrane protein YcgQ,  UPF0703/DUF1980 family
COG3691	S	Uncharacterized conserved protein YfcZ, UPF0381/DUF406 family
COG3692	S	Uncharacterized protein YifN, PemK superfamily
COG3693	G	Endo-1,4-beta-xylanase, GH35 family
COG3694	R	ABC-type uncharacterized transport system, permease component
COG3695	K	Alkylated DNA nucleotide flippase Atl1, participates in nucleotide excision repair, Ada-like DNA-binding domain
COG3696	P	Cu/Ag efflux pump CusA
COG3697	HI	Phosphoribosyl-dephospho-CoA transferase (holo-ACP synthetase)
COG3698	S	Uncharacterized protein YigE, DUF2233 family
COG3700	PR	Acid phosphatase (class B)
COG3701	U	Type IV secretory pathway, TrbF components
COG3702	U	Type IV secretory pathway, VirB3 components
COG3703	P	Cation transport regulator ChaC
COG3704	U	Type IV secretory pathway, VirB6 components
COG3705	E	ATP phosphoribosyltransferase regulatory subunit HisZ
COG3706	TK	Two-component response regulator, PleD family, consists of two REC domains and a diguanylate cyclase (GGDEF) domain
COG3707	TK	Two-component response regulator, AmiR/NasT family, consists of REC and RNA-binding antiterminator (ANTAR) domains
COG3708	K	Predicted transcriptional regulator YdeE, contains AraC-type DNA-binding domain
COG3709	G	Ribose 1,5-bisphosphokinase PhnN
COG3710	K	DNA-binding winged helix-turn-helix (wHTH) domain
COG3711	K	Transcriptional antiterminator
COG3712	PT	Periplasmic ferric-dicitrate binding protein FerR, regulates iron transport through sigma-19
COG3713	M	Outer membrane scaffolding protein for murein synthesis, MipA/OmpV family
COG3714	S	Uncharacterized membrane protein YhhN
COG3715	G	Phosphotransferase system, mannose/fructose/N-acetylgalactosamine-specific component IIC
COG3716	G	Phosphotransferase system, mannose/fructose/N-acetylgalactosamine-specific component IID
COG3717	G	5-keto 4-deoxyuronate isomerase
COG3718	G	5-deoxy-D-glucuronate isomerase
COG3719	J	Ribonuclease I
COG3720	P	Putative heme degradation protein
COG3721	P	Putative heme iron utilization protein
COG3722	K	DNA-binding transcriptional regulator, MltR family
COG3723	L	Recombinational DNA repair protein RecT
COG3724	E	Succinylarginine dihydrolase
COG3725	V	Membrane protein required for beta-lactamase induction
COG3726	S	Uncharacterized membrane protein affecting hemolysin expression
COG3727	L	G:T-mismatch repair DNA endonuclease, very short patch repair protein
COG3728	X	Phage terminase, small subunit
COG3729	R	General stress protein YciG, contains tandem KGG domains
COG3730	G	Phosphotransferase system sorbitol-specific component IIC
COG3731	G	Phosphotransferase system sorbitol-specific component IIA
COG3732	G	Phosphotransferase system sorbitol-specific component IIBC
COG3733	Q	Cu2+-containing amine oxidase
COG3734	G	2-keto-3-deoxy-galactonokinase
COG3735	S	Uncharacterized conserved protein YbaP, TraB family
COG3736	U	Type IV secretory pathway, component VirB8
COG3737	S	Uncharacterized conserved protein, contains Mth938-like domain
COG3738	S	Uncharacterized protein YijF, DUF1287 family
COG3739	S	Uncharacterized membrane protein YoaT, DUF817 family
COG3740	X	Phage head maturation protease
COG3741	E	N-formylglutamate amidohydrolase
COG3742	S	Uncharacterized protein, contains PIN domain
COG3743	L	 Predicted 5' DNA nuclease, flap endonuclease-1-like, helix-3-turn-helix (H3TH) domain
COG3744	V	PIN domain nuclease, a component of toxin-antitoxin system (PIN domain)
COG3745	UW	Flp pilus assembly protein CpaB
COG3746	P	Phosphate-selective porin
COG3747	X	Phage terminase, small subunit
COG3748	S	Uncharacterized membrane protein
COG3749	S	Uncharacterized conserved protein, DUF934 family
COG3750	S	Uncharacterized conserved protein, UPF0335 family
COG3751	JO	Proline 4-hydroxylase (includes Rps23 Pro-64 3,4-dihydroxylase Tpa1), contains SM-20 domain
COG3752	R	Steroid 5-alpha reductase family enzyme
COG3753	S	Uncharacterized conserved protein YidB, DUF937 family
COG3754	M	Lipopolysaccharide biosynthesis protein
COG3755	S	Uncharacterized conserved protein YecT, DUF1311 family
COG3756	S	Uncharacterized conserved protein YdaU, DUF1376 family
COG3757	M	Lyzozyme M1 (1,4-beta-N-acetylmuramidase), GH25 family
COG3758	T	Various environmental stresses-induced protein Ves (function unknown)
COG3759	S	Uncharacterized membrane protein
COG3760	S	Uncharacterized protein
COG3761	C	NADH:ubiquinone oxidoreductase 17.2 kD subunit
COG3762	S	Uncharacterized membrane protein
COG3763	S	Uncharacterized protein YneF, UPF0154 family
COG3764	M	Sortase (surface protein transpeptidase)
COG3765	M	LPS O-antigen chain length determinant protein, WzzB/FepE family
COG3766	S	Uncharacterized membrane protein YjfL, UPF0719 family
COG3767	S	Uncharacterized low-complexity protein
COG3768	S	Uncharacterized membrane protein YcjF, UPF0283 family
COG3769	G	Predicted mannosyl-3-phosphoglycerate phosphatase, HAD superfamily
COG3770	M	Murein endopeptidase
COG3771	S	Uncharacterized membrane protein YciS, DUF1049 family
COG3772	M	Phage-related lysozyme (muramidase), GH24 family
COG3773	DM	Cell wall hydrolase CwlJ, involved in spore germination
COG3774	M	Mannosyltransferase OCH1 or related enzyme
COG3775	G	Phosphotransferase system, galactitol-specific IIC component
COG3776	S	Uncharacterized conserved protein YhhL, DUF1145 family
COG3777	I	Hydroxyacyl-ACP dehydratase HTD2, hotdog domain
COG3778	X	Uncharacterized protein YmfQ in lambdoid prophage, DUF2313 family
COG3779	S	Uncharacterized conserved protein YegJ, DUF2314 family
COG3780	L	DNA endonuclease related to intein-encoded endonucleases
COG3781	P	Predicted membrane chloride channel, bestrophin family
COG3782	S	Uncharacterized protein
COG3783	C	Soluble cytochrome b562
COG3784	S	Uncharacterized conserved protein YdbL, DUF1318 family
COG3785	O	Heat shock protein HspQ
COG3786	M	L,D-peptidoglycan transpeptidase YkuD, ErfK/YbiS/YcfS/YnhG family
COG3787	S	Uncharacterized conserved protein YhbP, UPF0306 family
COG3788	S	Uncharacterized membrane protein YecN, MAPEG domain
COG3789	S	Uncharacterized protein YjfI, DUF2170 family
COG3790	S	Predicted membrane protein, encoded in cydAB operon
COG3791	S	Uncharacterized conserved protein
COG3792	S	Uncharacterized protein
COG3793	P	Tellurite resistance protein
COG3794	C	Plastocyanin
COG3795	S	Uncharacterized conserved protein
COG3797	S	Uncharacterized conserved protein, DUF1697 family
COG3798	S	Uncharacterized protein
COG3799	E	Methylaspartate ammonia-lyase
COG3800	R	Predicted transcriptional regulator
COG3801	S	Uncharacterized protein
COG3802	S	Uncharacterized protein
COG3803	S	Uncharacterized conserved protein, DUF924 family
COG3804	S	Uncharacterized protein
COG3805	Q	Aromatic ring-cleaving dioxygenase
COG3806	T	Anti-sigma factor ChrR, cupin superfamily
COG3807	S	SH3-like domain
COG3808	C	Na+ or H+-translocating membrane pyrophosphatase
COG3809	R	Predicted nucleic acid-binding protein, contains Zn-finger domain
COG3811	S	Uncharacterized protein YjhX, UPF0386 family
COG3812	S	Uncharacterized protein
COG3813	S	Uncharacterized protein
COG3814	S	Uncharacterized protein
COG3815	S	Uncharacterized membrane protein
COG3816	S	Uncharacterized protein
COG3817	S	Uncharacterized membrane protein
COG3818	R	Predicted acetyltransferase, GNAT superfamily
COG3819	S	Uncharacterized membrane protein
COG3820	S	Uncharacterized protein
COG3821	S	Uncharacterized membrane protein
COG3822	G	D-lyxose ketol-isomerase
COG3823	O	Glutamine cyclotransferase
COG3824	O	Predicted Zn-dependent protease, minimal metalloprotease (MMP)-like domain
COG3825	S	Uncharacterized conserved protein,  contains von Willebrand factor type A (vWA) domain
COG3826	S	Uncharacterized protein
COG3827	D	Cell pole-organizing protein PopZ
COG3828	R	Type 1 glutamine amidotransferase (GATase1)-like domain
COG3829	KT	Transcriptional regulator containing PAS, AAA-type ATPase, and DNA-binding Fis domains
COG3830	T	ACT domain, binds amino acids and other small ligands
COG3831	K	WGR domain, predicted DNA-binding domain in MolR
COG3832	S	Uncharacterized conserved protein YndB, AHSA1/START domain
COG3833	G	ABC-type maltose transport system, permease component
COG3835	KT	Sugar diacid utilization regulator
COG3836	G	2-keto-3-deoxy-L-rhamnonate aldolase RhmA
COG3837	S	Uncharacterized conserved protein, cupin superfamily
COG3838	U	Type IV secretory pathway, VirB2 components (pilins)
COG3839	G	ABC-type sugar transport system, ATPase component
COG3840	H	ABC-type thiamine transport system, ATPase component
COG3842	E	ABC-type Fe3+/spermidine/putrescine transport systems, ATPase components
COG3843	U	Type IV secretory pathway, VirD2 components (relaxase)
COG3844	E	Kynureninase
COG3845	R	ABC-type uncharacterized transport system, ATPase component
COG3846	U	Type IV secretory pathway, TrbL components
COG3847	UW	Flp pilus assembly protein, pilin Flp
COG3848	T	Phosphohistidine swiveling domain of PEP-utilizing enzymes
COG3850	T	Signal transduction histidine kinase, nitrate/nitrite-specific
COG3851	T	Signal transduction histidine kinase, glucose-6-phosphate specific
COG3852	T	Signal transduction histidine kinase, nitrogen specific
COG3853	V	Uncharacterized conserved protein YaaN involved in tellurite resistance
COG3854	D	Stage III sporulation protein SpoIIIAA
COG3855	G	Fructose-1,6-bisphosphatase
COG3856	S	Small basic protein (function unknown)
COG3857	L	ATP-dependent helicase/DNAse subunit B
COG3858	D	Spore germination protein YaaH
COG3859	H	Thiamine transporter ThiT
COG3860	S	Uncharacterized protein
COG3861	S	Stress response protein YsnF (function unknown)
COG3862	S	Uncharacterized protein with two CxxC motifs
COG3863	S	Uncharacterized protein YycO
COG3864	R	Predicted metal-dependent peptidase
COG3865	R	Glyoxalase superfamily enzyme, possibly 3-demethylubiquinone-9 3-methyltransferase
COG3866	G	Pectate lyase
COG3867	G	Arabinogalactan endo-1,4-beta-galactosidase
COG3868	S	Uncharacterized protein
COG3869	O	Protein-arginine kinase
COG3870	S	Uncharacterized protein YaaQ
COG3871	S	General stress protein 26 (function unknown)
COG3872	S	Uncharacterized conserved protein YqhQ
COG3874	S	Uncharacterized spore protein YtfJ
COG3875	M	Nickel-dependent lactate racemase
COG3876	S	Uncharacterized conserved protein YbbC, DUF1343 family
COG3877	S	Uncharacterized protein
COG3878	S	Uncharacterized protein YwqG
COG3879	S	Uncharacterized conserved protein YlxW, UPF0749 family
COG3880	O	Protein-arginine kinase activator protein McsA
COG3881	S	Uncharacterized protein YrrD, contains PRC-barrel domain
COG3882	I	Predicted enzyme involved in methoxymalonyl-ACP biosynthesis
COG3883	S	Uncharacterized N-terminal domain of peptidoglycan hydrolase CwlO
COG3884	I	Acyl-ACP thioesterase
COG3885	Q	Aromatic ring-opening dioxygenase, LigB subunit
COG3886	L	HKD family nuclease
COG3887	T	c-di-AMP phosphodiesterase, consists of a GGDEF-like and DHH domains
COG3888	K	Predicted transcriptional regulator
COG3889	S	Predicted periplasmic protein
COG3890	I	Phosphomevalonate kinase
COG3892	G	Myo-inositol catabolism protein IolC
COG3893	L	Inactivated superfamily I helicase
COG3894	S	Uncharacterized 2Fe-2 and 4Fe-4S clusters-containing protein, contains DUF4445 domain
COG3895	M	Membrane-bound inhibitor of C-type lysozyme
COG3896	V	Chloramphenicol 3-O-phosphotransferase
COG3897	R	Predicted nicotinamide N-methyase
COG3898	S	Uncharacterized membrane-anchored protein
COG3899	R	Predicted ATPase
COG3900	S	Predicted periplasmic protein
COG3901	K	Regulator of nitric oxide reductase transcription
COG3903	R	Predicted ATPase
COG3904	S	Predicted periplasmic protein
COG3905	K	Predicted transcriptional regulator
COG3906	S	Uncharacterized protein YrzB, UPF0473 family
COG3907	R	Membrane-associated enzyme, PAP2 (acid phosphatase) superfamily
COG3908	S	Uncharacterized protein
COG3909	C	Cytochrome c556
COG3910	R	Predicted ATPase
COG3911	R	Predicted ATPase
COG3913	S	Uncharacterized protein
COG3914	O	Predicted O-linked N-acetylglucosamine transferase, SPINDLY family
COG3915	S	Uncharacterized protein
COG3916	T	N-acyl-L-homoserine lactone synthetase
COG3917	Q	2-hydroxychromene-2-carboxylate isomerase
COG3918	S	Uncharacterized membrane protein
COG3919	R	Predicted ATP-dependent carboligase, ATP-grasp superfamily
COG3920	T	Two-component sensor histidine kinase, HisKA and HATPase domains
COG3921	S	Uncharacterized conserved protein
COG3923	L	Primosomal replication protein N''
COG3924	S	Uncharacterized membrane protein YhdT
COG3925	GT	N-terminal domain of the phosphotransferase system fructose-specific component IIB
COG3926	R	Lysozyme family protein
COG3930	S	Uncharacterized protein
COG3931	E	Predicted N-formylglutamate amidohydrolase
COG3932	S	Uncharacterized conserved protein
COG3933	K	Transcriptional regulatory protein LevR, contains PRD, AAA+ and EIIA domains
COG3934	G	Endo-1,4-beta-mannosidase
COG3935	L	DNA replication protein DnaD
COG3936	G	Membrane-bound acyltransferase YfiQ, involved in biofilm formation
COG3937	QT	Polyhydroxyalkanoate synthesis regulator phasin
COG3938	E	Proline racemase
COG3940	G	Beta-xylosidase, GH43 family
COG3941	X	Phage tail tape-measure protein, controls tail length
COG3942	M	Surface antigen
COG3943	S	Uncharacterized conserved protein
COG3944	M	Capsular polysaccharide biosynthesis protein
COG3945	R	Hemerythrin-like domain
COG3946	U	Type IV secretory pathway, VirJ component
COG3947	TK	Two-component response regulator, SAPR family, consists of REC, wHTH and BTAD domains
COG3948	X	Phage-related baseplate assembly protein
COG3949	S	Uncharacterized membrane protein YkvI
COG3950	R	Predicted ATP-binding protein involved in virulence
COG3951	N	Rod binding protein domain
COG3952	R	Uncharacterized N-terminal domain of lipid-A-disaccharide synthase
COG3953	X	SLT domain protein
COG3954	G	Phosphoribulokinase
COG3955	M	Uncharacterized protein, DUF1919 family
COG3956	R	Uncharacterized conserved protein YabN, contains tetrapyrrole methylase and MazG-like pyrophosphatase domain
COG3957	G	Phosphoketolase
COG3958	G	Transketolase, C-terminal subunit
COG3959	G	Transketolase, N-terminal subunit
COG3960	Q	Glyoxylate carboligase
COG3961	GHR	TPP-dependent 2-oxoacid decarboxylase, includes indolepyruvate decarboxylase
COG3962	G	TPP-dependent trihydroxycyclohexane-1,2-dione (THcHDO) dehydratase, myo-inositol metabolism
COG3963	I	Phospholipid N-methyltransferase
COG3964	R	Predicted amidohydrolase
COG3965	P	Predicted Co/Zn/Cd cation transporter, cation efflux family
COG3966	M	Poly D-alanine transfer protein DltD, involved inesterification of teichoic acids
COG3967	MI	Short-chain dehydrogenase involved in D-alanine esterification of teichoic acids
COG3968	E	Glutamine synthetase type III
COG3969	R	Predicted phosphoadenosine phosphosulfate sulfurtransferase, contains C-terminal DUF3440 domain
COG3970	R	Fumarylacetoacetate (FAA) hydrolase family protein
COG3971	Q	2-keto-4-pentenoate hydratase
COG3972	L	Superfamily I DNA and RNA helicases
COG3973	L	DNA helicase IV
COG3975	R	Predicted metalloprotease, contains C-terminal PDZ domain
COG3976	R	Uncharacterized protein, contains FMN-binding domain
COG3977	E	Alanine-alpha-ketoisovalerate (or valine-pyruvate) aminotransferase
COG3978	C	Acetolactate synthase small subunit, contains ACT domain
COG3979	G	Chitodextrinase
COG3980	M	Spore coat polysaccharide biosynthesis protein SpsG, predicted glycosyltransferase
COG3981	R	Predicted acetyltransferase
COG4001	S	Uncharacterized protein
COG4002	R	Predicted methyltransferase MtxX, methanogen marker protein 4
COG4003	S	Uncharacterized protein
COG4004	S	Uncharacterized protein
COG4006	V	CRISPR/Cas system-associated protein Csm6, COG1517 family
COG4007	R	Predicted dehydrogenase related to H2-forming N5,N10-methylenetetrahydromethanopterin dehydrogenase
COG4008	K	Predicted metal-binding transcription factor, methanogenesis marker domain 9
COG4009	S	Uncharacterized protein
COG4010	S	Uncharacterized protein
COG4012	S	Uncharacterized protein, DUF1786 family
COG4013	S	Uncharacterized protein
COG4014	S	Uncharacterized protein
COG4015	R	Predicted dinucleotide-utilizing enzyme of the ThiF/HesA family
COG4016	S	Uncharacterized protein, UPF0254 family
COG4017	S	Uncharacterized protein
COG4018	S	Uncharacterized protein
COG4019	S	Uncharacterized protein
COG4020	S	Uncharacterized protein
COG4021	J	tRNA(His) 5'-end guanylyltransferase
COG4022	S	Uncharacterized protein
COG4023	U	Preprotein translocase subunit Sec61beta
COG4024	S	Uncharacterized protein
COG4025	S	Uncharacterized membrane protein
COG4026	R	Uncharacterized protein, contains TOPRIM domain, potential nuclease
COG4027	F	3'-phosphoadenosine 5'-phosphosulfate sulfotransferase
COG4028	R	Predicted P-loop ATPase/GTPase
COG4029	S	Uncharacterized protein
COG4030	R	Predicted phosphohydrolase, HAD superfamily
COG4031	S	Uncharacterized protein
COG4032	H	Sulfopyruvate decarboxylase, TPP-binding subunit (coenzyme M biosynthesis)
COG4033	S	Uncharacterized protein
COG4034	S	Uncharacterized protein
COG4035	S	Uncharacterized membrane protein
COG4036	C	Energy-converting hydrogenase Eha subunit G
COG4037	C	Energy-converting hydrogenase Eha subunit F
COG4038	C	Energy-converting hydrogenase Eha subunit E
COG4039	C	Energy-converting hydrogenase Eha subunit C
COG4040	S	Uncharacterized membrane protein
COG4041	C	Energy-converting hydrogenase Eha subunit B
COG4042	C	Energy-converting hydrogenase Eha subunit A
COG4043	R	ASC-1 homology (ASCH) domain, predicted RNA-binding domain
COG4044	S	Uncharacterized protein
COG4046	S	Uncharacterized protein
COG4047	L	N-glycosylase/DNA lyase
COG4048	S	Uncharacterized protein
COG4049	R	Uncharacterized protein, contains archaeal-type C2H2 Zn-finger
COG4050	S	Uncharacterized protein
COG4051	S	Uncharacterized protein
COG4052	R	Uncharacterized protein related to methyl coenzyme M reductase subunit C, methanogenesis marker protein 7
COG4053	S	Uncharacterized protein
COG4054	H	Methyl coenzyme M reductase, beta subunit
COG4055	H	Methyl coenzyme M reductase, subunit D
COG4056	H	Methyl coenzyme M reductase, subunit C
COG4057	H	Methyl coenzyme M reductase, gamma subunit
COG4058	H	Methyl coenzyme M reductase, alpha subunit
COG4059	H	Tetrahydromethanopterin S-methyltransferase, subunit E
COG4060	H	Tetrahydromethanopterin S-methyltransferase, subunit D
COG4061	H	Tetrahydromethanopterin S-methyltransferase, subunit C
COG4062	H	Tetrahydromethanopterin S-methyltransferase, subunit B
COG4063	H	Tetrahydromethanopterin S-methyltransferase, subunit A
COG4064	H	Tetrahydromethanopterin S-methyltransferase, subunit G
COG4065	S	Uncharacterized protein
COG4066	S	Uncharacterized protein, UPF0305 family
COG4067	S	Uncharacterized conserved protein
COG4068	R	Predicted nucleic acid-binding protein, contains Zn-ribbon domain
COG4069	S	Uncharacterized protein
COG4070	S	Uncharacterized protein, methanogenesis marker protein 3, UPF0288 family
COG4071	S	Uncharacterized protein, related to F420-0:gamma-glutamyl ligase
COG4072	S	Uncharacterized protein
COG4073	S	Uncharacterized protein
COG4074	C	5,10-methenyltetrahydromethanopterin hydrogenase
COG4075	S	Uncharacterized protein, distantly related to nitrogen regulatory protein PII
COG4076	R	Predicted RNA methylase
COG4077	S	Uncharacterized protein
COG4078	C	Energy-converting hydrogenase Eha subunit H
COG4079	S	Uncharacterized protein
COG4080	J	SpoU rRNA Methylase family enzyme
COG4081	S	Uncharacterized protein
COG4083	L	Exosortase/Archaeosortase
COG4084	CO	Energy-converting hydrogenase A subunit M
COG4085	A	DNA/RNA endonuclease YhcR, contains UshA esterase domain
COG4086	S	Uncharacterized protein YpuA, DUF1002 family
COG4087	R	Soluble P-type ATPase
COG4088	J	tRNA Uridine 5-carbamoylmethylation protein Kti12 (Killer toxin insensitivity protein)
COG4089	S	Uncharacterized membrane protein
COG4090	S	Uncharacterized protein
COG4091	E	Predicted homoserine dehydrogenase, contains C-terminal SAF domain
COG4092	M	Predicted glycosyltransferase involved in capsule biosynthesis
COG4093	S	Uncharacterized protein
COG4094	S	Uncharacterized membrane protein
COG4095	S	Uncharacterized conserved protein, contains PQ loop repeat
COG4096	V	Type I site-specific restriction endonuclease, part of a restriction-modification system
COG4097	P	Predicted ferric reductase
COG4098	L	Superfamily II DNA/RNA helicase required for DNA uptake (late competence protein)
COG4099	R	Predicted peptidase
COG4100	PR	Cystathionine beta-lyase family protein involved in aluminum resistance
COG4101	R	Uncharacterized protein, RmlC-like cupin domain
COG4102	S	Uncharacterized conserved protein, DUF1501 family
COG4103	S	Uncharacterized conserved protein, tellurite resistance protein B (TerB) family
COG4104	U	Zn-binding Pro-Ala-Ala-Arg (PAAR) domain, incolved in TypeVI secretion
COG4105	M	Outer membrane protein assembly factor BamD, BamD/ComL family
COG4106	C	Trans-aconitate methyltransferase
COG4107	P	ABC-type phosphonate transport system, ATPase component
COG4108	J	Peptide chain release factor RF-3
COG4109	K	Predicted transcriptional regulator containing CBS domains
COG4110	V	Uncharacterized protein involved in tellurium resistance
COG4111	S	Uncharacterized conserved protein
COG4112	R	Predicted phosphoesterase, NUDIX family
COG4113	R	Predicted nucleic acid-binding protein, contains PIN domain
COG4114	P	Ferric iron reductase protein FhuF, involved in iron transport
COG4115	V	Toxin component of the Txe-Axe toxin-antitoxin module, Txe/YoeB family
COG4116	S	Uncharacterized protein YjbK
COG4117	P	Thiosulfate reductase cytochrome b subunit
COG4118	V	Antitoxin component of toxin-antitoxin stability system, DNA-binding transcriptional repressor
COG4119	FR	Predicted NTP pyrophosphohydrolase, NUDIX family
COG4120	R	ABC-type uncharacterized transport system, permease component
COG4121	J	tRNA U34 5-methylaminomethyl-2-thiouridine-forming methyltransferase MnmC
COG4122	R	Predicted O-methyltransferase YrrM
COG4123	J	tRNA1(Val) A37 N6-methylase TrmN6
COG4124	G	Beta-mannanase
COG4125	S	Uncharacterized membrane protein
COG4126	E	Asp/Glu/hydantoin racemase
COG4127	R	Predicted restriction endonuclease, Mrr-cat superfamily
COG4128	R	Zona occludens toxin, predicted ATPase
COG4129	S	Uncharacterized membrane protein YgaE, UPF0421/DUF939 family
COG4130	G	Predicted sugar epimerase, xylose isomerase-like family
COG4132	R	ABC-type uncharacterized transport system, permease component
COG4133	O	ABC-type transport system involved in cytochrome c biogenesis, ATPase component
COG4134	R	ABC-type uncharacterized transport system YnjBCD, periplasmic component
COG4135	R	ABC-type uncharacterized transport system YnjBCD, permease component
COG4136	R	ABC-type uncharacterized transport system YnjBCD, ATPase component
COG4137	R	ABC-type uncharacterized transport system, permease component
COG4138	H	ABC-type cobalamin transport system, ATPase component
COG4139	H	ABC-type cobalamin transport system, permease component
COG4143	H	ABC-type thiamine transport system, periplasmic component
COG4145	H	Na+/panthothenate symporter
COG4146	R	Uncharacterized membrane permease YidK, sodium:solute symporter family
COG4147	C	Na+(or H+)/acetate symporter ActP
COG4148	P	ABC-type molybdate transport system, ATPase component
COG4149	P	ABC-type molybdate transport system, permease component
COG4150	P	ABC-type sulfate transport system, periplasmic component
COG4152	R	ABC-type uncharacterized transport system, ATPase component
COG4154	G	L-fucose mutarotase/ribose pyranase, RbsD/FucU family
COG4158	R	Predicted ABC-type sugar transport system, permease component
COG4160	E	ABC-type arginine/histidine transport system, permease component
COG4161	E	ABC-type arginine transport system, ATPase component
COG4166	E	ABC-type oligopeptide transport system, periplasmic component
COG4167	V	ABC-type antimicrobial peptide transport system, ATPase component
COG4168	V	ABC-type antimicrobial peptide transport system, permease component
COG4170	V	ABC-type antimicrobial peptide transport system, ATPase component
COG4171	V	ABC-type antimicrobial peptide transport system, permease component
COG4172	Q	ABC-type microcin C transport system, duplicated ATPase component YejF
COG4174	Q	ABC-type microcin C transport system, permease component YejB
COG4175	E	ABC-type proline/glycine betaine transport system, ATPase component
COG4176	E	ABC-type proline/glycine betaine transport system, permease component
COG4177	E	ABC-type branched-chain amino acid transport system, permease component
COG4178	R	ABC-type uncharacterized transport system, permease and ATPase components
COG4181	Q	Predicted ABC-type transport system involved in lysophospholipase L1 biosynthesis, ATPase component
COG4185	R	Predicted ABC-type ATPase
COG4186	R	Calcineurin-like phosphoesterase superfamily protein
COG4187	E	Arginine utilization protein RocB
COG4188	R	Predicted dienelactone hydrolase
COG4189	K	Predicted transcriptional regulator
COG4190	K	Predicted transcriptional regulator
COG4191	T	Signal transduction histidine kinase regulating C4-dicarboxylate transport system
COG4192	T	Signal transduction histidine kinase regulating phosphoglycerate transport system
COG4193	G	Beta- N-acetylglucosaminidase
COG4194	S	Uncharacterized membrane protein
COG4195	X	Phage-related replication protein YjqB, UPF0714/DUF867 family
COG4196	S	Uncharacterized conserved protein, DUF2126 family
COG4197	K	DNA-binding transcriptional regulator YdaS, prophage-encoded, Cro superfamily
COG4198	S	Uncharacterized conserved protein, DUF1015 family
COG4199	L	ssDNA-specific exonuclease RecJ
COG4200	S	Uncharacterized protein
COG4206	H	Outer membrane cobalamin receptor protein
COG4208	P	ABC-type sulfate transport system, permease component
COG4209	G	ABC-type polysaccharide transport system, permease component
COG4211	G	ABC-type glucose/galactose transport system, permease component
COG4213	G	ABC-type xylose transport system, periplasmic component
COG4214	G	ABC-type xylose transport system, permease component
COG4215	E	ABC-type arginine transport system, permease component
COG4218	H	Tetrahydromethanopterin S-methyltransferase, subunit F
COG4219	T	Signal transducer regulating beta-lactamase production, contains  metallopeptidase domain
COG4220	X	Phage DNA packaging protein, Nu1 subunit of terminase
COG4221	C	NADP-dependent 3-hydroxy acid dehydrogenase YdfG
COG4222	S	Uncharacterized conserved protein
COG4223	S	Uncharacterized conserved protein
COG4224	S	Uncharacterized protein YnzC, UPF0291/DUF896 family
COG4225	G	Rhamnogalacturonyl hydrolase YesR
COG4226	R	Predicted nuclease of the RNAse H fold, HicB family
COG4227	L	Antirestriction protein ArdC
COG4228	X	Mu-like prophage DNA circulation protein
COG4229	E	Enolase-phosphatase E1 involved in merthionine salvage
COG4230	E	Delta 1-pyrroline-5-carboxylate dehydrogenase
COG4231	C	TPP-dependent indolepyruvate ferredoxin oxidoreductase, alpha subunit
COG4232	O	Thiol:disulfide interchange protein
COG4233	OC	Thiol-disulfide interchange protein, contains DsbC and DsbD domains
COG4235	CO	Cytochrome c-type biogenesis protein CcmH/NrfG
COG4237	C	Hydrogenase-4 membrane subunit HyfE
COG4238	M	Outer membrane murein-binding lipoprotein Lpp
COG4239	Q	ABC-type microcin C transport system, permease component YejE
COG4240	R	Pantothenate kinase-related protein Tda10 (topoisomerase I damage affected protein)
COG4241	S	Uncharacterized conserved protein YybS, DUF2232 family
COG4242	QR	Cyanophycinase and related exopeptidases
COG4243	S	Uncharacterized membrane protein
COG4244	S	Uncharacterized membrane protein
COG4245	S	Uncharacterized conserved protein YegL, contains vWA domain of TerY type
COG4246	S	Uncharacterized protein
COG4247	I	3-phytase (myo-inositol-hexaphosphate 3-phosphohydrolase)
COG4248	R	Uncharacterized protein with protein kinase and helix-hairpin-helix DNA-binding domains
COG4249	R	Uncharacterized protein, contains caspase domain
COG4250	T	Sensory domain  found in diguanylate cyclases and two-component systems (DICT domain)
COG4251	T	Bacteriophytochrome (light-regulated signal transduction histidine kinase)
COG4252	T	Extracellular (periplasmic) sensor domain CHASE2 (specificity unknown)
COG4253	S	Uncharacterized conserved protein, DUF2345 family
COG4254	R	Uncharacterized conserved protein, contains LysM and FecR  domains
COG4255	S	Uncharacterized protein
COG4256	H	Hemin uptake protein HemP
COG4257	V	Streptogramin lyase
COG4258	R	Predicted exporter
COG4259	S	Uncharacterized protein
COG4260	O	Membrane protease subunit, stomatin/prohibitin family, contains C-terminal Zn-ribbon domain
COG4261	R	Predicted acyltransferase, LPLAT superfamily
COG4262	R	Predicted spermidine synthase with an N-terminal membrane domain
COG4263	P	Nitrous oxide reductase
COG4264	P	Siderophore synthetase component
COG4266	F	Allantoicase
COG4267	S	Uncharacterized membrane protein
COG4268	V	5-methylcytosine-specific restriction endonuclease McrBC, regulatory subunit McrC
COG4269	S	Uncharacterized membrane protein YjgN, DUF898 family
COG4270	S	Uncharacterized membrane protein
COG4271	R	Predicted nucleotide-binding protein containing TIR -like domain
COG4272	S	Uncharacterized membrane protein
COG4273	S	Uncharacterized protein, contains metal-binding DGC domain
COG4274	S	Uncharacterized protein, contains GYD domain
COG4275	S	Uncharacterized protein
COG4276	R	Ligand-binding SRPBCC domain
COG4277	R	Predicted DNA-binding protein with the Helix-hairpin-helix motif
COG4278	S	Uncharacterized protein
COG4279	S	Uncharacterized conserved protein, contains Zn finger domain
COG4280	S	Uncharacterized membrane protein
COG4281	I	Acyl-CoA-binding protein
COG4282	M	Cell wall assembly regulator SMI1
COG4283	S	Uncharacterized protein
COG4284	G	UDP-N-acetylglucosamine pyrophosphorylase
COG4285	R	Uncharacterized conserved protein , conains N-terminal glutamine amidotransferase (GATase1)-like domain
COG4286	S	Uncharacterized protein, UPF0160 family
COG4287	R	PhoPQ-activated pathogenicity-related protein
COG4288	S	Uncharacterized protein
COG4289	S	Uncharacterized protein
COG4290	F	Guanyl-specific ribonuclease Sa
COG4291	S	Uncharacterized membrane protein
COG4292	S	Low temperature requirement protein LtrA (function unknown)
COG4293	S	Uncharacterized protein
COG4294	L	UV DNA damage repair endonuclease
COG4295	S	Uncharacterized protein
COG4296	S	Uncharacterized protein
COG4297	S	Uncharacterized protein YjlB
COG4298	S	Uncharacterized protein
COG4299	R	Predicted acyltransferase
COG4300	P	Cadmium resistance protein CadD, predicted permease
COG4301	R	Uncharacterized conserved protein, contains predicted SAM-dependent methyltransferase domain
COG4302	E	Ethanolamine ammonia-lyase, small subunit
COG4303	E	Ethanolamine ammonia-lyase, large subunit
COG4304	S	Uncharacterized protein
COG4305	M	Peptidoglycan-binding domain, expansin
COG4306	S	Uncharacterized protein
COG4307	S	Uncharacterized protein
COG4308	Q	Limonene-1,2-epoxide hydrolase
COG4309	S	Uncharacterized conserved protein, DUF2249 family
COG4310	R	Uncharacterized protein, cotains an aminopeptidase-like domain
COG4311	E	Sarcosine oxidase delta subunit
COG4312	R	Predicted dithiol-disulfide oxidoreductase, DUF899 family
COG4313	S	Uncharacterized conserved protein
COG4314	P	Nitrous oxide reductase accessory protein NosL
COG4315	S	Predicted lipoprotein with conserved Yx(FWY)xxD motif (function unknown)
COG4316	S	Uncharacterized protein
COG4317	F	Xanthosine utilization system component, XapX domain
COG4318	S	Uncharacterized protein
COG4319	R	Ketosteroid isomerase homolog
COG4320	S	Uncharacterized conserved protein, DUF2252 family
COG4321	R	Predicted DNA-binding protein, contains Ribbon-helix-helix (RHH) domain
COG4322	S	Uncharacterized protein
COG4323	S	Uncharacterized protein
COG4324	R	Predicted aminopeptidase
COG4325	S	Uncharacterized membrane protein
COG4326	D	Sporulation-control protein spo0M
COG4327	S	Uncharacterized membrane protein
COG4328	R	Predicted nuclease (RNAse H fold)
COG4329	S	Uncharacterized membrane protein
COG4330	S	Uncharacterized membrane protein
COG4331	S	Uncharacterized membrane protein
COG4332	S	Uncharacterized protein
COG4333	S	Uncharacterized protein
COG4334	S	Uncharacterized protein
COG4335	L	3-methyladenine DNA glycosylase AlkC
COG4336	S	Uncharacterized protein YcsI, UPF0317 family
COG4337	S	Uncharacterized protein
COG4338	S	Uncharacterized protein
COG4339	R	Predicted metal-dependent phosphohydrolase, HD superfamily
COG4340	S	Uncharacterized protein
COG4341	R	Predicted HD phosphohydrolase
COG4342	X	Intergrase/Recombinase
COG4343	V	CRISPR/Cas system-associated exonuclease Cas4, RecB family
COG4344	K	Predicted transciptional regulator, contains HTH domain
COG4345	S	Uncharacterized protein
COG4346	O	Predicted membrane-bound dolichyl-phosphate-mannose-protein mannosyltransferase
COG4347	S	Uncharacterized membrane protein YpjA
COG4352	J	Ribosomal protein L13E
COG4353	S	Uncharacterized protein
COG4354	S	Uncharacterized protein, contains GBA2_N and DUF608 domains
COG4357	S	Uncharacterized protein, contains Zn-finger domain of CHY type
COG4359	E	2-hydroxy-3-keto-5-methylthiopentenyl-1-phosphate phosphatase (methionine salvage)
COG4360	F	ATP adenylyltransferase (5',5'''-P-1,P-4-tetraphosphate phosphorylase II)
COG4362	P	Nitric oxide synthase, oxygenase domain
COG4365	S	Uncharacterized protein YllA, UPF0747 family
COG4367	S	Uncharacterized protein
COG4370	S	Uncharacterized protein
COG4371	S	Uncharacterized membrane protein
COG4372	S	Uncharacterized conserved protein, contains DUF3084 domain
COG4373	X	Mu-like prophage FluMu protein gp28
COG4374	V	PIN domain nuclease, a component of toxin-antitoxin system (PIN domain)
COG4377	S	Uncharacterized membrane protein YhfC
COG4378	S	Uncharacterized protein
COG4379	X	Mu-like prophage tail protein gpP
COG4380	S	Uncharacterized protein
COG4381	X	Mu-like prophage protein gp46
COG4382	X	Mu-like prophage protein gp16
COG4383	X	Mu-like prophage protein gp29
COG4384	X	Mu-like prophage protein gp45
COG4385	X	Bacteriophage P2-related tail formation protein
COG4386	X	Mu-like prophage tail sheath protein gpL
COG4387	X	Mu-like prophage protein gp36
COG4388	X	Mu-like prophage I protein
COG4389	L	Site-specific recombinase
COG4390	S	Uncharacterized protein
COG4391	S	Uncharacterized conserved protein, contains Zn-finger domain
COG4392	E	Branched-chain amino acid transport protein
COG4393	S	Uncharacterized membrane protein
COG4394	S	Uncharacterized protein
COG4395	I	Predicted lipid-binding transport protein, Tim44 family
COG4396	X	Mu-like prophage host-nuclease inhibitor protein Gam
COG4397	X	Mu-like prophage major head subunit gpT
COG4398	T	Small ligand-binding sensory domain FIST
COG4399	S	Uncharacterized membrane protein YheB, UPF0754 family
COG4401	E	Chorismate mutase
COG4402	S	Uncharacterized protein
COG4403	V	Lantibiotic modifying enzyme
COG4405	S	Uncharacterized protein YhfF
COG4408	S	Uncharacterized protein
COG4409	GM	Neuraminidase (sialidase)
COG4412	O	Bacillopeptidase F, M6 metalloprotease family
COG4413	E	Urea transporter
COG4416	X	Mu-like prophage FluMu protein Com
COG4420	S	Uncharacterized membrane protein
COG4421	M	Capsular polysaccharide biosynthesis protein
COG4422	X	Bacteriophage protein gp37
COG4423	S	Uncharacterized protein
COG4424	M	LPS sulfotransferase NodH
COG4425	S	Uncharacterized membrane protein
COG4427	S	Uncharacterized protein
COG4430	S	Uncharacterized conserved protein YdeI, YjbR/CyaY-like superfamily, DUF1801 family
COG4443	S	Uncharacterized protein
COG4445	J	tRNA isopentenyl-2-thiomethyl-A-37 hydroxylase MiaE (synthesis of 2-methylthio-cis-ribozeatin)
COG4446	S	Uncharacterized conserved protein, DUF1499 family
COG4447	R	Uncharacterized protein related to plant photosystem II stability/assembly factor
COG4448	E	L-asparaginase II
COG4449	R	Predicted protease, Abi (CAAX) family
COG4451	G	Ribulose bisphosphate carboxylase small subunit
COG4452	V	Inner membrane protein involved in colicin E2 resistance
COG4453	S	Uncharacterized conserved protein, DUF1778 family
COG4454	R	Uncharacterized copper-binding protein, cupredoxin-like subfamily
COG4455	R	Protein of avirulence locus involved in temperature-dependent protein secretion
COG4456	S	Virulence-associated protein VagC (function unknown)
COG4457	S	Uncharacterized protein
COG4458	S	Uncharacterized protein
COG4459	C	Periplasmic nitrate reductase system, NapE component
COG4460	S	Uncharacterized protein
COG4461	S	Uncharacterized protein YPO0702
COG4463	K	Transcriptional regulator CtsR
COG4464	T	Tyrosine-protein phosphatase YwqE
COG4465	K	GTP-sensing pleiotropic transcriptional regulator CodY
COG4466	S	Uncharacterized protein Veg
COG4467	L	Regulator of replication initiation timing
COG4468	G	Galactose-1-phosphate uridylyltransferase
COG4469	R	Competence protein CoiA-like family, contains a predicted nuclease domain
COG4470	S	Uncharacterized protein YutD
COG4471	S	Uncharacterized protein YlbG, UPF0298 family
COG4472	S	Uncharacterized protein, UPF0297 family
COG4473	U	Predicted ABC-type exoprotein transport system, permease component
COG4474	X	Uncharacterized SPBc2 prophage-derived protein YoqJ
COG4475	S	Uncharacterized protein YwlG, UPF0340 family
COG4476	S	Uncharacterized protein YktA, UPF0223 family
COG4477	D	Septation ring formation regulator EzrA
COG4478	S	Uncharacterized membrane protein
COG4479	S	Uncharacterized protein YozE, UPF0346 family
COG4481	S	Uncharacterized protein
COG4483	S	Uncharacterized protein YqgQ
COG4485	S	Uncharacterized membrane protein YfhO
COG4487	S	Uncharacterized protein
COG4492	R	ACT domain-containing protein
COG4493	S	Uncharacterized protein YktB, UPF0637 family
COG4495	S	Uncharacterized protein
COG4496	S	Uncharacterized protein YerC
COG4499	S	Uncharacterized membrane protein YukC
COG4502	F	5'(3')-deoxyribonucleotidase
COG4506	S	Uncharacterized beta-barrel protein YwiB, DUF1934 family
COG4508	F	Dimeric dUTPase, all-alpha-NTP-PPase (MazG) superfamily
COG4509	S	Uncharacterized protein
COG4512	KT	Accessory gene regulator protein AgrB
COG4517	S	Uncharacterized protein
COG4518	X	Mu-like prophage FluMu protein gp41
COG4519	S	Uncharacterized protein
COG4520	M	Surface antigen
COG4521	P	ABC-type taurine transport system, periplasmic component
COG4525	P	ABC-type taurine transport system, ATPase component
COG4529	R	Uncharacterized NAD(P)/FAD-binding protein YdhS
COG4530	S	Uncharacterized protein
COG4531	P	ABC-type Zn2+ transport system, periplasmic component/surface adhesin
COG4533	K	DNA-binding transcriptional regulator SgrR  of sgrS sRNA, contains a MarR-type HTH domain and a periplasmic-type solute-binding domain
COG4535	P	Mg2+ and Co2+ transporter CorC, contains CBS pair and CorC-HlyC domains
COG4536	P	Mg2+ and Co2+ transporter CorB, contains DUF21, CBS pair, and CorC-HlyC domains
COG4537	X	Competence protein ComGC
COG4538	S	Uncharacterized protein
COG4539	S	Uncharacterized membrane protein YGL010W
COG4540	X	Phage P2 baseplate assembly protein gpV
COG4541	S	Uncharacterized membrane protein
COG4542	Q	Protein involved in propanediol utilization, and related proteins (includes coumermycin biosynthetic...
COG4544	S	Uncharacterized conserved protein
COG4545	O	Glutaredoxin-related protein
COG4547	H	Cobalamin biosynthesis protein CobT (nicotinate-mononucleotide:5, 6-dimethylbenzimidazole phosphorib...
COG4548	P	Nitric oxide reductase activation protein
COG4549	S	Uncharacterized protein YcnI
COG4550	T	Cell fate regulator YmcA, YheA/YmcA/DUF963 family (controls sporulation, competence, biofilm development)
COG4551	R	Predicted protein tyrosine phosphatase
COG4552	R	Predicted acetyltransferase
COG4553	I	Poly-beta-hydroxyalkanoate depolymerase
COG4555	CP	ABC-type Na+ transport system, ATPase component NatA
COG4558	P	ABC-type hemin transport system, periplasmic component
COG4559	P	ABC-type hemin transport system, ATPase component
COG4564	T	Signal transduction histidine kinase
COG4565	KT	Response regulator of citrate/malate metabolism
COG4566	TK	Two-component response regulator, FixJ family, consists of REC and HTH domains
COG4567	TK	Two-component response regulator, ActR/RegA family, consists of REC and Fis-type HTH domains
COG4568	K	Transcriptional antiterminator Rof (Rho-off)
COG4569	Q	Acetaldehyde dehydrogenase (acetylating)
COG4570	L	Holliday junction resolvase RusA (prophage-encoded endonuclease)
COG4571	M	Outer membrane protease
COG4572	P	Cation transport regulator ChaB
COG4573	G	Tagatose-1,6-bisphosphate aldolase non-catalytic subunit AgaZ/GatZ
COG4574	O	Serine protease inhibitor ecotin
COG4575	J	Membrane-anchored ribosome-binding protein, inhibits growth in stationary phase, ElaB/YqjD/DUF883 family
COG4576	QC	Carboxysome shell and ethanolamine utilization microcompartment protein CcmK/EutM
COG4577	QC	Carboxysome shell and ethanolamine utilization microcompartment protein CcmL/EutN
COG4578	K	DNA-binding transcriptional regulator of glucitol operon
COG4579	T	Isocitrate dehydrogenase kinase/phosphatase
COG4580	G	Maltoporin (phage lambda and maltose receptor)
COG4581	L	Superfamily II RNA helicase
COG4582	D	Cell division protein ZapD, interacts with FtsZ
COG4583	E	Sarcosine oxidase gamma subunit
COG4584	X	Transposase
COG4585	T	Signal transduction histidine kinase
COG4586	R	ABC-type uncharacterized transport system, ATPase component
COG4587	R	ABC-type uncharacterized transport system, permease component
COG4588	M	Accessory colonization factor AcfC, contains ABC-type periplasmic domain
COG4589	R	Predicted CDP-diglyceride synthetase/phosphatidate cytidylyltransferase
COG4590	R	ABC-type uncharacterized transport system, permease component
COG4591	M	ABC-type transport system, involved in lipoprotein release, permease component
COG4592	P	ABC-type Fe2+-enterobactin transport system, periplasmic component
COG4594	P	ABC-type Fe3+-citrate transport system, periplasmic component
COG4597	E	ABC-type amino acid transport system, permease component
COG4598	E	ABC-type histidine transport system, ATPase component
COG4603	R	ABC-type uncharacterized transport system, permease component
COG4604	P	ABC-type enterochelin transport system, ATPase component
COG4605	P	ABC-type enterochelin transport system, permease component
COG4606	P	ABC-type enterochelin transport system, permease component
COG4607	P	ABC-type enterochelin transport system, periplasmic component
COG4608	E	ABC-type oligopeptide transport system, ATPase component
COG4615	P	ABC-type siderophore export system, fused ATPase and permease components
COG4618	U	ABC-type protease/lipase transport system, ATPase and permease components
COG4619	P	ABC-type iron transport system FetAB, ATPase component
COG4623	MT	Membrane-bound lytic murein transglycosylase MltF
COG4624	C	Iron only hydrogenase large subunit, C-terminal domain
COG4625	S	Uncharacterized conserved protein, contains a C-terminal beta-barrel porin domain
COG4626	X	Phage terminase-like protein, large subunit, contains N-terminal HTH domain
COG4627	R	Predicted SAM-depedendent methyltransferase
COG4628	S	Uncharacterized conserved protein, DUF2132 family
COG4630	F	Xanthine dehydrogenase, iron-sulfur cluster and FAD-binding subunit A
COG4631	F	Xanthine dehydrogenase, molybdopterin-binding subunit B
COG4632	G	Exopolysaccharide biosynthesis protein related to N-acetylglucosamine-1-phosphodiester alpha-N-acety...
COG4633	R	Plastocyanin domain containing protein
COG4634	R	Predicted nuclease, contains PIN domain, potential toxin-antitoxin system component
COG4635	H	Protoporphyrinogen IX oxidase, menaquinone-dependent (flavodoxin domain)
COG4636	R	Endonuclease, Uma2 family (restriction endonuclease fold)
COG4637	R	Predicted ATPase
COG4638	PR	Phenylpropionate dioxygenase or related ring-hydroxylating dioxygenase, large terminal subunit
COG4639	R	Predicted kinase
COG4640	S	Uncharacterized membrane protein YvbJ
COG4641	D	Spore maturation protein CgeB
COG4642	S	Uncharacterized conserved protein
COG4643	X	Uncharacterized domain associated with phage/plasmid primase
COG4644	X	Transposase and inactivated derivatives, TnpA family
COG4645	S	Uncharacterized protein
COG4646	L	Adenine-specific DNA methylase, N12 class
COG4647	Q	Acetone carboxylase, gamma subunit
COG4648	S	Uncharacterized membrane protein
COG4649	S	Uncharacterized protein
COG4650	KT	Sigma54-dependent transcription regulator containing an AAA-type ATPase domain and a DNA-binding domain
COG4651	P	Predicted Kef-type K+ transport protein, K+/H+ antiporter domain
COG4652	S	Uncharacterized protein
COG4653	X	Predicted phage phi-C31 gp36 major capsid-like protein
COG4654	C	Cytochrome c551/c552
COG4655	S	Uncharacterized membrane protein
COG4656	C	Na+-translocating ferredoxin:NAD+ oxidoreductase  RNF, RnfC subunit
COG4657	C	Na+-translocating ferredoxin:NAD+ oxidoreductase RNF, RnfA subunit
COG4658	C	Na+-translocating ferredoxin:NAD+ oxidoreductase  RNF, RnfD subunit
COG4659	C	Na+-translocating ferredoxin:NAD+ oxidoreductase RNF, RnfG subunit
COG4660	C	Na+-translocating ferredoxin:NAD+ oxidoreductase  RNF, RnfE subunit
COG4662	P	ABC-type tungstate transport system, periplasmic component
COG4663	Q	TRAP-type mannitol/chloroaromatic compound transport system, periplasmic component
COG4664	Q	TRAP-type mannitol/chloroaromatic compound transport system, large permease component
COG4665	Q	TRAP-type mannitol/chloroaromatic compound transport system, small permease component
COG4666	R	TRAP-type uncharacterized transport system, fused permease components
COG4667	I	Predicted phospholipase, patatin/cPLA2 family
COG4668	G	Mannitol/fructose-specific phosphotransferase system, IIA domain
COG4669	U	Type III secretory pathway, lipoprotein EscJ
COG4670	I	Acyl CoA:acetate/3-ketoacid CoA transferase
COG4671	R	Predicted glycosyl transferase
COG4672	X	Phage-related protein
COG4674	R	ABC-type uncharacterized transport system, ATPase component
COG4675	S	Microcystin-dependent protein  (function unknown)
COG4676	S	Uncharacterized conserved protein YfaP, DUF2135 family
COG4677	GI	Pectin methylesterase and related acyl-CoA thioesterases
COG4678	MX	Muramidase (phage lambda lysozyme)
COG4679	X	Phage-related protein
COG4680	J	mRNA-degrading endonuclease (mRNA interferase) HigB, toxic component of the HigAB toxin-antitoxin module
COG4681	S	Uncharacterized conserved protein YaeQ, suppresses RfaH defect
COG4682	S	Uncharacterized membrane protein YiaA
COG4683	S	Uncharacterized protein
COG4684	S	Uncharacterized membrane protein
COG4685	S	Uncharacterized conserved protein YfaA, DUF2138 family
COG4687	S	Uncharacterized protein
COG4688	S	Uncharacterized protein
COG4689	Q	Acetoacetate decarboxylase
COG4690	E	Dipeptidase
COG4691	V	Plasmid stability protein
COG4692	GM	Predicted neuraminidase (sialidase)
COG4693	P	Oxidoreductase (NAD-binding), involved in siderophore biosynthesis
COG4694	J	Wobble nucleotide-excising tRNase
COG4695	X	Phage portal protein BeeE
COG4696	R	Predicted phosphohydrolase, Cof family, HAD superfamily
COG4697	S	Uncharacterized protein
COG4698	S	Uncharacterized protein YpmS
COG4699	S	Uncharacterized protein
COG4700	S	Uncharacterized protein
COG4701	S	Uncharacterized protein
COG4702	S	Uncharacterized protein, UPF0303 family
COG4703	S	Uncharacterized protein YkuJ
COG4704	S	Uncharacterized conserved protein, DUF2141 family
COG4705	S	Uncharacterized membrane-anchored protein
COG4706	I	Predicted 3-hydroxylacyl-ACP dehydratase, HotDog domain
COG4707	X	Prophage pi2 protein 07
COG4708	S	Uncharacterized membrane protein
COG4709	S	Uncharacterized membrane protein
COG4710	R	Predicted DNA-binding protein with an HTH domain
COG4711	S	Uncharacterized membrane protein
COG4712	S	Uncharacterized protein
COG4713	S	Uncharacterized membrane protein
COG4714	S	Uncharacterized membrane-anchored protein
COG4715	S	Uncharacterized conserved protein, contains Zn finger domain
COG4716	S	Myosin-crossreactive antigen  (function unknown)
COG4717	S	Uncharacterized protein YhaN
COG4718	X	Phage-related protein
COG4719	S	Uncharacterized protein
COG4720	S	Uncharacterized membrane protein
COG4721	H	ABC-type thiamine/hydroxymethylpyrimidine transport system, permease component
COG4722	X	Phage-related protein
COG4723	X	Phage-related protein, tail component
COG4724	G	Endo-beta-N-acetylglucosaminidase D
COG4725	J	N6-adenosine-specific RNA methylase IME4
COG4726	NW	Tfp pilus assembly protein PilX
COG4727	S	Uncharacterized protein
COG4728	S	Uncharacterized protein
COG4729	S	Uncharacterized protein
COG4731	S	Uncharacterized conserved protein, DUF2147 family
COG4732	S	Predicted membrane protein
COG4733	X	Phage-related protein, tail component
COG4734	V	Antirestriction protein
COG4735	S	Uncharacterized protein YaaW, UPF0174 family
COG4736	C	Cbb3-type cytochrome oxidase, subunit 3
COG4737	S	Uncharacterized protein
COG4738	K	Predicted transcriptional regulator
COG4739	S	Uncharacterized protein, contains ferredoxin domain
COG4740	R	Predicted metalloprotease
COG4741	F	Predicted secreted endonuclease distantly related to archaeal Holliday junction resolvase
COG4742	K	Predicted transcriptional regulator, contains HTH domain
COG4743	S	Uncharacterized membrane protein
COG4744	S	Uncharacterized protein
COG4745	R	Predicted membrane-bound mannosyltransferase
COG4746	S	Uncharacterized protein
COG4747	S	Uncharacterized conserved protein, contains tandem ACT domains
COG4748	S	Uncharacterized protein
COG4749	S	Uncharacterized protein
COG4750	MI	CTP:phosphocholine cytidylyltransferase involved in choline phosphorylation for cell surface LPS epi...
COG4752	S	Uncharacterized protein
COG4753	TK	Two-component response regulator, YesN/AraC family, consists of REC and AraC-type DNA-binding domains
COG4754	S	Uncharacterized protein
COG4755	S	Uncharacterized protein
COG4756	R	Predicted cation transporter
COG4757	R	Predicted alpha/beta hydrolase
COG4758	S	Predicted membrane protein
COG4759	S	Uncharacterized protein
COG4760	S	Uncharacterized membrane protein, YccA/Bax inhibitor family
COG4762	S	Uncharacterized protein, UPF0548 family
COG4763	S	Uncharacterized membrane protein YcfT
COG4764	S	Uncharacterized protein
COG4765	S	Uncharacterized protein
COG4766	E	Ethanolamine utilization protein EutQ, cupin superfamily (function unknown)
COG4767	V	Glycopeptide antibiotics resistance protein
COG4768	S	Uncharacterized protein YoxC, contains an MCP-like domain
COG4769	S	Uncharacterized membrane protein
COG4770	I	Acetyl/propionyl-CoA carboxylase, alpha subunit
COG4771	P	Outer membrane receptor for ferrienterochelin and colicins
COG4772	P	Outer membrane receptor for Fe3+-dicitrate
COG4773	P	Outer membrane receptor for ferric coprogen and ferric-rhodotorulic acid
COG4774	P	Outer membrane receptor for monomeric catechols
COG4775	M	Outer membrane protein assembly factor BamA
COG4776	K	Exoribonuclease II
COG4778	P	Alpha-D-ribose 1-methylphosphonate 5-triphosphate synthase subunit PhnL
COG4779	P	ABC-type enterobactin transport system, permease component
COG4781	I	Membrane-anchored glycerophosphoryl diester phosphodiesterase (GDPDase), membrane domain
COG4782	R	Esterase/lipase superfamily enzyme
COG4783	R	Putative Zn-dependent protease, contains TPR repeats
COG4784	R	Putative Zn-dependent protease
COG4785	M	Lipoprotein NlpI, contains TPR repeats
COG4786	N	Flagellar basal body rod protein FlgG
COG4787	N	Flagellar basal body rod protein FlgF
COG4789	U	Type III secretory pathway, component EscV
COG4790	U	Type III secretory pathway, component EscR
COG4791	U	Type III secretory pathway, component EscT
COG4792	U	Type III secretory pathway, component EscU
COG4794	U	Type III secretory pathway, component EscS
COG4795	U	Type II secretory pathway, component PulJ
COG4796	U	Type II secretory pathway, component HofQ
COG4797	R	Predicted regulatory domain of a methyltransferase
COG4798	R	Predicted methyltransferase
COG4799	I	Acetyl-CoA carboxylase, carboxyltransferase component
COG4800	K	Predicted transcriptional regulator with an HTH domain
COG4801	R	Predicted acyltransferase, contains DUF342 domain
COG4802	C	Ferredoxin-thioredoxin reductase, catalytic subunit
COG4803	S	Uncharacterized membrane protein
COG4804	R	Predicted nuclease of restriction endonuclease-like (RecB) superfamily,  DUF1016 family
COG4805	S	Uncharacterized conserved protein, DUF885 familyt
COG4806	G	L-rhamnose isomerase
COG4807	S	Uncharacterized conserved protein YehS, DUF1456 family
COG4808	S	Uncharacterized lipoprotein YehR, DUF1307 family
COG4809	G	Archaeal ADP-dependent phosphofructokinase/glucokinase
COG4810	E	Ethanolamine utilization protein EutS, ethanolamine utilization microcompartment shell protein
COG4811	S	Uncharacterized membrane protein YobD, UPF0266 family
COG4812	E	Ethanolamine utilization cobalamin adenosyltransferase
COG4813	G	Trehalose utilization protein
COG4814	S	Uncharacterized protein with an alpha/beta hydrolase fold
COG4815	S	Uncharacterized protein
COG4816	E	Ethanolamine utilization protein EutL, ethanolamine utilization microcompartment shell protein
COG4817	L	DNA-binding ferritin-like protein (Dps family)
COG4818	S	Uncharacterized membrane protein
COG4819	E	Ethanolamine utilization protein EutA, possible chaperonin protecting lyase from inhibition
COG4820	E	Ethanolamine utilization protein EutJ, possible chaperonin
COG4821	R	Uncharacterized protein, contains SIS (Sugar ISomerase) phosphosugar binding domain
COG4822	H	Cobalamin biosynthesis protein CbiK, Co2+ chelatase
COG4823	V	Abortive infection bacteriophage resistance protein
COG4824	X	Phage-related holin (Lysis protein)
COG4825	S	Uncharacterized membrane-anchored protein
COG4826	O	Serine protease inhibitor
COG4827	R	Predicted transporter
COG4828	S	Uncharacterized membrane protein
COG4829	Q	Muconolactone delta-isomerase
COG4830	J	Ribosomal protein S26
COG4831	T	Roadblock/LC7 domain
COG4832	S	Uncharacterized protein
COG4833	G	Predicted alpha-1,6-mannanase, GH76 family
COG4834	S	Uncharacterized protein
COG4835	S	Uncharacterized protein
COG4836	S	Uncharacterized membrane protein YwzB
COG4837	O	Disulfide oxidoreductase YuzD
COG4838	S	Uncharacterized protein YlaN, UPF0358 family
COG4839	D	Cell division protein FtsL
COG4840	S	Uncharacterized protein YfkK, UPF0435 family
COG4841	S	Uncharacterized protein YneR
COG4842	S	Uncharacterized conserved protein YukE
COG4843	S	Uncharacterized protein YebE, UPF0316 family
COG4844	S	Uncharacterized protein YuzB, UPF0349 family
COG4845	V	Chloramphenicol O-acetyltransferase
COG4846	CO	Membrane protein CcdC involved in cytochrome C biogenesis
COG4847	S	Uncharacterized protein
COG4848	S	Uncharacterized protein YtpQ, UPF0354 family
COG4849	R	Predicted nucleotidyltransferase
COG4850	I	Phosphatidate phosphatase APP1
COG4851	R	Protein involved in sex pheromone biosynthesis
COG4852	S	Uncharacterized membrane protein
COG4853	T	Two-component signal transduction system YycFG, regulatory protein YycI
COG4854	S	Uncharacterized membrane protein
COG4855	F	Uncharacterized protein
COG4856	S	Uncharacterized protein, YbbR domain
COG4857	E	5-Methylthioribose kinase, methionine salvage pathway
COG4858	S	Uncharacterized membrane-anchored protein
COG4859	S	Uncharacterized protein
COG4860	K	Predicted DNA-binding transcriptional regulator, ArsR family
COG4861	S	Uncharacterized protein
COG4862	KTN	Negative regulator of genetic competence, sporulation and motility
COG4863	T	Two-component signal transduction system YycFG, regulatory protein YycH
COG4864	S	Uncharacterized protein YqfA, UPF0365 family
COG4865	E	Glutamate mutase epsilon subunit
COG4866	S	Uncharacterized protein
COG4867	S	Uncharacterized protein, contains von Willebrand factor type A (vWA) domain
COG4868	S	Uncharacterized protein, UPF0371 family
COG4869	Q	Propanediol utilization protein
COG4870	O	Cysteine protease, C1A family
COG4871	K	Metal-binding trascriptional regulator, contains putative Fe-S cluster and ArsR family DNA binding domain
COG4872	S	Uncharacterized membrane protein
COG4873	S	Uncharacterized protein YkvS
COG4874	S	Uncharacterized protein
COG4875	S	Uncharacterized protein
COG4876	S	Uncharacterized protein YdaT
COG4877	S	Uncharacterized protein
COG4878	S	Uncharacterized protein
COG4879	S	Uncharacterized protein
COG4880	R	Secreted protein containing C-terminal beta-propeller domain distantly related to WD-40 repeats
COG4881	S	Predicted membrane protein
COG4882	R	Predicted aminopeptidase, Iap family
COG4883	S	Uncharacterized protein
COG4884	S	Uncharacterized conserved protein YfeS, contains WGR domain
COG4885	S	Uncharacterized protein
COG4886	K	Leucine-rich repeat (LRR) protein
COG4887	S	Uncharacterized metal-binding protein conserved in archaea
COG4888	K	Transcription elongation factor Elf1, contains Zn-ribbon domain
COG4889	R	Predicted helicase
COG4890	S	Predicted outer membrane lipoprotein
COG4891	S	Uncharacterized protein
COG4892	R	Predicted heme/steroid binding protein
COG4893	S	Uncharacterized protein
COG4894	S	Uncharacterized protein YxjI
COG4895	S	Uncharacterized protein YwbE
COG4896	S	Uncharacterized protein YlaI
COG4897	S	General stress protein CsbA (function unknown)
COG4898	S	Uncharacterized protein
COG4899	S	Uncharacterized protein
COG4900	R	Predicted metallopeptidase
COG4901	J	Ribosomal protein S25
COG4902	S	Uncharacterized protein
COG4903	K	Competence transcription factor ComK
COG4904	S	Uncharacterized protein
COG4905	S	Uncharacterized membrane protein
COG4906	S	Uncharacterized membrane protein
COG4907	S	Uncharacterized membrane protein
COG4908	R	Uncharacterized protein, contains a NRPS condensation (elongation) domain
COG4909	Q	Propanediol dehydratase, large subunit
COG4910	Q	Propanediol dehydratase, small subunit
COG4911	S	Uncharacterized protein
COG4912	L	3-methyladenine DNA glycosylase AlkD
COG4913	S	Uncharacterized protein YPO0396
COG4914	R	Predicted nucleotidyltransferase
COG4915	QR	5-bromo-4-chloroindolyl phosphate hydrolysis protein
COG4916	S	Uncharacterized protein
COG4917	E	Ethanolamine utilization protein EutP, contains a P-loop NTPase domain
COG4918	S	Uncharacterized protein YqkB
COG4919	J	Ribosomal protein S30
COG4920	S	Uncharacterized membrane protein
COG4921	S	Uncharacterized protein
COG4922	R	Predicted SnoaL-like aldol condensation-catalyzing enzyme
COG4923	R	Predicted nuclease (RNAse H fold)
COG4924	S	Uncharacterized protein
COG4925	S	Uncharacterized protein
COG4926	X	Phage-related protein
COG4927	R	Predicted choloylglycine hydrolase
COG4928	R	Predicted P-loop ATPase, KAP-like
COG4929	S	Uncharacterized membrane-anchored protein
COG4930	O	Predicted ATP-dependent Lon-type protease
COG4932	S	Uncharacterized surface anchored protein
COG4933	K	Predicted transcriptional regulator, contains an HTH and PUA-like domains
COG4934	O	Serine protease, subtilase family
COG4935	O	Regulatory P domain of the subtilisin-like proprotein convertases and other proteases
COG4936	T	Ligand-binding sensor domain
COG4937	J	Ferredoxin-fold anticodon binding domain
COG4938	R	Predicted ATPase
COG4939	S	Major membrane immunogen, membrane-anchored lipoprotein
COG4940	X	Competence protein ComGF
COG4941	K	Predicted RNA polymerase sigma factor, contains C-terminal TPR domain
COG4942	D	Septal ring factor EnvC, activator of murein hydrolases AmiA and AmiB
COG4943	T	Environmental sensor c-di-GMP phosphodiesterase, contains periplasmic CSS-motif sensor and cytoplasmic EAL domain
COG4944	S	Uncharacterized protein
COG4945	GT	Carbohydrate-binding DOMON domain
COG4946	S	Uncharacterized N-terminal domain of tricorn protease
COG4947	R	Esterase/lipase superfamily enzyme
COG4948	MR	L-alanine-DL-glutamate epimerase or related enzyme of enolase superfamily
COG4949	S	Uncharacterized membrane-anchored protein
COG4950	S	N-terminal domain of uncharacterized protein YciW (function unknown)
COG4951	S	Uncharacterized protein
COG4952	M	L-rhamnose isomerase
COG4953	M	Membrane carboxypeptidase/penicillin-binding protein PbpC
COG4954	S	Uncharacterized protein
COG4955	S	Uncharacterized protein YpbB
COG4956	R	Uncharacterized conserved protein YacL, contains PIN and TRAM domains
COG4957	K	Predicted transcriptional regulator
COG4959	OU	Type IV secretory pathway, protease TraF
COG4960	OT	Flp pilus assembly protein, protease CpaA
COG4961	UW	Flp pilus assembly protein TadG
COG4962	UW	Pilus assembly protein, ATPase of CpaF family
COG4963	UW	Flp pilus assembly protein, ATPase CpaE
COG4964	UW	Flp pilus assembly protein, secretin CpaC
COG4965	UW	Flp pilus assembly protein TadB
COG4966	NW	Tfp pilus assembly protein PilW
COG4967	NW	Tfp pilus assembly protein PilV
COG4968	NW	Tfp pilus assembly protein PilE
COG4969	NW	Tfp pilus assembly protein, major pilin PilA
COG4970	NW	Tfp pilus assembly protein FimT
COG4972	NW	Tfp pilus assembly protein, ATPase PilM
COG4973	L	Site-specific recombinase XerC
COG4974	L	Site-specific recombinase XerD
COG4975	G	Glucose uptake protein GlcU
COG4976	R	Predicted methyltransferase, contains TPR repeat
COG4977	K	Transcriptional regulator GlxA family, contains an amidase domain and an AraC-type DNA-binding HTH domain
COG4978	T	Bacterial effector-binding domain
COG4980	R	Gas vesicle protein
COG4981	I	Enoyl reductase domain of yeast-type FAS1
COG4982	I	3-oxoacyl-ACP reductase domain of yeast-type FAS1
COG4983	S	Uncharacterized protein, contains Primase-polymerase (Primpol) domain
COG4984	S	Uncharacterized membrane protein
COG4985	P	ABC-type phosphate transport system, auxiliary component
COG4986	P	ABC-type anion transport system, duplicated permease component
COG4987	CO	ABC-type transport system involved in cytochrome bd biosynthesis, fused ATPase and permease components
COG4988	CO	ABC-type transport system involved in cytochrome bd biosynthesis, ATPase and permease components
COG4989	R	Predicted oxidoreductase
COG4990	S	Uncharacterized protein YvpB
COG4991	S	Uncharacterized conserved protein YraI
COG4992	E	Acetylornithine/succinyldiaminopimelate/putrescine aminotransferase
COG4993	G	Glucose dehydrogenase
COG4994	S	Uncharacterized protein
COG4995	S	Uncharacterized conserved protein, contains CHAT domain
COG4996	R	Predicted phosphatase
COG4997	R	Predicted house-cleaning noncanonical NTP pyrophosphatase, all-alpha NTP-PPase (MazG) superfamily
COG4998	L	Predicted endonuclease, RecB family
COG4999	T	Uncharacterized domain of BarA-like signal transduction histidine kinase
COG5000	T	Signal transduction histidine kinase involved in nitrogen fixation and metabolism regulation
COG5001	T	Predicted signal transduction protein containing a membrane domain, an EAL and a GGDEF domain
COG5002	T	Signal transduction histidine kinase
COG5003	X	Mu-like prophage protein gp37
COG5004	X	P2-like prophage tail protein X
COG5005	X	Mu-like prophage protein gpG
COG5006	E	Threonine/homoserine efflux transporter RhtA
COG5007	T	Acid stress-induced BolA-like protein IbaG/YrbA, predicted regulator of iron metabolism
COG5008	NW	Tfp pilus assembly protein, ATPase PilU
COG5009	M	Membrane carboxypeptidase/penicillin-binding protein
COG5010	UW	Flp pilus assembly protein TadD, contains TPR repeats
COG5011	S	Uncharacterized conserved protein, DUF2344 family
COG5012	C	Methanogenic corrinoid protein MtbC1
COG5013	CP	Nitrate reductase alpha subunit
COG5014	R	Uncharacterized Fe-S cluster-containing protein, radical SAM superfamily
COG5015	S	Uncharacterized protein, pyridoxamine 5'-phosphate oxidase (PNPOx-like) family
COG5016	C	Pyruvate/oxaloacetate carboxyltransferase
COG5017	G	UDP-N-acetylglucosamine transferase subunit ALG13
COG5018	R	Inhibitor of the KinA pathway to sporulation, predicted exonuclease
COG5019	DZ	Septin family protein
COG5022	R	Myosin heavy chain
COG5026	G	Hexokinase
COG5029	OI	Prenyltransferase, beta subunit
COG5031	H	Ubiquinone biosynthesis protein Coq4
COG5032	T	Phosphatidylinositol kinase or protein kinase, PI-3  family
COG5033	K	Transcription initiation factor IIF, auxiliary subunit
COG5036	PU	SPX domain-containing protein involved in vacuolar polyphosphate accumulation
COG5038	R	Ca2+-dependent lipid-binding protein, contains C2 domain
COG5039	GM	Exopolysaccharide biosynthesis protein EpsI, predicted pyruvyl transferase
COG5042	F	Purine nucleoside permease
COG5044	O	RAB proteins geranylgeranyltransferase component A (RAB escort protein)
COG5048	R	FOG: Zn-finger
COG5049	L	5'-3' exonuclease
COG5055	L	Recombination DNA repair protein (RAD52 pathway)
COG5074	U	t-SNARE complex subunit, syntaxin
COG5078	O	Ubiquitin-protein ligase
COG5083	I	Phosphatidate phosphatase PAH1, contains Lipin and LNS2 domains. can be involved in plasmid maintenance
COG5096	U	Vesicle coat complex, various subunits
COG5108	K	Mitochondrial DNA-directed RNA polymerase
COG5119	R	Uncharacterized protein, contains ParB-like nuclease domain
COG5126	T	Ca2+-binding protein, EF-hand superfamily
COG5135	S	Uncharacterized protein
COG5146	H	Pantothenate kinase
COG5153	U	Putative lipase essential for disintegration of autophagic bodies inside the vacuole
COG5160	O	Protease, Ulp1 family
COG5164	K	Transcription elongation factor
COG5180	A	PAB1-binding protein PBP1, interacts with poly(A)-binding protein
COG5183	O	E3 ubiquitin-protein ligase DOA10
COG5184	DZ	Alpha-tubulin suppressor and related RCC1 domain-containing proteins
COG5185	D	Protein involved in chromosome segregation, interacts with SMC proteins
COG5186	A	Poly(A) polymerase Pap1
COG5190	K	TFIIF-interacting CTD phosphatase, includes NLI-interacting factor
COG5206	O	Glycosylphosphatidylinositol transamidase (GPIT), subunit GPI8
COG5207	R	Uncharacterized Zn-finger protein, UBP-type
COG5212	T	cAMP phosphodiesterase
COG5238	TA	Ran GTPase-activating protein (RanGAP) involved in mRNA processing and transport
COG5239	A	mRNA deadenylase, 3'-5' endonuclease subunit Ccr4
COG5244	D	Dynactin complex subunit involved in mitotic spindle partitioning in anaphase B
COG5255	S	Uncharacterized protein
COG5256	J	Translation elongation factor EF-1alpha (GTPase)
COG5257	J	Translation initiation factor 2, gamma subunit (eIF-2gamma; GTPase)
COG5258	R	GTPase
COG5260	L	DNA polymerase sigma
COG5263	G	Glucan-binding domain (YG repeat)
COG5265	O	ABC-type transport system involved in Fe-S cluster assembly, permease and ATPase components
COG5266	R	Uncharacterized conserved protein, contains GH25 family domain
COG5267	S	Uncharacterized conserved protein, DUF1800 family
COG5268	U	Type IV secretory pathway, TrbD component
COG5270	J	PUA domain (predicted RNA-binding domain)
COG5271	J	Midasin, AAA ATPase with  vWA domain, involved in ribosome maturation
COG5272	O	Ubiquitin
COG5274	CI	Cytochrome b involved in lipid metabolism
COG5275	R	BRCT domain type II
COG5276	S	Uncharacterized conserved protein
COG5277	Z	Actin-related protein
COG5278	T	Extracellular (periplasmic) sensor domain CHASE3 (specificity unknown)
COG5279	D	Cytokinesis protein 3, contains TGc (transglutaminase/protease-like) domain
COG5280	X	Phage-related minor tail protein
COG5281	X	Phage-related minor tail protein
COG5282	S	Uncharacterized conserved protein, DUF2342 family
COG5283	X	Phage-related tail protein
COG5285	Q	Ectoine hydroxylase-related dioxygenase, phytanoyl-CoA dioxygenase (PhyH) family
COG5293	S	Uncharacterized protein YydD, contains DUF2326 domain
COG5294	S	Uncharacterized protein YxeA
COG5295	UW	Autotransporter adhesin
COG5297	G	Cellulase/cellobiase CelA1
COG5298	S	Uncharacterized protein YdaL
COG5301	X	Phage-related tail fibre protein
COG5302	X	Post-segregation antitoxin (ccd killing mechanism protein) encoded by the F plasmid
COG5304	K	Predicted DNA binding protein, CopG/RHH family
COG5305	S	Uncharacterized membrane protein
COG5306	S	Uncharacterized protein
COG5307	R	Guanine-nucleotide exchange factor, contains Sec7 domain
COG5309	G	Exo-beta-1,3-glucanase,  GH17 family
COG5310	Q	Homospermidine synthase
COG5314	X	Conjugal transfer/entry exclusion protein
COG5316	S	Uncharacterized protein
COG5317	S	Uncharacterized protein
COG5319	S	Uncharacterized protein
COG5321	S	Uncharacterized protein
COG5322	R	Predicted amino acid dehydrogenase
COG5323	X	Large terminase phage packaging protein
COG5324	J	tRNA splicing ligase
COG5328	S	Uncharacterized protein, UPF0262 family
COG5330	S	Uncharacterized conserved protein, DUF2336 family
COG5331	S	Uncharacterized protein
COG5336	C	FoF1-type ATP synthase assembly protein I
COG5337	M	Spore coat protein CotH
COG5338	S	Uncharacterized protein
COG5339	S	Uncharacterized conserved protein YdgA, DUF945 family
COG5340	V	Transcriptional regulator, predicted component of viral defense system
COG5341	S	Uncharacterized protein
COG5342	R	Invasion protein IalB, involved in pathogenesis
COG5343	T	Anti-sigma-K factor RskA
COG5345	S	Uncharacterized protein
COG5346	S	Uncharacterized membrane protein
COG5349	S	Uncharacterized conserved protein, DUF983 family
COG5350	R	Predicted protein tyrosine phosphatase
COG5351	S	Uncharacterized protein
COG5352	S	Uncharacterized protein
COG5353	S	Uncharacterized protein YpmB
COG5354	R	Uncharacterized protein, contains Trp-Asp (WD) repeat
COG5360	S	Uncharacterized conserved protein, heparinase superfamily
COG5361	X	Uncharacterized conserved protein
COG5362	X	Phage terminase large subunit
COG5368	S	Uncharacterized protein
COG5371	F	Golgi nucleoside diphosphatase
COG5373	S	Uncharacterized membrane protein
COG5375	S	Uncharacterized protein
COG5377	X	Phage-related protein, predicted endonuclease
COG5378	R	Predicted nucleic acid-binding protein, contains PIN domain
COG5379	I	S-adenosylmethionine:diacylglycerol 3-amino-3-carboxypropyl transferase
COG5380	O	Lipase chaperone LimK
COG5381	S	Uncharacterized protein
COG5383	R	Uncharacterized metalloenzyme YdcJ, glyoxalase superfamily
COG5384	J	U3 small nucleolar ribonucleoprotein component
COG5385	S	Uncharacterized protein
COG5386	P	Heme-binding NEAT domain
COG5387	O	Chaperone required for the assembly of the mitochondrial F1-ATPase
COG5388	S	Uncharacterized protein
COG5389	S	Uncharacterized protein
COG5393	S	Uncharacterized membrane protein YqjE
COG5394	QT	Polyhydroxyalkanoate (PHA) synthesis regulator protein, binds DNA and PHA
COG5395	S	Uncharacterized membrane protein
COG5397	S	Uncharacterized protein
COG5398	H	Heme oxygenase
COG5399	S	Uncharacterized protein
COG5400	S	Uncharacterized protein
COG5401	D	Spore germination protein GerM
COG5402	S	Uncharacterized protein
COG5403	S	Uncharacterized protein
COG5404	D	Cell division inhibitor SulA, prevents FtsZ ring assembly
COG5405	O	ATP-dependent protease HslVU (ClpYQ), peptidase subunit
COG5406	KLB	Nucleosome binding factor SPN, SPT16 subunit
COG5407	U	Preprotein translocase subunit Sec63
COG5410	S	Uncharacterized protein
COG5412	X	Phage-related protein
COG5413	S	Uncharacterized integral membrane protein
COG5414	K	TATA-binding protein-associated factor Taf7, part of the TFIID transcription initiation complex
COG5416	S	Uncharacterized integral membrane protein
COG5417	S	Uncharacterized ubiquitin-like protein YukD
COG5418	S	Predicted secreted protein
COG5419	S	Uncharacterized protein
COG5420	S	Uncharacterized protein
COG5421	X	Transposase
COG5423	S	Predicted metal-binding protein
COG5424	H	Pyrroloquinoline quinone (PQQ) biosynthesis protein C
COG5425	S	Usg protein (tryptophan operon, function unknown)
COG5426	S	Uncharacterized membrane protein
COG5427	S	Uncharacterized membrane protein
COG5428	S	Uncharacterized protein YuzE
COG5429	S	Uncharacterized protein
COG5430	S	Spore coat protein U (SCPU) domain, function unknown
COG5431	R	Predicted nucleic acid-binding protein, contains Zn-finger domain
COG5433	X	Predicted transposase YbfD/YdcC associated with H repeats
COG5434	G	Polygalacturonase
COG5435	S	Uncharacterized protein
COG5436	S	Uncharacterized membrane protein
COG5437	S	Predicted secreted protein
COG5438	S	Uncharacterized membrane protein
COG5439	S	Uncharacterized protein
COG5440	S	Uncharacterized protein
COG5441	S	Uncharacterized protein, UPF0261 family
COG5442	N	Flagellar biosynthesis regulator FlaF
COG5443	N	Flagellar biosynthesis regulator FlbT
COG5444	V	Predicted ribonuclease, toxin component of the YeeF-YezG toxin-antitoxin module
COG5445	S	Uncharacterized conserved protein YfaQ, DUF2300 domain
COG5446	R	Uncharacterized membrane protein, predicted cobalt tansporter CbtA
COG5447	S	Uncharacterized protein
COG5448	S	Uncharacterized protein
COG5449	S	Uncharacterized protein
COG5450	K	Transcription regulator of the Arc/MetJ class
COG5451	S	Predicted secreted protein
COG5452	S	Uncharacterized protein
COG5453	S	Uncharacterized protein
COG5454	S	Predicted secreted protein
COG5455	P	Periplasmic regulator RcnB of Ni and Co efflux
COG5456	P	Nitrogen fixation protein FixH
COG5457	S	Uncharacterized conserved protein YjiS, DUF1127 family
COG5458	S	Uncharacterized protein
COG5459	J	Ribosomal protein RSM22 (predicted mitochondrial rRNA methylase)
COG5460	S	Uncharacterized conserved protein, DUF2164 family
COG5461	W	Type IV pilus biogenesis protein CpaD/CtpE
COG5462	S	Predicted secreted (periplasmic) protein
COG5463	S	Uncharacterized conserved protein YgiB, involved in bioifilm formation, UPF0441/DUF1190 family
COG5464	L	Predicted transposase YdaD
COG5465	S	Uncharacterized protein
COG5466	S	Predicted small metal-binding protein
COG5467	S	Uncharacterized protein
COG5468	S	Predicted secreted (periplasmic) protein
COG5469	S	Predicted metal-binding protein
COG5470	S	Uncharacterized conserved protein, DUF1330 family
COG5471	X	Predicted phage recombinase, RecA/RadA family
COG5472	S	Predicted small integral membrane protein
COG5473	S	Uncharacterized membrane protein
COG5474	S	Uncharacterized protein
COG5475	S	Uncharacterized conserved protein YodC, DUF2158 family
COG5476	R	Microcystin degradation protein MlrC, contains DUF1485 domain
COG5477	S	Predicted small integral membrane protein
COG5478	P	Low affinity Fe/Cu permease
COG5479	S	Uncharacterized conserved protein, contains LGFP repeats
COG5480	S	Uncharacterized membrane protein
COG5481	S	Uncharacterized protein
COG5482	S	Uncharacterized protein
COG5483	S	Uncharacterized conserved protein, DUF488 family
COG5484	S	Uncharacterized protein YjcR
COG5485	R	Predicted ester cyclase
COG5486	S	Predicted metal-binding membrane protein
COG5487	S	Uncharacterized membrane protein YtjA, UPF0391 family
COG5488	S	Uncharacterized membrane protein
COG5489	S	Uncharacterized conserved protein, DUF736 family
COG5490	S	Uncharacterized protein
COG5491	D	Archaeal division protein CdvB, Snf7/Vps24/ESCRT-III family
COG5492	R	Uncharacterized conserved protein YjdB, contains Ig-like domain
COG5493	S	Uncharacterized protein
COG5494	O	Predicted thioredoxin/glutaredoxin
COG5495	R	Predicted oxidoreductase, contains short-chain dehydrogenase (SDR) and DUF2520 domains
COG5496	R	Predicted thioesterase
COG5497	S	Predicted secreted protein
COG5498	G	Endoglucanase Acf2
COG5499	V	Antitoxin component HigA of the HigAB toxin-antitoxin module, contains an N-terminal HTH domain
COG5500	S	Uncharacterized membrane protein
COG5501	S	Predicted secreted protein
COG5502	S	Uncharacterized conserved protein, DUF2267 family
COG5503	KV	DNA-dependent RNA polymerase auxiliary subunit epsilon
COG5504	S	Uncharacterized protein YjaZ
COG5505	S	Uncharacterized membrane protein
COG5506	S	Uncharacterized protein YueI
COG5507	S	Uncharacterized  conserved protein YbaA, DUF1428 family
COG5508	S	Uncharacterized protein
COG5509	S	Uncharacterized small protein, DUF1192 family
COG5510	S	Predicted small secreted protein
COG5511	X	Bacteriophage capsid protein
COG5512	R	Predicted  nucleic acid-binding protein, contains Zn-ribbon domain (includes truncated derivatives)
COG5513	S	Predicted secreted protein
COG5514	S	Uncharacterized protein
COG5515	S	Uncharacterized protein
COG5516	R	Conserved protein containing a Zn-ribbon-like motif, possibly RNA-binding
COG5517	Q	3-phenylpropionate/cinnamic acid dioxygenase, small subunit
COG5518	X	Bacteriophage capsid portal protein
COG5519	S	Uncharcterized protein, DUF927 family
COG5520	M	O-Glycosyl hydrolase
COG5521	G	Maltodextrin utilization protein YvdJ (function unknown)
COG5522	S	Uncharacterized membrane protein YwaF
COG5523	S	Uncharacterized membrane protein
COG5524	CT	Bacteriorhodopsin
COG5525	X	Phage terminase, large subunit GpA
COG5526	R	Lysozyme family protein
COG5527	X	Protein involved in initiation of plasmid replication
COG5528	S	Uncharacterized membrane protein
COG5529	Q	Pyocin large subunit
COG5530	S	Uncharacterized membrane protein
COG5531	B	Chromatin remodeling complex protein RSC6, contains SWIB domain
COG5532	S	Uncharacterized conserved protein YfdQ, DUF2303 family
COG5533	O	Ubiquitin C-terminal hydrolase
COG5534	X	Plasmid replication initiator protein
COG5542	G	Mannosyltransferase related to Gpi18
COG5544	S	Uncharacterized conserved protein YfiM, DUF2279 family
COG5545	X	Predicted P-loop ATPase and inactivated derivatives
COG5546	S	Uncharacterized membrane protein
COG5547	S	Uncharacterized membrane protein
COG5548	S	Uncharacterized membrane protein, UPF0136 family
COG5549	O	Predicted Zn-dependent protease
COG5550	O	Predicted aspartyl protease
COG5551	V	CRISPR/Cas system endoribonuclease Cas6, RAMP superfamily
COG5552	S	Uncharacterized protein
COG5553	R	Predicted metal-dependent enzyme of the double-stranded beta helix superfamily
COG5554	Q	Nitrogen fixation protein
COG5555	U	Cytolysin, a secreted calcineurin-like phosphatase
COG5556	S	Uncharacterized protein
COG5557	C	Ni/Fe-hydrogenase 2 integral membrane subunit HybB
COG5558	X	Transposase
COG5561	S	Predicted metal-binding protein
COG5562	S	Uncharacterized conserved protein YbcV, DUF1398 family
COG5563	S	Uncharacterized membrane protein
COG5564	S	Predicted TIM-barrel enzyme
COG5565	X	Bacteriophage terminase large (ATPase) subunit and inactivated derivatives
COG5566	K	Transcriptional regulator, Middle operon regulator (Mor) family
COG5567	S	Predicted small periplasmic lipoprotein YifL (function unknown0
COG5568	S	Uncharacterized protein
COG5569	P	Periplasmic Cu and Ag efflux protein CusF
COG5570	S	Uncharacterized protein
COG5571	R	Uncharacterized protein YhjY, contains autotransporter beta-barrel domain
COG5572	S	Uncharacterized membrane protein
COG5573	R	Predicted nucleic acid-binding protein, contains PIN domain
COG5577	M	Spore coat protein CotF
COG5578	S	Uncharacterized membrane protein YesL
COG5579	S	Uncharacterized protein, DUF1810 family
COG5580	O	Activator of HSP90 ATPase
COG5581	N	c-di-GMP-binding flagellar brake protein YcgR, contains PilZNR and PilZ domains
COG5582	S	Uncharacterized protein YpiB, UPF0302 family
COG5583	S	Uncharacterized protein
COG5584	S	Predicted small secreted protein
COG5585	T	NAD+--asparagine ADP-ribosyltransferase
COG5586	S	Uncharacterized protein
COG5587	S	Uncharacterized conserved protein, DUF2461 family
COG5588	S	Uncharacterized protein
COG5589	S	Uncharacterized protein
COG5590	H	Ubiquinone biosynthesis protein COQ9
COG5591	S	Uncharacterized protein
COG5592	R	Hemerythrin superfamily protein
COG5595	R	Predicted  nucleic acid-binding protein, contains Zn-ribbon domain
COG5597	M	Alpha-N-acetylglucosamine transferase
COG5598	H	Trimethylamine:corrinoid methyltransferase
COG5599	T	Protein tyrosine phosphatase
COG5602	B	Histone deacetylase complex, regulatory component SIN3
COG5605	C	Cytochrome c oxidase subunit IV
COG5606	R	Predicted DNA-binding protein, XRE-type HTH domain
COG5607	S	CHAD domain (function unknown)
COG5608	V	LEA14-like dessication related protein
COG5609	S	Uncharacterized protein YbcI
COG5610	R	Predicted hydrolase, HAD superfamily
COG5611	R	Predicted nucleic-acid-binding protein, contains PIN domain
COG5612	S	Uncharacterized membrane protein
COG5613	S	Uncharacterized protein
COG5614	X	Bacteriophage head-tail adaptor
COG5615	S	Uncharacterized membrane protein
COG5616	R	TolB amino-terminal domain (function unknown)
COG5617	S	Uncharacterized membrane protein
COG5618	S	Predicted periplasmic lipoprotein
COG5619	S	Uncharacterized protein
COG5620	S	Uncharacterized protein
COG5621	R	Predicted secreted hydrolase
COG5622	M	Protein required for attachment to host cells
COG5624	K	Transcription initiation factor TFIID, subunit TAF12
COG5625	K	Predicted DNA-binding transcriptional regulator, contains HTH domain
COG5626	S	Uncharacterized protein
COG5627	L	SUMO ligase MMS21, Smc5/6 complex, required for cell growth and DNA repair
COG5628	R	Predicted acetyltransferase
COG5630	E	Acetylglutamate synthase
COG5631	K	Predicted transcription regulator, contains HTH domain, MarR family
COG5632	M	N-acetylmuramoyl-L-alanine amidase CwlA
COG5633	S	Uncharacterized conserved protein YcfL
COG5634	S	Uncharacterized protein YukJ
COG5635	T	Predicted NTPase, NACHT family domain
COG5637	S	Uncharacterized membrane protein
COG5639	S	Uncharacterized protein
COG5640	O	Secreted trypsin-like serine protease
COG5642	S	Uncharacterized conserved protein, DUF2384 family
COG5643	R	Protein containing a metal-binding domain shared with formylmethanofuran dehydrogenase subunit E
COG5644	S	U3 small nucleolar RNA-associated protein 14
COG5645	S	Uncharacterized conserved protein YceK
COG5646	S	Uncharacterized conserved protein YdhG, YjbR/CyaY-like superfamily, DUF1801 family
COG5649	S	Uncharacterized protein
COG5650	S	Uncharacterized membrane protein
COG5651	S	PPE-repeat protein
COG5652	S	VanZ like family protein (function unknown)
COG5653	N	Acetyltransferase involved in cellulose biosynthesis, CelD/BcsL family
COG5654	S	Uncharacterized conserved protein, contains RES domain
COG5655	X	Plasmid rolling circle replication initiator protein REP and truncated derivatives
COG5658	S	Uncharacterized membrane protein
COG5659	X	SRSO17 transposase
COG5660	T	Predicted anti-sigma-YlaC factor YlaD, contains Zn-finger domain
COG5661	O	Predicted secreted Zn-dependent protease
COG5662	K	Transmembrane transcriptional regulator (anti-sigma factor RsiW)
COG5663	S	Uncharacterized protein, HAD superfamily
COG5664	O	Predicted secreted Zn-dependent protease
COG5665	K	CCR4-NOT transcriptional regulation complex, NOT5 subunit""")
	cogmap.close()

def printPlotStep():
	plotstep=open("plotstep.R", 'w')
	plotstep.write("""rm(list=ls());
library(Rsamtools)
library(OmicCircos)
library(data.table)
args<-commandArgs()
gl<-as.numeric(args[6])
makecog<-c(args[7])
measure<-data.frame(seg.name=seq(1:8), seg.start=seq(1:8), seg.end=seq(1:8)+1, seg.value=1)
measure2<-data.frame(seg.name=1, seg.start=1, seg.end=signif(2*gl/12/1000), seg.value=round(2*gl/12/1000,0))
measure4<-data.frame(seg.name=1, seg.start=1, seg.end=signif(4*gl/12/1000), seg.value=round(4*gl/12/1000,0))
measure8<-data.frame(seg.name=1, seg.start=1, seg.end=signif(8*gl/12/1000), seg.value=round(8*gl/12/1000,0))
measure10<-data.frame(seg.name=1, seg.start=1, seg.end=signif(10*gl/12/1000), seg.value=round(10*gl/12/1000,0))
measure["V5"]<-measure2["V5"]<-measure4["V5"]<-measure8["V5"]<-measure10["V5"]<-1
data<-read.table("contigplot.dat",header=F)
fdata<-read.table("forwardplot.dat",header=F)
rdata<-read.table("reverseplot.dat",header=F)
rnadata<-read.table("rna.dat",header=F)
gcdata<-read.table("gcskewplot.dat",header=F)
if(nrow(data)>1){
  contig<-gcdata["V1"][1,]
  sum<-0
  positive<-data.frame(name=0, value=0)
  negative<-data.frame(name=0, value=0)
  pcont=1
  ncont=1
  for(i in seq(1:nrow(gcdata))){
    if(contig==gcdata["V1"][i,]){
      sum<-sum+gcdata["V5"][i,]
    }else{
      if(sum>0){
        positive[pcont,1]<-as.character(contig)
        positive[pcont,2]<-sum
        pcont<-pcont+1
      }else{
        negative[ncont,1]<-as.character(contig)
        negative[ncont,2]<-sum
        ncont<-ncont+1
      }
      contig<-gcdata["V1"][i,]
      sum<-0
      sum<-sum+gcdata["V5"][i,]
    }
  }
  if(sum>0){
    positive[pcont,1]<-as.character(contig)
    positive[pcont,2]<-sum
  }else{
    negative[ncont,1]<-as.character(contig)
    negative[ncont,2]<-sum
  }
  positive<-positive[order(positive$value),]
  negative<-negative[order(negative$value),]
  if(nrow(positive>1)){
    if(nrow(negative)>1){
      newcontig<-rbind(positive,negative)
    }else{
      newcontig<-positive
    }
  }else{
    if(nrow(negative)>1){
      newcontig<-negative
    }
  }
    newcontig<-newcontig[newcontig$name!=0 & newcontig$value!=0,]
    for(i in seq(1:nrow(newcontig))){
      tmp<-data[i,]
      data[i,]<-data[row<-which(data == as.character(newcontig["name"][i,])),]
      data[row,]<-tmp
    }
}
data["V5"]<-data["V4"]<-1
colnames(data)<- c("chr", "start", "end","V4","V5")
colnames(rnadata)<- c("Gene", "start", "end","Contig","color")
colnames(fdata)<-c("Gene","start","end","Contig","Cog")
colnames(rdata)<-c("Gene","start","end","Contig","Cog")
colnames(gcdata)<-c("Contig","start","end","gccontent","gcskew")
tocirmeasure<-segAnglePo(measure, seg=c(as.matrix(measure["seg.name"][,])))
tocirmeasure[2,2]<-300;tocirmeasure[2,3]<-620
tocirmeasure[3,2]<-0;tocirmeasure[3,3]<-620
tocirmeasure[4,2]<-420;tocirmeasure[4,3]<-620
tocirmeasure[5,2]<-90;tocirmeasure[5,3]<-620
tocirmeasure[6,2]<-120;tocirmeasure[6,3]<-620
tocirmeasure[7,2]<-180;tocirmeasure[7,3]<-620
tocirmeasure[8,2]<-240;tocirmeasure[8,3]<-620
tocirmeasure2<-segAnglePo(measure2, seg=c(as.matrix(measure2["seg.name"][,])))
tocirmeasure2[1,2]<-330
tocirmeasure4<-segAnglePo(measure4, seg=c(as.matrix(measure4["seg.name"][,])))
tocirmeasure4[1,2]<-395
tocirmeasure8<-segAnglePo(measure8, seg=c(as.matrix(measure8["seg.name"][,])))
tocirmeasure8[1,2]<-146
tocirmeasure10<-segAnglePo(measure10, seg=c(as.matrix(measure10["seg.name"][,])))
tocirmeasure10[1,2]<-210
tocir <- segAnglePo(data, seg=c(as.matrix(data["chr"][,])))
tocirf<-segAnglePo(fdata, seg=c(as.matrix(fdata["Gene"][,])))
tocirr<-segAnglePo(rdata, seg=c(as.matrix(rdata["Gene"][,])))
tocirrna<-segAnglePo(rnadata, seg=c(as.matrix(rnadata["Gene"][,])))
tocirgc<-segAnglePo(gcdata, seg=c(as.matrix(gcdata["Contig"][,])))
getl<-function (contig) {
  row<-which(data == as.character(contig))
  return(as.numeric(data["end"][row,]))
}
getal<-function (contig) {
  row<-which(tocir == as.character(contig))
  return(as.numeric(tocir[row,3]) -  as.numeric(tocir[row,2]))
}
getsa<-function (contig) {
  row<-which(tocir == as.character(contig))
  return(as.numeric(tocir[row,2]))
}
for(i in seq(1:nrow(tocirf))){
  tocirf[i,2]<-getsa(c(as.matrix(fdata["Contig"][i,])))+(getal(fdata["Contig"][i,])/getl(c(as.matrix(fdata["Contig"][i,]))))*as.numeric(fdata["start"][i,])
  tocirf[i,3]<-getsa(fdata["Contig"][i,])+(getal(fdata["Contig"][i,])/getl(c(as.matrix(fdata["Contig"][i,]))))*as.numeric(fdata["end"][i,])
  tocirf[i,1]<-paste(c("bar_"),i,sep="")
}
fdata["Gene"]<-as.data.frame(tocirf[,1])
for(i in seq(1:nrow(tocirr))){
  tocirr[i,2]<-getsa(rdata["Contig"][i,])+(getal(rdata["Contig"][i,])/getl(c(as.matrix(rdata["Contig"][i,]))))*as.numeric(rdata["start"][i,])
  tocirr[i,3]<-getsa(rdata["Contig"][i,])+(getal(rdata["Contig"][i,])/getl(c(as.matrix(rdata["Contig"][i,]))))*as.numeric(rdata["end"][i,])
  tocirr[i,1]<-paste(c("bar_"),i,sep="")
  }
rdata["Gene"]<-as.data.frame(tocirr[,1])
for(i in seq(1:nrow(tocirrna))){
  tocirrna[i,2]<-getsa(rnadata["Contig"][i,])+(getal(rnadata["Contig"][i,])/getl(c(as.matrix(rnadata["Contig"][i,]))))*as.numeric(rnadata["start"][i,])
  tocirrna[i,3]<-getsa(rnadata["Contig"][i,])+(getal(rnadata["Contig"][i,])/getl(c(as.matrix(rnadata["Contig"][i,]))))*as.numeric(rnadata["end"][i,])
  tocirrna[i,1]<-paste(c("bar_"),i,sep="")
}
rnadata["Gene"]<-as.data.frame(tocirrna[,1])
for(i in seq(1:nrow(tocirgc))){
  tocirgc[i,2]<-getsa(gcdata["Contig"][i,])+(getal(gcdata["Contig"][i,])/getl(c(as.matrix(gcdata["Contig"][i,]))))*as.numeric(gcdata["start"][i,])
  tocirgc[i,3]<-getsa(gcdata["Contig"][i,])+(getal(gcdata["Contig"][i,])/getl(c(as.matrix(gcdata["Contig"][i,]))))*as.numeric(gcdata["end"][i,])
  tocirgc[i,6]<-gcdata["start"][i,]
  tocirgc[i,7]<-gcdata["end"][i,]
  tocirgc[i,1]<-paste(c("bar_"),i,sep="")
  }
gcdata["Contig"]<-as.data.frame(tocirgc[,1])
if(makecog==c("Y")){
  colorlist<-list( "A" = "darkcyan", "B" = "sienna", "C" = "orange", "D" = "yellow", "E" = "green",
                   "F" = "pink", "G" = "steelblue", "H" = "purple", "I" = "brown", "J" = "violet", 
                   "K" = "maroon", "L" = "gold", "M" = "dark green", "N" = "dark red", "O" = "dark blue", 
                   "P" = "cyan", "Q" = "dark orange", "R" = "turquoise", "S" = "dark violet", "T" = "chocolate",
                   "U" = "beige", "V" = "yellowgreen", "W" = "dimgray", "X" = "gray" ,"Y" = "orangered", 
                   "Z" = "dark cyan")
  
  fdata["V6"]<-rdata["V6"]<-1
  fdata["V6"]<-as.character(colorlist[c(as.matrix(fdata["Cog"]))])
  rdata["V6"]<-as.character(colorlist[c(as.matrix(rdata["Cog"]))])
}
mymedian<-median(gcdata$gccontent)
pdf(file="Rplot.pdf", width = 10, height =10)
par(mar=c(2,2,2,2))
plot(c(0,1000), c(0,1000), type="n", axes=FALSE, xlab="", ylab="", main="")
if(nrow(data)>1){
  circos(R=400, cir=tocir, W=10,type="chr", print.chr.lab=F, scale=F)
}
if(makecog==c("Y")){
  circos(R=340, cir=tocirf, W=60, mapping=fdata, type="b3", col.v=7, col=c(as.matrix(fdata["V6"])), B=F,scale=F, lwd=abs(as.matrix((fdata["end"]-fdata["start"])/4000)))
  circos(R=290, cir=tocirr, W=60, mapping=rdata, type="b3", col.v=7, col=c(as.matrix(rdata["V6"])), B=F,scale=F, lwd=abs(as.matrix((rdata["end"]-rdata["start"])/4000)))
}else{
  circos(R=340, cir=tocirf, W=60, mapping=fdata, type="b3", col.v=7, col=c("dark green"), B=F,scale=F, lwd=abs(as.matrix((fdata["end"]-fdata["start"])/4000)))
  circos(R=290, cir=tocirr, W=60, mapping=rdata, type="b3", col.v=7, col=c("dark red"), B=F,scale=F, lwd=abs(as.matrix((rdata["end"]-rdata["start"])/4000)))
}
circos(R=250, cir=tocirrna, W=50, mapping=rnadata, type="b3", col.v=6, col=c(as.matrix(rnadata["color"])), B=F,scale=T, lwd=abs(as.matrix((rnadata["end"]-rnadata["start"])/4000)))
circos(R=200, cir=tocirgc, W=30, mapping=gcdata, type="b", col.v=4, col=ifelse(gcdata["gccontent"]>=mymedian,c("black"),c("white")), B=F,scale=F, lwd=0.4)
circos(R=200, cir=tocirgc, W=-30, mapping=gcdata, type="b", col.v=4, col=ifelse(gcdata["gccontent"]>=mymedian,c("white"),c("gray")), B=F,scale=F, lwd=0.4)
circos(R=130, cir=tocirgc, W=40, mapping=gcdata, type="b", col.v=5, col=ifelse(gcdata["gcskew"]>0,c("green"),c("white")), B=F,scale=F, lwd=0.4)
circos(R=130, cir=tocirgc, W=-40, mapping=gcdata, type="b", col.v=5, col=ifelse(gcdata["gcskew"]>0,c("white"),c("purple")), B=F,scale=F, lwd=0.4)
circos(R=62, cir=tocirmeasure, W=5, mapping=measure, type="b3", col.v=4, col=c("gray"), B=F, lwd=2)
circos(R=65, cir=tocirmeasure2, W=30, mapping=measure2, type="label2", col.v=4, col=c("gray"), B=F,scale=F, cex =0.5, side="out")
circos(R=65, cir=tocirmeasure4, W=30, mapping=measure4, type="label2", col.v=4, col=c("gray"), B=F,scale=F, cex =0.5, side="out")
circos(R=65, cir=tocirmeasure8, W=30, mapping=measure8, type="label2", col.v=4, col=c("gray"), B=F,scale=F, cex =0.5, side="out")
circos(R=65, cir=tocirmeasure10, W=30, mapping=measure10, type="label2", col.v=4, col=c("gray"), B=F,scale=F, cex =0.5, side="out")
legend(350,420, text.col=c("gray"), cex=0.6,legend="x Kb", box.col="white") ;
if(makecog== c("Y")){
  code<-c("A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z")
  cogletters<-rbind(fdata["Cog"],rdata["Cog"])
  letters<-ifelse(code %in% c(as.matrix(cogletters)),code,FALSE)
  letters<-letters[which(letters != FALSE)]
  lcolors<-as.character(colorlist[c(as.matrix(letters))])
  
  legend("right", legend = c(letters, "tRNA","rRNA", "GC Content","GC Skew +","GC Skew -"), 
         ncol = 1,
         xpd = NA, cex = 0.8,  bty="n",
         fill=c(lcolors,"red","blue","black","purple","green"),
         border = c("white"),
         title = "COG Categories") 
}else{
  legend("right", legend = c("Forward genes","Reverse Genes","tRNA","rRNA", "GC Content","GC Skew +","GC Skew -"), 
         ncol = 1,
         xpd = NA, cex = 0.8,  bty="n",
         fill=c("dark green","dark red","red","blue","black","purple","green"),
         border = c("white"))  
}
dev.off()
""")

	plotstep.close()



def GBKParser(genbank_file, makecog, filterc, clength):
	gbkname=genbank_file.replace("/"," ").split()[len(genbank_file.replace("/"," ").split())-1]
	fna=open(str(gbkname+".fna"), 'w')
	contig=open("contigplot.dat", 'w') #only contgis that contains genes
	forward = open("forwardplot.dat", 'w')
	reverse = open("reverseplot.dat", 'w')
	rna= open("rna.dat", 'w')
	if makecog is not None:
		printCogMap()
		cogMap=pd.read_csv("cognames2003-2014.tab", sep='\t', header=0, index_col=0)
		cogAnnotation=pd.read_csv(makecog, sep='\t', header=0, index_col=0)
		cogAnnotation=cogAnnotation.loc[(cogAnnotation.ftype == "CDS")]

	genomelength=0
	recs = [rec for rec in SeqIO.parse(genbank_file, "genbank")]
	for rec in recs:
		contigname=rec[0:].id
		contiglen=len(rec[0:].seq)
		contigseq=rec[0:].seq
		contigband=0
		if contiglen>clength:
			genomelength+=contiglen
			feats = [feat for feat in rec.features if feat.type == "CDS"]
			for feat in feats:
				feat.location=str(feat.location).replace("("," ").replace(")","").replace("]","").replace("[","").replace(">","").replace("<","").replace(":"," ")
				locations=feat.location.split()
				gene=str(feat.qualifiers["locus_tag"]).replace("'","").replace("[","").replace("]","")
	
				if "join" not in str(feat.location):

					if makecog is not None and gene in cogAnnotation.index:
						cogID=cogAnnotation.loc[gene,"COG"]
						if str(cogID) == "nan":
							cog="S"
						else:
							cog=cogMap.loc[cogID,"func"]
							cog=cog[0]
						contigband=1
						if locations[2]=="+":
							forward.write("%s %s %s %s %s" % (gene, int(locations[0])+1, int(locations[1])+1, contigname, cog))  #gene, start, end, contig
							forward.write("\n")
						else:
							reverse.write("%s %s %s %s %s" % (gene, int(locations[0])+1, int(locations[1])+1, contigname, cog))  #gene, start, end, contig
							reverse.write("\n")
					else:
						contigband=1
						if locations[2]=="+":
							forward.write("%s %s %s %s %s" % (gene, int(locations[0])+1, int(locations[1])+1, contigname, "E"))  #just for color
							forward.write("\n")
						else:
							reverse.write("%s %s %s %s %s" % (gene, int(locations[0])+1, int(locations[1])+1, contigname, "M"))  #just for color
							reverse.write("\n")
				else:
					print "Warning: Join present, not possible to parse gene:",gene
	
			rrnafeats = [feat for feat in rec.features if feat.type == "rRNA"]
			for feat in rrnafeats:
				feat.location=str(feat.location).replace("("," ").replace(")","").replace("]","").replace("[","").replace(">","").replace("<","").replace(":"," ")
				locations=feat.location.split()
				gene=str(feat.qualifiers["locus_tag"]).replace("'","").replace("[","").replace("]","")
				
				#if makecog is not None and gene in cogAnnotation.index:
				contigband=1
				rna.write("%s %s %s %s %s" % (gene, int(locations[0])+1, int(locations[1])+1, contigname, "blue"))  #gene, start, end, contig
				rna.write("\n")
	
			trnafeats = [feat for feat in rec.features if feat.type == "tRNA"]
			for feat in trnafeats:
				feat.location=str(feat.location).replace("("," ").replace(")","").replace("]","").replace("[","").replace(">","").replace("<","").replace(":"," ")
				locations=feat.location.split()
				gene=str(feat.qualifiers["locus_tag"]).replace("'","").replace("[","").replace("]","")
				
				#if makecog is not None and gene in cogAnnotation.index:
				contigband=1
				rna.write("%s %s %s %s %s" % (gene, int(locations[0])+1, int(locations[1])+1, contigname, "red"))  #gene, start, end, contig
				rna.write("\n")
	
			if filterc:
				if contigband==1:
					contig.write(str(contigname+" "+"1 "+str(contiglen)))
					contig.write("\n")
			else:
				contig.write(str(contigname+" "+"1 "+str(contiglen)))
				contig.write("\n")
	
			fna.write(">%s \n" % (contigname))
			fna.write("%s\n" % (contigseq))




	fna.close()
	contig.close()
	forward.close()
	reverse.close()
	rna.close()
	return genomelength

def GC_content_window(s):
	gc = sum(s.count(x) for x in ['G','C','g','c','S','s'])
	gc_content = gc/float(len(s))
	return round(gc_content,4) 


def GC_skew_window(s):
	g = s.count('G')+s.count('g')
	c = s.count('C')+s.count('c')

	try:
		skew = (g-c)/float(g+c)
	except ZeroDivisionError:
		skew = 0
	return round(skew,4)


def GCcalc(filename,window,step,filteredcontigs):

	filterc=open(filteredcontigs,'r')
	filteredc=filterc.read()
	gcplot=open("gcskewplot.dat", 'w')#only contgis that contains genes

	seqobj = SeqIO.parse(filename,'fasta')

	for record in seqobj: 
		pos_array = []
		gc_content_value_array = []
		gc_skew_value_array = []
		name = record.id
		seq = record.seq
		start = 0
		end = 0
		gc = 0
		gc_skew = 0
		if name in filteredc:
			for i in range(0,len(seq),step):
				subseq = seq[i:i+window]
				gc_content = (GC_content_window(subseq))
				gc_skew = (GC_skew_window(subseq))
				start = (i + 1 if (i+1<=len(seq)) else i)
				end = ( i + step if (i+ step<=len(seq)) else len(seq))
				gcplot.write("%s %s %s %s %s\n" % (name,start,end,gc_content,gc_skew))

		gcplot.close
		filterc.close

def main():
	parser = OptionParser(usage = "Usage: python wrapper.py -f genbankfile.gbk")
	parser.add_option("-g","--gbk",dest="filename",help="Input Fasta format file",metavar="GENBANK FILE")
	parser.add_option("-c","--cogAssignFile",dest="cogoption",help="default:None, tsv from prokka outputs that include COGs and the specific CDS you may want to plot",default=None)
	parser.add_option("-f","--filterContigs",dest="filterc",help="default:False, show only contigs that contains genes",default=False, action='store_true')
	parser.add_option("-l","--cLength",dest="clength",help="default:500 filter contigs with less than X bp",default=500)
	parser.add_option("-w","--window",dest="window",help="default:3000, window to take for gccontent and gc skew",default=3000)
	parser.add_option("-s","--step",dest="step",help="default:1500 step to move your window",default=1500)
	parser.add_option("-n","--removeTmpFiles",dest="removeTmpFiles",help="True remove temporary files",default=True,action='store_false')

	(options,args) = parser.parse_args()

	makecog = options.cogoption
	filterc= options.filterc
	genbank_file = options.filename
	window = int(options.window)
	step = int(options.step)
	gbkname=genbank_file.replace("/"," ").split()[len(genbank_file.replace("/"," ").split())-1]
	clength=int(options.clength)
	removeTmpFiles=options.removeTmpFiles
	
	if makecog is not None:
		makecog=os.path.abspath(makecog)

	genbank_file=os.path.abspath(genbank_file)

	resultsfolder=str("results_"+gbkname+".faa")
	subprocess.call(["rm","-rf",str("results_"+gbkname+".faa")])
	subprocess.call(["mkdir",str("results_"+gbkname+".faa")])
	os.chdir(resultsfolder)

	print "Parsing GBK"

	gl=GBKParser(genbank_file, makecog, filterc, clength)
	print "Genome length: ", gl
	print "Computing GC content and GC Skew +/-"
	GCcalc(str(gbkname+".fna"),window,step,"contigplot.dat")
	print "Plotting"
	if makecog is None:
		makecog="N"
	else:
		makecog="Y"

	printPlotStep()
	subprocess.call(["Rscript", "plotstep.R", str(gl), str(makecog)])
	subprocess.call(["mv","Rplot.pdf",str(str(gbkname).replace(".gbk","")+".pdf")])

	if removeTmpFiles:
		subprocess.call("rm -f plotstep.R cognames2003-2014.tab", shell=True)

	print "Done :D"



if __name__ == '__main__':
	main()
	sys.exit()
