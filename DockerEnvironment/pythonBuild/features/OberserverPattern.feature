Feature: ObserverPattern
  Scenario: GetTheAlarm
    Given that the user is subscribed to the alarm
    When the Feinstaubalarm is detected and the user has not been notified yet
    Then the user is notified about the Feinstaub Alarm