## Workflow:

### Get latest data
`python -m pylab.bet365.main --get_new_history`

### ETL: Initial Run:
1. pull latest data as csv from google sheet "bet365 history revamped". Save the csv as `pylab/bet365/csv/bet365_history.csv`

url: `https://docs.google.com/spreadsheets/d/1i4zZaT-KcKqvTfpgouEJPPofWXA2EueKJ9yNNZvWMPA/export?format=csv&gid=0` 

`python -m pylab.bet365.main --download_history`

2. run data_enricher for first pass, generate csv which provides suggestions for manual edit:

`python -m pylab.bet365.main --suggest_update_history`



### ETL: Second Run: 

`python -m pylab.bet365.main --enrich_history`

At this point, the bet365 history sheet has been updated manually according to suggestions generated from the first run.

1. pull latest data as csv from bet365 history google sheet

2. run data enricher again to generate csv with enriched data

3. upload to google sheet (new sheet: "bet365 history enriched")

4. load csv data into database



