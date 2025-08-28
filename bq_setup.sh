#!/bin/bash
#
# This script sets up the ecommerce dataset, tables, and views in BigQuery.

set -e # Exit immediately if a command exits with a non-zero status.

echo "Creating ecommerce dataset..."
bq mk --dataset --description "Dataset for ecommerce data" ecommerce

echo "Creating table: ecommerce.all_sessions_raw_20170801"
bq query --use_legacy_sql=false \
"
#standardSQL

# copy one day of ecommerce data to explore
CREATE OR REPLACE TABLE ecommerce.all_sessions_raw_20170801
#schema
(
  fullVisitorId STRING NOT NULL OPTIONS(description='Unique visitor ID'),
  channelGrouping STRING NOT NULL OPTIONS(description='Channel e.g. Direct, Organic, Referral...'),
  totalTransactionRevenue INT64 OPTIONS(description='Revenue * 10^6 for the transaction')
)
 OPTIONS(
   description='Raw data from analyst team into our dataset for 08/01/2017'
 ) AS
 SELECT
    fullVisitorId,
    channelGrouping,
    totalTransactionRevenue
 FROM \`data-to-insights.ecommerce.all_sessions_raw\`
 WHERE date = '20170801'
;
"

echo "Creating table: ecommerce.revenue_transactions_20170801"
bq query --use_legacy_sql=false \
"
#standardSQL

# create a table of transactions with revenue
CREATE OR REPLACE TABLE ecommerce.revenue_transactions_20170801
#schema
(
  fullVisitorId STRING NOT NULL OPTIONS(description='Unique visitor ID'),
  visitId STRING NOT NULL OPTIONS(description='ID of the session, not unique across all users'),
  channelGrouping STRING NOT NULL OPTIONS(description='Channel e.g. Direct, Organic, Referral...'),
  totalTransactionRevenue FLOAT64 NOT NULL OPTIONS(description='Revenue for the transaction')
)
 OPTIONS(
   description='Revenue transactions for 08/01/2017'
 ) AS
 SELECT DISTINCT
  fullVisitorId,
  CAST(visitId AS STRING) AS visitId,
  channelGrouping,
  totalTransactionRevenue / 1000000 AS totalTransactionRevenue
 FROM \`data-to-insights.ecommerce.all_sessions_raw\`
 WHERE date = '20170801'
      AND totalTransactionRevenue IS NOT NULL
;
"

echo "Creating view: ecommerce.vw_latest_transactions"
bq query --use_legacy_sql=false \
"
#standardSQL
CREATE OR REPLACE VIEW ecommerce.vw_latest_transactions
OPTIONS(
  description='latest 100 ecommerce transactions',
  labels=[('report_type','operational')]
)
AS
SELECT DISTINCT
  date,
  fullVisitorId,
  CAST(visitId AS STRING) AS visitId,
  channelGrouping,
  totalTransactionRevenue / 1000000 AS totalTransactionRevenue
 FROM \`data-to-insights.ecommerce.all_sessions_raw\`
 WHERE totalTransactionRevenue IS NOT NULL
 ORDER BY date DESC # latest transactions
 LIMIT 100
;
"

echo "Creating view: ecommerce.vw_large_transactions"
bq query --use_legacy_sql=false \
"
#standardSQL
CREATE OR REPLACE VIEW ecommerce.vw_large_transactions
OPTIONS(
  description='large transactions for review',
  labels=[('org_unit','loss_prevention')],
  expiration_timestamp=TIMESTAMP_ADD(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
)
AS
WITH transactions_with_products AS (
  SELECT
    date, fullVisitorId, CAST(visitId AS STRING) AS visitId, channelGrouping,
    totalTransactionRevenue, currencyCode, p.v2ProductName
  FROM \`data-to-insights.ecommerce.all_sessions_raw\`, UNNEST(hits) AS h, UNNEST(h.product) AS p
  WHERE totalTransactionRevenue IS NOT NULL
    AND (totalTransactionRevenue / 1000000) > 1000
    AND currencyCode = 'USD'
)
SELECT
  SESSION_USER() AS viewer_ldap,
  REGEXP_EXTRACT(SESSION_USER(), r'@(.+)') AS domain,
  date, fullVisitorId, visitId, channelGrouping,
  totalTransactionRevenue / 1000000 AS totalTransactionRevenue,
  currencyCode,
  STRING_AGG(DISTINCT v2ProductName ORDER BY v2ProductName LIMIT 10) AS products_ordered
FROM transactions_with_products
WHERE REGEXP_EXTRACT(SESSION_USER(), r'@(.+)') IN ('qwiklabs.net')
GROUP BY viewer_ldap, domain, date, fullVisitorId, visitId, channelGrouping, totalTransactionRevenue, currencyCode
ORDER BY date DESC
LIMIT 10;
"

echo "BigQuery setup complete."