Feature: customize bot
  Scenario: customize bot
    Given that the user is registered to the service
    When the user writes some predetermined customizing command in the chat with the bot device,
    Then the bot should respond with the customizing status (succesfull / unsuccessfull) and save the customized options.