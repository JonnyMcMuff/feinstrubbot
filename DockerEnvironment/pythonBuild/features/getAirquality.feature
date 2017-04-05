Feature: GetAirQuality
  Scenario: GetTheQuality
    Given that the user is registered to the service (air quality)
    When the the user asks the bot the question "How is the air quality?"
    Then the user is notified about the level.