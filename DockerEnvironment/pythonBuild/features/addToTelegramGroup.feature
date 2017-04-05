Feature: add to telegram group
  Scenario: groupMessages
    Given that the user is registered to the service
    When the user adds the bot to a group
    Then the group should get information about Feinstaub Alarm