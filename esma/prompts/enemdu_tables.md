# ENEMDU 2024
The 2024 National Survey of Employment, Unemployment, and Underemployment (ENEMDU), conducted by the National Institute of Statistics and Censuses (INEC), is a continuous quarterly survey that has been measuring Ecuador's labor market conditions since its inception in 1987. Its coverage is national, encompassing urban and rural areas across all provinces except Galápagos, through in-person household interviews. The 2024 sample comprises 17,066 households (2,438 primary sampling units with 7 households each), collected quarterly in March, June, September, and December. The survey generates indicators on employment, unemployment, underemployment, income, working conditions, and sociodemographic characteristics, with statistical representativeness at the national level, by geographic area (urban/rural), five self-represented cities (Quito, Guayaquil, Cuenca, Machala, Ambato), and other urban and rural domains.

## Tables
The enemdu-2024 database is composed by 10 different tables:
- BDDENEMDU_PERSONAS_2024_ANUAL
- BDDENEMDU_VIVIENDA_2024_ANUAL

### BDDENEMDU_PERSONAS_2024_ANUAL  
**Module Name**: Personas 2024 Anual  

**Description:**  
Person-level module capturing demographic characteristics, household composition, educational attainment, labor market participation, employment conditions, income sources (monetary and in-kind), social security coverage, and poverty status. Supports individual-level analysis and aggregated statistics on employment quality, unemployment, underemployment, income distribution, and welfare indicators for the Ecuadorian population aged 5 years and older.

**Business Domain:** Employment, Labor Market, Demographics, Income, Education, Social Security, Poverty

**Identifiers**: Each row represents an individual within a household. Records are uniquely identified by: **ID_PERSONA** (or composite: PROV, CIUDAD, CONGLOMERADO, PANELM, VIVIENDA, HOGAR, P01).

**Expansion Factor**: **FEXP** provides survey weight for national and domain-level population estimates.

**Key Topics Covered:**  

- **Demographics & Household Structure:** Sex, age, relationship to household head, marital status, ethnic self-identification, place of birth.

- **Education:** School attendance and shift, education level and years completed, literacy, degrees obtained.

- **Health & Social Security:** Coverage type (IESS general/voluntary/peasant, ISSFA/ISSPOL, private insurance, municipal, public health), contribution status.

- **Employment & Labor Market:**  
  - **Work Status:** Work last week, activities performed, job absence, hours worked, desire/availability for additional hours.
  - **Job Search:** Methods used, weeks searching, reasons for not searching, availability to work.
  - **Occupational Details:** Economic activity (ISIC 4.1), occupation (ISCO-08), employment category, contract type, tenure, workplace characteristics.
  - **Employment Benefits:** Food, housing, transport, vacation, social security, medical insurance, 13th/14th salary.
  - **Secondary Employment:** Multiple jobs indicator, hours and characteristics of secondary job.
  - **Activity Classification (CONDACT):** Adequate employment, time/income underemployment, other inadequate employment, unpaid work, unemployment (open/hidden), inactive population.
  - **Employment Sector (SECEMP):** Formal, informal, domestic service, unclassified.

- **Income Sources (Monthly):**  
  - **Labor Income:** Self-employed/employer earnings, salaried income, deductions, in-kind payments, secondary job income (INGRL).
  - **Non-Labor Income:** Capital income (rent, interest, dividends), pensions, gifts, remittances, social transfers (Human Development Bond, Disability Bond).
  - **Per Capita Income:** INGPC for household welfare analysis.

- **Poverty Indicators:** Income-based poverty (POBREZA) and extreme poverty (EPOBREZA) classification.

- **Geographic Variables:** Province (PROV), domain (Quito, Guayaquil, Cuenca, Machala, Ambato, rest of country), urban/rural area (AREA), survey period (PERIODO, MES).

**Special Notes:** Survey follows ILO standards (13th, 16th, 19th ICLS). Activity condition classification aligns with 2014 methodology incorporating 19th ICLS underemployment recommendations. Questions P20-P78 focus on population 15 years and older.

### BDDENEMDU_VIVIENDA_2024_ANUAL  
**Module Name**: Vivienda 2024 Anual  

**Description:**  
Household-level module capturing physical housing characteristics, construction materials, dwelling conditions, access to basic services (water, sanitation, electricity), and housing tenure. Supports analysis of living conditions, housing quality, infrastructure access, and residential welfare indicators.

**Business Domain:** Housing, Infrastructure, Living Conditions

**Identifiers**: Each row represents a household within a dwelling. Records are uniquely identified by: **ID_HOGAR** (or composite: CIUDAD, CONGLOMERADO, PANELM, VIVIENDA, HOGAR).

**Expansion Factor**: **FEXP** provides survey weight for national and domain-level household estimates.

**Key Topics Covered:**  

- **Access & Location:** Main access road to dwelling (paved, cobblestone, dirt road, path, river/sea) (VI01), geographic area (urban/rural).

- **Housing Type & Structure:** Dwelling type (house/villa, apartment, tenement rooms, mediagua, rancho/shack, hut, other) (VI02), number of rooms (VI06), number of bedrooms (VI07), business rooms (VI07A), availability of extra space (VI07B).

- **Construction Materials & Condition:**  
  - **Roof:** Material (concrete, asbestos, zinc/aluminum, tile, palm/straw, other) and condition (good/regular/bad) (VI03A, VI03B).
  - **Floor:** Material (wood flooring, ceramic/tile, marble, brick/cement, untreated wood, cane, earth, other) and condition (VI04A, VI04B).
  - **Walls:** Material (concrete/brick, asbestos/cement, adobe, wood, plastered cane, unplastered cane, other) and condition (VI05A, VI05B).

- **Basic Services & Utilities:**  
  - **Cooking:** Cooking fuel (gas, firewood/charcoal, electricity, other) (VI08).
  - **Sanitation:** Type of toilet facility (flush toilet with sewer/septic tank/cesspool, latrine, none) (VI09).
  - **Water:** Source (public network, public tap, piped from other source, water truck/tricycle, well, river/spring, other) (VI10), water meter availability (VI101), water board provision (VI102), water delivery method (piped inside/outside dwelling, other means) (VI10A).
  - **Bathing:** Shower service (exclusive, shared, none) (VI11).
  - **Electricity:** Lighting source (public electric company, private generator, candle/gas, none) (VI12).
  - **Waste Management:** Garbage disposal method (contracted service, municipal service, street/river disposal, burned/buried, other) (VI13).

- **Housing Tenure:** Ownership status (rented, antichresis/rent, owned and being paid, fully owned, ceded/borrowed, received for services, other) (VI14).

- **Geographic & Survey Variables:** City (CIUDAD), cluster (CONGLOMERADO), panel (PANELM), stratum (ESTRATO), primary sampling unit (UPM), survey period (PERIODO, MES).

**Special Notes:** This module provides essential indicators for housing quality assessment, access to basic services, and living conditions analysis. Data collected at household level within each surveyed dwelling.