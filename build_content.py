import json
from pathlib import Path
sources={
 'gdpr':{'title':'GDPR — Regulation (EU) 2016/679','url':'https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng','type':'Binding EU law'},
 'uavg':{'title':'UAVG — Dutch GDPR Implementation Act','url':'https://wetten.overheid.nl/BWBR0040940/','type':'Binding Dutch law'},
 'whw':{'title':'WHW — Higher Education and Research Act','url':'https://wetten.overheid.nl/BWBR0005682/','type':'Binding Dutch law'},
 'ai':{'title':'AI Act — Regulation (EU) 2024/1689 (original text)','url':'https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng','type':'Binding EU law; read with amendments'},
 'omnibus':{'title':'Digital Omnibus on AI — Regulation (EU) 2026/1744','url':'https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng','type':'Binding EU amending law'},
 'timeline':{'title':'European Commission — AI Act implementation','url':'https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai','type':'Official explanatory guidance'},
 'literacy':{'title':'European Commission — AI literacy Q&A','url':'https://digital-strategy.ec.europa.eu/en/faqs/ai-literacy-questions-answers','type':'Official explanatory guidance'},
 'edpb':{'title':'EDPB guidelines and recommendations','url':'https://www.edpb.europa.eu/our-work-tools/general-guidance/guidelines-recommendations-best-practices_en','type':'Regulatory guidance index'},
 'ap':{'title':'Autoriteit Persoonsgegevens','url':'https://autoriteitpersoonsgegevens.nl/','type':'Dutch supervisory authority guidance'},
 'curia':{'title':'Court of Justice of the European Union','url':'https://curia.europa.eu/','type':'Case law search'},
 'surf':{'title':'SURF Privacy Expertise Centrum','url':'https://pec.surf.nl/','type':'Sector guidance'},
}
modules=[{'id':k,'title':t,'description':d} for k,t,d in [
 ('gdpr','GDPR foundations','Core concepts and the Dutch legal context.'),('ai','AI Act foundations','Scope, roles, classification and application dates.'),('research','Research','Scientific research, data reuse and AI development.'),('education','Education','Teaching, learning, assessment and student rights.'),('operations','Operations','Staff, suppliers and organizational accountability.')]]
lessons=[]
def add(id,module,title,level,objective,concepts,example,nuance,terms,refs,questions):
 def ref(s):
  key,loc=s.split('|',1); assert key in sources; return {'source':key,'location':loc}
 lessons.append(dict(id=id,module=module,title=title,level=level,objective=objective,concepts=concepts,example=example,nuance=nuance,terms=terms,references=[ref(s) for s in refs],questions=[dict(id=f'{id}-{i+1}',statement=q,answer=a,explanation=e,references=[ref(s) for s in r]) for i,(q,a,e,r) in enumerate(questions)]))
G='gdpr|'; A='ai|'; O='omnibus|'; U='uavg|'; W='whw|'
add('g01','gdpr','Personal data and identifiability','Foundation','Distinguish personal, pseudonymized and anonymous information.',[
'Personal data concern an identified or identifiable natural person. Identification can be indirect; a name is not required.',
'Pseudonymization separates identifying information from the remaining data. It reduces risk but does not automatically make data anonymous.',
'Anonymity requires considering means reasonably likely to be used to identify a person, taking account of context and available technology.'],
'A student research assistant replaces interviewees’ names with codes and keeps the key separately. The coded records still relate to identifiable participants.',
'Identifiability is contextual. Removing direct identifiers does not establish that a dataset is anonymous; consider linkage and small groups.',{'persoonsgegevens':'personal data','betrokkene':'data subject','pseudonimisering':'pseudonymization'},[G+'Art. 4(1), 4(5); Recital 26'],[
('A student number can be personal data even when a name is absent.',True,'An identifier can enable indirect identification.',[G+'Art. 4(1); Recital 26']),
('Keeping a code key in a separate secure location makes the coded records anonymous for the university.',False,'The university can still link records to individuals; separation is a safeguard.',[G+'Art. 4(5); Recital 26']),
('A group-level statistic can fall outside GDPR if no natural person is reasonably identifiable.',True,'Genuinely anonymous information is outside GDPR’s personal-data scope.',[G+'Recital 26'])])
add('g02','gdpr','Principles and lawful bases','Foundation','Identify a purpose and lawful basis before processing.',[
'Article 5 sets principles including fairness, transparency, purpose limitation, minimization, accuracy, storage limitation, security and accountability.',
'Article 6 requires an applicable lawful basis. Public task must have a basis in EU or member-state law; consent is not a universal default.',
'Special-category data require an applicable Article 9 condition in addition to Article 6.'],
'A university collects only details necessary to administer enrollment under its relevant legal duties.',
'A university cannot assume that every activity is a public task. Identify the actual purpose and legal basis; Article 6(1)(f) is unavailable to public authorities when performing their tasks.',{'grondslag':'lawful basis','doelbinding':'purpose limitation','dataminimalisatie':'data minimization'},[G+'Art. 5, 6, 9; Recitals 39, 43, 45'],[
('A lawful basis makes the data-minimization principle optional.',False,'The principles apply alongside the lawful basis.',[G+'Art. 5–6']),
('A public-task basis needs a foundation in EU or member-state law.',True,'Article 6(3) requires the legal basis for processing under Article 6(1)(e).',[G+'Art. 6(1)(e), 6(3); Recital 45']),
('An Article 9 condition replaces the need for an Article 6 lawful basis.',False,'Both layers must be addressed for special-category processing.',[G+'Art. 6, 9'])])
add('g03','gdpr','Controllers, processors and joint control','Intermediate','Classify parties by what they actually do.',[
'A controller determines purposes and means of processing. A processor acts on behalf of a controller.',
'Joint controllers jointly determine purposes and means; Article 26 requires an arrangement reflecting their responsibilities.',
'Article 28 requires sufficient processor guarantees and a binding agreement containing the prescribed terms.'],
'A university instructs a survey hosting company to store responses. The company may be a processor for that activity; a partner university defining a joint study may be a joint controller.',
'A contract label does not settle the classification. A provider may have different roles for different processing purposes.',{'verwerkingsverantwoordelijke':'controller','verwerker':'processor','gezamenlijke verwerkingsverantwoordelijken':'joint controllers'},[G+'Art. 4(7)–(8), 26, 28; Recital 79'],[
('Two universities can be joint controllers without having identical responsibilities.',True,'Article 26 calls for a transparent allocation of responsibilities, not identical roles.',[G+'Art. 26; Recital 79']),
('A company is a processor for all activities whenever a contract calls it a processor.',False,'Actual purposes and means determine the role for each activity.',[G+'Art. 4(7)–(8), 28(10)']),
('A controller must assess whether a processor provides sufficient guarantees.',True,'Article 28(1) places this requirement on the controller.',[G+'Art. 28(1)'])])
add('g04','gdpr','Rights, transparency and automated decisions','Intermediate','Recognize rights and their limits.',[
'Articles 13 and 14 govern information provision. Access, rectification, erasure, restriction, portability and objection have distinct conditions.',
'Erasure is not unconditional; Article 17(3) contains exceptions including legal obligations and certain public-interest purposes.',
'Article 22 concerns decisions based solely on automated processing that produce legal or similarly significant effects, subject to exceptions and safeguards.'],
'A student asks for access to their personal data in a learning platform. The university must evaluate the request under Article 15 and respect other persons’ rights.',
'A nominal human signature is not necessarily meaningful review. Examine actual decision-making, not only the workflow diagram.',{'inzagerecht':'right of access','recht op gegevenswissing':'right to erasure'},[G+'Art. 12–22; Recitals 58–71'],[
('A valid erasure request can be refused for records that must be retained under an applicable legal obligation.',True,'Article 17(3)(b) provides an exception where retention is necessary.',[G+'Art. 17(3)(b)']),
('The right to data portability applies to every lawful basis.',False,'Article 20 applies to automated processing based on consent or contract, subject to its conditions.',[G+'Art. 20(1)']),
('Article 22 addresses only decisions that produce legal or similarly significant effects and are based solely on automated processing.',True,'These are the central conditions in Article 22(1); other GDPR duties can still apply outside it.',[G+'Art. 22(1); Recital 71'])])
add('g05','gdpr','Accountability, security and DPIAs','Intermediate','Understand when safeguards and impact assessment are required.',[
'Controllers must demonstrate compliance and implement appropriate technical and organizational measures.',
'A DPIA is required where processing is likely to result in high risk to individuals. It assesses necessity, proportionality, risks and measures before processing.',
'If high risk remains absent measures to mitigate it, Article 36 requires prior consultation with the supervisory authority.'],
'A university proposes systematic monitoring of students. A DPIA may be required based on the nature, scope, context and purpose.',
'A DPIA is not merely a security review, and its completion does not by itself establish lawfulness.',{'gegevensbeschermingseffectbeoordeling':'data protection impact assessment','functionaris voor gegevensbescherming':'data protection officer'},[G+'Art. 5(2), 24–25, 32, 35–36; Recitals 75, 78, 84, 90–94'],[
('A DPIA examines risks to individuals’ rights and freedoms, not only risks to the university.',True,'The focus is the impact on natural persons.',[G+'Art. 35(7); Recital 90']),
('A DPIA is required for every new spreadsheet containing personal data.',False,'The trigger is likely high risk, not the mere existence of personal data.',[G+'Art. 35(1)']),
('An existing security certification removes the controller’s accountability obligations.',False,'Certification may help demonstrate compliance but does not remove responsibility.',[G+'Art. 24, 42(4)'])])
add('a01','ai','Scope, roles and research exclusions','Foundation','Separate AI Act roles from GDPR roles.',[
'The AI Act regulates AI systems and certain models. It defines providers and deployers by their activities, not by GDPR classifications.',
'A university using an AI system under its authority can be a deployer. A university developing and putting its own AI system into service may be a provider.',
'Article 2(6) excludes systems/models and outputs specifically developed and put into service solely for scientific research and development. Article 2(8) separately addresses pre-market research, testing and development; real-world testing is not covered by that exclusion.'],
'A lab builds a research-only model; a faculty separately adopts a commercial tool for administrative tasks. The two uses need different scope assessments.',
'An AI Act research exclusion does not exempt personal-data processing from GDPR. Reassess when intended purpose changes.',{'aanbieder':'provider','gebruiksverantwoordelijke':'deployer'},[A+'Art. 2(6)–(8), 3(1), 3(3)–(4); Recital 25',O+'Art. 1 (amendments)'],[
('An AI Act deployer is necessarily a GDPR processor.',False,'These are separate legal classifications based on different activities.',[A+'Art. 3(4)',G+'Art. 4(8)']),
('A university’s internal use of a commercial AI system can fall within the AI Act.',True,'Organizational use under its authority can make it a deployer.',[A+'Art. 3(4)']),
('The AI Act scientific-research exclusion also removes GDPR obligations.',False,'GDPR remains separately applicable to personal-data processing.',[A+'Art. 2(7)',G+'Art. 2'])])
add('a02','ai','AI literacy and prohibited practices','Intermediate','Understand already applicable duties and prohibitions.',[
'Amended Article 4 requires providers and deployers to support AI literacy of staff and others operating or using AI on their behalf. Measures should reflect knowledge, context and affected persons.',
'The July 2026 amendment removed the original wording requiring a sufficient level; the obligation to take literacy measures remains.',
'Article 5 prohibits specified practices, including emotion inference in workplaces and educational institutions based on biometric data, subject to the medical or safety exception.'],
'A faculty organizes context-specific training for staff using generative AI and prohibits an emotion-recognition system intended to infer students’ emotions during examinations.',
'Article 4 does not mandate one standard training course or certificate. High-risk systems can entail additional obligations.',{'AI-geletterdheid':'AI literacy','verboden AI-praktijken':'prohibited AI practices'},[A+'Art. 4–5, 3(39); Recital 44',O+'Art. 1(5); Recital 8','literacy|Article 4 amendment Q&A'],[
('The 2026 amendment removed every obligation for deployers to support AI literacy.',False,'The amended Article 4 retains the duty to take measures to support literacy.',[O+'Art. 1(5)']),
('AI literacy measures should reflect how AI is used and who is affected.',True,'The amended text expressly includes context and affected people.',[O+'Art. 1(5)']),
('A university may infer student emotions from biometric data for ordinary classroom engagement monitoring without considering Article 5.',False,'The educational emotion-inference prohibition is directly relevant; ordinary engagement is not the medical/safety exception.',[A+'Art. 5(1)(f), 3(39); Recital 44'])])
add('a03','ai','High-risk AI and the implementation calendar','Intermediate','Recognize intended-purpose classification and distinguish future rules from current duties.',[
'Annex III lists education and employment use cases. Article 6 governs classification, including a limited exception for systems that do not pose a significant risk, subject to conditions; profiling of natural persons defeats that exception.',
'High-risk requirements include risk management, data governance and human oversight. Provider and deployer duties differ.',
'The 2026 Digital Omnibus postpones Annex III high-risk rules to 2 December 2027 and relevant Annex I product rules to 2 August 2028. The general application date was 2 August 2026; prohibitions and literacy started in February 2025. Transitional rules matter.'],
'A university considers AI for admissions ranking. It should plan for the high-risk framework, while applying GDPR and any AI Act obligations already in force.',
'High-risk does not mean prohibited. Classification depends on intended purpose and the applicable legal conditions. Dates should be rechecked before practical reliance.',{'AI-systemen met een hoog risico':'high-risk AI systems','menselijk toezicht':'human oversight'},[A+'Art. 6, 9–15, 26, 113; Annex III(3)–(4)',O+'Art. 1 (amendments to Art. 113)','timeline|Current application timeline'],[
('Every AI tool used at a university is high-risk solely because its user is a university.',False,'The specific intended purpose and Article 6 classification criteria matter.',[A+'Art. 6; Annex III']),
('An Annex III admissions system can be high-risk even though its vendor is not a university.',True,'The intended admissions use, not the vendor’s institutional identity, drives classification.',[A+'Art. 6; Annex III(3)(a)']),
('The general Annex III high-risk application date is 2 December 2027 under the July 2026 amendments.',True,'The amendment extends this deadline; other duties may already apply.',[O+'Art. 1 (Art. 113 amendment)','timeline|High-risk application dates'])])
add('r01','research','Participation consent and research lawful bases','Intermediate','Separate informed consent from the GDPR basis.',[
'Agreement to participate in research and GDPR consent serve different purposes. A study can rely on another valid Article 6 basis while obtaining ethical participation consent.',
'GDPR consent must be freely given, specific, informed and unambiguous. Withdrawal must be as easy as giving consent.',
'For special categories, an Article 9 condition is also necessary. Dutch UAVG Article 24 provides a conditional research exception.'],
'A cognitive science study uses informed participation consent, while the university evaluates whether public task is the appropriate GDPR basis.',
'Recital 33 recognizes that some scientific research purposes cannot be fully identified initially, but it does not authorize unlimited consent.',{'toestemming':'consent','wetenschappelijk onderzoek':'scientific research'},[G+'Art. 4(11), 6–7, 9; Recitals 33, 42–43',U+'Art. 24'],[
('A signed research participation form establishes GDPR consent for every later use of the data.',False,'GDPR consent has its own conditions and scope. Later purposes require separate consideration.',[G+'Art. 4(11), 5(1)(b), 7; Recital 33']),
('Ethical participation consent can coexist with a different GDPR lawful basis.',True,'The two concepts are distinct; the chosen GDPR basis must satisfy Article 6.',[G+'Art. 6–7']),
('Scientific research automatically permits processing special-category data under Dutch law.',False,'Article 9 and UAVG Article 24 impose conditions; research status alone is not enough.',[G+'Art. 9(2)(j), 89(1)',U+'Art. 24'])])
add('r02','research','Secondary use, retention and research safeguards','Intermediate','Understand compatibility and research-specific safeguards.',[
'Further processing for scientific research is not considered incompatible with the initial purposes under Article 5(1)(b) when Article 89(1) applies.',
'Longer storage for research can be permitted subject to appropriate safeguards; GDPR itself sets no universal ten-year research retention period.',
'Article 89 requires safeguards, especially minimization. UAVG Article 44 allows certain rights to be limited in specified research/statistical circumstances.'],
'A lab wishes to reuse interview records from an earlier project. It checks purpose, lawful basis, transparency, identifiability and safeguards before reuse.',
'Open science does not require public release of personal data. Institutional retention rules and funder requirements must be considered separately.',{'hergebruik':'reuse','bewaartermijn':'retention period','waarborgen':'safeguards'},[G+'Art. 5(1)(b), 5(1)(e), 6(4), 89; Recitals 50, 156–159',U+'Art. 44'],[
('GDPR itself imposes a ten-year minimum retention period on all university research data.',False,'Retention depends on purpose, applicable law and safeguards; institutional requirements are separate.',[G+'Art. 5(1)(e), 89(1)']),
('Research compatibility under Article 5(1)(b) is linked to Article 89(1) safeguards.',True,'The special compatibility rule expressly refers to Article 89(1).',[G+'Art. 5(1)(b), 89(1)']),
('UAVG Article 44 removes all data subject rights for any research activity.',False,'It addresses specific rights and conditions, not a blanket exemption.',[U+'Art. 44',G+'Art. 89'])])
add('r03','research','International collaborations and AI development','Advanced','Distinguish sharing arrangements, transfers and research exclusions.',[
'Partners’ controller/processor roles depend on actual purposes and means. Sharing personal data must have a lawful basis and appropriate safeguards.',
'Chapter V applies to qualifying transfers to third countries or international organizations. Adequacy, appropriate safeguards or narrowly applicable derogations are different routes.',
'Research-only AI exclusions are purpose-dependent. A research system later deployed in student services must be reassessed.'],
'A Dutch lab gives an external Canadian research partner access to identifiable study data. It checks the recipient and whether an adequacy decision covers that recipient, or another valid transfer route is needed.',
'Access from abroad may be relevant even without downloading. A collaboration agreement alone is not a Chapter V transfer mechanism.',{'doorgifte':'international transfer','adequaatheidsbesluit':'adequacy decision'},[G+'Art. 26, 28, 44–49; Recitals 101–108',A+'Art. 2(6)–(8)'],[
('A collaboration agreement alone establishes a valid GDPR transfer mechanism for all third-country recipients.',False,'Chapter V requires an applicable mechanism and conditions; an ordinary collaboration agreement is not sufficient.',[G+'Art. 44–49']),
('A research-only AI system later used operationally should be reassessed under the AI Act.',True,'The scope exclusion depends on the system’s scientific-only purpose and use.',[A+'Art. 2(6), 2(8)']),
('Adequacy decisions must be checked for their scope, rather than assuming they cover every recipient in a country.',True,'Adequacy can apply to a country, territory, specified sector or international organization.',[G+'Art. 45(1)'])])
add('e01','education','Student records, examinations and retention','Intermediate','Connect GDPR principles with Dutch education responsibilities.',[
'Student administration and examination processing require a specific purpose, lawful basis, access controls and defined retention.',
'WHW Articles 7.12 and 7.12b establish the examination board and its responsibilities. This does not grant unrestricted access to every student record.',
'Erasure requests must be assessed against relevant legal obligations and other exceptions, rather than handled automatically.'],
'A student requests deletion of assessment records during an appeal. The university considers applicable retention rules, examination responsibilities and the need to preserve evidence.',
'Retention periods for exam scripts may depend on institutional schedules and other rules. Do not infer a single period from GDPR or WHW.',{'examencommissie':'examination board','tentamen':'examination'},[G+'Art. 5, 6, 17(3), 32',W+'Art. 7.12, 7.12b'],[
('The examination board’s statutory duties permit it to see every student’s health information without a necessity assessment.',False,'Access must still be justified and minimized; health data have extra protection.',[W+'Art. 7.12, 7.12b',G+'Art. 5(1)(c), 9']),
('A student’s erasure request can be limited by an applicable statutory retention obligation.',True,'Article 17(3)(b) may apply where processing is necessary to comply with a legal obligation.',[G+'Art. 17(3)(b)']),
('The examination board has a statutory role in determining whether degree requirements are met.',True,'This follows from WHW Article 7.12(2).',[W+'Art. 7.12(2)'])])
add('e02','education','Learning analytics, proctoring and accommodations','Advanced','Assess monitoring and sensitive student data.',[
'Learning analytics and remote proctoring can involve profiling or systematic monitoring. A DPIA may be required where high risk is likely.',
'Information about disability or health is special-category data. An applicable Article 9 condition is required; access must be minimized.',
'AI intended to detect prohibited behavior during tests is listed in Annex III(3)(d); Article 6 classification and the updated implementation calendar matter.'],
'A faculty compares invasive webcam monitoring with less intrusive assessment methods and considers the impact on students with disabilities.',
'Consent may be difficult to establish as freely given when students lack a genuine choice. Assess alternatives rather than assuming consent resolves monitoring risks.',{'leeranalyses':'learning analytics','bijzondere persoonsgegevens':'special-category personal data'},[G+'Art. 5, 7, 9, 35; Recitals 43, 75, 91',A+'Art. 6; Annex III(3)(d)',O+'Art. 1 (Art. 113 amendment)'],[
('Student disability information can constitute special-category health data.',True,'Information revealing physical or mental health is covered by Article 9.',[G+'Art. 4(15), 9(1)']),
('A mandatory proctoring checkbox necessarily establishes freely given GDPR consent.',False,'A lack of real choice can undermine consent.',[G+'Art. 4(11), 7; Recital 43']),
('AI intended to monitor prohibited behavior during examinations is explicitly listed in Annex III.',True,'Annex III(3)(d) lists this use; Article 6 and transition dates still matter.',[A+'Annex III(3)(d); Art. 6',O+'Art. 1 (Art. 113 amendment)'])])
add('e03','education','AI-assisted admissions and grading','Advanced','Distinguish high-risk AI classification, human review and automated decisions.',[
'AI intended to determine access/admission or evaluate learning outcomes can be listed high-risk under Annex III(3), subject to Article 6.',
'GDPR Article 22 applies to solely automated significant decisions, with specific exceptions and safeguards. A human rubber stamp may not amount to genuine human involvement.',
'AI Act human oversight and GDPR automated-decision rules are separate requirements. High-risk application deadlines do not postpone GDPR.'],
'A course uses an AI-generated grading suggestion. A qualified examiner independently evaluates the work and can change the proposed result.',
'Human review can matter for Article 22 but does not automatically remove an AI system from Annex III classification.',{'geautomatiseerde besluitvorming':'automated decision-making','menselijk toezicht':'human oversight'},[G+'Art. 22; Recital 71',A+'Art. 6, 14, 26; Annex III(3)(a)–(b)',O+'Art. 1 (Art. 113 amendment)'],[
('Adding an examiner’s approval button automatically makes the decision non-automated under GDPR.',False,'Actual meaningful involvement matters, not a nominal approval step.',[G+'Art. 22(1); Recital 71']),
('An AI system evaluating learning outcomes can fall within Annex III even when an examiner reviews its output.',True,'Human review does not itself settle Article 6 classification.',[A+'Art. 6; Annex III(3)(b)']),
('The delayed AI Act high-risk deadline suspends GDPR Article 22 for university grading.',False,'GDPR applies independently.',[G+'Art. 22',O+'Art. 1 (Art. 113 amendment)'])])
add('o01','operations','Procurement, cloud services and subprocessors','Intermediate','Recognize controller duties and processor chains.',[
'A processor contract must include Article 28 requirements, including instructions, confidentiality, security, assistance and return/deletion provisions.',
'A processor needs specific or general written authorization before engaging another processor. General authorization requires notice of intended changes and opportunity to object.',
'Where a supplier uses data for its own purposes, its role for that activity must be assessed separately.'],
'A university procures cloud transcription software. It investigates whether recordings are used for vendor training, who has access and where processing takes place.',
'An EU server location is not proof that all processing, support or transfers stay within the EEA.',{'subverwerker':'subprocessor','verwerkersovereenkomst':'data processing agreement'},[G+'Art. 28(2)–(4), 28(10), 32, 44; Recital 81'],[
('A processor can engage a subprocessor without any written authorization if it remains responsible for the service.',False,'Article 28(2) requires specific or general written authorization.',[G+'Art. 28(2)']),
('Under general authorization, intended subprocessor changes must be communicated so the controller can object.',True,'Article 28(2) explicitly requires this opportunity.',[G+'Art. 28(2)']),
('An EU hosting address establishes that every remote support activity remains in the EEA.',False,'Access arrangements and actual recipients must be checked separately.',[G+'Art. 28, 44–49'])])
add('o02','operations','Staff monitoring, recruitment and health data','Advanced','Apply GDPR and AI Act concepts to employment.',[
'Employee data processing requires a lawful basis and proportionality. Employment power imbalance can undermine freely given consent.',
'Health and absence-related data may be special-category data; Dutch law contains limited exceptions. Do not infer unrestricted employer access.',
'AI for recruitment, selection or specified worker-management decisions is listed in Annex III(4); workplace emotion inference is generally prohibited subject to the medical/safety exception.'],
'HR considers an AI tool to rank applicants and a dashboard to track employees’ behavior. Each purpose and technology requires its own legal assessment.',
'High-risk obligations apply according to the updated calendar, while prohibited practices and GDPR already apply.',{'werknemersgegevens':'employee data','ziekteverzuim':'sickness absence'},[G+'Art. 5–7, 9, 22, 35; Recital 43',U+'Art. 30',A+'Art. 5(1)(f), 6; Annex III(4)',O+'Art. 1 (Art. 113 amendment)'],[
('An employment contract makes any form of employee monitoring necessary for contract performance.',False,'Necessity and proportionality must be established for the specific processing.',[G+'Art. 5(1)(c), 6(1)(b)']),
('AI intended to rank job applicants can be listed high-risk under the AI Act.',True,'Recruitment and selection are included in Annex III(4)(a).',[A+'Art. 6; Annex III(4)(a)']),
('An employer’s legitimate interest alone is enough to process special-category health data.',False,'An applicable Article 9 condition is also required.',[G+'Art. 6, 9'])])
add('o03','operations','Breaches, responsibilities and oversight','Intermediate','Distinguish institutional accountability from specialist duties.',[
'A personal data breach can concern confidentiality, integrity or availability. Controllers document breaches and notify the authority unless risk to individuals is unlikely.',
'Where notification is required, the controller must notify without undue delay and, where feasible, within 72 hours after awareness. Processors notify controllers without undue delay.',
'The DPO advises and monitors independently. The controller remains accountable. A high-risk breach may also require communication to affected individuals.'],
'An email with student records goes to the wrong recipient. The university assesses risk, documents the event and determines whether notification is required.',
'Not every security incident is a personal data breach, and not every breach requires notification. Internal reporting deadlines can be stricter.',{'datalek':'personal data breach','toezichthouder':'supervisory authority'},[G+'Art. 4(12), 33–34, 37–39; Recitals 85–88, 97'],[
('A controller must document personal data breaches even when notification to the authority is not required.',True,'Article 33(5) requires documentation of breaches and relevant facts.',[G+'Art. 33(5)']),
('A processor has the same 72-hour statutory notification deadline to the authority as a controller.',False,'The processor must notify the controller without undue delay; the controller assesses authority notification.',[G+'Art. 33(1), 33(2)']),
('Appointing a DPO transfers the controller’s responsibility for compliance to the DPO.',False,'The DPO advises and monitors; accountability remains with the controller.',[G+'Art. 5(2), 24, 39'])])
Path(__file__).with_name('curriculum.json').write_text(json.dumps({'version':'1.0','reviewed':'2026-11-27','sources':sources,'modules':modules,'lessons':lessons},ensure_ascii=False,indent=2),encoding='utf-8')
print(len(lessons),'lessons',sum(len(l['questions']) for l in lessons),'questions')
