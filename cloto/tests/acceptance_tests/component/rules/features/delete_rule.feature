Feature: Delete Elasticity Rule
  As a user
  I want to delete a specific elasticity rule
  In order to manage my rules

  Scenario Outline: Delete a created rule

    Given the created rule with "<name>", "<condition>" and "<action>" in the "<server_id>"
    When I delete the rule in "<server_id>"
    Then the rule is deleted

    Examples:

    | server_id   | name      | condition | action  |
    | qatestserver| random    | default   | default |
    | qaserver    | alertCPU  | default   | default |

  Scenario Outline: Delete a non existent rule

    Given the created rule with "<name>", "<condition>" and "<action>" in the "<server_id>"
    When I delete "<another_rule_id>"
    Then I obtain an "<Error_code>" and the "<FaultElement>"

    Examples:

    | server_id   | name      | condition | action  | another_rule_id | Error_code  | FaultElement  |
    | qatestserver| random    | default   | default | testing         | 404         | itemNotFound  |
    | qatestserver| alertCPU  | default   | default | qa              | 404         | itemNotFound  |

  Scenario Outline: Delete a existent rule in other server

    Given the created rule with "<name>", "<condition>" and "<action>" in the "<server_id>"
    When I delete the rule in "<another_server_id>"
    Then I obtain an "<Error_code>" and the "<FaultElement>"

    Examples:

    | server_id   | name      | condition | action  | another_server_id | Error_code  | FaultElement  |
    | qatestserver| random    | default   | default | testingserver     | 404         | itemNotFound  |
    | qatestserver| alertCPU  | default   | default | qaserver          | 404         | itemNotFound  |


  Scenario Outline: Delete a rule with incorrect token

    Given the created rule with "<name>", "<condition>" and "<action>" in the "<server_id>"
    And incorrect "<token>"
    When I delete the rule in "<server_id>"
    Then I obtain an "<Error_code>" and the "<FaultElement>"

    Examples:

      | Error_code  | FaultElement  | token     | server_id   | name    | condition | action  |
      | 401         | unauthorized  | 1a2b3c    | qatestserver| random  | default   | default |
      | 401         | unauthorized  | old_token | qatestserver| random  | default   | default |
      | 401         | unauthorized  |           | qatestserver| random  | default   | default |
      | 401         | unauthorized  | null      | qatestserver| random  | default   | default |
