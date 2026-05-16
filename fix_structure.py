import re

with open('/tmp/gosidehustlesisi.github.io/side-hustle.html', 'r') as f:
    content = f.read()

# Add missing CSS classes to the stylesheet
# Check if .chart-box CSS already exists
if '.chart-box {' not in content:
    # Add chart-box CSS before .exec-summary
    chart_box_css = '''        .chart-box {
            background: var(--bg-elevated);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1.5rem 0;
        }
        .chart-insight-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            flex-wrap: wrap;
            gap: 0.5rem;
        }
        .insight-tag {
            background: rgba(245, 158, 11, 0.15);
            color: var(--accent-gold);
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .insight-metric {
            color: var(--accent-cyan);
            font-weight: 700;
            font-size: 0.9rem;
        }
        .chart-caption-headline {
            font-size: 1rem;
            font-weight: 600;
            color: var(--text-primary);
            margin: 1rem 0 0.5rem;
        }
        .chart-insight-body {
            color: var(--text-secondary);
            font-size: 0.9rem;
            line-height: 1.6;
            margin-bottom: 1rem;
        }
        .chart-insight-action {
            margin-top: 1rem;
        }
        .project-footer {
            background: var(--bg-elevated);
            border-top: 1px solid var(--border);
            padding: 1rem 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
            font-size: 0.8rem;
        }
        .data-sources {
            color: var(--text-muted);
        }
        .repo-link {
            color: var(--accent-cyan);
            text-decoration: none;
            font-weight: 600;
            transition: color 0.2s;
        }
        .repo-link:hover {
            color: var(--accent-cyan-hover);
        }
'''
    content = content.replace(
        '        .exec-summary {',
        chart_box_css + '        .exec-summary {'
    )
    print("Added chart-box and project-footer CSS")

# Define project metadata
projects = {
    'NASA C-MAPSS': {
        'repo': 'https://github.com/gosidehustlesisi/sierra-applied-ml',
        'notebook': 'https://github.com/gosidehustlesisi/sierra-applied-ml/blob/main/projects/predictive-maintenance-transit/notebooks/predictive_maintenance_analysis.ipynb',
        'data': 'NASA C-MAPSS · UCI Bike Sharing',
        'iframe': 'https://gosidehustlesisi.github.io/charts/sensor_degradation.html',
        'iframe_title': 'NASA C-MAPSS Interactive Sensor Degradation',
        'iframe_hint': '★ Interactive — Toggle 21 sensors, hover for RUL correlation, click buttons to filter',
        'metric': '94% RUL Accuracy',
        'tag': 'Key Finding',
        'tldr': 'You only need 5 sensors to predict engine failure 25+ cycles before breakdown.',
    },
    '20 Newsgroups': {
        'repo': 'https://github.com/gosidehustlesisi/sierra-applied-ml',
        'notebook': 'https://github.com/gosidehustlesisi/sierra-applied-ml/blob/main/projects/nlp-text-classification-pipeline/notebooks/nlp_classification_analysis.ipynb',
        'data': 'sklearn 20 Newsgroups · CMU Lang (1995)',
        'iframe': 'https://gosidehustlesisi.github.io/charts/nlp_confusion_matrix.html',
        'iframe2': 'https://gosidehustlesisi.github.io/charts/newsgroups_accuracy.html',
        'iframe_title': 'NLP Confusion Matrix Interactive',
        'iframe_title2': '20 Newsgroups Accuracy Interactive',
        'iframe_hint': '★ Interactive — Toggle normalize view, hover cells for precision/recall',
        'iframe_hint2': '★ Interactive — Toggle model comparison, hover for accuracy scores',
        'metric': '67.87% Accuracy',
        'tag': 'Key Finding',
        'tldr': 'Simple beats fancy. TF-IDF + Naive Bayes runs 400× faster than BERT with only 21% accuracy trade-off.',
    },
    'Zeus-URSA': {
        'repo': 'https://github.com/gosidehustlesisi',
        'notebook': None,
        'data': 'Gemini AI Studio · MCP Protocol',
        'iframe': None,
        'metric': None,
        'tag': None,
        'tldr': None,
    },
    'Demand Forecasting': {
        'repo': 'https://github.com/gosidehustlesisi/sierra-applied-ml',
        'notebook': 'https://github.com/gosidehustlesisi/sierra-applied-ml/blob/main/projects/demand-forecasting-operations/notebooks/demand_forecasting.ipynb',
        'data': 'UCI Bike Sharing · USDOT BTS',
        'iframe': 'https://gosidehustlesisi.github.io/charts/ensemble_forecast.html',
        'iframe_title': 'Demand Forecasting Ensemble Interactive',
        'iframe_hint': '★ Interactive — Toggle models (ARIMA/XGB/RF/Ensemble), horizon slider 7/14/30 days',
        'metric': '73% Variance Explained',
        'tag': 'Key Finding',
        'tldr': 'Ensemble model (ARIMA + XGBoost + Random Forest) outperforms any single model by 12-18%.',
    },
    'Capital Portfolio': {
        'repo': 'https://github.com/gosidehustlesisi/sierra-pmo-analytics',
        'notebook': 'https://github.com/gosidehustlesisi/sierra-pmo-analytics/blob/main/projects/capital-portfolio-governance/notebooks/capital_portfolio_analysis.ipynb',
        'data': 'USASpending.gov · Federal Program Inventory',
        'iframe': 'https://gosidehustlesisi.github.io/charts/capital_portfolio.html',
        'iframe_title': 'Capital Portfolio Interactive',
        'iframe_hint': '★ Interactive — Hover agencies for spending, toggle year ranges',
        'metric': '$4T Portfolio',
        'tag': 'Key Finding',
        'tldr': 'Top 10 agencies capture 60% of capital spending. IT modernization is the fastest-growing category.',
    },
    'NHTSA Safety': {
        'repo': 'https://github.com/gosidehustlesisi/sierra-mobility-data',
        'notebook': 'https://github.com/gosidehustlesisi/sierra-mobility-data/blob/main/projects/nhtsa-safety/notebooks/nhtsa_safety_analysis.ipynb',
        'data': 'NHTSA FARS · USDOT BTS · WMATA',
        'iframe': 'https://gosidehustlesisi.github.io/charts/fatalities_choropleth.html',
        'iframe2': 'https://gosidehustlesisi.github.io/charts/wmata_ridership.html',
        'iframe3': 'https://gosidehustlesisi.github.io/charts/bts_airline_delays.html',
        'iframe_title': 'NHTSA Fatalities Choropleth Interactive',
        'iframe_title2': 'WMATA Ridership Interactive',
        'iframe_title3': 'BTS Airline Delays Interactive',
        'iframe_hint': '★ Interactive — 10-year animation, year slider, hover state details',
        'iframe_hint2': '★ Interactive — Toggle weekdays/weekends, hover for ridership counts',
        'iframe_hint3': '★ Interactive — Filter by carrier, hover for delay stats',
        'metric': '37,133 Fatalities',
        'tag': 'Key Finding',
        'tldr': 'Rural states have 3× higher fatality rates per capita than urban states.',
    },
    'EVO3 Agent Swarm': {
        'repo': 'https://github.com/gosidehustlesisi',
        'notebook': None,
        'data': 'OpenClaw · Gemini AI Studio',
        'iframe': None,
        'metric': None,
        'tag': None,
        'tldr': None,
    },
    'Federal Data Governance': {
        'repo': 'https://github.com/gosidehustlesisi/sierra-data-governance',
        'notebook': 'https://github.com/gosidehustlesisi/sierra-data-governance/blob/main/projects/data-governance-dashboard/notebooks/governance_dashboard.ipynb',
        'data': 'Data.gov · FOIA.gov · OMB Guidance',
        'iframe': 'https://gosidehustlesisi.github.io/charts/data_gov_agencies.html',
        'iframe_title': 'Data.gov Agency Catalog Interactive',
        'iframe_hint': '★ Interactive — Filter by agency, hover for dataset counts',
        'metric': '144K Datasets',
        'tag': 'Key Finding',
        'tldr': '60% of federal datasets are geospatial. Only 12% have machine-readable metadata.',
    },
    'Census Demographics': {
        'repo': 'https://github.com/gosidehustlesisi/sierra-public-sector-insights',
        'notebook': 'https://github.com/gosidehustlesisi/sierra-public-sector-insights/blob/main/projects/census-demographics/notebooks/census_demographics_analysis.ipynb',
        'data': 'US Census ACS · 331M Population',
        'iframe': 'https://gosidehustlesisi.github.io/charts/census_demographics.html',
        'iframe_title': 'Census Demographics Interactive',
        'iframe_hint': '★ Interactive — Toggle age brackets, hover for population counts',
        'metric': '331M People',
        'tag': 'Key Finding',
        'tldr': 'The US is aging faster than projected. 65+ population will double by 2060.',
    },
    'BLS Labor Market': {
        'repo': 'https://github.com/gosidehustlesisi/sierra-public-sector-insights',
        'notebook': 'https://github.com/gosidehustlesisi/sierra-public-sector-insights/blob/main/projects/bls-labor-market/notebooks/bls_labor_market_analysis.ipynb',
        'data': 'BLS Employment · CES · LAUS',
        'iframe': 'https://gosidehustlesisi.github.io/charts/bls_employment.html',
        'iframe_title': 'BLS Employment Interactive',
        'iframe_hint': '★ Interactive — Toggle sectors, hover for unemployment rates',
        'metric': '164M Jobs',
        'tag': 'Key Finding',
        'tldr': 'Healthcare added 3.2M jobs in 5 years — the fastest-growing sector.',
    },
    'openclaw AI Infrastructure': {
        'repo': 'https://github.com/gosidehustlesisi',
        'notebook': None,
        'data': 'OpenClaw Gateway · Node.js · MCP',
        'iframe': None,
        'metric': None,
        'tag': None,
        'tldr': None,
    },
    'arXiv Research': {
        'repo': 'https://github.com/gosidehustlesisi/sierra-genai-engineering',
        'notebook': 'https://github.com/gosidehustlesisi/sierra-genai-engineering/blob/main/projects/arxiv-classifier-research-engine/notebooks/arxiv_classification_analysis.ipynb',
        'data': 'arXiv API · 2.4M Papers · 155 Categories',
        'iframe': 'https://gosidehustlesisi.github.io/charts/arxiv_categories.html',
        'iframe_title': 'arXiv Categories Interactive',
        'iframe_hint': '★ Interactive — Toggle categories, hover for paper counts',
        'metric': '89% Accuracy',
        'tag': 'Key Finding',
        'tldr': 'CS and Physics dominate arXiv. Astro-ph has the highest citation density.',
    },
    'World Bank': {
        'repo': 'https://github.com/gosidehustlesisi/sierra-public-sector-insights',
        'notebook': 'https://github.com/gosidehustlesisi/sierra-public-sector-insights/blob/main/projects/world-bank-development/notebooks/world_bank_analysis.ipynb',
        'data': 'World Bank API · 1,400+ Indicators · 190+ Countries',
        'iframe': 'https://gosidehustlesisi.github.io/charts/world_bank_gdp_life.html',
        'iframe_title': 'World Bank Indicators Interactive',
        'iframe_hint': '★ Interactive — Hover countries for details, bubble size = population',
        'metric': '36% → 8% Poverty',
        'tag': 'Key Finding',
        'tldr': 'Extreme poverty dropped from 36% to 8% in 30 years. Sub-Saharan Africa lags 20 years behind.',
    },
    'USASpending': {
        'repo': 'https://github.com/gosidehustlesisi/sierra-pmo-analytics',
        'notebook': 'https://github.com/gosidehustlesisi/sierra-pmo-analytics/blob/main/projects/usaspending-federal-awards/notebooks/usaspending_analysis.ipynb',
        'data': 'USASpending.gov · $4T Awards · 2.4M Transactions',
        'iframe': 'https://gosidehustlesisi.github.io/charts/foia_processing.html',
        'iframe2': 'https://gosidehustlesisi.github.io/charts/omb_policy_timeline.html',
        'iframe_title': 'FOIA Processing Interactive',
        'iframe_title2': 'OMB Policy Timeline Interactive',
        'iframe_hint': '★ Interactive — Toggle agency view, hover for median days',
        'iframe_hint2': '★ Interactive — Scroll timeline, hover policy details',
        'metric': '2.4M Transactions',
        'tag': 'Key Finding',
        'tldr': 'Top 10 contractors capture 34% of federal spending. 60% of awards go to small businesses.',
    },
}

# For projects with iframes, ensure they're wrapped in proper chart-box
# and placed BEFORE the transfer-box

def build_chart_box(iframe_url, title, hint, metric, tag, tldr, iframe_num=''):
    if not iframe_url:
        return ''
    iframe_block = f'''                    <div class="chart-box">
                        <div class="chart-insight-header">
                            <span class="insight-tag">{tag}</span>
                            <span class="insight-metric">{metric}</span>
                        </div>
                        <!-- INTERACTIVE: {title} -->
                        <div style="border:1px solid var(--border); border-radius:12px; overflow:hidden; margin-bottom:12px;">
                            <iframe src="{iframe_url}" 
                                width="100%" height="550" 
                                style="border:none; background:var(--bg-deep);"
                                loading="lazy"
                                title="{title}">
                            </iframe>
                        </div>
                        <div style="text-align:center; margin-bottom:8px;">
                            <span style="font-size:11px; color:var(--accent-gold);">{hint}</span>
                        </div>
                        <div class="tldr">
                            <p><strong>{tldr}</strong></p>
                        </div>
                    </div>'''
    return iframe_block

def build_project_footer(data, notebook_url, repo_url):
    if notebook_url:
        demo_link = f'<a class="demo-link" href="{notebook_url}">▶ Live Demo</a>'
    else:
        demo_link = ''
    
    if demo_link:
        links_div = f'''<div style="display:flex;gap:1rem;">
                        {demo_link}
                        <a class="repo-link" href="{repo_url}">View Repository →</a>
                    </div>'''
    else:
        links_div = f'''<div style="display:flex;gap:1rem;">
                        <a class="repo-link" href="{repo_url}">View Repository →</a>
                    </div>'''
    
    footer = f'''                <div class="project-footer">
                    <span class="data-sources">Data: {data}</span>
                    {links_div}
                </div>'''
    return footer

# Process each project
for title, meta in projects.items():
    # Find the project section
    pattern = rf'(<div class="project-title">{re.escape(title)}.*?</div>.*?)(</div>\s*</div>\s*<div class="project-card">|</div>\s*</div>\s*</section>|</div>\s*</div>\s*<div style="text-align:center")'
    
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        print(f"Warning: Could not find project: {title}")
        continue
    
    section = match.group(1)
    end_marker = match.group(2)
    
    # Check if project already has a footer
    if 'project-footer' in section:
        print(f"Skipping {title} - already has footer")
        continue
    
    # Extract existing parts
    has_iframe = 'iframe src' in section
    has_demo = 'demo-link' in section
    
    # For projects with iframes, we need to restructure
    if meta['iframe'] and has_iframe:
        # Build chart boxes
        chart_boxes = ''
        if 'iframe' in meta and meta['iframe']:
            chart_boxes += build_chart_box(
                meta['iframe'], meta['iframe_title'], meta['iframe_hint'],
                meta['metric'], meta['tag'], meta['tldr']
            ) + '\n'
        if 'iframe2' in meta and meta['iframe2']:
            chart_boxes += build_chart_box(
                meta['iframe2'], meta['iframe_title2'], meta['iframe_hint2'],
                meta['metric'], meta['tag'], meta['tldr2'] if 'tldr2' in meta else meta['tldr']
            ) + '\n'
        if 'iframe3' in meta and meta['iframe3']:
            chart_boxes += build_chart_box(
                meta['iframe3'], meta['iframe_title3'], meta['iframe_hint3'],
                meta['metric'], meta['tag'], meta['tldr3'] if 'tldr3' in meta else meta['tldr']
            ) + '\n'
        
        # Remove existing iframe blocks and their wrappers from section
        # (the interactive hint div and the iframe wrapper div)
        section = re.sub(
            r'\s*<!-- INTERACTIVE:.*?-->\s*<div style="border:1px solid var\(--border\);[^"]*">\s*<iframe src="[^"]*"[^>]*>\s*</iframe>\s*</div>\s*<div style="text-align:center[^"]*">\s*<span style="font-size:11px[^"]*">[^<]*</span>\s*</div>',
            '',
            section,
            flags=re.DOTALL
        )
        
        # Also remove any existing chart-box that might have partial structure
        section = re.sub(
            r'\s*<div class="chart-box">.*?</div>\s*(?=\s*<div class="technical-detail">|\s*<div style="margin-top:1rem;")',
            '',
            section,
            flags=re.DOTALL
        )
        
        # Insert chart boxes before technical-detail or after tldr
        if 'technical-detail' in section:
            section = re.sub(
                r'(\s*<div class="technical-detail">)',
                chart_boxes + r'\1',
                section,
                flags=re.DOTALL
            )
        else:
            section = re.sub(
                r'(\s*<div class="transfer-box">)',
                chart_boxes + r'\1',
                section,
                flags=re.DOTALL
            )
    
    # For projects without iframes but with notebooks (Zeus-URSA, EVO3, openclaw)
    # Add demo-link if missing
    if meta['notebook'] and not has_demo:
        demo_html = f'''                    <div style="margin-top:1rem;">
                        <a class="demo-link" href="{meta['notebook']}">▶ Live Demo</a>
                    </div>'''
        # Insert before transfer-box
        section = re.sub(
            r'(\s*<div class="transfer-box">)',
            demo_html + r'\1',
            section,
            flags=re.DOTALL
        )
    
    # Add project-footer before the closing </div></div>
    footer = build_project_footer(meta['data'], meta['notebook'], meta['repo'])
    # Insert before the last </div></div> of the project-card
    section = re.sub(
        r'(\s*</div>\s*</div>\s*)(</div>\s*</div>\s*<div class="project-card">|</div>\s*</div>\s*</section>|</div>\s*</div>\s*<div style="text-align:center")',
        footer + r'\n            \1\2',
        section,
        flags=re.DOTALL
    )
    
    # Replace in content
    old_section = match.group(0)
    new_section = section + end_marker
    content = content.replace(old_section, new_section, 1)
    print(f"Processed: {title}")

with open('/tmp/gosidehustlesisi.github.io/side-hustle.html', 'w') as f:
    f.write(content)

print("\nDone! File written.")
