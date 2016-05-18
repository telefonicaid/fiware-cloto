Feature: As a user
  I want subscribe servers to subscriptions
  In order to activate rules in the servers subscribed


  @basic
  Scenario Outline: Create a new subscription

    Given a created rule in the "<server_id>"
    When I create a new subscription in "<server_id>" with "<url_to_notify>"
    Then the subscription is created

    Examples:
    | server_id   | name    | condition | action  | url_to_notify                       |
    | qatestserver| random  | default   | default | http://127.0.0.1:8000/v1.0/0comsdsd |
    | qatestserver| random  | default   | default | http://localhost:8080/notify?hello  |
    | testserver  | random  | default   | default | http://localhost                    |
    | qaserver    | random  | default   | default | http://localhost/notify%20space/    |


  Scenario Outline: Create subscription with incorrect url

    Given a created rule in the "<server_id>"
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


  Scenario Outline: Create subscription from a nonexistent rule_id

    Given the rule "<rule_id>"
    When I create a new subscription in "<server_id>" with "<url_to_notify>"
    Then I obtain an "<Error_code>" and the "<FaultElement>"

    Examples:

    | server_id   | rule_id    | url_to_notify                  | Error_code  | FaultElement  |
    | qatestserver| rule_test  | http://localhost:8080/notify   | 404         | itemNotFound  |


  Scenario Outline: Create subscription from a non existant server_id or incorrect server_id
    Given a created rule in the "<server_id>"
    When I create a new subscription in "<another_server_id>" with "<url_to_notify>"
    Then I obtain an "<Error_code>" and the "<FaultElement>"

    Examples:

    | server_id   | name    | condition | action  | url_to_notify     | Error_code  | FaultElement  | another_server_id |
    | qatestserver| random  | default   | default | http://localhost  | 404         | itemNotFound  | random            |
    | qatestserver| random  | default   | default | http://localhost  | 404         | itemNotFound  | qa                |


  @security
  Scenario Outline: Create subscription with incorrect token

    Given a created rule in the "<server_id>"
    And incorrect "<token>"
    When I create a new subscription in "<server_id>" with "<url_to_notify>"
    Then I obtain an "<Error_code>" and the "<FaultElement>"

      Examples:

      | Error_code  | FaultElement  | token     | server_id   | name    | condition | action  | url_to_notify   |
      | 401         | unauthorized  | 1a2b3c    | qatestserver| random  | default   | default | http://localhost|
      | 401         | unauthorized  | old_token | qatestserver| random  | default   | default | another_name2   |
      | 401         | unauthorized  |           | qatestserver| random  | default   | default | another_name3   |
      | 401         | unauthorized  | null      | qatestserver| random  | default   | default | another_name4   |


  Scenario Outline: Create a subscription created before

    Given a created rule in the "<server_id>"
    When I create a new subscription in "<server_id>" with "<url_to_notify>"
    And I create the same subscription
    Then I obtain an "<Error_code>" and the "<FaultElement>"

    Examples:

    | Error_code  | FaultElement  | server_id   | name    | condition | action  | url_to_notify   |
    | 409         | conflict      | qatestserver| random  | default   | default | http://localhost|
