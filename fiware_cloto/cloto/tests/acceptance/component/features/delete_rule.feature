Feature: Delete Elasticity Rule
  As a user
  I want to delete a specific elasticity rule
  In order to manage my rules

  @basic
  Scenario Outline: Delete a created rule

    Given a created rule in the server with id "<server_id>"
    When I delete the rule in the server with id "<server_id>"
    Then the rule is deleted

    Examples:

    | server_id   |
    | qatestserver|
    | qaserver    |

  Scenario Outline: Delete a non existent rule

    Given a created rule in the server with id "<server_id>"
    When I delete other rule with id "<another_rule_id>"
    Then I obtain an error code "<Error_code>" and the fault element "<FaultElement>"

    Examples:

    | server_id   | another_rule_id | Error_code  | FaultElement  |
    | qatestserver| testing         | 404         | itemNotFound  |
    | qatestserver| qa              | 404         | itemNotFound  |

  Scenario Outline: Delete a existent rule in other server

    Given a created rule in the server with id "<server_id>"
    When I delete the rule in other server with id "<another_server_id>"
    Then I obtain an error code "<Error_code>" and the fault element "<FaultElement>"

    Examples:

    | server_id   | another_server_id | Error_code  | FaultElement  |
    | qatestserver| testingserver     | 404         | itemNotFound  |
    | qatestserver| qaserver          | 404         | itemNotFound  |

  @security
  Scenario Outline: Delete a rule with incorrect token

    Given a created rule in the server with id "<server_id>"
    And an incorrect token with value "<token>"
    When I delete the rule in the server with id "<server_id>"
    Then I obtain an error code "<Error_code>" and the fault element "<FaultElement>"

    Examples:

      | Error_code  | FaultElement  | token     | server_id   |
      | 401         | unauthorized  | 1a2b3c    | qatestserver|
      | 401         | unauthorized  | old_token | qatestserver|
      | 401         | unauthorized  |           | qatestserver|
      | 401         | unauthorized  | null      | qatestserver|
