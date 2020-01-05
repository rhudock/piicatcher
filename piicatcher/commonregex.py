# coding: utf-8
from types import MethodType
import re

date = re.compile(
    r'(?:(?<!\:)(?<!\:\d)[0-3]?\d(?:st|nd|rd|th)?\s+(?:of\s+)?(?:jan\.?|january|feb\.?|february|mar\.?|march|'
    r'apr\.?|april|may|jun\.?|june|jul\.?|july|aug\.?|august|sep\.?|september|oct\.?|october|'
    r'nov\.?|november|dec\.?|december)|(?:jan\.?|january|feb\.?|february|mar\.?|march|apr\.?|'
    r'april|may|jun\.?|june|jul\.?|july|aug\.?|august|sep\.?|september|oct\.?|october|nov\.?|'
    r'november|dec\.?|december)\s+(?<!\:)(?<!\:\d)[0-3]?\d(?:st|nd|rd|th)?)(?:\,)?\s*(?:\d{4})?|'
    r'[0-3]?\d[-\./][0-3]?\d[-\./]\d{2,4}',
    re.IGNORECASE)
time = re.compile('\d{1,2}:\d{2} ?(?:[ap]\.?m\.?)?|\d[ap]\.?m\.?', re.IGNORECASE)
phone = re.compile(
    r'((?:(?<![\d-])(?:\+?\d{1,3}[-.\s*]?)?(?:\(?\d{3}\)?[-.\s*]?)?\d{3}[-.\s*]?\d{4}(?![\d-]))|'
    r'(?:(?<![\d-])(?:(?:\(\+?\d{2}\))|(?:\+?\d{2}))\s*\d{2}\s*\d{3}\s*\d{4}(?![\d-])))')
phones_with_exts = re.compile(
    r'((?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*(?:[2-9]1[02-9]|[2-9][02-8]1|[2-9]'
    r'[02-8][02-9])\s*\)|(?:[2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)'
    r'?(?:[2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?(?:[0-9]{4})'
    r'(?:\s*(?:#|x\.?|ext\.?|extension)\s*(?:\d+)?))',
    re.IGNORECASE)
link = re.compile(
    r'(?i)((?:https?://|www\d{0,3}[.])?[a-z0-9.\-]+[.](?:(?:international)|'
    r'(?:construction)|(?:contractors)|(?:enterprises)|(?:photography)|'
    r'(?:immobilien)|(?:management)|(?:technology)|(?:directory)|(?:education)|'
    r'(?:equipment)|(?:institute)|(?:marketing)|(?:solutions)|(?:builders)|'
    r'(?:clothing)|(?:computer)|(?:democrat)|(?:diamonds)|(?:graphics)|'
    r'(?:holdings)|(?:lighting)|(?:plumbing)|(?:training)|(?:ventures)|(?:academy)|(?:careers)|'
    r'(?:company)|(?:domains)|(?:florist)|(?:gallery)|(?:guitars)|(?:holiday)|(?:kitchen)|'
    r'(?:recipes)|(?:shiksha)|(?:singles)|(?:support)|(?:systems)|(?:agency)|(?:berlin)|'
    r'(?:camera)|(?:center)|(?:coffee)|(?:estate)|(?:kaufen)|(?:luxury)|(?:monash)|'
    r'(?:museum)|(?:photos)|(?:repair)|(?:social)|(?:tattoo)|(?:travel)|(?:viajes)|'
    r'(?:voyage)|(?:build)|(?:cheap)|(?:codes)|(?:dance)|(?:email)|(?:glass)|(?:house)|'
    r'(?:ninja)|(?:photo)|(?:shoes)|(?:solar)|(?:today)|(?:aero)|(?:arpa)|(?:asia)|(?:bike)|'
    r'(?:buzz)|(?:camp)|(?:club)|(?:coop)|(?:farm)|(?:gift)|(?:guru)|(?:info)|(?:jobs)|(?:kiwi)'
    r'|(?:land)|(?:limo)|(?:link)|(?:menu)|(?:mobi)|(?:moda)|(?:name)|(?:pics)|(?:pink)|(?:post)'
    r'|(?:rich)|(?:ruhr)|(?:sexy)|(?:tips)|(?:wang)|(?:wien)|(?:zone)|(?:biz)|(?:cab)|(?:cat)'
    r'|(?:ceo)|(?:com)|(?:edu)|(?:gov)|(?:int)|(?:mil)|(?:net)|(?:onl)|(?:org)|(?:pro)|'
    r'(?:red)|(?:tel)|(?:uno)|(?:xxx)|(?:ac)|(?:ad)|(?:ae)|(?:af)|(?:ag)|(?:ai)|(?:al)|'
    r'(?:am)|(?:an)|(?:ao)|(?:aq)|(?:ar)|(?:as)|(?:at)|(?:au)|(?:aw)|(?:ax)|(?:az)|(?:ba)|'
    r'(?:bb)|(?:bd)|(?:be)|(?:bf)|(?:bg)|(?:bh)|(?:bi)|(?:bj)|(?:bm)|(?:bn)|(?:bo)|(?:br)|'
    r'(?:bs)|(?:bt)|(?:bv)|(?:bw)|(?:by)|(?:bz)|(?:ca)|(?:cc)|(?:cd)|(?:cf)|(?:cg)|(?:ch)|'
    r'(?:ci)|(?:ck)|(?:cl)|(?:cm)|(?:cn)|(?:co)|(?:cr)|(?:cu)|(?:cv)|(?:cw)|(?:cx)|(?:cy)|'
    r'(?:cz)|(?:de)|(?:dj)|(?:dk)|(?:dm)|(?:do)|(?:dz)|(?:ec)|(?:ee)|(?:eg)|(?:er)|(?:es)|'
    r'(?:et)|(?:eu)|(?:fi)|(?:fj)|(?:fk)|(?:fm)|(?:fo)|(?:fr)|(?:ga)|(?:gb)|(?:gd)|(?:ge)|'
    r'(?:gf)|(?:gg)|(?:gh)|(?:gi)|(?:gl)|(?:gm)|(?:gn)|(?:gp)|(?:gq)|(?:gr)|(?:gs)|(?:gt)|'
    r'(?:gu)|(?:gw)|(?:gy)|(?:hk)|(?:hm)|(?:hn)|(?:hr)|(?:ht)|(?:hu)|(?:id)|(?:ie)|(?:il)|'
    r'(?:im)|(?:in)|(?:io)|(?:iq)|(?:ir)|(?:is)|(?:it)|(?:je)|(?:jm)|(?:jo)|(?:jp)|(?:ke)|'
    r'(?:kg)|(?:kh)|(?:ki)|(?:km)|(?:kn)|(?:kp)|(?:kr)|(?:kw)|(?:ky)|(?:kz)|(?:la)|(?:lb)|'
    r'(?:lc)|(?:li)|(?:lk)|(?:lr)|(?:ls)|(?:lt)|(?:lu)|(?:lv)|(?:ly)|(?:ma)|(?:mc)|(?:md)|'
    r'(?:me)|(?:mg)|(?:mh)|(?:mk)|(?:ml)|(?:mm)|(?:mn)|(?:mo)|(?:mp)|(?:mq)|(?:mr)|(?:ms)|'
    r'(?:mt)|(?:mu)|(?:mv)|(?:mw)|(?:mx)|(?:my)|(?:mz)|(?:na)|(?:nc)|(?:ne)|(?:nf)|(?:ng)|'
    r'(?:ni)|(?:nl)|(?:no)|(?:np)|(?:nr)|(?:nu)|(?:nz)|(?:om)|(?:pa)|(?:pe)|(?:pf)|(?:pg)|'
    r'(?:ph)|(?:pk)|(?:pl)|(?:pm)|(?:pn)|(?:pr)|(?:ps)|(?:pt)|(?:pw)|(?:py)|(?:qa)|(?:re)|'
    r'(?:ro)|(?:rs)|(?:ru)|(?:rw)|(?:sa)|(?:sb)|(?:sc)|(?:sd)|(?:se)|(?:sg)|(?:sh)|(?:si)|'
    r'(?:sj)|(?:sk)|(?:sl)|(?:sm)|(?:sn)|(?:so)|(?:sr)|(?:st)|(?:su)|(?:sv)|(?:sx)|(?:sy)|'
    r'(?:sz)|(?:tc)|(?:td)|(?:tf)|(?:tg)|(?:th)|(?:tj)|(?:tk)|(?:tl)|(?:tm)|(?:tn)|(?:to)|'
    r'(?:tp)|(?:tr)|(?:tt)|(?:tv)|(?:tw)|(?:tz)|(?:ua)|(?:ug)|(?:uk)|(?:us)|(?:uy)|(?:uz)|'
    r'(?:va)|(?:vc)|(?:ve)|(?:vg)|(?:vi)|(?:vn)|(?:vu)|(?:wf)|(?:ws)|(?:ye)|(?:yt)|(?:za)|'
    r'(?:zm)|(?:zw))(?:/[^\s()<>]+[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019])?)',
    re.IGNORECASE)
email = re.compile(
    r"([a-z0-9!#$%&'*+\/=?^_`{|.}~-]+@(?:[a-z0-9](?:[a-z0-9-]"
    r"*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)",
    re.IGNORECASE)
ip = re.compile(
    r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
    r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
    r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
    r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)',
    re.IGNORECASE)
ipv6 = re.compile(
    r'\s*(?!.*::.*::)(?:(?!:)|:(?=:))(?:[0-9a-f]{0,4}(?:(?<=::)|(?<!::):)){6}(?:'
    r'[0-9a-f]{0,4}(?:(?<=::)|(?<!::):)[0-9a-f]'
    r'{0,4}(?:(?<=::)|(?<!:)|(?<=:)(?<!::):)|(?:25[0-4]|2[0-4]\d|1\d\d|'
    r'[1-9]?\d)(?:\.(?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)){3})\s*',
    re.VERBOSE | re.IGNORECASE | re.DOTALL)
price = re.compile(r'[$]\s?[+-]?[0-9]{1,3}(?:(?:,?[0-9]{3}))*(?:\.[0-9]{1,2})?')
hex_color = re.compile('(#(?:[0-9a-fA-F]{8})|#(?:[0-9a-fA-F]{3}){1,2})\\b')
credit_card = re.compile('((?:(?:\\d{4}[- ]?){3}\\d{4}|\\d{15,16}))(?![\\d])')
btc_address = re.compile('(?<![a-km-zA-HJ-NP-Z0-9])[13][a-km-zA-HJ-NP-Z0-9]{26,33}(?![a-km-zA-HJ-NP-Z0-9])')
street_address = re.compile(
    r'\d{1,4} [\w\s]{1,20}(?:street|st|avenue|ave|road|rd|highway|hwy|square|sq|trail|trl|drive|'
    r'dr|court|ct|park|parkway|pkwy|circle|cir|boulevard|blvd)\W?(?=\s|$)',
    re.IGNORECASE)
zip_code = re.compile(r'\b\d{5}(?:[-\s]\d{4})?\b')
po_box = re.compile(r'P\.? ?O\.? Box \d+', re.IGNORECASE)
ssn = re.compile(
    r'(?!000|666|333)0*(?:[0-6][0-9][0-9]|[0-7][0-6][0-9]|[0-7][0-7][0-2])[- ](?!00)[0-9]{2}[- ](?!0000)[0-9]{4}')
icdten = re.compile(r'[A-TV-Z][0-9][0-9AB]\.?[0-9A-TV-Z]{0,4}')
icdnine = re.compile(r'(V\d{2}\.\d{1,2}|\d{3}\.\d{1,2}|E\d{3}\.\d)\b(?!\s?(?:lb|kg)s?)')
mastercard = re.compile(r"(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}")
visa = re.compile(r"\b([4]\d{3}[\s]\d{4}[\s]\d{4}[\s]\d{4}|[4]\d{3}[-]\d{4}[-]\d{4}[-\n"
                  r"]\d{4}|[4]\d{3}[.]\d{4}[.]\d{4}[.]\d{4}|[4]\d{3}\d{4}\d{4}\d{4})\b")
amex = re.compile(r"3[47][0-9]{13}$")
tax = re.compile(r"(\b1040 {0,2}ES\b)|(Tax {0,2}(Ident\S*|Num\S*|Info\S*|Sch\S*)\b)", re.IGNORECASE)
medical_doctor = re.compile(r'\b!(MDM|DRM)(Clinician|Physician|Reading MD|Dr.?:?|Provider|S*,?s*M.?D.?)\b',
                            re.IGNORECASE)
bank_transfer = re.compile(r'\b(ACH |Account|Acct|Rout\S*|Group|Bank|Checking|Member|Credit Card|Wire )'
                           r'(.?:?\s*)(Trans|Pay|Acc|No|Nu|Num|Number)(.?:?\w*)', re.IGNORECASE)
medical_records = re.compile(r'\b(DISCHARGE DIAGNOSIS|ALLERGY|ADMIT DIAGNOSIS|diastolic|hypertension|'
                             r'Stress Test|Oximitry|Discharge px|Hospitalization|past medical hx)\b', re.IGNORECASE)
treatment_terms = re.compile(r'(Abortion|abuse|addiction|AIDS|alcohol|Alopecia|Alzheimer|anxiety|bacteria|'
                             r'beneficiary|Biopsy|Bipolar Disorder|Birth certificate|Birth Date|birthdate|'
                             r'Cadaver|Cancer|Carcinoma|Catheter|chronic|cocaine|COPD|Colonoscopy|deceased|'
                             r'decubitus|dementia|Depression|detox|discharge|disease|drug abuse|eating disorder|'
                             r'End Stage|Endoscopy|ETOH Abuse|Family History|Gastric Bypass|hallucination|'
                             r'health insurance|heroin|HIV Positive|hysterectomy|IBAN|idiopathic|Illness|'
                             r'impotence|Infection|Infectious|Infertility|intake|isolation|Kidney|laceration|'
                             r'Malignant|Medical Record|Miscarriage|narcotic|Pathology|prostate|Prosthetics|'
                             r'Psychiatric|psychosis|rape|Rehab|rehabilitation|reproductive|resuscitate|'
                             r'schizophrenia|seizure|sexually transmitted disease|Substance Abuse|Suicide|'
                             r'Syndrome|Therapy|Transplant|Trauma|Treatment plan|triage|tuberculosis|Tumor|'
                             r'Vaccination|vasectomy)', re.IGNORECASE)
# State Driver's Licenses; source https://github.com/adambullmer/USDLRegex/blob/master/regex.json
california = re.compile(r'\b[A-Z]{1}[0-9]{7}\b')
common_drugs = re.compile(r'\b(Lisinopril|Atorvastatin|Levothyroxine|Metformin|Amlodipine|Metoprolol|Omeprazole|'
                          r'Simvastatin|'
                          r'Losartan|Albuterol|Gabapentin|Acetaminophen|Hydrocodone|Bitartrate|Sertraline|Fluticasone|'
                          r'Montelukast|Furosemide|Amoxicillin|Pantoprazole|Escitalopram|Alprazolam|Prednisone'
                          r'|Bupropion'
                          r'|Pravastatin|Citalopram|Dextroamphetamine|Saccharate|Amphetamine|Aspartate|Ibuprofen'
                          r'|Carvedilol|Trazodone'
                          r'|Fluoxetine|Tramadol|Insulin|Clonazepam|Tamsulosin|Atenolol|Meloxicam|Rosuvastatin'
                          r'|Clopidogrel'
                          r'|Propranolol|Aspirin|Cyclobenzaprine|Glipizide|Duloxetine|Methylphenidate|Ranitidine'
                          r'|Venlafaxine|'
                          r'Zolpidem|Tartrate|Warfarin|Oxycodone|Norethindrone|Allopurinol|Ergocalciferol|Azithromycin|'
                          r'Metronidazole|Loratadine|Lorazepam|Estradiol|Norgestimate|Lamotrigine|Glimepiride|'
                          r'Propionate|'
                          r'Salmeterol|Xinafoate|Cetirizine|Hydrochlorothiazide|Potassium|Paroxetine|Spironolactone'
                          r'|Fenofibrate|'
                          r'Naproxen|Pregabalin|Formoterol|Diltiazem|Quetiapine|Fumarate|Topiramate|Bacitracin|'
                          r'Neomycin|Polymyxin|Clonidine|Buspirone|Latanoprost|Tiotropium|Ondansetron|Lovastatin'
                          r'|Valsartan|'
                          r'Finasteride|Amitriptyline|Esomeprazole|Tizanidine|Alendronate|Lisdexamfetamine|Dimesylate|'
                          r'Ferrous Sulfate|Apixaban|Diclofenac|Sitagliptin|Folic Acid|Sumatriptan|'
                          r'Drospirenone|Ethinyl|'
                          r'Hydroxyzine|Oxybutynin|Triamterene|Cephalexin|Triamcinolone|Benazepril|'
                          r'Hydralazine|Celecoxib|'
                          r'Ciprofloxacin|Ropinirole|Rivaroxaban|Levetiracetam|Isosorbide|Mononitrate|'
                          r'Aripiprazole|Doxycycline|'
                          r'Famotidine|Clavulanate|Methotrexate|Mirtazapine|Nifedipine|Sulfamethoxazole|'
                          r'Trimethoprim|Enalapril'
                          r'|Maleate|Docusate|Pioglitazone|Divalproex|Donepezil|Hydroxychloroquine|'
                          r'Prednisolone|Thyroid|Guanfacine'
                          r'|Testosterone|Ramipril|Diazepam|Levonorgestrel|Clindamycin|Gemfibrozil|Baclofen|'
                          r'Temazepam|Nitroglycerin'
                          r'|Nebivolol|Verapamil|Timolol|Promethazine|Benzonatate|Memantine|Doxazosin|Mesylate|'
                          r'Ezetimibe|Valacyclovir'
                          r'|Beclomethasone|Hydrocortisone|Morphine|Risperidone|Methylprednisolone|Omega-3-acid|'
                          r'Oseltamivir|Besylate'
                          r'|Meclizine|Polyethylene Glycol|Liraglutide|Desogestrel|Levofloxacin|Acyclovir|'
                          r'Brimonidine|Digoxin|Adalimumab'
                          r'|Cyanocobalamin|Magnesium|Ipratropium|Chlorthalidone|Glyburide|Levocetirizine|'
                          r'Dihydrochloride|Carbamazepine'
                          r'|Etonogestrel|Methocarbamol|Pramipexole|Lithium|Dicyclomine|Fluconazole|Nortriptyline|'
                          r'Carbidopa|Levodopa'
                          r'|Nitrofurantoin|Mupirocin|Butalbital|Lansoprazole|Dexmethylphenidate|Budesonide|Mirabegron|'
                          r'Canagliflozin|Menthol|Terazosin|Progesterone|Amiodarone|Mometasone|Cefdinir|'
                          r'Atomoxetine|Linagliptin\b)', re.IGNORECASE)


regexes = {
    "dates": date,
    "times": time,
    "phones": phone,
    "phones_with_exts": phones_with_exts,
    "links": link,
    "emails": email,
    "ips": ip,
    "ipv6s": ipv6,
    "prices": price,
    "hex_colors": hex_color,
    "credit_cards": credit_card,
    "btc_addresses": btc_address,
    "street_addresses": street_address,
    "zip_codes": zip_code,
    "po_boxes": po_box,
    "ssn_number": ssn,
    "icd10_codes": icdten,
    "icd9_codes": icdnine,
    "mastercard": mastercard,
    "visa": visa,
    "amex": amex,
    "tax": tax,
    "medical_doctor": medical_doctor,
    "bank_transfer": bank_transfer,
    "medical_records": medical_records,
    'treatment_terms': treatment_terms,
    "california": california,
    'common_drugs': common_drugs

}


class regex:

    def __init__(self, obj, regex):
        self.obj = obj
        self.regex = regex

    def __call__(self, *args):
        def regex_method(text=None):
            value = []
            for x in self.regex.findall(text or self.obj.text):
                if hasattr(x, "strip"):
                    value.append(x.strip)
                else:
                    value.append(x)
            return value
        return regex_method


class CommonRegex(object):

    def __init__(self, text=""):
        self.text = text

        for k, v in list(regexes.items()):
            setattr(self, k, regex(self, v)(self))

        if text:
            for key in list(regexes.keys()):
                method = getattr(self, key)
                setattr(self, key, method())
