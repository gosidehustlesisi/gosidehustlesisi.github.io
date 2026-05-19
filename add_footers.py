import re

with open('/tmp/gosidehustlesisi.github.io/side-hustle.html', 'r') as f:
    content = f.read()

# Project metadata for footers
project_footers = {
    'NASA C-MAPSS': {
        'data': 'NASA C-MAPSS · UCI Bike Sharing',
        'notebook': 'https://github.com/gosidehustlesisi/sierra-applied-ml/blob/main/projects/predictive-maintenance-transit/notebooks/predictive_maintenance_analysis.ipynb',
        'repo': 'https://github.com/gosidehustlesisi/sierra-applied-ml',
    },
    '20 Newsgroups': {
        'data': 'sklearn 20 Newsgroups · CMU Lang (1995)',
        'notebook': 'https://github.com/gosidehustlesisi/sierra-applied-ml/blob/main/projects/nlp-text-classification-pipeline/notebooks/nlp_classification_analysis.ipynb',
        'repo': 'https://github.com/gosidehustlesisi/sierra-applied-ml',
    },
    'Zeus-URSA': {
        'data': 'Gemini AI Studio · MCP Protocol',
        'notebook': None,
        'repo': 'https://github.com/gosidehustlesisi',
    },
    'Demand Forecasting': {
        'data': 'UCI Bike Sharing · USDOT BTS',
        'notebook': 'https://github.com/gosidehustlesisi/sierra-applied-ml/blob/main/projects/demand-forecasting-operations/notebooks/demand_forecasting.ipynb',
        'repo': 'https://github.com/gosidehustlesisi/sierra-applied-ml',
    },
    'Capital Portfolio': {
        'data': 'USASpending.gov · Federal Program Inventory',
        'notebook': 'https://github.com/gosidehustlesisi/sierra-pmo-analytics/blob/main/projects/capital-portfolio-governance/notebooks/capital_portfolio_analysis.ipynb',
        'repo': 'https://github.com/gosidehustlesisi/sierra-pmo-analytics',
    },
    'NHTSA Safety': {
        'data': 'NHTSA FARS · USDOT BTS · WMATA',
        'notebook': 'https://github.com/gosidehustlesisi/sierra-mobility-data/blob/main/projects/nhtsa-safety/notebooks/nhtsa_safety_analysis.ipynb',
        'repo': 'https://github.com/gosidehustlesisi/sierra-mobility-data',
    },
    'EVO3 Agent Swarm': {
        'data': 'OpenClaw · Gemini AI Studio',
        'notebook': None,
        'repo': 'https://github.com/gosidehustlesisi',
    },
    'Federal Data Governance': {
        'data': 'Data.gov · FOIA.gov · OMB Guidance',
        'notebook': 'https://github.com/gosidehustlesisi/sierra-data-governance/blob/main/projects/data-governance-dashboard/notebooks/governance_dashboard.ipynb',
        'repo': 'https://github.com/gosidehustlesisi/sierra-data-governance',
    },
    'Census Demographics': {
        'data': 'US Census ACS · 331M Population',
        'notebook': 'https://github.com/gosidehustlesisi/sierra-public-sector-insights/blob/main/projects/census-demographics/notebooks/census_demographics_analysis.ipynb',
        'repo': 'https://github.com/gosidehustlesisi/sierra-public-sector-insights',
    },
    'BLS Labor Market': {
        'data': 'BLS Employment · CES · LAUS',
        'notebook': 'https://github.com/gosidehustlesisi/sierra-public-sector-insights/blob/main/projects/bls-labor-market/notebooks/bls_labor_market_analysis.ipynb',
        'repo': 'https://github.com/gosidehustlesisi/sierra-public-sector-insights',
    },
    'openclaw AI Infrastructure': {
        'data': 'OpenClaw Gateway · Node.js · MCP',
        'notebook': None,
        'repo': 'https://github.com/gosidehustlesisi',
    },
    'arXiv Research': {
        'data': 'arXiv API · 2.4M Papers · 155 Categories',
        'notebook': 'https://github.com/gosidehustlesisi/sierra-genai-engineering/blob/main/projects/arxiv-classifier-research-engine/notebooks/arxiv_classification_analysis.ipynb',
        'repo': 'https://github.com/gosidehustlesisi/sierra-genai-engineering',
    },
    'World Bank': {
        'data': 'World Bank API · 1,400+ Indicators · 190+ Countries',
        'notebook': 'https://github.com/gosidehustlesisi/sierra-public-sector-insights/blob/main/projects/world-bank-development/notebooks/world_bank_analysis.ipynb',
        'repo': 'https://github.com/gosidehustlesisi/sierra-public-sector-insights',
    },
    'USASpending': {
        'data': 'USASpending.gov · $4T Awards · 2.4M Transactions',
        'notebook': 'https://github.com/gosidehustlesisi/sierra-pmo-analytics/blob/main/projects/usaspending-federal-awards/notebooks/usaspending_analysis.ipynb',
        'repo': 'https://github.com/gosidehustlesisi/sierra-pmo-analytics',
    },
}

# Find each project section and add footer before </div></div> closing
for title, meta in project_footers.items():
    # Pattern to find the project section from title to its closing
    # The project ends with </div> (project-body) </div> (project-card)
    pattern = rf'(<div class="project-title">{re.escape(title)}.*?</div>\s*</div>)(\s*</div>\s*<div class="project-card">|\s*</div>\s*</div>\s*<div style="text-align:center"|\s*</div>\s*</div>\s*</section>)'
    
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        print(f"Warning: Could not find end of project: {title}")
        continue
    
    # Check if footer already exists
    section = match.group(1)
    if 'project-footer' in section:
        print(f"Skipping {title} - already has footer")
        continue
    
    # Build footer HTML
    if meta['notebook']:
        footer_html = f'''                <div class="project-footer">
                    <span class="data-sources">Data: {meta['data']}</span>
                    <div style="display:flex;gap:1rem;">
                        <a class="demo-link" href="{meta['notebook']}">▶ Live Demo</a>
                        <a class="repo-link" href="{meta['repo']}">View Repository →</a>
                    </div>
                </div>'''
    else:
        footer_html = f'''                <div class="project-footer">
                    <span class="data-sources">Data: {meta['data']}</span>
                    <div style="display:flex;gap:1rem;">
                        <a class="repo-link" href="{meta['repo']}">View Repository →</a>
                    </div>
                </div>'''
    
    # The section ends with </div> (project-body) then </div> (project-card)
    # We need to insert the footer between these two closing divs
    # The match.group(1) already includes the </div></div> at the end
    # Let me use a different approach - insert before the last </div></div>
    
    # Find the specific closing pattern for this project
    old_end = match.group(1)
    # Insert footer before the last </div> of project-body
    # The old_end ends with </div> (closing project-body) </div> (closing project-card)
    new_end = old_end.rstrip() + '\n' + footer_html + '\n            '
    
    content = content.replace(old_end, new_end, 1)
    print(f"Added footer to: {title}")

with open('/tmp/gosidehustlesisi.github.io/side-hustle.html', 'w') as f:
    f.write(content)

print("\nDone! File written.")
