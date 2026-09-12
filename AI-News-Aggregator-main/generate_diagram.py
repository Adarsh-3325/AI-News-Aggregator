import os

svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1140" width="100%" height="100%" style="background-color: #FFFFFF; font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">

  <defs>
    <!-- Arrowhead markers -->
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#475569" />
    </marker>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#2563EB" />
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#059669" />
    </marker>
    <marker id="arrow-purple" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#6366F1" />
    </marker>

    <!-- Subtle Shadows -->
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0F172A" flood-opacity="0.06" />
    </filter>
    <filter id="shadow-lg" x="-8%" y="-8%" width="116%" height="116%">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#4338CA" flood-opacity="0.12" />
    </filter>

    <!-- Gradients -->
    <linearGradient id="header-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0F172A"/>
      <stop offset="50%" stop-color="#1E1B4B"/>
      <stop offset="100%" stop-color="#312E81"/>
    </linearGradient>

    <linearGradient id="agent-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FAFAFF"/>
      <stop offset="100%" stop-color="#F0F3FF"/>
    </linearGradient>

    <linearGradient id="banner-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#059669"/>
      <stop offset="50%" stop-color="#0D9488"/>
      <stop offset="100%" stop-color="#0284C7"/>
    </linearGradient>
  </defs>

  <!-- ============================================================ -->
  <!-- HEADER SECTION -->
  <!-- ============================================================ -->
  <rect x="30" y="20" width="1540" height="90" rx="14" fill="url(#header-grad)" filter="url(#shadow)" />
  <text x="50" y="54" fill="#FFFFFF" font-size="24" font-weight="800" letter-spacing="-0.5px">AI News Intelligence &amp; Agentic RAG Platform</text>
  <text x="50" y="80" fill="#93C5FD" font-size="14" font-weight="600">Architecture Flow Diagram (Python Only)</text>
  
  <rect x="1050" y="42" width="500" height="34" rx="17" fill="rgba(255, 255, 255, 0.12)" />
  <text x="1300" y="64" fill="#E0E7FF" font-size="12" font-weight="600" text-anchor="middle">Autonomous News Ingestion  |  Agentic RAG  |  Personalized Delivery</text>

  <!-- ============================================================ -->
  <!-- SECTION 1: DATA SOURCES -->
  <!-- ============================================================ -->
  <g transform="translate(30, 130)">
    <rect x="0" y="0" width="340" height="240" rx="12" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5" filter="url(#shadow)"/>
    <rect x="0" y="0" width="340" height="42" rx="12" fill="#0D9488" />
    <!-- Round bottom corners fix -->
    <rect x="0" y="30" width="340" height="12" fill="#0D9488" />
    <text x="16" y="27" fill="#FFFFFF" font-size="15" font-weight="700">1. Data Sources (Ingestion)</text>

    <!-- Source Items -->
    <!-- Google News -->
    <rect x="14" y="54" width="312" height="38" rx="8" fill="#FFFFFF" stroke="#E2E8F0"/>
    <circle cx="34" cy="73" r="10" fill="#EA4335"/>
    <text x="34" y="77" fill="#FFF" font-size="10" font-weight="800" text-anchor="middle">G</text>
    <text x="54" y="71" fill="#0F172A" font-size="13" font-weight="700">Google News RSS</text>
    <text x="54" y="84" fill="#64748B" font-size="11">Latest news articles</text>

    <!-- YouTube -->
    <rect x="14" y="98" width="312" height="38" rx="8" fill="#FFFFFF" stroke="#E2E8F0"/>
    <rect x="24" y="107" width="20" height="14" rx="3" fill="#FF0000"/>
    <polygon points="31,111 37,114 31,117" fill="#FFF"/>
    <text x="54" y="115" fill="#0F172A" font-size="13" font-weight="700">YouTube</text>
    <text x="54" y="128" fill="#64748B" font-size="11">Video transcripts</text>

    <!-- Open Meteo -->
    <rect x="14" y="142" width="312" height="38" rx="8" fill="#FFFFFF" stroke="#E2E8F0"/>
    <circle cx="34" cy="161" r="10" fill="#0284C7"/>
    <text x="34" y="165" fill="#FFF" font-size="10" font-weight="800" text-anchor="middle">W</text>
    <text x="54" y="159" fill="#0F172A" font-size="13" font-weight="700">Open-Meteo</text>
    <text x="54" y="172" fill="#64748B" font-size="11">Weather data &amp; forecasts</text>

    <!-- Other Sources -->
    <rect x="14" y="186" width="312" height="38" rx="8" fill="#FFFFFF" stroke="#E2E8F0"/>
    <circle cx="34" cy="205" r="10" fill="#8B5CF6"/>
    <text x="34" y="209" fill="#FFF" font-size="10" font-weight="800" text-anchor="middle">+</text>
    <text x="54" y="203" fill="#0F172A" font-size="13" font-weight="700">Other Sources</text>
    <text x="54" y="216" fill="#64748B" font-size="11">Tech, Markets, Startups, etc.</text>
  </g>

  <!-- Arrow: Sec 1 -> Sec 2 -->
  <path d="M 370 250 L 400 250" stroke="#0D9488" stroke-width="2.5" marker-end="url(#arrow)" />

  <!-- ============================================================ -->
  <!-- SECTION 2: INGESTION PIPELINE -->
  <!-- ============================================================ -->
  <g transform="translate(410, 130)">
    <rect x="0" y="0" width="330" height="240" rx="12" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5" filter="url(#shadow)"/>
    <rect x="0" y="0" width="330" height="42" rx="12" fill="#4F46E5" />
    <rect x="0" y="30" width="330" height="12" fill="#4F46E5" />
    <text x="16" y="27" fill="#FFFFFF" font-size="15" font-weight="700">2. Ingestion Pipeline (ETL + Processing)</text>

    <!-- Vertical Flow Cards -->
    <rect x="20" y="52" width="290" height="34" rx="6" fill="#EEF2FF" stroke="#C7D2FE"/>
    <text x="30" y="73" fill="#3730A3" font-size="12" font-weight="700">Fetch &amp; Parse</text>
    <text x="290" y="73" fill="#4338CA" font-size="11" text-anchor="end">RSS, APIs, Scrapers</text>

    <path d="M 165 86 L 165 96" stroke="#6366F1" stroke-width="2" marker-end="url(#arrow-purple)"/>

    <rect x="20" y="98" width="290" height="34" rx="6" fill="#EEF2FF" stroke="#C7D2FE"/>
    <text x="30" y="119" fill="#3730A3" font-size="12" font-weight="700">Clean &amp; Normalize</text>
    <text x="290" y="119" fill="#4338CA" font-size="11" text-anchor="end">Remove noise, deduplicate</text>

    <path d="M 165 132 L 165 142" stroke="#6366F1" stroke-width="2" marker-end="url(#arrow-purple)"/>

    <rect x="20" y="144" width="290" height="34" rx="6" fill="#EEF2FF" stroke="#C7D2FE"/>
    <text x="30" y="165" fill="#3730A3" font-size="12" font-weight="700">Extract Metadata</text>
    <text x="290" y="165" fill="#4338CA" font-size="11" text-anchor="end">title, source, date, category</text>

    <path d="M 165 178 L 165 188" stroke="#6366F1" stroke-width="2" marker-end="url(#arrow-purple)"/>

    <rect x="20" y="190" width="290" height="38" rx="6" fill="#312E81"/>
    <text x="30" y="213" fill="#FFFFFF" font-size="12" font-weight="700">Generate Summary</text>
    <rect x="210" y="197" width="90" height="22" rx="11" fill="#6366F1"/>
    <text x="255" y="212" fill="#FFF" font-size="11" font-weight="700" text-anchor="middle">LLM — Groq</text>
  </g>

  <!-- Arrow: Sec 2 -> Sec 3 -->
  <path d="M 740 250 L 770 250" stroke="#4F46E5" stroke-width="2.5" marker-end="url(#arrow)" />

  <!-- ============================================================ -->
  <!-- SECTION 3: EMBEDDING GENERATION -->
  <!-- ============================================================ -->
  <g transform="translate(780, 130)">
    <rect x="0" y="0" width="340" height="240" rx="12" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5" filter="url(#shadow)"/>
    <rect x="0" y="0" width="340" height="42" rx="12" fill="#D97706" />
    <rect x="0" y="30" width="340" height="12" fill="#D97706" />
    <text x="16" y="27" fill="#FFFFFF" font-size="15" font-weight="700">3. Embedding Generation (FastEmbed)</text>

    <!-- Flow -->
    <rect x="20" y="52" width="300" height="34" rx="6" fill="#FFFBEB" stroke="#FDE68A"/>
    <text x="30" y="73" fill="#92400E" font-size="12" font-weight="700">Text (Article / Query)</text>

    <path d="M 170 86 L 170 96" stroke="#D97706" stroke-width="2" marker-end="url(#arrow)"/>

    <rect x="20" y="98" width="300" height="48" rx="8" fill="#D97706"/>
    <text x="30" y="118" fill="#FFFFFF" font-size="13" font-weight="800">FastEmbed</text>
    <text x="30" y="135" fill="#FEF3C7" font-size="11">BAAI/bge-small-en-v1.5</text>
    <rect x="185" y="110" width="125" height="24" rx="12" fill="rgba(255,255,255,0.2)"/>
    <text x="247" y="126" fill="#FFF" font-size="10" font-weight="700" text-anchor="middle">Local (No API cost)</text>

    <path d="M 170 146 L 170 156" stroke="#D97706" stroke-width="2" marker-end="url(#arrow)"/>

    <rect x="20" y="158" width="300" height="66" rx="8" fill="#FFFBEB" stroke="#FDE68A"/>
    <text x="30" y="178" fill="#92400E" font-size="12" font-weight="700">384-dimensional Embedding Vector</text>
    <rect x="30" y="186" width="280" height="26" rx="4" fill="#FFFFFF" stroke="#FEF3C7"/>
    <text x="170" y="203" fill="#B45309" font-family="monospace" font-size="11" text-anchor="middle">[0.12, -0.43, 0.87, 0.34, ...]</text>
  </g>

  <!-- Arrow: Sec 3 -> Sec 4 -->
  <path d="M 1120 250 L 1150 250" stroke="#D97706" stroke-width="2.5" marker-end="url(#arrow)" />

  <!-- ============================================================ -->
  <!-- SECTION 4: STORAGE LAYER -->
  <!-- ============================================================ -->
  <g transform="translate(1160, 130)">
    <rect x="0" y="0" width="410" height="240" rx="12" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5" filter="url(#shadow)"/>
    <rect x="0" y="0" width="410" height="42" rx="12" fill="#2563EB" />
    <rect x="0" y="30" width="410" height="12" fill="#2563EB" />
    <text x="16" y="27" fill="#FFFFFF" font-size="15" font-weight="700">4. Storage Layer</text>

    <!-- Card 1: PostgreSQL -->
    <g transform="translate(14, 52)">
      <rect x="0" y="0" width="185" height="174" rx="8" fill="#FFFFFF" stroke="#BFDBFE" stroke-width="1.5"/>
      <rect x="0" y="0" width="185" height="30" rx="8" fill="#DBEAFE"/>
      <text x="10" y="20" fill="#1E40AF" font-size="13" font-weight="800">PostgreSQL</text>
      <text x="175" y="20" fill="#2563EB" font-size="10" font-weight="700" text-anchor="end">Relational Data</text>

      <text x="12" y="48" fill="#334155" font-size="11" font-weight="600">• Users &amp; Preferences</text>
      <text x="12" y="68" fill="#334155" font-size="11" font-weight="600">• Articles Metadata</text>
      <text x="12" y="88" fill="#334155" font-size="11" font-weight="600">• LLM Summaries / Digests</text>
      <text x="12" y="108" fill="#334155" font-size="11" font-weight="600">• Agent Runs &amp; Logs</text>
      <text x="12" y="128" fill="#334155" font-size="11" font-weight="600">• Email Schedules &amp; Logs</text>
      <rect x="10" y="142" width="165" height="22" rx="4" fill="#EFF6FF"/>
      <text x="92" y="157" fill="#1D4ED8" font-size="10" font-weight="700" text-anchor="middle">SQLAlchemy ORM</text>
    </g>

    <!-- Card 2: ChromaDB -->
    <g transform="translate(210, 52)">
      <rect x="0" y="0" width="185" height="174" rx="8" fill="#FFFFFF" stroke="#DDD6FE" stroke-width="1.5"/>
      <rect x="0" y="0" width="185" height="30" rx="8" fill="#EDE9FE"/>
      <text x="10" y="20" fill="#5B21B6" font-size="13" font-weight="800">ChromaDB</text>
      <text x="175" y="20" fill="#7C3AED" font-size="10" font-weight="700" text-anchor="end">Vector Store</text>

      <text x="12" y="48" fill="#334155" font-size="11" font-weight="600">• Article Embeddings</text>
      <text x="12" y="68" fill="#334155" font-size="11" font-weight="600">• Semantic Vector Search</text>
      <text x="12" y="88" fill="#334155" font-size="11" font-weight="600">• Metadata Filtering</text>
      <text x="12" y="108" fill="#334155" font-size="11" font-weight="600">• Persistent Storage</text>
      <text x="12" y="128" fill="#334155" font-size="11" font-weight="600">• Zero API Cost</text>
      <rect x="10" y="142" width="165" height="22" rx="4" fill="#F5F3FF"/>
      <text x="92" y="157" fill="#6D28D9" font-size="10" font-weight="700" text-anchor="middle">HNSW Cosine Index</text>
    </g>
  </g>

  <!-- ============================================================ -->
  <!-- SECTION 6: USER QUERY (Left of LangGraph) -->
  <!-- ============================================================ -->
  <g transform="translate(30, 400)">
    <rect x="0" y="0" width="280" height="400" rx="12" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5" filter="url(#shadow)"/>
    <rect x="0" y="0" width="280" height="42" rx="12" fill="#059669" />
    <rect x="0" y="30" width="280" height="12" fill="#059669" />
    <text x="16" y="27" fill="#FFFFFF" font-size="15" font-weight="700">User Query (Web / App)</text>

    <!-- User Icon Card -->
    <rect x="16" y="54" width="248" height="50" rx="8" fill="#ECFDF5" stroke="#A7F3D0"/>
    <circle cx="42" cy="79" r="14" fill="#10B981"/>
    <circle cx="42" cy="75" r="5" fill="#FFF"/>
    <path d="M 33 87 C 33 81 51 81 51 87" fill="#FFF"/>
    <text x="66" y="75" fill="#065F46" font-size="13" font-weight="700">Interactive User Query</text>
    <text x="66" y="89" fill="#047857" font-size="11">Via Chat UI or REST API</text>

    <text x="16" y="125" fill="#475569" font-size="12" font-weight="700">Example Questions:</text>

    <!-- Question cards -->
    <rect x="16" y="136" width="248" height="52" rx="6" fill="#FFFFFF" stroke="#E2E8F0"/>
    <text x="26" y="157" fill="#0F172A" font-size="11" font-weight="600">“Summarize today's AI news”</text>
    <text x="26" y="174" fill="#64748B" font-size="10">Topic: Frontier AI &amp; LLMs</text>

    <rect x="16" y="196" width="248" height="52" rx="6" fill="#FFFFFF" stroke="#E2E8F0"/>
    <text x="26" y="217" fill="#0F172A" font-size="11" font-weight="600">“What's happening in geopolitics?”</text>
    <text x="26" y="234" fill="#64748B" font-size="10">Topic: World News &amp; Diplomacy</text>

    <rect x="16" y="256" width="248" height="52" rx="6" fill="#FFFFFF" stroke="#E2E8F0"/>
    <text x="26" y="277" fill="#0F172A" font-size="11" font-weight="600">“Explain OpenAI's latest model”</text>
    <text x="26" y="294" fill="#64748B" font-size="10">Topic: Model Releases &amp; Tech</text>

    <rect x="16" y="316" width="248" height="52" rx="6" fill="#FFFFFF" stroke="#E2E8F0"/>
    <text x="26" y="337" fill="#0F172A" font-size="11" font-weight="600">“Compare latest AI announcements”</text>
    <text x="26" y="354" fill="#64748B" font-size="10">Multi-source comparison</text>

    <rect x="16" y="374" width="248" height="18" rx="4" fill="#ECFDF5"/>
    <text x="140" y="387" fill="#047857" font-size="10" font-weight="700" text-anchor="middle">Input Stream → FastAPI Backend</text>
  </g>

  <!-- Arrow: Sec 6 -> Sec 5 -->
  <path d="M 310 600 L 335 600" stroke="#059669" stroke-width="3" marker-end="url(#arrow-green)"/>

  <!-- ============================================================ -->
  <!-- SECTION 5: LANGGRAPH AGENT (CENTERPIECE) -->
  <!-- ============================================================ -->
  <g transform="translate(340, 390)">
    <!-- Outer Card with glow border -->
    <rect x="0" y="0" width="930" height="420" rx="16" fill="url(#agent-bg)" stroke="#6366F1" stroke-width="2.5" filter="url(#shadow-lg)"/>
    
    <!-- Title Header Bar -->
    <rect x="0" y="0" width="930" height="48" rx="16" fill="#312E81" />
    <rect x="0" y="34" width="930" height="14" fill="#312E81" />
    <text x="20" y="30" fill="#FFFFFF" font-size="17" font-weight="800">5. LangGraph Agent (Agentic RAG Workflow) — Visual Centerpiece</text>
    <rect x="740" y="10" width="170" height="28" rx="14" fill="#4338CA"/>
    <text x="825" y="28" fill="#EEF2FF" font-size="11" font-weight="700" text-anchor="middle">StateGraph Engine</text>

    <!-- SUBSECTION A: AGENT TOOLS (Left column inside Agent) -->
    <g transform="translate(16, 62)">
      <rect x="0" y="0" width="245" height="344" rx="10" fill="#FFFFFF" stroke="#C7D2FE" stroke-width="1.5"/>
      <rect x="0" y="0" width="245" height="32" rx="10" fill="#E0E7FF"/>
      <text x="12" y="21" fill="#3730A3" font-size="13" font-weight="800">A. Agent Tools</text>

      <g transform="translate(10, 40)">
        <rect x="0" y="0" width="225" height="42" rx="6" fill="#F5F3FF" stroke="#DDD6FE"/>
        <text x="10" y="18" fill="#5B21B6" font-size="11" font-weight="700">Vector Search Tool</text>
        <text x="10" y="32" fill="#6D28D9" font-size="10">ChromaDB Persistent Store</text>

        <rect x="0" y="48" width="225" height="42" rx="6" fill="#EFF6FF" stroke="#BFDBFE"/>
        <text x="10" y="66" fill="#1E40AF" font-size="11" font-weight="700">Web Search Tool</text>
        <text x="10" y="80" fill="#2563EB" font-size="10">Google CSE / Brave Search API</text>

        <rect x="0" y="96" width="225" height="42" rx="6" fill="#ECFDF5" stroke="#A7F3D0"/>
        <text x="10" y="114" fill="#065F46" font-size="11" font-weight="700">News Retrieval Tool</text>
        <text x="10" y="128" fill="#059669" font-size="10">Google News RSS &amp; Scrapers</text>

        <rect x="0" y="144" width="225" height="42" rx="6" fill="#FEF2F2" stroke="#FECACA"/>
        <text x="10" y="162" fill="#991B1B" font-size="11" font-weight="700">YouTube Transcript Tool</text>
        <text x="10" y="176" fill="#DC2626" font-size="10">Video Subtitles &amp; Key Transcripts</text>

        <rect x="0" y="192" width="225" height="42" rx="6" fill="#F0F9FF" stroke="#BAE6FD"/>
        <text x="10" y="210" fill="#075985" font-size="11" font-weight="700">Weather Tool</text>
        <text x="10" y="224" fill="#0284C7" font-size="10">Open-Meteo Weather API</text>

        <rect x="0" y="240" width="225" height="42" rx="6" fill="#F8FAFC" stroke="#E2E8F0"/>
        <text x="10" y="258" fill="#334155" font-size="11" font-weight="700">Other Tools</text>
        <text x="10" y="272" fill="#64748B" font-size="10">Calculator, Date Parser, Utilities</text>
      </g>
    </g>

    <!-- SUBSECTION B: LANGGRAPH STATEGRAPH FLOW (Middle column inside Agent) -->
    <g transform="translate(275, 62)">
      <rect x="0" y="0" width="425" height="344" rx="10" fill="#FFFFFF" stroke="#C7D2FE" stroke-width="1.5"/>
      <rect x="0" y="0" width="425" height="32" rx="10" fill="#E0E7FF"/>
      <text x="12" y="21" fill="#3730A3" font-size="13" font-weight="800">B. LangGraph StateGraph Decision Workflow</text>

      <!-- Step 1 -->
      <rect x="15" y="42" width="395" height="32" rx="6" fill="#EEF2FF" stroke="#818CF8"/>
      <text x="25" y="62" fill="#312E81" font-size="11" font-weight="700">1. Query Analysis &amp; Routing</text>
      <text x="400" y="62" fill="#4338CA" font-size="10" text-anchor="end">Decide which tools to use</text>

      <path d="M 212 74 L 212 84" stroke="#6366F1" stroke-width="2" marker-end="url(#arrow-purple)"/>

      <!-- Step 2 -->
      <rect x="15" y="86" width="395" height="32" rx="6" fill="#EEF2FF" stroke="#818CF8"/>
      <text x="25" y="106" fill="#312E81" font-size="11" font-weight="700">2. Retrieval</text>
      <text x="400" y="106" fill="#4338CA" font-size="10" text-anchor="end">Vector search from ChromaDB</text>

      <path d="M 212 118 L 212 128" stroke="#6366F1" stroke-width="2" marker-end="url(#arrow-purple)"/>

      <!-- Step 3 Decision Diamond -->
      <polygon points="212,130 330,150 212,170 94,150" fill="#FEF3C7" stroke="#F59E0B" stroke-width="1.5"/>
      <text x="212" y="148" fill="#92400E" font-size="11" font-weight="800" text-anchor="middle">3. Relevance Check</text>
      <text x="212" y="161" fill="#B45309" font-size="9" text-anchor="middle">Is information sufficient?</text>

      <!-- Branching: YES (Down) vs NO (Right/Down) -->
      <!-- YES Branch -->
      <path d="M 140 160 L 140 226 L 15 226 L 15 240" fill="none" stroke="#059669" stroke-width="2" marker-end="url(#arrow-green)"/>
      <rect x="60" y="180" width="70" height="18" rx="4" fill="#D1FAE5"/>
      <text x="95" y="193" fill="#065F46" font-size="10" font-weight="800" text-anchor="middle">YES (Sufficient)</text>

      <!-- NO Branch -->
      <path d="M 280 160 L 280 178 L 330 178 L 330 190" fill="none" stroke="#DC2626" stroke-width="2" marker-end="url(#arrow)"/>
      <rect x="290" y="165" width="75" height="18" rx="4" fill="#FEE2E2"/>
      <text x="327" y="178" fill="#991B1B" font-size="10" font-weight="800" text-anchor="middle">NO (Weak score)</text>

      <!-- Step 4: Live Research -->
      <rect x="235" y="192" width="175" height="38" rx="6" fill="#FEF2F2" stroke="#FCA5A5"/>
      <text x="245" y="208" fill="#991B1B" font-size="11" font-weight="800">4. Live Research (Fallback)</text>
      <text x="245" y="222" fill="#B91C1C" font-size="10">Web Search / Google News API</text>

      <path d="M 322 230 L 322 238 L 212 238 L 212 242" fill="none" stroke="#6366F1" stroke-width="2" marker-end="url(#arrow-purple)"/>

      <!-- Step 5 -->
      <rect x="15" y="244" width="395" height="34" rx="6" fill="#EEF2FF" stroke="#818CF8"/>
      <text x="25" y="265" fill="#312E81" font-size="11" font-weight="700">5. Evidence Verification</text>
      <text x="400" y="265" fill="#4338CA" font-size="10" text-anchor="end">Validate &amp; filter sources</text>

      <path d="M 212 278 L 212 288" stroke="#6366F1" stroke-width="2" marker-end="url(#arrow-purple)"/>

      <!-- Step 6 -->
      <rect x="15" y="290" width="395" height="42" rx="8" fill="#312E81"/>
      <text x="25" y="312" fill="#FFFFFF" font-size="12" font-weight="800">6. Synthesis</text>
      <text x="25" y="325" fill="#C7D2FE" font-size="10">Grounded response with explicit citations</text>
      <rect x="300" y="298" width="100" height="24" rx="12" fill="#6366F1"/>
      <text x="350" y="314" fill="#FFF" font-size="10" font-weight="700" text-anchor="middle">Groq LLM</text>
    </g>

    <!-- RIGHT SIDE OF LANGGRAPH: LLM GROQ CARD -->
    <g transform="translate(714, 62)">
      <rect x="0" y="0" width="200" height="344" rx="10" fill="#FFFFFF" stroke="#F59E0B" stroke-width="1.5"/>
      <rect x="0" y="0" width="200" height="32" rx="10" fill="#FEF3C7"/>
      <text x="12" y="21" fill="#92400E" font-size="13" font-weight="800">LLM — Groq</text>

      <g transform="translate(10, 42)">
        <rect x="0" y="0" width="180" height="50" rx="6" fill="#FFFBEB" stroke="#FDE68A"/>
        <text x="10" y="22" fill="#78350F" font-size="12" font-weight="800">LLaMA 3.3 / Qwen 2.5</text>
        <text x="10" y="38" fill="#B45309" font-size="10">Ultra-fast inference engine</text>

        <rect x="0" y="60" width="180" height="42" rx="6" fill="#F8FAFC" stroke="#E2E8F0"/>
        <text x="10" y="78" fill="#0F172A" font-size="11" font-weight="700">• Fast Inference</text>
        <text x="10" y="93" fill="#64748B" font-size="10">&lt;500ms token generation</text>

        <rect x="0" y="112" width="180" height="42" rx="6" fill="#F8FAFC" stroke="#E2E8F0"/>
        <text x="10" y="130" fill="#0F172A" font-size="11" font-weight="700">• Grounded Synthesis</text>
        <text x="10" y="145" fill="#64748B" font-size="10">No hallucinations/extrapolation</text>

        <rect x="0" y="164" width="180" height="42" rx="6" fill="#F8FAFC" stroke="#E2E8F0"/>
        <text x="10" y="182" fill="#0F172A" font-size="11" font-weight="700">• Source-Aware</text>
        <text x="10" y="197" fill="#64748B" font-size="10">Inline news publication refs</text>

        <rect x="0" y="216" width="180" height="70" rx="6" fill="#FEF3C7" stroke="#F59E0B"/>
        <text x="10" y="235" fill="#78350F" font-size="11" font-weight="800">Zero API Cost Option</text>
        <text x="10" y="250" fill="#92400E" font-size="10">Free tier Groq Cloud API</text>
        <text x="10" y="265" fill="#92400E" font-size="10">High rate-limit capacity</text>
      </g>
    </g>
  </g>

  <!-- Arrow: Sec 5 -> Sec 7 -->
  <path d="M 1270 600 L 1295 600" stroke="#6366F1" stroke-width="3" marker-end="url(#arrow-purple)"/>

  <!-- ============================================================ -->
  <!-- SECTION 7: RESPONSE TO USER (Right of LangGraph) -->
  <!-- ============================================================ -->
  <g transform="translate(1290, 400)">
    <rect x="0" y="0" width="280" height="400" rx="12" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5" filter="url(#shadow)"/>
    <rect x="0" y="0" width="280" height="42" rx="12" fill="#E11D48" />
    <rect x="0" y="30" width="280" height="12" fill="#E11D48" />
    <text x="16" y="27" fill="#FFFFFF" font-size="15" font-weight="700">Response to User</text>

    <!-- Response feature items -->
    <g transform="translate(14, 54)">
      <rect x="0" y="0" width="252" height="55" rx="8" fill="#FFF1F2" stroke="#FECDD3"/>
      <text x="12" y="22" fill="#9F1239" font-size="12" font-weight="800">Concise Fact-Based Answer</text>
      <text x="12" y="40" fill="#BE123C" font-size="11">Hype-free technical summary</text>

      <rect x="0" y="65" width="252" height="55" rx="8" fill="#FFFFFF" stroke="#E2E8F0"/>
      <text x="12" y="87" fill="#0F172A" font-size="12" font-weight="700">Source Citations</text>
      <text x="12" y="105" fill="#64748B" font-size="11">Direct links to original articles</text>

      <rect x="0" y="130" width="252" height="55" rx="8" fill="#FFFFFF" stroke="#E2E8F0"/>
      <text x="12" y="152" fill="#0F172A" font-size="12" font-weight="700">Related Articles</text>
      <text x="12" y="170" fill="#64748B" font-size="11">Cross-topic coverage recommendations</text>

      <rect x="0" y="195" width="252" height="55" rx="8" fill="#FFFFFF" stroke="#E2E8F0"/>
      <text x="12" y="217" fill="#0F172A" font-size="12" font-weight="700">Follow-up Questions</text>
      <text x="12" y="235" fill="#64748B" font-size="11">Suggested query continuations</text>

      <rect x="0" y="260" width="252" height="55" rx="8" fill="#FFFFFF" stroke="#E2E8F0"/>
      <text x="12" y="282" fill="#0F172A" font-size="12" font-weight="700">Real-Time Information</text>
      <text x="12" y="300" fill="#64748B" font-size="11">Up-to-the-minute news freshness</text>
    </g>

    <rect x="14" y="374" width="252" height="18" rx="4" fill="#FFF1F2"/>
    <text x="140" y="387" fill="#9F1239" font-size="10" font-weight="700" text-anchor="middle">Delivered via UI Chat &amp; REST API</text>
  </g>

  <!-- ============================================================ -->
  <!-- SECTION 8: SCHEDULED NEWS DIGEST (Bottom Left) -->
  <!-- ============================================================ -->
  <g transform="translate(30, 830)">
    <rect x="0" y="0" width="450" height="210" rx="12" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5" filter="url(#shadow)"/>
    <rect x="0" y="0" width="450" height="42" rx="12" fill="#0284C7" />
    <rect x="0" y="30" width="450" height="12" fill="#0284C7" />
    <text x="16" y="27" fill="#FFFFFF" font-size="15" font-weight="700">6. Scheduled News Digest (Background Jobs)</text>

    <g transform="translate(16, 54)">
      <rect x="0" y="0" width="200" height="64" rx="8" fill="#F0F9FF" stroke="#BAE6FD"/>
      <text x="12" y="24" fill="#0369A1" font-size="13" font-weight="800">APScheduler</text>
      <text x="12" y="42" fill="#0284C7" font-size="11">Python Async Scheduler</text>
      <text x="12" y="55" fill="#64748B" font-size="10">Cron / Interval triggers</text>

      <rect x="218" y="0" width="200" height="64" rx="8" fill="#FFFFFF" stroke="#E2E8F0"/>
      <text x="230" y="24" fill="#0F172A" font-size="12" font-weight="700">Personalized Digest</text>
      <text x="230" y="42" fill="#64748B" font-size="11">Multi-topic weighting</text>
      <text x="230" y="55" fill="#64748B" font-size="10">Custom user schedules</text>

      <rect x="0" y="74" width="200" height="64" rx="8" fill="#FFFFFF" stroke="#E2E8F0"/>
      <text x="12" y="98" fill="#0F172A" font-size="12" font-weight="700">LLM Summarization</text>
      <text x="12" y="116" fill="#64748B" font-size="11">Batch Groq summarization</text>
      <text x="12" y="129" fill="#64748B" font-size="10">Hype-free curation</text>

      <rect x="218" y="74" width="200" height="64" rx="8" fill="#EFF6FF" stroke="#BFDBFE"/>
      <text x="230" y="98" fill="#1E40AF" font-size="12" font-weight="800">Gmail SMTP</text>
      <text x="230" y="116" fill="#2563EB" font-size="11">HTML email delivery</text>
      <text x="230" y="129" fill="#1D4ED8" font-size="10">Idempotent sent logs</text>
    </g>
  </g>

  <!-- Arrow: Sec 8 -> Sec 9 -->
  <path d="M 480 935 L 510 935" stroke="#0284C7" stroke-width="2.5" marker-end="url(#arrow-blue)"/>

  <!-- ============================================================ -->
  <!-- SECTION 9: FASTAPI BACKEND (Bottom Center) -->
  <!-- ============================================================ -->
  <g transform="translate(520, 830)">
    <rect x="0" y="0" width="560" height="210" rx="12" fill="#F8FAFC" stroke="#0D9488" stroke-width="2" filter="url(#shadow)"/>
    <rect x="0" y="0" width="560" height="42" rx="12" fill="#0D9488" />
    <rect x="0" y="30" width="560" height="12" fill="#0D9488" />
    <text x="16" y="27" fill="#FFFFFF" font-size="15" font-weight="700">7. FastAPI Backend (Python)</text>
    <rect x="420" y="8" width="125" height="26" rx="13" fill="#047857"/>
    <text x="482" y="25" fill="#FFFFFF" font-size="11" font-weight="800" text-anchor="middle">100% Python</text>

    <!-- Grid of Endpoints & Features -->
    <g transform="translate(16, 54)">
      <rect x="0" y="0" width="256" height="40" rx="6" fill="#CCFBF1" stroke="#5EEAD4"/>
      <text x="12" y="24" fill="#0F766E" font-size="12" font-weight="800">REST APIs for Frontend</text>
      <text x="244" y="24" fill="#0D9488" font-size="10" font-weight="600" text-anchor="end">JSON Endpoints</text>

      <rect x="272" y="0" width="256" height="40" rx="6" fill="#FFFFFF" stroke="#E2E8F0"/>
      <text x="284" y="24" fill="#0F172A" font-size="12" font-weight="700">Agent Endpoints</text>
      <text x="516" y="24" fill="#64748B" font-size="11" text-anchor="end">/api/ask, /api/search</text>

      <rect x="0" y="48" width="256" height="40" rx="6" fill="#FFFFFF" stroke="#E2E8F0"/>
      <text x="12" y="72" fill="#0F172A" font-size="12" font-weight="700">User Management</text>
      <text x="244" y="72" fill="#64748B" font-size="11" text-anchor="end">Profiles &amp; Topics</text>

      <rect x="272" y="48" width="256" height="40" rx="6" fill="#FFFFFF" stroke="#E2E8F0"/>
      <text x="284" y="72" fill="#0F172A" font-size="12" font-weight="700">Digest Scheduling</text>
      <text x="516" y="72" fill="#64748B" font-size="11" text-anchor="end">Cron Management</text>

      <rect x="0" y="96" width="256" height="40" rx="6" fill="#FFFFFF" stroke="#E2E8F0"/>
      <text x="12" y="120" fill="#0F172A" font-size="12" font-weight="700">Secure Authentication</text>
      <text x="244" y="120" fill="#64748B" font-size="11" text-anchor="end">JWT Tokens</text>

      <rect x="272" y="96" width="256" height="40" rx="6" fill="#FFFFFF" stroke="#E2E8F0"/>
      <text x="284" y="120" fill="#0F172A" font-size="12" font-weight="700">Background Tasks</text>
      <text x="516" y="120" fill="#64748B" font-size="11" text-anchor="end">Async Execution</text>
    </g>
  </g>

  <!-- Arrow: Sec 9 <-> Sec 10 -->
  <path d="M 1080 935 L 1110 935" stroke="#0D9488" stroke-width="2.5" marker-end="url(#arrow)" />

  <!-- ============================================================ -->
  <!-- SECTION 10: REACT FRONTEND (Bottom Right) -->
  <!-- ============================================================ -->
  <g transform="translate(1120, 830)">
    <rect x="0" y="0" width="450" height="210" rx="12" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5" filter="url(#shadow)"/>
    <rect x="0" y="0" width="450" height="42" rx="12" fill="#2563EB" />
    <rect x="0" y="30" width="450" height="12" fill="#2563EB" />
    <text x="16" y="27" fill="#FFFFFF" font-size="15" font-weight="700">8. Frontend (React + Vite)</text>

    <g transform="translate(16, 54)">
      <rect x="0" y="0" width="200" height="40" rx="6" fill="#EFF6FF" stroke="#BFDBFE"/>
      <text x="12" y="24" fill="#1E40AF" font-size="12" font-weight="700">News Feed UI</text>
      <text x="188" y="24" fill="#2563EB" font-size="10" text-anchor="end">Categorized</text>

      <rect x="218" y="0" width="200" height="40" rx="6" fill="#EFF6FF" stroke="#BFDBFE"/>
      <text x="230" y="24" fill="#1E40AF" font-size="12" font-weight="700">Ask AI Chat Interface</text>
      <text x="406" y="24" fill="#2563EB" font-size="10" text-anchor="end">Agentic RAG</text>

      <rect x="0" y="48" width="200" height="40" rx="6" fill="#FFFFFF" stroke="#E2E8F0"/>
      <text x="12" y="72" fill="#0F172A" font-size="12" font-weight="700">Topic Preferences</text>
      <text x="188" y="72" fill="#64748B" font-size="10" text-anchor="end">Multi-topic</text>

      <rect x="218" y="48" width="200" height="40" rx="6" fill="#FFFFFF" stroke="#E2E8F0"/>
      <text x="230" y="72" fill="#0F172A" font-size="12" font-weight="700">Article Search &amp; Filter</text>
      <text x="406" y="72" fill="#64748B" font-size="10" text-anchor="end">Real-time</text>

      <rect x="0" y="96" width="200" height="40" rx="6" fill="#FFFFFF" stroke="#E2E8F0"/>
      <text x="12" y="120" fill="#0F172A" font-size="12" font-weight="700">Responsive SPA</text>
      <text x="188" y="120" fill="#64748B" font-size="10" text-anchor="end">Tailwind / CSS</text>

      <rect x="218" y="96" width="200" height="40" rx="6" fill="#E0F2FE" stroke="#BAE6FD"/>
      <text x="230" y="120" fill="#0369A1" font-size="12" font-weight="800">React 19 + Vite</text>
      <text x="406" y="120" fill="#0284C7" font-size="10" text-anchor="end">Port 5173</text>
    </g>
  </g>

  <!-- ============================================================ -->
  <!-- BOTTOM GOAL BANNER -->
  <!-- ============================================================ -->
  <g transform="translate(30, 1060)">
    <rect x="0" y="0" width="1540" height="60" rx="12" fill="url(#banner-grad)" filter="url(#shadow)"/>
    <text x="770" y="26" fill="#FFFFFF" font-size="15" font-weight="800" text-anchor="middle">🎯 Goal: Autonomous, Trustworthy, Real-Time News Intelligence with Agentic AI</text>
    <text x="770" y="46" fill="#E0F2FE" font-size="12" font-weight="600" text-anchor="middle">No Express.js  |  No MongoDB  |  Full Python Backend  |  Agentic RAG  |  Real-World Data  |  Production Ready</text>
  </g>

</svg>
'''

output_path = r"c:\Users\adars\Downloads\AI-News-Aggregator-main\AI-News-Aggregator-main\architecture_diagram.svg"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(svg_content)

print(f"Successfully wrote SVG diagram to {output_path}")
