Feature: add to telegram group
  Scenario: groupMessages
    Given that the user is registered to the service (add to Group)
    When the user adds the bot to a group
    Then the group should get information about Feinstaub Alarm
