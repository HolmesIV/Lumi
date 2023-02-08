import re

# List of regexes for ingredient matching based on description
# Dyes, Fragrances, and Emotives
dye = re.compile('ci {0,3}[0-9].*', re.I)
fragrance = re.compile('.*frag.*', re.I)
emotive = re.compile('.*(vitamin|panthenol|leaf).*', re.I)

# Other
solids = re.compile('.*(mica|zinc gluc|tapioc|silicate).*', re.I)
edta = re.compile('.*edta.*', re.I)

# Oils
oil = re.compile('.*( oil |petro|paraffin|hexadec|butter).*', re.I)
fatacid = re.compile('.*(myrist|palmit|cocoat).*', re.I)

# Silicone
silicone = re.compile('.*dimethicone.*', re.I)

# Polymers
polymer = re.compile('.*([oy]mer|polysorb|carbopol|acrylo).*', re.I)
xanthum = re.compile('.*xanth.*', re.I)

# Preservatives
preserves = re.compile('.*(phenoxyeth|triethanolam|benzo[ai]|behent|cit |mit |climbaz).*', re.I)
paraben = re.compile('(methyl|propyl|ethyl) *paraben.*', re.I)

# Glycerins
glycerin = re.compile('.*glycerin.*', re.I)
polyols = re.compile('.*(diol|glycol|glyceryl).*', re.I)

# Emulsifiers
emuls = re.compile('.*(peg|ceteth).*', re.I)
stearyls = re.compile('.*(stear[iy]|cet[ye]|caprylyl ether).*', re.I)

# Acids/Bases/Salts
acids = re.compile('.*citr[ia].*', re.I)
bases = re.compile('(sodium|potassium|na|k) *hydrox.*', re.I)
salts = re.compile('(sodium|potassium|na|k|phosphate) *(chloride|cl).*', re.I)

# Water
water = re.compile('(?!tri).*water.*', re.I)

reg_dict = {
    "Dye": [dye],
    "Fragrance": [fragrance],
    "Emotive": [emotive],
    "Dispersed Solid Particles": [solids],
    "Preservatives": [preserves, paraben, edta],
    "Oil": [oil, fatacid],
    "Silicone": [silicone],
    "Polymer Structurants": [polymer, xanthum],
    "Glycerin": [glycerin],
    "Polyols": [polyols],
    "Emulsifiers": [emuls, stearyls],
    "Acid": [acids],
    "Neutralizer": [bases],
    "Salt": [salts],
    "Water": [water],
}


function_groups = {
    "Water": ["Water"],
    "Polyols": ["Glycerin", "Polyols"],
    "Polymer Structurants": ["Polymer", "Hydrocolloid", "Oil Thickener"],
    "Neutralizer": ["Base"],
    "Acid": ["Acid"],
    "Dispersed Solid Particles": ["Veegum", "Particles", "Elastomers"],
    "Oil": ["Non-polar", "Polar", "Silicone"],
    "Emulsifier": ["Hydrocarbon Emulfisifier", "Silicone Surfactant"],
    "Preservatives": ["Preservatives", "Kelating Preservative", "Antioxidant"],
    "UV Protection": ["UV Procection"],
    "Salt": ["Salt", "Electrolyte"],
    "Emotive": ["Dye", "Fragrance", "Claim"],
}


function_buckets = {
    "nan": "",
    "CI 19140 Food Yellow 4 Cosmetic Grade":                "Fragrance",
    "Water-Local-Demin-Pasteurised":                        "Water",
    "Sunflower Seed Oil Low Oleic":                         "Oil",
    "L-lysine monohydrochloride":                           "Unk",
    "Glycerin Refined Grade 98%":                           "Water Soluble Polyols",
    "Sodium Chloride Powder":                               "Electrolyte",
    "CIT 1.1: MIT 0.4 magnesium salt stabilised":           "Preservative",
    "Sodium Hydroxide flake 97%":                           "Neutralizer",
    "Climbazole":                                           "Preservative",
    "Citric Acid Monohydrate":                              "Acid",
    "Zinc Gluconate":                                       "Dispersed Solid particles",
    "Saturne P":                                            "Unk",
    "Disodium EDTA":                                        "Kelating/Preservatives",
    "Behentrimonium Chloride and DPG":                      "Preservative",
    "CI 15985 E110 Food Yellow 3 Cosmetic Grade":           "Dye",
    "Cetearyl Alcohol 30-70 C16-C18":                       "Oil",
    "Dimethicone 600K and Amodimethicone 2000nm":           "Oil",
    "Sunflower Seed Oil High Oleic":                        "Oil",
    "Sodium Hydroxide Solution (50%)":                      "Neutralizer",
    "Peg-100 Stearate (Vegetable or Synthetic)":            "Emulsifier",
    "USP White Petrolatum G-2212":                          "Oil",
    "Dimethicone  200 CST":                                 "Oil",
    "Methylparaben":                                        "Preservative",
    "Glycerin Pharmacopeia Grade 99.5%":                    "Water Soluble Polyols",
    "Stearic Acid C18 34-56% - C16 40-65% (Animal Based)":  "Oil",
    "Theobroma Cacao (Cocoa) Seed Butter 100%":             "Oil",
    "Iso Propyl Myristate":                                 "Oil",
    "Glycol Stearate 97% + Stearamide AMP 3%":              "Water Soluble Polyols",
    "Phenoxyethanol":                                       "Preservative",
    "1,3 Butylene Glycol ":                                 "Water Soluble Polyols",
    "Magnesium Aluminum Silicate (pH 9-10 @5%)":            "Dispersed Solid particles",
    "Cetyl Alcohol High C16 Low MP Solid":                  "Oil",
    "Xanthan Gum (Cosmetic Grade)":                         "Polymer Structurants",
    "FRAG Cocoa Glow Void Mod 10":                          "Fragrance",
    "Cocos Nucifera (Coconut) Oil 100%":                    "Oil",
    "Propyl  paraben ":                                     "Preservative",
    "Water-Local-Demineralised-MicroTreated":               "Water",
    "Hydroxyethyl cellulose Vis 3400-5500mPas (1% Solution)": "Unk",
    "Glyceryl Stearate 40% Monostearate Veg Pdr/Flk/Plt":   "Water Soluble Polyols",
    "Caramel Liq Sulphite ammonia 150d PC":                 "Unk",
    "Dimethicone and Dimethiconol ~1500cst":                "Oil",
    "VITAMIN E ACETATE":                                    "Emotive",
    "MICRO TREATED DEMIN WATER":                            "Water",
    "Caprylyl Glycol":                                      "Water Soluble Polyols",
    "Isohexadecane":                                        "Oil",
    "Ammonium Acryloyldimethyltaurate/Beheneth- 25 Methacrylate C": "Polymer Structurants",
    "Ammonium acryloyldimethyl taurate / VP copolymer":     "Polymer Structurants",
    "Aloe Barbadensis Leaf Juice Powder(Organic)":          "Emotive",
    "Cetearyl Alcohol+Cetearyl Glucoside":                  "Oil",
    "Capric/Caprylic Triglyceride 70:30":                   "Oil",
    "Stearic Acid C16- 40-65% C18- 34-58%":                 "Oil",
    "Glycerin Pharmacopeia Grade Vege Derived":             "Water Soluble Polyols",
    "HYDROXYACETOPHENONE":                                  "Antioxidant",
    "Zemea (Propanediol)":                                  "Unk",
    "Dimethicone 5 cst":                                    "Oil",
    "Dicaprylyl ether":                                     "Oil",
    "Stearyl Alcohol Deo Grade":                            "Oil",
    "Tapioca Ster":                                         "Dispersed Solid particles",
    "Centella Asiatica Leaf Extract [2%] + Water + Glycerin": "Emotive",
    "MICRO TREATED DEMIN WATER- De-ionized":                 "Water",
    "Sodium Acrylate/Sodium Acryloyldimethyl Taurate Copolymer + C15-19 Alkane + Poly": "Polymer Structurants",
    "Citric Acid 50% Liquid (low colour)":                  "Acid",
    "Polyglyceryl-3 Methyl Glucose Distearate ()":          "Emulsifier",
    "D--Panthenol (75%)":                                   "Emotive",
    "Sodium Benzoate":                                      "Preservative",
    "Propanediol 100%":                                     "Water Soluble Polyols",
    "Stearyl Alcohol":                                      "Oil",
    "Cetyl Palmitate":                                      "Oil",
    "Isopropyl Palmitate":                                  "Oil",
    "POTASSIUM HYDROXIDE 45% W/W SOLUTION":                 "Neutralizer",
    "Ceteth-20":                                            "Emulsifier",
    "Sodium Acrylate/Sodium Acryloyldimethyl Taurate Copolymer": "Polymer Structurants",
    "Mineral Oil 70 SUS + Tocopherol 0.002%":               "Oil",
    "Glyceryl Stearate (50% monostearate, low glycerol)":   "Water Soluble Polyols",
    "Carbopol 980-2% Disp Methylparaben":                   "Polymer Structurants",
    "Dimethicone 50 cst":                                   "Oil",
    "USP White Petrolatum/ G2212":                          "Oil",
    "Dimethicone 350 cst":                                  "Oil",
    "Triethanolamine 99 (85%) + water (15%) Low DEA":       "Neutralizer",
    "BUTYROSPERMUM PARKII (SHEA BUTTER)":                   "Oil",
    "Glyceryl Stearate 43% Monostearate Veg Pdr/Flk":       "Emulsifier",
    "Carbomer 100% (45,000-65,000) mPas":                   "Polymer Structurants",
    "Acrylates crosspolymer  Powder  55000mPas(0.5% mucilage)": "Polymer Structurants",
    "Butylene Glycol 1,3-":                                 "Water Soluble Polyols",
    "Frag: CONVERTIBLE":                                    "Fragrance",
    "Mica 77% + TiO2 23% Sparkle Gold":                     "Dispersed Solid particles",
    "Mineral Oil 80 cSt(20C)":                              "Oil",
    "Hydroxystearic Acid":                                  "Emulsifier",
    "Disodium Phosphate Anhydrous PhEur/USP":               "Salt",
    "Paraffin 60% Microcrystalline Wax 40% + BHT":          "Oil",
    "Paraffinum Liquidum 30(saybolt) 20cSt(20C)":           "Oil",
    "Paraffin Wax 140/145 MP 60-62.8":                      "Oil",
    "Polysorbate 20 and Ascorbic Acid and Panthenol":       "Polymer Structurants",
    "Cetyl PEG/PPG-10/1 Dimethicone":                       "Emulsifier",
    "Ethylhexyl Cocoate":                                   "Oil",
    "Mica 72% + TiO2 28% Sparkle Violet":                   "Dispersed Solid particles",
    "CI15985+CI14700+CI47005 Dye Soln":                     "Dye",
    "BYE DRY BL":                                           "Dye",
    "Carbomer (Carbopol Ultrez 10)":                        "Polymer",
}