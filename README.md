# Procedure

This section describes the procedure (setup and steps) taken to create an expertise database.

## Setup
 
### Initial Search

- Limit search to the Scopus database since Scopus provides easy downloads of a paper's references and cited by details.
- Keyword search in scopus `key("digital transformation" or "digital innovation" or "digitization" or "digitilization")` (call this search `keywords`).
- Limit all papers from years 2014-2019.
- Include only papers from sources with a top Scopus source scores (more than 1.0).

### Continued search assumptions

- Assume papers from sources with high source score are credible, and that papers referenced in a credible paper are also credible (regardless if the referenced paper has a high source score).
- Assume a paper is a `core` paper if it is either referenced by `x` or more papers in the database, or if it cites `y` or more papers in the database and has a top source score. We use `x=3` and `y=4`.

## Steps

Initialize our expertise `database` to the empty set.

1. Search Scopus with `keywords`, limit years `2014-2019`.
2. Sort resulting papers by relevance using Scopus and download the first 200 papers (see `source` directory for the first 200 relevant papers).
3. Limit the 200 papers to those with top source scores (call this `seed_papers`). See `data` directory for source scores downloaded from Scopus. 
4. For each paper in `seed_papers`, grab the reference paper details through Scopus (call this `reference_papers`). See the `database\reference\` directory. 
5. If a paper `rp` in `reference_papers` is referenced by more than 2 `seed_papers`, add `rp` to the `database`.
6. For each paper in `database`, grab the cited by paper details through Scopus (call this `citedby_papers`). See the `database\citeby\` directory
7. If a paper `cp` in `citedby_papers` references more than 3 papers in `database_papers`, add `cp` to the `database` (limit only `cp` papers with top source scores).
8. Repeat step 4-7, except replace `seed_papers` with `database`. Stop when database size is the same after two consecutive rounds.
9. Save resulting database papers to `database\db.csv` file.

# Run

To run the code that creates the expertise database, clone or download this github repository, go to the directory through using the command line, and run `python main.py source\digitaltrans_2014-2019_keywords_200rel(2).csv`, where the `.csv` file is the seed source file (in this case the top 200 most relevant papers after searching `keywords` through Scopus). After the code is done running, an expertise database will be created as a file `database\db.csv`.

# Results

This experiment resulted in an expertise database `database\db.csv` consisting of 60 documents on the topic of Digital Transformation and Innovation (DTI). These documents all reference and cite each other tightly from 2014-2019. Due to this tight linking from paper sources with high scores, we feel this resulted in an influencial body of literature that represents a core part of the research areas and studies that ground the contemporary field of DTI. However, our implementation does not cover all core research due to a few limitations of our method which we list in the next section.

# Limitations

- Scopus is the only database used due to their ease of downloading a paper's references and cite by details. Therefore relevant papers outside of Scopus are not considered. However once you read through papers in the expertise database, you may find other relevant papers this way.
- Some source titles do not have source scores through Scopus (e.g. conference proceedings) even though the source may be influencial and crediable. A work around would be to manually check these sources and give them a score larger than the limit threshold for the source to be considered.
- This model favours papers whos credible and active authors cite their own work several times.
- This model favours papers which cite huge numbers of papers, although this encourages literature reviews and surveys to be added to the expertise database.