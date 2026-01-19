# ADR 02: Parquet for intermediate storage
**Date:** 11 Jan,2026

**Context:** CSV files are text heavy,don't store data-types,slow to read in bulk and can easily be updated manually.All of create the risk of data being unreliable at the time of analysis.
**Choice:** Using Apache Parquet as format for files with cleaned data.
**Pros:** Columnar storage allowing faster reads.Includes 'metadata'.Files are compressed upto 80% compared to CSV.
**Cons:** Not human readable,requires specialized viewer to open.