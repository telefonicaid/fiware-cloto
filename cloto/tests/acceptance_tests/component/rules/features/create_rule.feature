Feature: Create Elasticity Rule
  As a user
  I want to create elasticity rules
  In order to manage automatically the servers

  Scenario Outline: Create a rule

    Given a created "<server_id>" inside tenant
    When I create a rule with "<name>", "<condition>" and "<action>"
    Then the rule is saved in Policy Manager

    Examples:

    | server_id   | name    | condition | action  |
    | qatestserver| random  | default   | default |


  Scenario Outline: Create a rule with missing parameters

    Given a created "<server_id>" inside tenant
    When I create a rule with "<name>", "<condition>" and "<action>"
    Then the rule is saved in Policy Manager

    Examples:

    | server_id   | name      | condition | action  |
    | qatestserver| None      | default   | default |
    | qatestserver| random    | None      | default |
    | qatestserver| random    | default   | None    |
    | qatestserver| random    |           | default |
    | qatestserver|           | default   | default |
    | qatestserver| random    | default   |         |
    | qatestserver| random    | default   | default |
    | qatestserver| long_name | default   | default |