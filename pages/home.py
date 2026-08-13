import streamlit as st
import textwrap

# ============================================================
# MIRAI AI — SIGNATURE HOME PAGE
# "AI INTERVIEW COCKPIT" EXPERIENCE
# ============================================================

st.set_page_config(
    page_title="Mirai AI — Your Personal AI Interview Coach",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

def render_html(content):
    st.html(textwrap.dedent(content))

# ============================================================
# SIGNATURE UI
# ============================================================

render_html("""
<style>
:root {
    --bg: #F7F8FC;
    --panel: #FFFFFF;
    --panel-2: #F0F1F8;
    --line: rgba(35,39,70,.10);
    --white: #20243A;
    --muted: #6F758D;
    --purple: #8B7CFF;
    --purple-2: #B6AEFF;
    --cyan: #66E4D5;
    --pink: #FF72B6;
    --lime: #B9F36B;
}

html, body, [data-testid="stAppViewContainer"] {
    background: #F7F8FC !important;
}

.stApp {
    background:
        radial-gradient(circle at 8% 7%, rgba(139,124,255,.13), transparent 25%),
        radial-gradient(circle at 93% 17%, rgba(102,228,213,.08), transparent 23%),
        #070811 !important;
    color: #20243A !important;
}

[data-testid="stSidebar"] { display: none; }

.block-container {
    max-width: 1260px;
    padding: 1rem 2rem 5rem;
}

/* ---------- TOP BAR ---------- */

.topbar {
    display:flex;
    align-items:center;
    justify-content:space-between;
    height:58px;
    position:relative;
    z-index:5;
}

.logo {
    color:#20243A;
    font-size:24px;
    font-weight:900;
    letter-spacing:-1.2px;
}

.logo-mark {
    display:inline-flex;
    width:31px;
    height:31px;
    align-items:center;
    justify-content:center;
    margin-right:7px;
    border-radius:10px;
    background:linear-gradient(135deg,#8B7CFF,#5D50D9);
    box-shadow:0 0 25px rgba(139,124,255,.30);
    font-size:16px;
}

.logo span { color:var(--purple-2); }

.top-status {
    display:flex;
    align-items:center;
    gap:8px;
    color:#9DA3BC;
    font-size:11px;
    letter-spacing:.7px;
    text-transform:uppercase;
}

.live-dot {
    width:7px;
    height:7px;
    border-radius:50%;
    background:var(--cyan);
    box-shadow:0 0 12px var(--cyan);
}

/* ---------- HERO ---------- */

.hero-wrap {
    position:relative;
    min-height:710px;
    margin-top:12px;
    overflow:hidden;
    border:1px solid rgba(43,48,82,.10);
    border-radius:34px;
    background:
        radial-gradient(circle at 50% 50%, rgba(139,124,255,.11), transparent 31%),
        radial-gradient(circle at 82% 10%, rgba(102,228,213,.07), transparent 25%),
        linear-gradient(145deg,#0A0C18,#0B0D19 52%,#090B15);
    box-shadow:0 35px 120px rgba(0,0,0,.42);
}

.grid {
    position:absolute;
    inset:0;
    opacity:.22;
    background-image:
        linear-gradient(rgba(255,255,255,.055) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,.055) 1px, transparent 1px);
    background-size:52px 52px;
    mask-image:linear-gradient(to bottom,black,transparent 88%);
}

.hero-copy {
    position:relative;
    z-index:3;
    padding:76px 70px 0;
    max-width:760px;
}

.kicker {
    display:inline-flex;
    align-items:center;
    gap:8px;
    padding:8px 12px;
    border:1px solid rgba(139,124,255,.34);
    border-radius:999px;
    background:rgba(139,124,255,.08);
    color:#BEB7FF;
    font-size:10px;
    font-weight:900;
    letter-spacing:1.7px;
    text-transform:uppercase;
}

.hero-title {
    margin:25px 0 20px;
    color:#20243A;
    font-size:clamp(53px,7vw,91px);
    line-height:.91;
    letter-spacing:-5.5px;
    font-weight:950;
}

.hero-title .ghost {
    color:transparent;
    -webkit-text-stroke:1px rgba(255,255,255,.25);
}

.hero-title .gradient {
    background:linear-gradient(100deg,#6758D8 0%,#7B6CF2 45%,#20A99A 100%);
    -webkit-background-clip:text;
    background-clip:text;
    -webkit-text-fill-color:transparent;
}

.hero-description {
    max-width:570px;
    color:#687089;
    font-size:16px;
    line-height:1.75;
}

.hero-description strong { color:#3A3E58; }

/* ---------- CENTRAL AI ORB ---------- */

.orb-stage {
    position:absolute;
    right:54px;
    top:78px;
    width:455px;
    height:455px;
}

.ring {
    position:absolute;
    inset:12%;
    border:1px solid rgba(139,124,255,.28);
    border-radius:50%;
    box-shadow:0 0 50px rgba(139,124,255,.08);
}

.ring.r2 {
    inset:25%;
    border-color:rgba(102,228,213,.22);
}

.ring.r3 {
    inset:37%;
    border-color:rgba(255,114,182,.22);
}

.orb {
    position:absolute;
    width:128px;
    height:128px;
    left:50%;
    top:50%;
    transform:translate(-50%,-50%);
    border-radius:50%;
    background:
        radial-gradient(circle at 34% 28%,#D9D4FF 0 3%,transparent 4%),
        radial-gradient(circle at 60% 40%,#9B8FFF 0 10%,transparent 11%),
        radial-gradient(circle at 42% 65%,#5E51D6 0 20%,transparent 21%),
        radial-gradient(circle at 50% 50%,#201C50,#0D0F20 72%);
    border:1px solid rgba(255,255,255,.18);
    box-shadow:
        0 0 45px rgba(139,124,255,.42),
        0 0 110px rgba(139,124,255,.16);
}

.orb:after {
    content:"M";
    position:absolute;
    inset:0;
    display:flex;
    align-items:center;
    justify-content:center;
    color:white;
    font-size:42px;
    font-weight:950;
    opacity:.88;
}

.signal {
    position:absolute;
    padding:9px 12px;
    border:1px solid rgba(255,255,255,.10);
    border-radius:13px;
    background:rgba(255,255,255,.88);
    box-shadow:0 12px 35px rgba(53,57,91,.10);
    backdrop-filter:blur(12px);
    color:#646A82;
    font-size:10px;
    letter-spacing:.3px;
}

.signal b {
    display:block;
    margin-top:4px;
    color:#20243A;
    font-size:12px;
}

.signal.s1 { left:0; top:22%; }
.signal.s2 { right:0; top:42%; }
.signal.s3 { left:13%; bottom:14%; }
.signal.s4 { right:11%; bottom:8%; }

.signal .green { color:var(--cyan); }
.signal .purple { color:var(--purple-2); }
.signal .pink { color:var(--pink); }

/* ---------- HERO META ---------- */

.hero-meta {
    position:absolute;
    left:70px;
    bottom:50px;
    display:flex;
    gap:10px;
    z-index:3;
}

.meta {
    padding:11px 14px;
    border:1px solid rgba(43,48,82,.10);
    border-radius:13px;
    background:rgba(255,255,255,.68);
    color:#747B91;
    font-size:10px;
}

.meta b {
    display:block;
    color:#454A63;
    font-size:12px;
    margin-bottom:3px;
}

/* ---------- BUTTONS ---------- */

/* Keep the rest of the page untouched.
   Only these three navigation buttons get stronger,
   light-friendly backgrounds and readable text. */

.hero-buttons {
    position:relative;
    z-index:5;
    max-width:440px;
    margin:34px 0 0 70px;
}

.hero-buttons .stButton > button {
    min-height:52px !important;
    border-radius:13px !important;
    font-weight:800 !important;
    background:#7C5CE7 !important;
    color:#FFFFFF !important;
    border:1px solid #7C5CE7 !important;
    box-shadow:0 8px 22px rgba(124,92,231,.20) !important;
}

.hero-buttons .stButton > button:hover {
    background:#6D4BD8 !important;
    color:#FFFFFF !important;
    border-color:#6D4BD8 !important;
}

/* Create Account — stronger purple background */
.hero-buttons div:nth-child(2) .stButton > button {
    background:#7C5CE7 !important;
    color:#FFFFFF !important;
    border-color:#7C5CE7 !important;
    box-shadow:0 8px 22px rgba(124,92,231,.20) !important;
}

.hero-buttons div:nth-child(2) .stButton > button:hover {
    background:#6D4BD8 !important;
    color:#FFFFFF !important;
}

/* Bottom Start Your Mirai Journey button */
.final ~ div .stButton > button {
    min-height:52px !important;
    border-radius:13px !important;
    background:#7C5CE7 !important;
    color:#FFFFFF !important;
    border:1px solid #7C5CE7 !important;
    font-weight:850 !important;
    box-shadow:0 8px 22px rgba(124,92,231,.20) !important;
}

.final ~ div .stButton > button:hover {
    background:#6D4BD8 !important;
    color:#FFFFFF !important;
}

/* ---------- SECTION HEAD ---------- */

.section {
    padding:105px 0 20px;
}

.section-head {
    display:flex;
    justify-content:space-between;
    align-items:end;
    gap:30px;
    margin-bottom:34px;
}

.section-kicker {
    color:#8D81FF;
    font-size:10px;
    font-weight:900;
    letter-spacing:1.7px;
    text-transform:uppercase;
}

.section-title {
    color:#20243A;
    font-size:clamp(31px,4vw,51px);
    line-height:1;
    letter-spacing:-2.8px;
    font-weight:900;
    margin-top:9px;
}

.section-desc {
    max-width:470px;
    color:#70768B;
    line-height:1.7;
    font-size:14px;
}

/* ---------- FEATURE TILES ---------- */

.tile {
    min-height:275px;
    padding:27px;
    border:1px solid rgba(43,48,82,.10);
    border-radius:24px;
    background:linear-gradient(145deg,#FFFFFF,#F7F8FC);
    position:relative;
    overflow:hidden;
}

.tile:before {
    content:"";
    position:absolute;
    width:170px;
    height:170px;
    right:-80px;
    top:-80px;
    border-radius:50%;
    background:rgba(139,124,255,.09);
}

.tile-num {
    color:#5E637D;
    font-family:monospace;
    font-size:11px;
}

.tile-icon {
    margin-top:32px;
    font-size:28px;
}

.tile-title {
    margin-top:18px;
    color:#20243A;
    font-size:19px;
    font-weight:850;
}

.tile-copy {
    margin-top:9px;
    color:#747B91;
    font-size:13px;
    line-height:1.7;
}

/* ---------- INTERVIEW TIMELINE ---------- */

.timeline {
    margin-top:45px;
    padding:30px;
    border:1px solid rgba(43,48,82,.10);
    border-radius:25px;
    background:#FFFFFF;
}

.timeline-row {
    display:flex;
    align-items:center;
    gap:15px;
    padding:16px 0;
    border-bottom:1px solid rgba(255,255,255,.06);
}

.timeline-row:last-child { border-bottom:0; }

.timeline-dot {
    width:10px;
    height:10px;
    flex:0 0 10px;
    border-radius:50%;
    background:#8B7CFF;
    box-shadow:0 0 14px rgba(139,124,255,.55);
}

.timeline-dot.cyan { background:var(--cyan); box-shadow:0 0 14px rgba(102,228,213,.45); }
.timeline-dot.pink { background:var(--pink); box-shadow:0 0 14px rgba(255,114,182,.45); }

.timeline-name {
    width:160px;
    color:#343952;
    font-size:13px;
    font-weight:800;
}

.timeline-copy {
    color:#70768B;
    font-size:12px;
}

/* ---------- AI REPORT ---------- */

.report {
    margin-top:105px;
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:18px;
    padding:18px;
    border:1px solid rgba(43,48,82,.10);
    border-radius:28px;
    background:#FFFFFF;
}

.report-left {
    padding:35px;
    border-radius:20px;
    background:
        radial-gradient(circle at 80% 20%,rgba(139,124,255,.15),transparent 35%),
        #111429;
}

.report-right {
    padding:25px;
    border-radius:20px;
    background:#F8F9FC;
}

.report-title {
    color:#20243A;
    font-size:33px;
    line-height:1.05;
    letter-spacing:-1.8px;
    font-weight:900;
}

.report-copy {
    margin-top:14px;
    color:#747B91;
    line-height:1.7;
    font-size:13px;
}

.question-card {
    margin-top:30px;
    padding:18px;
    border:1px solid rgba(43,48,82,.10);
    border-radius:16px;
    background:rgba(255,255,255,.68);
    color:#454A63;
    line-height:1.7;
    font-size:13px;
}

.question-label {
    color:#9185FF;
    font-size:9px;
    font-weight:900;
    letter-spacing:1.4px;
}

.report-row {
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding:17px 0;
    border-bottom:1px solid rgba(255,255,255,.06);
}

.report-row:last-child { border-bottom:0; }

.report-label { color:#858CA4; font-size:12px; }

.report-score {
    color:#20243A;
    font-size:18px;
    font-weight:900;
}

.bar {
    width:42%;
    height:6px;
    margin-left:auto;
    margin-right:16px;
    border-radius:99px;
    background:#242840;
    overflow:hidden;
}

.bar span {
    display:block;
    height:100%;
    border-radius:99px;
    background:linear-gradient(90deg,#8174FF,#66E4D5);
}

/* ---------- CTA ---------- */

.final {
    margin-top:105px;
    padding:80px 30px;
    text-align:center;
    border:1px solid rgba(139,124,255,.20);
    border-radius:32px;
    background:
        radial-gradient(circle at 50% 0%,rgba(139,124,255,.19),transparent 42%),
        linear-gradient(180deg,#111329,#0B0D18);
}

.final-kicker {
    color:#A69CFF;
    font-size:10px;
    font-weight:900;
    letter-spacing:1.8px;
}

.final-title {
    margin-top:14px;
    color:#20243A;
    font-size:clamp(37px,5vw,62px);
    font-weight:950;
    line-height:.98;
    letter-spacing:-3.2px;
}

.final-copy {
    max-width:590px;
    margin:18px auto 28px;
    color:#747B91;
    font-size:14px;
    line-height:1.75;
}

.footer {
    text-align:center;
    color:#7A8094;
    font-size:11px;
    padding:35px 0 5px;
}

/* ---------- MOBILE ---------- */

@media (max-width:900px) {
    .hero-wrap { min-height:900px; }
    .hero-copy { padding:55px 30px 0; }
    .orb-stage {
        position:relative;
        right:auto;
        top:auto;
        margin:40px auto 0;
        width:min(420px,90vw);
        height:420px;
    }
    .hero-meta { left:30px; bottom:30px; flex-wrap:wrap; }
    .hero-buttons { margin-left:30px; margin-right:30px; }
    .report { grid-template-columns:1fr; }
}

@media (max-width:600px) {
    .block-container { padding-left:12px; padding-right:12px; }
    .hero-wrap { border-radius:24px; }
    .hero-title { letter-spacing:-3px; }
    .top-status { display:none; }
    .orb-stage { transform:scale(.86); margin-left:auto; margin-right:auto; }
    .hero-meta { display:none; }
    .section { padding-top:75px; }
    .section-head { display:block; }
}


/* SIGN IN + CREATE ACCOUNT — same exact background */
.st-key-hero_buttons .stButton > button {
    background: #7C5CE7 !important;
    background-color: #7C5CE7 !important;
    color: #FFFFFF !important;
    border: 1px solid #7C5CE7 !important;
    box-shadow: 0 8px 22px rgba(124,92,231,.20) !important;
}

.st-key-hero_buttons .stButton > button:hover {
    background: #6D4BD8 !important;
    background-color: #6D4BD8 !important;
    color: #FFFFFF !important;
    border-color: #6D4BD8 !important;
}

</style>
""")

# ============================================================
# TOP BAR
# ============================================================

render_html("""
<div class="topbar">
    <div class="logo">
        <span class="logo-mark">✦</span>Mirai<span> AI</span>
    </div>
    <div class="top-status">
        <span class="live-dot"></span>
        Interview engine online
    </div>
</div>
""")

# ============================================================
# HERO — AI INTERVIEW COCKPIT
# ============================================================

render_html("""
<div class="hero-wrap">
    <div class="grid"></div>

    <div class="hero-copy">
        <div class="kicker">✦ PERSONAL AI INTERVIEW COACH</div>

        <div class="hero-title">
            DON'T JUST<br>
            <span class="ghost">PREPARE.</span><br>
            <span class="gradient">EVOLVE.</span>
        </div>

        <div class="hero-description">
            Mirai turns your profile, answers and performance into
            <strong>one living interview system</strong> that gets smarter
            with every practice session.
        </div>
    </div>

    <div class="orb-stage">
        <div class="ring"></div>
        <div class="ring r2"></div>
        <div class="ring r3"></div>
        <div class="orb"></div>

        <div class="signal s1">
            LIVE SIGNAL
            <b class="green">● Interview ready</b>
        </div>

        <div class="signal s2">
            NEXT MOVE
            <b class="purple">Adaptive question</b>
        </div>

        <div class="signal s3">
            PROFILE
            <b>AI / ML · Fresher</b>
        </div>

        <div class="signal s4">
            SCORE
            <b class="pink">82% ↑</b>
        </div>
    </div>

    <div class="hero-meta">
        <div class="meta"><b>01 · PROFILE</b>Know the candidate</div>
        <div class="meta"><b>02 · SIMULATE</b>Ask the right question</div>
        <div class="meta"><b>03 · ANALYZE</b>Turn answers into progress</div>
    </div>
</div>
""")

# Hero actions stay functional and intentionally simple.
with st.container(key="hero_buttons"):
    c1, c2 = st.columns([1, 1])

    with c1:
        if st.button("🔐 Sign In", use_container_width=True):
            st.session_state.main_app_active = True
            st.session_state.page = "login"
            st.switch_page("app.py")

    with c2:
        if st.button("✨ Create Account", type="primary", use_container_width=True):
            st.session_state.main_app_active = True
            st.session_state.page = "signup"
            st.switch_page("app.py")

# ============================================================
# SECTION 01 — WHY MIRAI
# ============================================================

render_html("""
<div class="section">
    <div class="section-head">
        <div>
            <div class="section-kicker">01 / THE SYSTEM</div>
            <div class="section-title">A mock interview<br>that actually adapts.</div>
        </div>
        <div class="section-desc">
            Forget the endless list of generic questions.
            Mirai builds the interview around the person sitting in front of it.
        </div>
    </div>
</div>
""")

a, b, c = st.columns(3)

cards = [
    ("01", "🧠", "Know you first", "Your education, target role, experience and skills become the starting signal for the interview."),
    ("02", "⚡", "React to your answer", "The experience is built around answering, evaluating and improving — not just clicking through questions."),
    ("03", "📡", "Turn signals into progress", "Feedback, scores and interview history give you a trail you can actually learn from."),
]

for col, (num, icon, title, copy) in zip((a, b, c), cards):
    with col:
        render_html(f"""
        <div class="tile">
            <div class="tile-num">{num} / 03</div>
            <div class="tile-icon">{icon}</div>
            <div class="tile-title">{title}</div>
            <div class="tile-copy">{copy}</div>
        </div>
        """)

# ============================================================
# SECTION 02 — INTERVIEW FLOW
# ============================================================

render_html("""
<div class="section">
    <div class="section-head">
        <div>
            <div class="section-kicker">02 / THE LOOP</div>
            <div class="section-title">Every answer<br>creates a signal.</div>
        </div>
        <div class="section-desc">
            Your preparation isn't a straight line.
            It's a loop: profile → interview → evaluation → improvement → repeat.
        </div>
    </div>

    <div class="timeline">
        <div class="timeline-row">
            <div class="timeline-dot"></div>
            <div class="timeline-name">PROFILE</div>
            <div class="timeline-copy">Role, education, experience, technical skills and career goal.</div>
        </div>

        <div class="timeline-row">
            <div class="timeline-dot cyan"></div>
            <div class="timeline-name">INTERVIEW</div>
            <div class="timeline-copy">Enter the simulated interview and answer questions in your own words.</div>
        </div>

        <div class="timeline-row">
            <div class="timeline-dot pink"></div>
            <div class="timeline-name">EVALUATION</div>
            <div class="timeline-copy">Your answer becomes structured feedback instead of disappearing after the session.</div>
        </div>

        <div class="timeline-row">
            <div class="timeline-dot"></div>
            <div class="timeline-name">PROGRESS</div>
            <div class="timeline-copy">Use your results and history to decide what to improve next.</div>
        </div>
    </div>
</div>
""")

# ============================================================
# SECTION 03 — LIVE AI REPORT
# ============================================================

render_html("""
<div class="report">
    <div class="report-left">
        <div class="section-kicker">03 / INSIDE MIRAI</div>
        <div class="report-title">See what the AI sees.</div>

        <div class="report-copy">
            A good interview tool shouldn't stop at “correct” or “wrong”.
            It should help you understand the quality of the answer.
        </div>

        <div class="question-card">
            <div class="question-label">MIRAI GENERATED QUESTION</div>
            <br>
            Explain how you would detect overfitting in a machine learning
            model and what techniques you would use to prevent it.
        </div>
    </div>

    <div class="report-right">
        <div class="section-kicker">ANSWER SIGNALS</div>

        <div class="report-row">
            <div class="report-label">Technical understanding</div>
            <div class="bar"><span style="width:82%"></span></div>
            <div class="report-score">82</div>
        </div>

        <div class="report-row">
            <div class="report-label">Communication</div>
            <div class="bar"><span style="width:76%"></span></div>
            <div class="report-score">76</div>
        </div>

        <div class="report-row">
            <div class="report-label">Problem solving</div>
            <div class="bar"><span style="width:79%"></span></div>
            <div class="report-score">79</div>
        </div>

        <div class="report-row">
            <div class="report-label">Answer structure</div>
            <div class="bar"><span style="width:84%"></span></div>
            <div class="report-score">84</div>
        </div>
    </div>
</div>
""")

# ============================================================
# SECTION 04 — FINAL CTA
# ============================================================

render_html("""
<div class="final">
    <div class="final-kicker">04 / YOUR TURN</div>
    <div class="final-title">
        Walk in prepared.<br>
        Walk out better.
    </div>
    <div class="final-copy">
        Build your profile. Step into the interview.
        Learn from every answer. Let Mirai become the place
        where your next version is trained.
    </div>
</div>
""")

cta_left, cta_mid, cta_right = st.columns([1, 1.3, 1])

with cta_mid:
    if st.button(
        "🚀 Start Your Mirai Journey",
        type="primary",
        use_container_width=True,
    ):
        st.session_state.main_app_active = True
        st.session_state.page = "welcome"
        st.switch_page("app.py")

render_html("""
<div class="footer">
    MIRAI AI · YOUR PERSONAL AI INTERVIEW COACH
    <br><br>
    Prepare smarter. Interview better.
</div>
""")