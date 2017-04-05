Feature: FeinstaubAlarm
  Scenario: GetTheAlarm
    Given that the user is registered to the service
    When the Feinstaubalarm is raised
    Then the user is notified about the Feinstaub Alarm
  Scenario: VVSTickets
    Given that the user is registered to the service
    When the Feinstaubalarm is raised
    Then the user is notified about the cheaper VVS tickets
