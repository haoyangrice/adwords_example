#!/usr/bin/env python
#
# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This example illustrates how to retrieve all the campaign targets.

To set campaign targets, run add_campaign_targeting_criteria.py.

The LoadFromStorage method is pulling credentials and properties from a
"googleads.yaml" file. By default, it looks for this file in your home
directory. For more information, see the "Caching authentication information"
section of our README.

Modified by Hao Yang to get all CRM lists applied to each campaign.
"""

from googleads import adwords


PAGE_SIZE = 1000


def main(client):

  # get a campaign lookup table.
  report_downloader = client.GetReportDownloader(version='v201710')

  query = """SELECT CampaignId, CampaignName, CampaignStatus
            FROM CAMPAIGN_PERFORMANCE_REPORT DURING YESTERDAY
          """
  with open('temp_campaign.csv', 'w') as output_file:
    report_downloader.DownloadReportWithAwql(
    query, 'CSV', output_file, skip_report_header=True,
    skip_column_header=False, skip_report_summary=True,
    include_zero_impressions=True)

  campaign_lookup = pd.read_csv('temp_campaign.csv')

  # Initialize appropriate service.
  campaign_criterion_service = client.GetService(
      'CampaignCriterionService', version='v201710')

  # Construct selector and get all campaign targets.
  offset = 0
  selector = {
      #'fields': ['CampaignId', 'Id', 'CriteriaType', 'BidModifier', 'PlatformName',
      #           'LanguageName', 'LocationName', 'KeywordText'],
      'fields': ['CampaignId', 'CampaignName', 'CampaignStatus', 'Id', 'CriteriaType', 'UserListName'],
      'predicates': [{
          'field': 'CriteriaType',
          'operator': 'IN',
          'values': ['USER_LIST']
          #'values': ['KEYWORD', 'LANGUAGE', 'LOCATION', 'PLATFORM']
      #},
      #    {'field':'CampaignStatus',
      #    'operator': 'EQUALS',
      #    'values': ['ENABLED']
      }],
      'paging': {
          'startIndex': str(offset),
          'numberResults': str(PAGE_SIZE)
      }
  }
  more_pages = True

  result = pd.DataFrame({})

  while more_pages:
    page = campaign_criterion_service.get(selector)

    # Display results.
    if 'entries' in page:
      for campaign_criterion in page['entries']:
        temp = pd.Series({})
        negative = ''
        if (campaign_criterion['CampaignCriterion.Type']
            == 'NegativeCampaignCriterion'):
          negative = 'Negative '
        else:
          negative = None
        criterion = campaign_criterion['criterion']
        temp['Negative'], temp['CampaignId'], temp['type'], temp['id'], temp['UserListId'] = \
            negative, campaign_criterion['campaignId'], criterion['type'], criterion['id'], criterion['userListId']
        temp['UserListName'] = criterion['userListName']

        result = result.append(temp.to_frame().T)

    offset += PAGE_SIZE
    selector['paging']['startIndex'] = str(offset)
    more_pages = offset < int(page['totalNumEntries'])


  ll = pd.read_csv(r'Z:\Google\TargetCPC-Hao\TempFiles\temp_all_kw.csv')

  result2 = result.merge(campaign_lookup, left_on='CampaignId', right_on='Campaign ID', how='left')

  result2.sort_values(by='CampaignId').to_csv('current_crm_list_campaign_all.csv', index=False)

if __name__ == '__main__':
  # Initialize client object.
  yaml = r'C:/Google/Adwords_Credentials/googleads.yaml'
  client = adwords.AdWordsClient.LoadFromStorage(yaml)

  main(adwords_client)
