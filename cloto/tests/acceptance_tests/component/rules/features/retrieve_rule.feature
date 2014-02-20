Feature: Retrieve Elasticity Rule
  As a user
  I want to get a specific elasticity rule
  In order to manage my rules

  Scenario Outline: Retrieve a created rule

    Given the created rule with "<name>", "<condition>" and "<action>" in the "<server_id>"
    When I retrieve the rule
    Then I obtain the Rule data

    Examples:

    | server_id   | name      | condition | action  |
    | qatestserver| random    | default   | default |
    | qatestserver| alertCPU  | default   | default |

  Scenario Outline: Retrieve a non existent rule

    Given the created rule with "<name>", "<condition>" and "<action>" in the "<server_id>"
    When I retrieve "<another_rule_id>"
    Then I obtain an "<Error_code>" and the "<FaultElement>"

    Examples:

    | server_id   | name      | condition | action  | another_rule_id | Error_code  | FaultElement  |
    | qatestserver| random    | default   | default | testing         | 404         | itemNotFound  |
    | qatestserver| alertCPU  | default   | default | qa              | 404         | itemNotFound  |


