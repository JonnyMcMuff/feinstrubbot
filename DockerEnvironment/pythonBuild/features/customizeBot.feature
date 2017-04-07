Feature: customize bot
  Scenario: update quiet hours
    Given that the user is registered to the service2
    When the user text to the bot "Set quiet hours from $start$ to $end$"
    Then the user is notified about the his new quiet hours.

  Scenario: update username
    Given that the user is registered to the service3
    When the user text to the bot "Please call me NewUsername"
    Then the user is notified about the his new name.

  Scenario: set notification interval
    Given that the user is registered to the service4
    When the user text to the bot "Please notify my every x min"
    Then the user is notified about the his saved customisation.