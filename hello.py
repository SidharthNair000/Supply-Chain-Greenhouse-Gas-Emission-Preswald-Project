import pandas as pd
import plotly.express as px
from preswald import text, plotly

# Load the data 
df = pd.read_csv('data/SupplyChain.csv')


df['2017 NAICS Code'] = df['2017 NAICS Code'].astype(str)

# Emission Analysis Scatter Plot
fig = px.scatter(
    df,
    x="2017 NAICS Code",
    y="Supply Chain Emission Factors with Margins",
    color="Supply Chain Emission Factors without Margins",
    hover_name="2017 NAICS Title",
    title="Distribution of Supply Chain Emission Factors by Industry",
    labels={
        "2017 NAICS Code": "NAICS Industry Code",
        "Supply Chain Emission Factors with Margins": "Total Emissions (kg CO2e/$)",
        "Supply Chain Emission Factors without Margins": "Base Emissions"
    }
)

# Sector Density Analysis
sector_df = df.copy()
sector_df['Sector'] = sector_df['2017 NAICS Code'].str[:2]
hotspot_map = px.density_heatmap(
    sector_df,
    x="Sector",
    y="Supply Chain Emission Factors with Margins",
    z="Supply Chain Emission Factors without Margins",
    histfunc="avg",
    title="Density of Emission Factors by Industry Sector",
    labels={
        "Sector": "NAICS Sector Code",
        "Supply Chain Emission Factors with Margins": "Total Emissions",
        "Supply Chain Emission Factors without Margins": "Avg Base Emissions"
    }
)

# Sector Richness Analysis
richness = df.groupby("2017 NAICS Title")["Supply Chain Emission Factors with Margins"].mean().reset_index(name="avg_emissions")
richness_plot = px.bar(
    richness.sort_values("avg_emissions", ascending=False).head(20),
    x="2017 NAICS Title",
    y="avg_emissions",
    title="Top 20 Industries by Average Emission Factors",
    labels={
        "2017 NAICS Title": "Industry",
        "avg_emissions": "Average Emissions (kg CO2e/$)"
    }
)

# Hierarchical Distribution Analysis
df_treemap = df.copy()
df_treemap['Sector'] = df_treemap['2017 NAICS Code'].str[:2]
treemap_plot = px.treemap(
    df_treemap,
    path=["Sector", "2017 NAICS Title"],
    values="Supply Chain Emission Factors with Margins",
    color="Supply Chain Emission Factors without Margins",
    title="Taxonomic Distribution of Emission Factors by Sector and Industry"
)

# Emission Components Analysis
components_plot = px.bar(
    df.nlargest(20, "Supply Chain Emission Factors with Margins"),
    x="2017 NAICS Title",
    y=["Supply Chain Emission Factors without Margins", "Margins of Supply Chain Emission Factors"],
    title="Breakdown of Top 20 Emission Factors (Base vs Margins)",
    labels={
        "2017 NAICS Title": "Industry",
        "value": "Emissions (kg CO2e/$)",
        "variable": "Component"
    }
)

# Displays
text("# Supply Chain Emission Factors Analysis")

text("## Emission Factors Distribution")
text("Figure 1 illustrates the distribution of supply chain emission factors across different industries. "
     "Each point represents an industry (by NAICS code), with color indicating the base emissions before margins. "
     "The vertical position shows the total emission factor including margins.")
plotly(fig)

text("## Sector Density Analysis")
text("Figure 2 presents a density heatmap of emission factors by industry sector (first 2 digits of NAICS code). "
     "The intensity shows the concentration of industries with particular emission profiles, helping identify "
     "sectors that typically have higher supply chain emissions.")
plotly(hotspot_map)

text("## High Emission Industries")
text("Figure 3 shows the top 20 industries with the highest average emission factors. This analysis helps "
     "identify which specific economic activities contribute most to supply chain emissions per dollar of output.")
plotly(richness_plot)

text("## Hierarchical Sector Distribution")
text("Figure 4 depicts the hierarchical relationship between industry sectors and specific industries. "
     "The size of each rectangle represents the relative magnitude of emissions, while the color indicates "
     "the base emission intensity before margins are applied.")
plotly(treemap_plot)

text("## Emission Components Breakdown")
text("Figure 5 examines the composition of emission factors for the top 20 industries, showing how much "
     "comes from direct emissions versus supply chain margins. This decomposition helps identify where "
     "emission reductions might be most effective.")
plotly(components_plot)