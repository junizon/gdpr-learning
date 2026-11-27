import hmac
import json
import random
from datetime import datetime, date, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo
import streamlit as st

ROOT = Path(__file__).parent
COURSE = json.loads((ROOT / 'curriculum.json').read_text(encoding='utf-8'))
LESSONS = {l['id']:l for l in COURSE['lessons']}
QUESTIONS = {q['id']:(l,q) for l in LESSONS.values() for q in l['questions']}
TZ = ZoneInfo('Europe/Amsterdam')

def today(): return datetime.now(TZ).date().isoformat()
def fresh(): return {'schema':1,'read':[], 'bookmarks':[], 'days':[], 'attempts':{}, 'last':None}
def secret(key, default=None):
    try: return st.secrets.get(key,default)
    except (FileNotFoundError, st.errors.StreamlitSecretNotFoundError): return default

def clean_progress(p):
    if not isinstance(p,dict) or p.get('schema') != 1: raise ValueError('Unsupported backup format')
    out=fresh()
    for key in ('read','bookmarks'):
        out[key]=list(dict.fromkeys(x for x in p.get(key,[]) if isinstance(x,str) and x in LESSONS))
    out['days']=sorted(set(date.fromisoformat(x).isoformat() for x in p.get('days',[]) if isinstance(x,str)))
    out['last']=p.get('last') if p.get('last') in LESSONS else None
    for k,v in p.get('attempts',{}).items():
        if k not in QUESTIONS or not isinstance(v,dict): continue
        out['attempts'][k]={'count':max(0,int(v['count'])),'correct':max(0,int(v['correct'])),'last_ok':bool(v['last_ok']), 'confidence':v.get('confidence','Not sure') if v.get('confidence') in ['Certain','Somewhat certain','Guessing','Not sure'] else 'Not sure', 'run':max(0,int(v.get('run',0))), 'due':date.fromisoformat(v['due']).isoformat()}
    return out

def load():
    dsn=secret('progress_dsn')
    if dsn:
        import psycopg
        with psycopg.connect(dsn, connect_timeout=8) as conn:
            with conn.cursor() as c:
                c.execute('CREATE TABLE IF NOT EXISTS gdpr_learning_progress (id TEXT PRIMARY KEY, payload JSONB NOT NULL)')
                c.execute('SELECT payload FROM gdpr_learning_progress WHERE id=%s',('personal',))
                row=c.fetchone()
        return clean_progress(row[0]) if row else fresh()
    path=ROOT/'.progress.json'
    return clean_progress(json.loads(path.read_text())) if path.exists() else fresh()

def persist(p):
    dsn=secret('progress_dsn')
    if dsn:
        import psycopg
        from psycopg.types.json import Jsonb
        with psycopg.connect(dsn,connect_timeout=8) as conn:
            with conn.cursor() as c:
                c.execute('INSERT INTO gdpr_learning_progress(id,payload) VALUES (%s,%s) ON CONFLICT(id) DO UPDATE SET payload=EXCLUDED.payload',('personal',Jsonb(p)))
    else:
        path=ROOT/'.progress.json'; tmp=path.with_suffix('.tmp'); tmp.write_text(json.dumps(p),encoding='utf-8'); tmp.replace(path)

def save(p):
    st.session_state.progress=p
    try: persist(p); st.session_state.save_error=None
    except Exception: st.session_state.save_error='Progress could not be saved to storage. Export a backup before leaving.'

def study(p):
    if today() not in p['days']: p['days'].append(today())

def streak(p):
    days=set(p['days']); d=date.fromisoformat(today()); n=0
    if d.isoformat() not in days: d-=timedelta(days=1)
    while d.isoformat() in days: n+=1; d-=timedelta(days=1)
    return n

def mastered(l,p):
    return all(p['attempts'].get(q['id'],{}).get('last_ok',False) for q in l['questions'])

def refs(items):
    for r in items:
        s=COURSE['sources'][r['source']]
        st.markdown(f"[{s['title']}]({s['url']}) — {r['location']}  \n*{s['type']}*")

def launch(ids):
    ids=list(dict.fromkeys(ids)); random.SystemRandom().shuffle(ids)
    st.session_state.quiz={'ids':ids,'idx':0,'result':None,'score':0,'missed':[],'nonce':random.randrange(10**12)}
    st.session_state.nav='Quiz'; st.rerun()

def goto(page):
    st.session_state.nav=page
    st.rerun()

def open_lesson(lid):
    st.session_state.lesson=lid; st.session_state.nav='Learn'; st.rerun()

def due_ids(p):
    return [k for k,v in p['attempts'].items() if v['due']<=today() and QUESTIONS[k][0]['id'] in p['read']]

st.set_page_config(page_title='GDPR & AI Governance',page_icon='📚',layout='centered',initial_sidebar_state='collapsed')
# Presentation only: keep curriculum, quiz logic and storage unchanged.
st.markdown("""
<style>
.stApp { background: var(--background-color); }
.block-container { max-width: 1000px; padding-top: 2.7rem; padding-bottom: 3rem; }
.study-hero {
    background: linear-gradient(118deg, #173b49 0%, #235566 63%, #306b70 100%);
    border-radius: 17px; padding: 1.65rem 1.85rem; margin-bottom: .65rem;
    color: #fff; position: relative; overflow: hidden;
    border: 1px solid rgba(255,255,255,.09);
}
.study-hero:after { content: ""; position: absolute; width: 220px; height: 220px;
    border: 1px solid rgba(255,255,255,.13); border-radius: 50%; right: -65px; top: -110px;
    box-shadow: 0 0 0 25px rgba(255,255,255,.045), 0 0 0 52px rgba(255,255,255,.035);
    pointer-events: none; }
.study-kicker { font-size: .73rem; font-weight: 650; letter-spacing: .13em; text-transform: uppercase; color: #c3e2dd; margin-bottom: .45rem; }
.study-hero h1 { font-family: Georgia, 'Times New Roman', serif; font-weight: 500; font-size: clamp(1.65rem, 4.5vw, 2.6rem); line-height: 1.17; color: #fff !important; padding: 0; margin: 0 0 .45rem; letter-spacing: -.025em; position: relative; z-index: 1; }
.study-hero p { color: #e0efed; margin: 0; font-size: .94rem; line-height: 1.45; position: relative; z-index: 1; }
[data-testid="stMetric"] { border: 1px solid color-mix(in srgb, currentColor 14%, transparent); border-radius: 12px; padding: .8rem 1rem; background: color-mix(in srgb, #43877e 5%, var(--background-color)); }
[data-testid="stMetricValue"] { font-weight: 600; font-variant-numeric: tabular-nums; }
[data-testid="stVerticalBlockBorderWrapper"] > div { border-radius: 13px; }
[data-testid="stProgress"] [role="progressbar"] > div { background: #368b80 !important; }
.stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] { background: #256c64; border-color: #256c64; color: white; }
.stButton > button[kind="primary"]:hover { background: #1d554e; border-color: #1d554e; color: white; }
.stButton > button:not([kind="primary"]):hover { border-color: #368b80; color: #368b80; }
.study-module { display: flex; align-items: center; gap: .55rem; margin-bottom: .1rem; }
.study-module-num { display: inline-flex; align-items: center; justify-content: center; font-size: .76rem; font-weight: 700; border-radius: 8px; width: 2.15rem; height: 2.15rem; flex-shrink: 0; color: var(--module-ink); background: var(--module-bg); }
.study-module-tag { font-size: .72rem; text-transform: uppercase; letter-spacing: .085em; font-weight: 650; opacity: .8; }
@media (max-width: 640px) {
    .block-container { padding: 2.1rem 1rem 2rem; }
    .study-hero { padding: 1.3rem 1.15rem; border-radius: 13px; }
    [data-testid="stMetric"] { padding: .55rem .65rem; }
}

/* Readable study typography on desktop and mobile. */
html { font-size: 19px !important; }
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] a { font-size: 1rem; line-height: 1.65; }
[data-testid="stCaptionContainer"] p { font-size: .88rem; line-height: 1.5; }
[data-testid="stWidgetLabel"] p,
[data-testid="stRadio"] label p,
[data-baseweb="select"] { font-size: 1rem !important; }
.stButton button p, .stFormSubmitButton button p,
[data-testid="stDownloadButton"] button p { font-size: 1rem; }
.study-hero p { font-size: 1rem; }
.study-kicker, .study-module-tag { font-size: .8rem; }
@media (max-width: 640px) {
    html { font-size: 18px !important; }
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li { line-height: 1.6; }
}
</style>
<div class="study-hero">
    <div class="study-kicker">Personal learning studio</div>
    <h1>GDPR &amp; AI Governance</h1>
    <p>Dutch and EU higher education &nbsp;·&nbsp; Learn, practice, revisit.</p>
</div>
""", unsafe_allow_html=True)
password=secret('app_password')
if not isinstance(password,str) or not password:
    st.warning('Access is not configured. Set app_password in Streamlit Secrets before using this app.'); st.stop()
if not st.session_state.get('authenticated'):
    with st.form('login'):
        supplied=st.text_input('Password',type='password'); submit=st.form_submit_button('Sign in')
    if submit:
        if hmac.compare_digest(supplied.encode(),password.encode()):
            st.session_state.authenticated=True; st.rerun()
        else: st.error('Incorrect password.')
    st.stop()
if 'progress' not in st.session_state:
    try: st.session_state.progress=load()
    except Exception:
        st.error('Could not load saved progress. Check storage configuration before continuing.'); st.stop()
p=st.session_state.progress
if 'nav' not in st.session_state: st.session_state.nav='Home'
if 'lesson' not in st.session_state: st.session_state.lesson=next(iter(LESSONS))
if not secret('progress_dsn'):
    st.caption('Progress storage is temporary. Export a backup in Progress.')
if st.session_state.get('save_error'): st.error(st.session_state.save_error)
# Synchronize widget state before creating widgets; callbacks run before reruns.
pages=['Home','Learn','Quiz','Revision','Progress','Legal library']
def change_nav(): st.session_state.nav=st.session_state.nav_widget
def back_home(): st.session_state.nav='Home'
if st.session_state.nav!='Home':
    st.button('← Back to Home',key='home_top',on_click=back_home)
st.session_state.nav_widget=st.session_state.nav
st.selectbox('Navigate',pages,key='nav_widget',on_change=change_nav)
page=st.session_state.nav
if page=='Home':
    c1,c2,c3=st.columns(3); c1.metric('Day streak',streak(p)); c2.metric('Lessons read',f"{len(p['read'])}/{len(LESSONS)}"); c3.metric('Quiz passed',f"{sum(mastered(l,p) for l in LESSONS.values())}/{len(LESSONS)}")
    if p['last'] and st.button('Resume last lesson',use_container_width=True): open_lesson(p['last'])
    st.subheader('Your learning path')
    module_style = {
        'gdpr': ('01', 'Foundation', '#dcecea', '#205c55'),
        'ai': ('02', 'Foundation', '#e3e8f7', '#3d508e'),
        'research': ('03', 'Applied study', '#f0e5f5', '#704583'),
        'education': ('04', 'Applied study', '#f7ebd8', '#805619'),
        'operations': ('05', 'Applied study', '#e4ebf1', '#425d72'),
    }
    modules=COURSE['modules']
    for start in range(0,len(modules),2):
        pair=modules[start:start+2]
        columns=st.columns(2) if len(pair)==2 else [st.container()]
        for col,m in zip(columns,pair):
            items=[l for l in LESSONS.values() if l['module']==m['id']]; n=sum(l['id'] in p['read'] for l in items)
            num,tag,bg,ink=module_style.get(m['id'], ('--','Study','#e4ebf1','#425d72'))
            with col:
                with st.container(border=True):
                    st.markdown(f'<div class="study-module"><span class="study-module-num" style="--module-bg:{bg};--module-ink:{ink}">{num}</span><span class="study-module-tag">{tag}</span></div>',unsafe_allow_html=True)
                    st.subheader(m['title']); st.write(m['description']); st.progress(n/len(items),text=f'{n} of {len(items)} lessons read')
                    if st.button('Open module',key='open_'+m['id'],use_container_width=True): open_lesson(next((l['id'] for l in items if l['id'] not in p['read']),items[0]['id']))
    st.caption(f"Curriculum {COURSE['version']} · prepared {COURSE['reviewed']} · educational material, not institutional policy or case-specific legal advice.")
elif page=='Learn':
    mods={m['id']:m for m in COURSE['modules']}
    current=LESSONS[st.session_state.lesson]
    def change_module():
        st.session_state.lesson=next(l['id'] for l in LESSONS.values() if l['module']==st.session_state.module_widget)
    def change_lesson(): st.session_state.lesson=st.session_state.lesson_widget
    module=current['module']
    st.session_state.module_widget=module
    st.selectbox('Module',list(mods),format_func=lambda k:mods[k]['title'],key='module_widget',on_change=change_module)
    ids=[l['id'] for l in LESSONS.values() if l['module']==module]
    lid=current['id']
    st.session_state.lesson_widget=lid
    st.selectbox('Lesson',ids,format_func=lambda k:('✓ ' if k in p['read'] else '')+LESSONS[k]['title'],key='lesson_widget',on_change=change_lesson)
    l=LESSONS[lid]
    if p['last']!=lid: p['last']=lid; save(p)
    st.header(l['title']); st.caption(l['level']); st.markdown('**Learning objective**'); st.write(l['objective'])
    st.markdown('**Core concepts**')
    for item in l['concepts']: st.markdown('- '+item)
    st.markdown('**University example (fictional)**'); st.write(l['example'])
    st.markdown('**Important nuance**'); st.write(l['nuance'])
    with st.expander('Dutch terminology'):
        for k,v in l['terms'].items(): st.markdown(f'**{k}** — {v}')
    with st.expander('Articles, recitals and legal sources',expanded=True): refs(l['references'])
    col1,col2=st.columns(2)
    if col1.button('Remove bookmark' if lid in p['bookmarks'] else 'Bookmark',use_container_width=True):
        if lid in p['bookmarks']: p['bookmarks'].remove(lid)
        else: p['bookmarks'].append(lid)
        save(p); st.rerun()
    if col2.button('Mark as read' if lid not in p['read'] else 'Read ✓',disabled=lid in p['read'],use_container_width=True):
        p['read'].append(lid); study(p); save(p); st.rerun()
    if st.button('Take lesson quiz',disabled=lid not in p['read'],type='primary',use_container_width=True): launch(q['id'] for q in l['questions'])
    if lid not in p['read']: st.caption('Mark the lesson as read to unlock its quiz.')
    if ids.index(lid)<len(ids)-1 and st.button('Next lesson'): open_lesson(ids[ids.index(lid)+1])
    st.button('← Back to Home',key='home_lesson_bottom',on_click=back_home,use_container_width=True)
elif page=='Quiz':
    quiz=st.session_state.get('quiz')
    if not quiz:
        st.header('Practice'); eligible=[l for l in LESSONS.values() if l['id'] in p['read']]
        if not eligible: st.info('Read a lesson first to unlock its quiz.')
        else:
            lid=st.selectbox('Choose a completed lesson',[l['id'] for l in eligible],format_func=lambda k:LESSONS[k]['title'])
            if st.button('Start quiz',type='primary'): launch(q['id'] for q in LESSONS[lid]['questions'])
    elif quiz['idx']>=len(quiz['ids']):
        st.header('Quiz complete'); st.metric('Score',f"{quiz['score']} / {len(quiz['ids'])}")
        if quiz['missed']:
            st.write('Review the explanations and try the missed questions again.')
            if st.button('Retry missed questions',type='primary'): launch(quiz['missed'])
        else: st.success('All questions correct in this round.')
        if st.button('Finish'): st.session_state.quiz=None; goto('Home')
    else:
        qid=quiz['ids'][quiz['idx']]; l,q=QUESTIONS[qid]; tag=f"{quiz['nonce']}_{quiz['idx']}"
        st.caption(l['title']); st.progress(quiz['idx']/len(quiz['ids']),text=f"Question {quiz['idx']+1} of {len(quiz['ids'])}")
        st.subheader(q['statement'])
        if quiz['result'] is None:
            confidence=st.radio('How confident are you?',['Certain','Somewhat certain','Guessing','Not sure'],index=3,horizontal=True,key='confidence_'+tag)
            c1,c2=st.columns(2); choice=None
            if c1.button('True',key='true_'+tag,use_container_width=True): choice=True
            if c2.button('False',key='false_'+tag,use_container_width=True): choice=False
            if choice is not None:
                ok=choice==q['answer']; old=p['attempts'].get(qid,{}); run=old.get('run',0)+1 if ok else 0
                interval=([1,3,7,14,30][min(run-1,4)] if ok else 0)
                p['attempts'][qid]={'count':old.get('count',0)+1,'correct':old.get('correct',0)+int(ok),'last_ok':ok,'confidence':confidence,'run':run,'due':(date.fromisoformat(today())+timedelta(days=interval)).isoformat()}
                quiz['result']={'ok':ok,'choice':choice}; quiz['score']+=int(ok)
                if not ok: quiz['missed'].append(qid)
                study(p); save(p); st.rerun()
        else:
            result=quiz['result']; msg=f"{'Correct' if result['ok'] else 'Incorrect'} — {'True' if q['answer'] else 'False'}"
            (st.success if result['ok'] else st.error)(msg)
            st.write(q['explanation']); refs(q['references'])
            if st.button('Next question' if quiz['idx']+1<len(quiz['ids']) else 'See results',type='primary',use_container_width=True):
                quiz['idx']+=1; quiz['result']=None; st.rerun()
        if st.button('Exit quiz'): st.session_state.quiz=None; goto('Home')
elif page=='Revision':
    st.header('Revision'); due=due_ids(p); unlocked=[q['id'] for l in LESSONS.values() if l['id'] in p['read'] for q in l['questions']]
    missed=[k for k in unlocked if k in p['attempts'] and not p['attempts'][k]['last_ok']]
    misconceptions=[k for k in missed if p['attempts'][k]['confidence']=='Certain']
    st.write('Questions return after 1, 3, 7, 14 and 30 days of consecutive correct answers. Incorrect answers are due immediately.')
    for label,ids,key in [('Due for review',due,'due'),('Incorrect answers',missed,'missed'),('Confident but incorrect',misconceptions,'mis'),('Mixed practice (up to 10)',random.sample(unlocked,min(10,len(unlocked))),'mix')]:
        st.write(f'**{label}** · {len(ids)} questions')
        if st.button('Start',key='rev_'+key,disabled=not ids): launch(ids)
    st.caption('Only questions from lessons you have marked as read are included.')
elif page=='Progress':
    st.header('My progress'); st.metric('Current day streak',streak(p)); st.write(f"Study days: {len(p['days'])} · Questions attempted: {len(p['attempts'])} / {len(QUESTIONS)}")
    for m in COURSE['modules']:
        items=[l for l in LESSONS.values() if l['module']==m['id']]; n=sum(mastered(l,p) for l in items)
        st.progress(n/len(items),text=f"{m['title']}: {n}/{len(items)} quizzes currently passed")
    st.subheader('Bookmarks')
    if not p['bookmarks']: st.caption('No bookmarks yet.')
    for lid in p['bookmarks']:
        if st.button(LESSONS[lid]['title'],key='bookmark_'+lid): open_lesson(lid)
    st.subheader('Backup and restore')
    st.download_button('Export my progress',json.dumps(p,indent=2),file_name='gdpr-progress.json',mime='application/json',use_container_width=True)
    uploaded=st.file_uploader('Restore a progress backup',type='json',help='Only import your own learning-progress JSON. No case files or documents.',key='restore')
    if uploaded is not None:
        if uploaded.size>1_000_000: st.error('Backup exceeds the size limit.')
        else:
            try:
                replacement=clean_progress(json.loads(uploaded.getvalue())); st.warning('Restoring replaces the current learning record. Export the current record first if needed.')
                if st.button('Confirm restore'): save(replacement); st.session_state.quiz=None; st.success('Restored in this session.')
            except (ValueError,TypeError,KeyError,AttributeError): st.error('Invalid learning-progress backup.')
elif page=='Legal library':
    st.header('Legal library'); st.caption('Primary legislation and supporting guidance are distinct. Read the AI Act with its 2026 amendment.')
    term=st.text_input('Search source title or type').casefold().strip()
    for s in COURSE['sources'].values():
        if term in (s['title']+' '+s['type']).casefold(): st.markdown(f"[{s['title']}]({s['url']})  \n*{s['type']}*")
    st.subheader('AI Act timeline')
    st.markdown('- 2 February 2025: prohibitions and literacy provisions.\n- 2 August 2025: general-purpose AI model rules (subject to transition).\n- 27 July 2026: Digital Omnibus entered into force.\n- 2 August 2026: general application date, subject to exceptions.\n- 2 December 2027: general Annex III high-risk application date.\n- 2 August 2028: relevant Annex I product high-risk application date.')
    refs([{'source':'omnibus','location':'Art. 1 (amendments to Art. 113)'},{'source':'timeline','location':'Official implementation dates'}])
    st.caption('Dates checked against the Commission and July 2026 amendment. Recheck before practical use.')
if st.sidebar.button('Sign out'):
    st.session_state.clear(); st.rerun()
