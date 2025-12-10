import os
from datetime import datetime

class Reporter:
    def __init__(self, target_username, graph):
        self.target = target_username
        self.graph = graph
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def generate_html(self):
        filename = f"report_{self.target}.html"
        
        # --- 1. INTELLIGENCE ANALYSIS (Stats & Risk) ---
        total_nodes = len(self.graph.nodes)
        accounts = [n for n in self.graph.nodes.values() if n.type == "Account"]
        emails = [n for n in self.graph.nodes.values() if n.type == "Email"]
        
        # Dynamic Risk Scoring Logic
        risk_score = 0
        risk_factors = []
        
        if len(accounts) > 0: 
            risk_score += 10
        if len(accounts) > 5: 
            risk_score += 20
            risk_factors.append("High footprint visibility")
            
        if len(emails) > 0: 
            risk_score += 40  # Emails are high risk
            risk_factors.append("Email address exposed")
        
        # Determine Badge Color & Label
        risk_level = "LOW"
        risk_color = "#10b981" # Emerald Green
        if risk_score > 30:
            risk_level = "MODERATE"
            risk_color = "#f59e0b" # Amber Orange
        if risk_score > 60:
            risk_level = "CRITICAL"
            risk_color = "#ef4444" # Red

        # --- 2. HTML TEMPLATE ---
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Digital Footprint Dossier: {self.target}</title>
            <style>
                :root {{
                    --primary-slate: #1e293b;
                    --secondary-slate: #334155;
                    --bg-gray: #f8fafc;
                    --accent-blue: #3b82f6;
                    --border-color: #e2e8f0;
                }}
                
                body {{
                    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
                    background-color: var(--bg-gray);
                    color: #1e293b;
                    margin: 0;
                    padding: 0;
                }}

                /* --- HEADER --- */
                .header {{
                    background: var(--primary-slate);
                    color: white;
                    padding: 1.5rem 2rem;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    border-bottom: 4px solid var(--accent-blue);
                }}
                .brand h1 {{ margin: 0; font-size: 1.25rem; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; }}
                .brand span {{ color: #94a3b8; font-size: 0.8rem; font-weight: 500; }}
                .meta-info {{ text-align: right; font-size: 0.85rem; color: #cbd5e1; }}

                /* --- LAYOUT --- */
                .container {{ max-width: 1200px; margin: 2rem auto; padding: 0 1.5rem; }}
                
                /* --- KPI CARDS --- */
                .stats-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 1.5rem;
                    margin-bottom: 2rem;
                }}
                
                .card {{
                    background: white;
                    padding: 1.5rem;
                    border-radius: 8px;
                    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1);
                    border: 1px solid var(--border-color);
                    transition: all 0.2s;
                }}
                .card:hover {{ transform: translateY(-2px); box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }}
                
                .stat-title {{ color: #64748b; font-size: 0.75rem; text-transform: uppercase; font-weight: 700; letter-spacing: 0.05em; }}
                .stat-value {{ font-size: 2.25rem; font-weight: 800; color: var(--primary-slate); margin-top: 0.5rem; }}
                
                .risk-badge {{
                    background-color: {risk_color};
                    color: white;
                    padding: 0.25rem 0.75rem;
                    border-radius: 9999px;
                    font-size: 1rem;
                    vertical-align: middle;
                }}

                /* --- MAIN CONTENT GRID --- */
                .content-grid {{
                    display: grid;
                    grid-template-columns: 2fr 1fr; /* Table takes 2/3, Graph takes 1/3 */
                    gap: 2rem;
                }}
                @media (max-width: 1024px) {{ .content-grid {{ grid-template-columns: 1fr; }} }}

                .section-header {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 1rem;
                    padding-bottom: 0.5rem;
                    border-bottom: 2px solid var(--border-color);
                }}
                .section-title {{ font-size: 1.1rem; font-weight: 700; color: var(--secondary-slate); }}

                /* --- TABLE --- */
                .table-container {{
                    background: white;
                    border-radius: 8px;
                    border: 1px solid var(--border-color);
                    overflow: hidden;
                }}
                
                .search-bar {{
                    padding: 1rem;
                    background: #f8fafc;
                    border-bottom: 1px solid var(--border-color);
                }}
                .search-input {{
                    width: 100%;
                    padding: 0.5rem 1rem;
                    border: 1px solid #cbd5e1;
                    border-radius: 6px;
                    font-size: 0.9rem;
                    box-sizing: border-box; /* Fixes padding issues */
                }}
                .search-input:focus {{ outline: none; border-color: var(--accent-blue); }}

                table {{ width: 100%; border-collapse: collapse; }}
                th {{
                    background: #f1f5f9;
                    text-align: left;
                    padding: 0.75rem 1.5rem;
                    font-size: 0.75rem;
                    text-transform: uppercase;
                    color: #64748b;
                    font-weight: 700;
                }}
                td {{ padding: 1rem 1.5rem; border-bottom: 1px solid var(--border-color); font-size: 0.9rem; }}
                tr:last-child td {{ border-bottom: none; }}
                
                .platform-tag {{ font-weight: 600; color: var(--primary-slate); }}
                .source-badge {{ 
                    background: #e0f2fe; color: #0369a1; 
                    padding: 2px 8px; border-radius: 4px; 
                    font-size: 0.75rem; font-weight: 600; 
                }}
                .link-text {{ color: var(--accent-blue); text-decoration: none; font-family: monospace; }}
                .link-text:hover {{ text-decoration: underline; }}

                /* --- GRAPH IMAGE --- */
                .graph-card {{
                    background: white;
                    padding: 1rem;
                    border-radius: 8px;
                    border: 1px solid var(--border-color);
                    text-align: center;
                }}
                .graph-card img {{ max-width: 100%; height: auto; border-radius: 4px; }}
                .graph-caption {{ margin-top: 1rem; font-size: 0.8rem; color: #64748b; }}

                .footer {{ text-align: center; margin-top: 4rem; font-size: 0.8rem; color: #94a3b8; padding-bottom: 2rem; }}
            </style>
        </head>
        <body>
            <div class="header">
                <div class="brand">
                    <h1>DIGITAL FOOTPRINT DOSSIER</h1>
                    <span>OpSec Analysis Tool // v1.0</span>
                </div>
                <div class="meta-info">
                    <div>TARGET: <strong>{self.target}</strong></div>
                    <div>GENERATED: {self.timestamp}</div>
                </div>
            </div>

            <div class="container">
                
                <div class="stats-grid">
                    <div class="card">
                        <div class="stat-title">Total Data Points</div>
                        <div class="stat-value">{total_nodes}</div>
                    </div>
                    <div class="card">
                        <div class="stat-title">Accounts Found</div>
                        <div class="stat-value">{len(accounts)}</div>
                    </div>
                    <div class="card">
                        <div class="stat-title">Email Leaks</div>
                        <div class="stat-value" style="color: {'#ef4444' if len(emails) > 0 else '#10b981'}">
                            {len(emails)}
                        </div>
                    </div>
                    <div class="card">
                        <div class="stat-title">Risk Assessment</div>
                        <div class="stat-value">
                            <span class="risk-badge">{risk_level}</span>
                        </div>
                    </div>
                </div>

                <div class="content-grid">
                    
                    <div>
                        <div class="section-header">
                            <div class="section-title">DETAILED FINDINGS</div>
                        </div>
                        <div class="table-container">
                            <div class="search-bar">
                                <input type="text" id="searchInput" class="search-input" placeholder="Filter findings (e.g., 'Twitter', 'Leaked')..." onkeyup="filterTable()">
                            </div>
                            <table id="findingsTable">
                                <thead>
                                    <tr>
                                        <th>Platform</th>
                                        <th>URL / Data</th>
                                        <th>Source</th>
                                    </tr>
                                </thead>
                                <tbody>
        """
        
        # --- GENERATE TABLE ROWS ---
        for node in self.graph.nodes.values():
            if node.type != "Person": 
                # Intelligent Platform Labeling
                # We check 'platform' first, then 'site_name', then fallback to 'Unknown'
                platform_label = getattr(node, 'platform', getattr(node, 'site_name', 'Unknown'))
                
                # Special styling for Email nodes
                row_style = ""
                if node.type == "Email": 
                    platform_label = "EMAIL LEAK"
                    row_style = "color: #ef4444; font-weight:bold;"
                
                # Link Formatting
                link = getattr(node, 'url', node.id)
                display_link = link
                if "http" in link:
                    # Shorten long URLs visually but keep the link intact
                    short_link = link[:45] + "..." if len(link) > 45 else link
                    display_link = f"<a href='{link}' target='_blank' class='link-text'>{short_link}</a>"
                
                html_content += f"""
                                    <tr>
                                        <td><div class="platform-tag" style="{row_style}">{platform_label}</div></td>
                                        <td>{display_link}</td>
                                        <td><span class="source-badge">{node.source}</span></td>
                                    </tr>
                """

        html_content += f"""
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <div>
                        <div class="section-header">
                            <div class="section-title">RELATIONSHIP MAP</div>
                        </div>
                        <div class="graph-card">
                            <img src="scan_{self.target}.png" alt="Network Graph Analysis">
                            <div class="graph-caption">
                                <p><strong>Visual Identity Cluster</strong></p>
                                <p>This graph visualizes the connection between the target identity and discovered assets across the surface web.</p>
                            </div>
                        </div>
                        
                        <div style="margin-top: 2rem;">
                            <div class="section-header">
                                <div class="section-title">RISK FACTORS</div>
                            </div>
                            <div class="card" style="padding: 1rem;">
                                <ul style="margin: 0; padding-left: 1.5rem; color: #64748b; font-size: 0.9rem;">
                                    {''.join([f'<li style="margin-bottom:0.5rem">{factor}</li>' for factor in risk_factors]) or '<li>No critical risk factors identified.</li>'}
                                </ul>
                            </div>
                        </div>
                    </div>
                
                </div> <div class="footer">
                    GENERATED BY DIGITAL FOOTPRINT MAPPER | CONFIDENTIAL | AUTHORIZED USER: [REDACTED]
                </div>
            </div>

            <script>
                function filterTable() {{
                    var input, filter, table, tr, td, i, txtValue;
                    input = document.getElementById("searchInput");
                    filter = input.value.toUpperCase();
                    table = document.getElementById("findingsTable");
                    tr = table.getElementsByTagName("tr");

                    for (i = 0; i < tr.length; i++) {{
                        // Check both Platform (col 0) and Data (col 1)
                        td0 = tr[i].getElementsByTagName("td")[0]; 
                        td1 = tr[i].getElementsByTagName("td")[1];
                        
                        if (td0 || td1) {{
                            txt0 = td0.textContent || td0.innerText;
                            txt1 = td1.textContent || td1.innerText;
                            
                            if (txt0.toUpperCase().indexOf(filter) > -1 || txt1.toUpperCase().indexOf(filter) > -1) {{
                                tr[i].style.display = "";
                            }} else {{
                                tr[i].style.display = "none";
                            }}
                        }}
                    }}
                }}
            </script>
        </body>
        </html>
        """

        with open(filename, "w") as f:
            f.write(html_content)
        
        print(f"\n[+] Professional Report generated: {os.path.abspath(filename)}")
