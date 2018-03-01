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

"""This example adds demographic criteria to a campaign.

The LoadFromStorage method is pulling credentials and properties from a
"googleads.yaml" file. By default, it looks for this file in your home
directory. For more information, see the "Caching authentication information"
section of our README.

"""

from googleads import adwords


campaign_id = CAMPAIGN_ID # It should be a string.


def main(client, campaign_id):
  # Initialize appropriate service.
  campaign_criterion_service = client.GetService(
      'CampaignCriterionService', version='v201710')

  # Create the ad group criteria.
  campaign_criteria = [
      # Targeting criterion.
      #{
      #    'xsi_type': 'CampaignCriterion',
      #    'campaignId': campaign_id,
      #    'criterion': {
      #        'xsi_type': 'CriterionUserList',
      #        'userListId': '456909634'
      #    }
      #}#,
      # Exclusion criterion.
      {
          'xsi_type': 'NegativeCampaignCriterion',
          'campaignId': campaign_id,
          'criterion': {
              'xsi_type': 'CriterionUserList',
              #'id': '603283035112',
 [             'userListId': '460604067'
          }
      }
  ]

  # Create operations.
  operations = []
  for criterion in campaign_criteria:
    operations.append({
        'operator': 'REMOVE',#'ADD', #
        'operand': criterion
    })

  response = campaign_criterion_service.mutate(operations)

  if response and response['value']:
    criteria = response['value']
    for campaign_criterion in criteria:
      criterion = campaign_criterion['criterion']
      print ('Ad group criterion with ad group ID %s, criterion ID %s and '
             'type "%s" was added.' %
             (campaign_criterion['adGroupId'], criterion['id'],
              criterion['type']))
  else:
    print 'No criteria were returned.'


if __name__ == '__main__':
  # Initialize client object.
  yaml = r'C:/Google/Adwords_Credentials/googleads.yaml'
  client = adwords.AdWordsClient.LoadFromStorage(yaml)

  main(client, campaign_id)

  """
  response= campaign_criterion_service.query('SELECT CampaignId, CampaignName, '
                                'IsNegative, Id, UserListId, UserListName, CriteriaType '
                                'WHERE CampaignId= "326949878" AND CriteriaType="USER_LIST" ')
  """
