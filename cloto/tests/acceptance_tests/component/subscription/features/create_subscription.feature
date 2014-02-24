Feature: As a user
  I want subscribe servers to subscriptions
  In order to activate rules in the servers subscribed


Scenario Outline: Create a new subscription

  Given the created rule with "<name>", "<condition>" and "<action>" in the "<server_id>"
  When I create a new subscription in "<server_id>" with "<url_to_notify>"
  Then the subscription is created

  Examples:
  | server_id   | name    | condition | action  | url_to_notify                       |
  | qatestserver| random  | default   | default | http://localhost:8080/notify        |
  | qatestserver| random  | default   | default | http://localhost:8080/notify?hello  |
  | qatestserver| random  | default   | default | http://localhost                    |



Scenario Outline: Create subscription with incorrect url

  Given the created rule with "<name>", "<condition>" and "<action>" in the "<server_id>"
  When I create a new subscription in "<server_id>" with "<url_to_notify>"
  Then I obtain an "<Error_code>" and the "<FaultElement>"

  Examples:

  | server_id   | name    | condition | action  | url_to_notify       | Error_code  | FaultElement  |
  | qatestserver| random  | default   | default | localhost           | 400         | badRequest    |
  | qatestserver| random  | default   | default | http://localhost!   | 400         | badRequest    |
  | qatestserver| random  | default   | default | http://localhost¿   | 400         | badRequest    |
  | qatestserver| random  | default   | default | http://localhost$   | 400         | badRequest    |
  | qatestserver| random  | default   | default | http://localhost&   | 400         | badRequest    |
  | qatestserver| random  | default   | default | http://localhost(   | 400         | badRequest    |
  | qatestserver| random  | default   | default | http://localhost*   | 400         | badRequest    |
  | qatestserver| random  | default   | default | http://localhost\   | 400         | badRequest    |
  | qatestserver| random  | default   | default | http://localhost,   | 400         | badRequest    |

Scenario Outline: Create subscription from a non existant rule_id

  Given the rule "<rule_id>"
  When   When I create a new subscription in "<server_id>" with "<url_to_notify>"
  Then Then I obtain an "<Error_code>" and the "<FaultElement>"

  Examples:

  | server_id   | rule_id    | url_to_notify                  | Error_code  | FaultElement  |
  | qatestserver| rule_test  | http://localhost:8080/notify   | 400         | badRequest    |
