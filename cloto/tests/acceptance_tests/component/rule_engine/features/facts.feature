Feature: Calculate facts
  As a Scalability Manager
  I want receive the facts calculated
  In order to match with the server rules


  Scenario Outline: Calculate Facts when window size is one

    Given the window size is "<window_size>"
    And the following rule subscribed in "<server_id>"
    | name  | condition                                              | action                                         |
    | rule1 | ?serv <- (server (server-id ?x) (cpu ?y&:(> ?y 0.10))' | assert (alertCPU ?x))(python-call notify-user) |
    When context update is received to "<server_id>" with values "<cpu>", "<memory>", "<disk>" and "<network>"
    Then the fact is introduced in the Rule Engine

    Examples:

    | window_size | server_id | cpu   | memory  | disk  | network |
    | 1           | qatest    | 0.75  | 0.8     | 0.1   | 0.15    |


  Scenario Outline: Calculate Facts when window size is between 1 and 10 and has sufficient contexts updates

    Given the window size is "<window_size>"
    And the following rule subscribed in "<server_id>"
    | name  | condition                                              | action                                         |
    | rule1 | ?serv <- (server (server-id ?x) (cpu ?y&:(< ?y 0.10))' | assert (alertCPU ?x))(python-call notify-user) |
    And "<number>" of contexts in "<server_id>"
    When context update is received to "<server_id>" with values "<cpu>", "<memory>", "<disk>" and "<network>"
    Then the fact is introduced in the Rule Engine

    Examples:

    | window_size | number  | server_id | cpu   | memory  | disk  | network |
    | 2           | 1       | qatest    | 0.75  | 0.8     | 0.1   | 0.15    |
    | 5           | 4       | qatest    | 0.75  | 0.8     | 0.1   | 0.15    |
    | 10          | 9       | qatest    | 0.75  | 0.8     | 0.1   | 0.15    |


  Scenario Outline: Insufficient contexts updates to calculate facts

    Given the window size is "<window_size>"
    And the following rule subscribed in "<server_id>"
    | name  | condition                                              | action                                         |
    | rule1 | ?serv <- (server (server-id ?x) (cpu ?y&:(> ?y 0.99))' | assert (alertCPU ?x))(python-call notify-user) |
    And "<number>" of contexts in "<server_id>"
    When context update is received to "<server_id>" with values "<cpu>", "<memory>", "<disk>" and "<network>"
    Then the fact is not introduced in the Rule Engine

    Examples:

    | window_size | number  | server_id | cpu   | memory  | disk  | network |
    | 2           | 0       | qatest    | 0.75  | 0.8     | 0.1   | 0.15    |
    | 5           | 3       | qatest    | 0.75  | 0.8     | 0.1   | 0.15    |
    | 10          | 8       | qatest    | 0.75  | 0.8     | 0.1   | 0.15    |
