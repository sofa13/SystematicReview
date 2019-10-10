# Setup
 
- Limit searching only the Scopus database since Scopus provides easy downloads of a paper's references and cited by details.
- Include only papers from Journals with a top Scopus source scores (more than 1.0).
- Assume papers from source with high source score are credible, and that papers referenced in credible paper are credible. However a paper that cites a credible referenced paper is not necessarily credible, therefore filter these paper by source score as well.
- Limit all papers from years 2014-2019.

# Steps to create an expertise database

Initialize our expertise `database` to the empty set.

1. Search Scopus with `title-abs-key("digital transformation" or "digital innovation" or "digitization" or "digitilization")`, limit years `2014-2019`.
2. Sort resulting papers by relevance using Scopus and download the first 600 papers (see `source` directory).
3. Limit the 600 papers to those with top source scores (call this `seed_papers`). See `data` directory for source scores downloaded from Scopus. 
4. For each paper in `seed_papers`, grab the reference paper details through Scopus (call this `reference_papers`). See the `database\reference\` directory. 
5. If a paper `rp` in `reference_papers` is referenced by more than 2 `seed_papers`, add `rp` to the `database`.
6. For each paper in `database`, grab the cited by paper details through Scopus (call this `citedby_papers`). See the `database\citeby\` directory
7. If a paper `cp` in `citedby_papers` references more than 3 papers in `database_papers`, add `cp` to the `database` (limit only `cp` papers with top source scores).
8. Repeat step 4-7, except replace `seed_papers` with `database`. Stop when database size is the same after two consecutive rounds.
9. Save resulting database papers to `database\db.csv` directory.

# Limitations

- Some source titles do not have source scores through Scopus even though they may be very influencial and crediable sources. A work around would be to manually check these sources and give them a score larger than the limit threshold for the source to be considered.
- This model favours papers whos credible and active authors cite their own work several times.
- This model also favours papers which cite huge numbers of papers, although this encourages literature reviews to be added to the expertise database.
- Scopus is the only database used due to their ease of downloading a paper's references and cite by details. Therefore relevant papers outside of Scopus are not considered. However once you read through papers in the expertise database, you may find other relevant papers this way.