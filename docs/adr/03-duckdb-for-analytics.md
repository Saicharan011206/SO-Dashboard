# ADR 03: DuckDB for Analytical Layer
**Date:** 11 Jan,2026

**Context:** We need to perform analytics on 14 different files consisting of 630,000+ rows of data.Loading all the data to pandas each time in memory inefficient.
**Choice:** Use DuckDB as the unified analytical engine.
**Pros:** It can be used to query parquet files without needing to import them each time.It uses vectorized execution,making aggregations much faster than standard python loops.It is serverless(just a .db file).
**Cons:**It is an OLAP(analytical) database,not meant for high-frequency individual row updates.