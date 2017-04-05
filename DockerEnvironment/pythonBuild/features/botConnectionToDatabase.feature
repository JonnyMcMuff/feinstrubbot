Feature: bot connection to database
  Scenario: databaseConnection
    Given that there is a working setup of an external database
    When the bot tries to connect to the database
    Then it should get a working connection and be able to retrieve user data