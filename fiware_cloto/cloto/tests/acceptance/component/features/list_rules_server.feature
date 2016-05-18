Feature: As a user
  I want to list all the rules of specific server
  In order to manage the rules of a server

  @basic
  Scenario Outline: List server with only one rule

    Given "<number>" rule created in a server with server id "<server_id>"
    When I get the rules list from server with server id "<server_id>"
    Then I obtain all the rules of the server

    Examples:

    | number  | server_id     |
    | 1       | qatestserver  |


  Scenario Outline: List server with several rules
    Given "<number>" rules created in a server with server id "<server_id>"
    When I get the rules list from server with server id "<server_id>"
    Then I obtain all the rules of the server

    Examples:

    | number  | server_id     |
    | 2       | qatestserver  |
    | 5       | qatestserver  |
    | 100     | qatestserver  |

  Scenario Outline: List server without rules created

    Given a created server with server id "<server_id>" without rules
    When I get the rules list from server with server id "<server_id>"
    Then I obtain zero rules

    Examples:

    | server_id       |
    | qatestserver    |

  Scenario Outline: List rules from non existent server

    Given a created server with server id "<server_id>" inside a tenant
    When I get the rules list from server with server id "<server_id>"
    Then I obtain an error code "<Error_code>" and the fault element "<FaultElement>"

    Examples:

    | server_id | Error_code  | FaultElement  |
    | random    | 404         | itemNotFound  |

  @security
  Scenario Outline: List rules with incorrect token

    Given a created rule in the server with id "<server_id>"
    And an incorrect token with value "<token>"
    When I get the rules list from server with server id "<server_id>"
    Then I obtain an error code "<Error_code>" and the fault element "<FaultElement>"

    Examples:

      | Error_code  | FaultElement  | token     | server_id   |
      | 401         | unauthorized  | 1a2b3c    | qatestserver|
      | 401         | unauthorized  | old_token | qatestserver|
      | 401         | unauthorized  |           | qatestserver|
      | 401         | unauthorized  | null      | qatestserver|

