Feature: Retrieve subscription
  As a user
  I want get rule subscriptions from server
  In order to manage my server subscriptions

  @basic
  Scenario Outline: Retrieve a subscription

    Given a subscription created in "<server_id>"
    When I retrieve the subscription in "<server_id>"
    Then I get all subscription information

    Examples:

    | server_id     |
    | qatestserver  |

  Scenario Outline: retrieve subscription in another server or non existent server

    Given a subscription created in "<server_id>"
    When I retrieve the subscription in "<another_server_id>"
    Then I obtain an "<Error_code>" and the "<FaultElement>"

    Examples:

    | server_id     | another_server_id | Error_code  | FaultElement  |
    | qatestserver  | qa                | 404         | itemNotFound  |
    | qatestserver  | random            | 404         | itemNotFound  |


  Scenario Outline: Retrieve a non existent subscription

    Given a subscription created in "<server_id>"
    When I retrieve a not existent subscription in "<server_id>"
    Then I obtain an "<Error_code>" and the "<FaultElement>"

    Examples:

    | server_id     | Error_code  | FaultElement  |
    | qatestserver  | 404         | itemNotFound  |
    | qatestserver  | 404         | itemNotFound  |

  @security
  Scenario Outline: Retrieve a subscription with incorrect token

    Given a subscription created in "<server_id>"
    And incorrect "<token>"
    When I retrieve the subscription in "<server_id>"
    Then I obtain an "<Error_code>" and the "<FaultElement>"

    Examples:

    | Error_code  | FaultElement  | token     | server_id   |
    | 401         | unauthorized  | 1a2b3c    | qatestserver|
    | 401         | unauthorized  | old_token | qatestserver|
    | 401         | unauthorized  |           | qatestserver|
    | 401         | unauthorized  | null      | qatestserver|