# ADR 001: Pandas for Data Ingestion and Transformation

**Date:** Jan 11,2026



**Context:** The dataset chosen for this project contains csv files with data spanning 14 years(2011-2024),during which the survey schema evolved significantly.

<ul>

<li>**Schema Inconsistency:** Column names change from year to year.</li>

<li>**Low Quality Entires:** Need to filter out 'troll' or incomplete responses to ensure analytical reliability.</li>

</ul>

**Choice:** Pandas is industry-standard for data